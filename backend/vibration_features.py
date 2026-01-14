# # vibration_features.py
# import numpy as np
# from scipy.stats import skew, kurtosis, entropy
# from scipy.signal import find_peaks
# from scipy.fft import fft

# class VibrationFeatureExtractor:
#     def extract(self, signal: np.ndarray) -> np.ndarray:
#         """Extract vibration features matching the notebook"""
#         if len(signal) == 0:
#             return np.zeros(20)  # Fixed to 20 features as per placeholder

#         features = []

#         # Time Domain Features
#         features.append(np.mean(signal))                  # Mean
#         features.append(np.std(signal))                   # Standard Deviation
#         features.append(np.max(np.abs(signal)))           # Absolute Max
#         features.append(np.min(signal))                   # Min
#         features.append(np.ptp(signal))                   # Peak-to-Peak
#         features.append(skew(signal))                     # Skewness
#         features.append(kurtosis(signal))                 # Kurtosis
#         features.append(np.sqrt(np.mean(signal**2)))      # RMS
#         features.append(np.mean(np.abs(signal)))          # Mean Absolute
#         features.append(np.max(signal**2))                # Peak Squared (energy proxy)

#         # Additional Time Domain (Crest, Clearance, Shape, Impulse Factors)
#         rms = features[7]  # RMS from above
#         mean_abs = features[8]
#         peak = features[2]  # Abs max as peak
#         if rms > 0:
#             features.append(peak / rms)                   # Crest Factor
#         else:
#             features.append(0.0)
#         if mean_abs > 0:
#             features.append(peak / np.sqrt(mean_abs))     # Clearance Factor (approx)
#             features.append(rms / mean_abs)               # Shape Factor
#             features.append(peak / mean_abs)              # Impulse Factor
#         else:
#             features.append(0.0)
#             features.append(0.0)
#             features.append(0.0)

#         # Frequency Domain Features (FFT-based)
#         fft_vals = np.abs(fft(signal))[:len(signal)//2]  # One-sided FFT
#         freqs = np.linspace(0, 1, len(fft_vals))         # Normalized freq
#         if len(fft_vals) > 0:
#             features.append(np.mean(fft_vals))            # FFT Mean
#             features.append(np.std(fft_vals))             # FFT Std
#             features.append(np.max(fft_vals))             # FFT Max
#             dominant_freq_idx = np.argmax(fft_vals)
#             features.append(freqs[dominant_freq_idx])     # Dominant Frequency (normalized)
#             if np.sum(fft_vals) > 0:
#                 spectral_ent = entropy(fft_vals / np.sum(fft_vals))
#                 features.append(spectral_ent)             # Spectral Entropy
#             else:
#                 features.append(0.0)
#             features.append(skew(fft_vals))               # Spectral Skewness
#             features.append(kurtosis(fft_vals))           # Spectral Kurtosis
#         else:
#             features.extend([0.0] * 7)  # Pad freq features

#         # Truncate or pad to exactly 20 features (match your training)
#         features = np.array(features[:20])
#         if len(features) < 20:
#             features = np.pad(features, (0, 20 - len(features)))

#         return features

"""
vibration_features.py
Place this file in the same directory as main.py
"""

import numpy as np


class VibrationFeatureExtractor:
    """
    Feature extractor for vibration signal analysis
    Extracts 20 statistical features from vibration data
    """
    
    def extract(self, vibration_array):
        """
        Extract 20 statistical features from vibration signal
        
        Args:
            vibration_array: numpy array of vibration values
            
        Returns:
            numpy array of 20 features
        """
        features = []
        
        # Time domain features (8)
        features.append(np.mean(vibration_array))           # 1. Mean
        features.append(np.std(vibration_array))            # 2. Standard deviation
        features.append(np.max(vibration_array))            # 3. Maximum
        features.append(np.min(vibration_array))            # 4. Minimum
        features.append(np.median(vibration_array))         # 5. Median
        features.append(np.percentile(vibration_array, 25)) # 6. 25th percentile
        features.append(np.percentile(vibration_array, 75)) # 7. 75th percentile
        features.append(np.ptp(vibration_array))            # 8. Peak-to-peak
        
        # Statistical moments (2)
        features.append(np.var(vibration_array))            # 9. Variance
        features.append(np.mean(np.abs(vibration_array)))   # 10. Mean absolute value
        
        # Energy-based features (2)
        features.append(np.sum(vibration_array**2))         # 11. Energy
        features.append(np.sqrt(np.mean(vibration_array**2))) # 12. RMS
        
        # Zero crossing rate (1)
        zero_crossings = np.sum(np.diff(np.sign(vibration_array)) != 0)
        features.append(zero_crossings)                     # 13. Zero crossings
        
        # Peak features (2)
        threshold = np.mean(vibration_array) + 2 * np.std(vibration_array)
        peaks = vibration_array[vibration_array > threshold]
        features.append(len(peaks))                         # 14. Number of peaks
        features.append(np.mean(peaks) if len(peaks) > 0 else 0)  # 15. Mean peak value
        
        # Entropy approximation (1)
        hist, _ = np.histogram(vibration_array, bins=10)
        hist = hist / (np.sum(hist) + 1e-10)
        entropy = -np.sum(hist * np.log(hist + 1e-10))
        features.append(entropy)                            # 16. Entropy
        
        # Derivative features (3)
        diff = np.diff(vibration_array)
        features.append(np.sum(np.abs(diff)))               # 17. Total variation
        features.append(np.max(np.abs(diff)))               # 18. Max derivative
        features.append(np.mean(np.abs(diff)))              # 19. Mean derivative
        
        # Length (1)
        features.append(len(vibration_array))               # 20. Signal length
        
        return np.array(features)