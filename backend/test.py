import requests
import os
import numpy as np
import json

# Check for optional dependencies
try:
    import soundfile as sf
    HAS_SOUNDFILE = True
except ImportError:
    HAS_SOUNDFILE = False
    print(" Warning: soundfile not installed. Audio generation will be skipped.")
    print("   Install with: pip install soundfile")
    print()

# Configuration
API_URL = "http://localhost:8000"
DEMO_DATA_DIR = "./demo_data"

def generate_demo_audio(filename, duration=5, sample_rate=16000, anomaly=False):
    """Generate a demo audio file with optional anomaly patterns"""
    if not HAS_SOUNDFILE:
        print(f"⚠️  Skipping audio generation for {filename} (soundfile not installed)")
        return None
    
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    if anomaly:
        # Tool-like sounds: higher frequency components, irregular patterns
        audio = (np.sin(2 * np.pi * 440 * t) * 0.3 +  # Base tone
                np.sin(2 * np.pi * 880 * t) * 0.2 +   # Harmonic
                np.random.normal(0, 0.15, len(t)) +   # Noise
                np.sin(2 * np.pi * 150 * t) * 0.4)    # Low frequency impact
        # Add sharp transients (tool impacts)
        for i in range(10):
            pos = int(np.random.random() * len(t))
            audio[pos:pos+100] += np.random.normal(0, 0.5, 100)
    else:
        # Normal ambient railway sounds: lower frequency, more regular
        audio = (np.sin(2 * np.pi * 220 * t) * 0.2 +
                np.random.normal(0, 0.05, len(t)) +
                np.sin(2 * np.pi * 50 * t) * 0.1)
    
    # Normalize
    audio = audio / np.max(np.abs(audio)) * 0.8
    
    # Save as WAV
    filepath = os.path.join(DEMO_DATA_DIR, filename)
    sf.write(filepath, audio, sample_rate)
    return filepath

def check_health():
    """Check if API is running"""
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        print("=" * 60)
        print("🏥 HEALTH CHECK")
        print("=" * 60)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print()
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print("=" * 60)
        print("❌ CONNECTION ERROR")
        print("=" * 60)
        print("API is not running or not accessible.")
        print(f"Expected URL: {API_URL}")
        print()
        print("To start the API, run:")
        print("  python main.py")
        print("or")
        print("  uvicorn main:app --reload")
        print()
        return False
    except Exception as e:
        print(f"❌ Unexpected error during health check: {e}")
        return False

def generate_vibration_data():
    """Generate vibration test data files"""
    np.random.seed(42)
    
    # High risk - with anomalies
    vib1 = np.random.normal(0.15, 0.05, 150)
    vib1[50:70] += np.random.normal(0.4, 0.1, 20)
    vib1[100:110] += np.random.normal(0.3, 0.08, 10)
    with open(os.path.join(DEMO_DATA_DIR, 'vibration_data_1.txt'), 'w') as f:
        f.write(','.join([f'{x:.6f}' for x in vib1]))
    
    # Medium risk - minor anomalies
    np.random.seed(43)
    vib2 = np.random.normal(0.12, 0.04, 150)
    vib2[60:80] += np.random.normal(0.25, 0.08, 20)
    with open(os.path.join(DEMO_DATA_DIR, 'vibration_data_2.txt'), 'w') as f:
        f.write(','.join([f'{x:.6f}' for x in vib2]))
    
    # Low risk - normal
    np.random.seed(44)
    vib3 = np.random.normal(0.10, 0.03, 150)
    with open(os.path.join(DEMO_DATA_DIR, 'vibration_data_3.txt'), 'w') as f:
        f.write(','.join([f'{x:.6f}' for x in vib3]))

