# AI Study Twin — Android Application Guide

This repository contains a full Native Android Application wrapper as well as a Progressive Web App (PWA) configuration for **AI Study Twin**.

---

## Architecture Options

### 1. Progressive Web App (PWA) — Instant Installation on Phone
No Android Studio required!
1. Open Chrome or Edge browser on your Android mobile device.
2. Navigate to your hosted AI Study Twin server URL (e.g. `http://<your-computer-ip>:8000`).
3. Tap the **⋮ (Menu)** icon in Chrome and tap **"Add to Home Screen"** or **"Install App"**.
4. AI Study Twin will install on your Android home screen and app drawer as a standalone native app!

---

### 2. Native Android Studio Project (`android/` directory)

#### Prerequisites
- Android Studio Hedgehog or newer installed.
- JDK 17 or JDK 21 installed.
- Android SDK 34.

#### Steps to Build APK
1. Launch **Android Studio**.
2. Click **Open Project** and select the `android/` directory inside `ai-study-twin`.
3. Allow Gradle sync to complete.
4. In `MainActivity.kt`, update the `serverUrl` string to your computer's local IP address or production server domain (e.g., `http://192.168.1.100:8000` for physical phone testing, or `http://10.0.2.2:8000` for the Android Emulator).
5. Click **Build > Build Bundle(s) / APK(s) > Build APK(s)**.
6. The generated `.apk` file will be saved in `android/app/build/outputs/apk/debug/app-debug.apk`. Transfer and install it on any Android device!

---

### 3. Progressive Web App Features
- **PWA Web Manifest** (`frontend/public/manifest.json`)
- **Service Worker Offline Cache** (`frontend/public/sw.js`)
- **Mobile Responsive Drawer & Bottom Navigation**
- **Swipe-to-Refresh Support**
- **Mobile Status Bar Synchronization (`#0f172a`)**
