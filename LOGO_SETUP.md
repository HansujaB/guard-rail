# Logo Setup Instructions

## Current Status

The application currently uses a Shield icon from `lucide-react` as a placeholder logo. You need to replace this with your actual logo.

## Where Logo is Used

1. **Login Page** (`src/pages/Login.tsx` - line ~52)
   - Location: Left panel branding section
   - Current: Shield icon in a colored box
   - Size: 64x64px (w-16 h-16)

2. **Sidebar** (`src/components/layout/Sidebar.tsx` - line ~57)
   - Location: Sidebar header
   - Current: Shield icon in a colored box
   - Size: 40x40px (w-10 h-10)

## How to Add Your Logo

1. **Add logo file to public folder:**
   ```
   public/logo.svg  (or logo.png, logo.jpg)
   ```

2. **Update Login.tsx:**
   Replace the Shield icon with:
   ```tsx
   <img src="/logo.svg" alt="IRSS COMMAND Logo" className="w-10 h-10" />
   ```

3. **Update Sidebar.tsx:**
   Replace the Shield icon with:
   ```tsx
   <img src="/logo.svg" alt="IRSS COMMAND Logo" className="w-6 h-6" />
   ```

## Recommended Logo Formats

- **SVG** (recommended): Scalable, small file size
- **PNG**: Use with transparent background
- **Recommended size**: 512x512px minimum for high-quality rendering

## Notes

- Make sure the logo has a transparent background for best appearance
- Adjust the size classes (w-10, h-10, etc.) based on your logo's aspect ratio
- You may want to remove the colored background boxes if your logo includes its own background