def generate_sequence_data():
    """Generate sequence test data files"""
    # High risk - with anomalies
    np.random.seed(45)
    seq1 = np.random.normal(0.5, 0.15, 60)
    seq1[40:50] += np.random.normal(0.3, 0.1, 10)
    with open(os.path.join(DEMO_DATA_DIR, 'sequence_data_1.txt'), 'w') as f:
        f.write(','.join([f'{x:.6f}' for x in seq1]))
    
    # Medium risk - minor anomalies
    np.random.seed(46)
    seq2 = np.random.normal(0.45, 0.12, 60)
    seq2[30:40] += np.random.normal(0.2, 0.08, 10)
    with open(os.path.join(DEMO_DATA_DIR, 'sequence_data_2.txt'), 'w') as f:
        f.write(','.join([f'{x:.6f}' for x in seq2]))
    
    # Low risk - normal
    np.random.seed(47)
    seq3 = np.random.normal(0.4, 0.1, 60)
    with open(os.path.join(DEMO_DATA_DIR, 'sequence_data_3.txt'), 'w') as f:
        f.write(','.join([f'{x:.6f}' for x in seq3]))

def run_test_case(case_name, vibration_file, sequence_file, audio_file, 
                  pir, weather_ignore=False):
    """Run a single test case"""
    print("=" * 60)
    print(f"🧪 TEST CASE: {case_name}")
    print("=" * 60)
    
    # Read vibration data
    vib_path = os.path.join(DEMO_DATA_DIR, vibration_file)
    if not os.path.exists(vib_path):
        print(f"❌ Vibration file not found: {vib_path}")
        return None
    
    with open(vib_path, 'r') as f:
        vibration_data = f.read()
    
    # Read sequence data
    seq_path = os.path.join(DEMO_DATA_DIR, sequence_file)
    if not os.path.exists(seq_path):
        print(f"❌ Sequence file not found: {seq_path}")
        return None
    
    with open(seq_path, 'r') as f:
        sequence_data = f.read()
    
    # Check audio file
    audio_path = os.path.join(DEMO_DATA_DIR, audio_file)
    if not os.path.exists(audio_path):
        print(f"❌ Audio file not found: {audio_path}")
        print(f"   Please install soundfile: pip install soundfile")
        return None
    
    # Prepare files
    files = {
        'acoustic_file': (audio_file, open(audio_path, 'rb'), 'audio/wav')
    }
    
    # Prepare form data
    data = {
        'vibration': vibration_data,
        'sequence': sequence_data,
        'pir': pir,
        'weather_ignore': weather_ignore
    }
    
    try:
        response = requests.post(f"{API_URL}/predict/intent", files=files, data=data, timeout=30)
        
        # Close files
        for file_tuple in files.values():
            file_tuple[1].close()
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"📊 INTENT SCORE: {result['intent_score']}")
            print(f"🚨 ALERT TRIGGERED: {result['alert_triggered']}")
            print()
            
            print("Individual Scores:")
            for key, value in result['individual_scores'].items():
                print(f"  • {key}: {value}")
            print()
            
            if result['reasons']:
                print("Reasons:")
                for reason in result['reasons']:
                    print(f"  • {reason}")
            print()
            
            if result['alert']:
                print("⚠️  ALERT DETAILS:")
                print(f"  • Alert ID: {result['alert']['alert_id']}")
                print(f"  • Risk Level: {result['alert']['risk'].upper()}")
                print(f"  • Intent Score: {result['alert']['intent_score']}")
                print(f"  • Reasons: {', '.join(result['alert']['reason'])}")
            else:
                print("✅ No alert triggered - situation appears normal")
            
            print()
            return result
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            print()
            return None
            
    except requests.exceptions.Timeout:
        print("❌ Request timeout - API took too long to respond")
        print()
        return None
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - API not accessible")
        print()
        return None
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print()
        return None

def main():
    """Main test runner"""
    print("\n" + "=" * 60)
    print("🚂 RAILWAY TRACK INTRUSION DETECTION - TEST SUITE")
    print("=" * 60)
    print()
    
    # Check dependencies
    if not HAS_SOUNDFILE:
        print("=" * 60)
        print("❌ MISSING DEPENDENCY")
        print("=" * 60)
        print("The 'soundfile' package is required to run tests.")
        print()
        print("Install it with:")
        print("  pip install soundfile")
        print()
        print("If you're in a virtual environment (venv), activate it first:")
        print("  .\\venv\\Scripts\\activate  # Windows")
        print("  source venv/bin/activate   # Linux/Mac")
        print()
        return
    
    # Create demo_data directory if it doesn't exist
    os.makedirs(DEMO_DATA_DIR, exist_ok=True)
    
    # Check if API is running
    if not check_health():
        return
    
    print("📁 Generating demo files...")
    print()
    
    # Generate all demo files
    try:
        generate_vibration_data()
        generate_sequence_data()
        
        audio_high_risk = generate_demo_audio("audio_high_risk.wav", anomaly=True)
        audio_medium_risk = generate_demo_audio("audio_medium_risk.wav", anomaly=True)
        audio_low_risk = generate_demo_audio("audio_low_risk.wav", anomaly=False)
        
        print("✅ Demo files generated successfully!")
        print()
    except Exception as e:
        print(f"❌ Failed to generate demo files: {e}")
        return
    
    # Run test cases
    test_results = []
    
    # Test Case 1: High Risk - All indicators suggest intrusion
    result1 = run_test_case(
        case_name="HIGH RISK - Intrusion with Tool Activity",
        vibration_file="vibration_data_1.txt",
        sequence_file="sequence_data_1.txt",
        audio_file="audio_high_risk.wav",
        pir=1,
        weather_ignore=False
    )
    test_results.append(("High Risk", result1))
    
    # Test Case 2: Medium Risk - Some indicators
    result2 = run_test_case(
        case_name="MEDIUM RISK - Partial Anomaly Detection",
        vibration_file="vibration_data_2.txt",
        sequence_file="sequence_data_2.txt",
        audio_file="audio_medium_risk.wav",
        pir=1,
        weather_ignore=False
    )
    test_results.append(("Medium Risk", result2))
    
    # Test Case 3: Low Risk - Normal operation
    result3 = run_test_case(
        case_name="LOW RISK - Normal Railway Operation",
        vibration_file="vibration_data_3.txt",
        sequence_file="sequence_data_3.txt",
        audio_file="audio_low_risk.wav",
        pir=0,
        weather_ignore=False
    )
    test_results.append(("Low Risk", result3))
    
    # Test Case 4: Weather Override - High risk ignored
    result4 = run_test_case(
        case_name="WEATHER OVERRIDE - High Risk Event Ignored",
        vibration_file="vibration_data_1.txt",
        sequence_file="sequence_data_1.txt",
        audio_file="audio_high_risk.wav",
        pir=1,
        weather_ignore=True
    )
    test_results.append(("Weather Override", result4))
    
    # Summary
    print("=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    successful = sum(1 for _, result in test_results if result is not None)
    total = len(test_results)
    
    print(f"Total Tests: {total}")
    print(f"Successful: {successful}")
    print(f"Failed: {total - successful}")
    print()
    
    for name, result in test_results:
        if result:
            status = "✅ PASS"
            score = result.get('intent_score', 'N/A')
            alert = "🚨 ALERT" if result.get('alert_triggered', False) else "✓ Normal"
            print(f"{status} - {name}: Score={score}, {alert}")
        else:
            print(f"❌ FAIL - {name}")
    
    print()
    print("=" * 60)
    print("✅ TEST SUITE COMPLETED")
    print("=" * 60)
    print()
    print("📝 Notes:")
    print("  • API Endpoint: /predict/intent")
    print("  • Data Directory: ./demo_data/")
    print("  • Human Detection: PIR sensor only (YOLO disabled)")
    print()

if __name__ == "__main__":
    main()