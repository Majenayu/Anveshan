# SUNDAY - Yoga Wellness Platform

## Overview
SUNDAY is an AI-powered yoga wellness platform that combines voice interaction with real-time pose detection and correction. It uses a Python-based voice assistant and a web interface for AR-based yoga pose correction via TensorFlow.js. The platform features a dark-themed UI, real-time camera-based pose analysis, and audio feedback for wellness coaching. The business vision is to provide an accessible, AI-guided yoga experience to users, enhancing their wellness journey with personalized feedback and intuitive interaction.

## User Preferences
Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
The frontend is a client-side web application using vanilla JavaScript with TensorFlow.js for ML inference. It provides an interactive, camera-based yoga pose correction system that runs entirely in the browser. Key components include TensorFlow.js for real-time pose estimation, Tailwind CSS for a dark-themed UI, Tone.js for audio feedback, and WebRTC for camera access. This design prioritizes privacy and low latency by processing ML client-side.

### Backend Architecture
The backend uses a dual-component architecture:
1.  **HTTP Server (`server.py`)**: A simple Python HTTP server serving static files on port 5000, designed for minimal dependencies.
2.  **Voice Assistant (`assistant.py`)**: A separate Python process utilizing the `speech_recognition` library for voice input, `pyttsx3` for text-to-speech, and Selenium WebDriver for browser automation. This allows for hands-free voice control of the web platform.

### Data Storage
File-based JSON storage is used for lightweight persistence, tracking assistant state in `sunday_status.json` and logging conversations in `conversation_log.txt`. This is suitable for a single-user desktop application.

### Voice Interaction System
The system features a wake word-activated voice assistant ("Sunday") with dynamic energy threshold adjustment for robust speech recognition. It uses a threading model for concurrent listening and browser control.

### Browser Automation Layer
Selenium WebDriver is used to control a Chrome browser instance, enabling the voice assistant to interact with the web application. Chrome is configured with specific flags for development and testing, such as disabling web security and enabling autoplay.

### AR Pose Correction System
The AR correction system provides real-time visual feedback on yoga pose accuracy using the MoveNet SinglePose Lightning model. It features an angle-based validation system for three core poses (Tadasana, Vrikshasana, Namastey) with a normalized 0-100% scoring system and color-coded visual feedback (Green for correct, Red for major issues). Visual feedback includes a skeleton overlay on the video feed and real-time text suggestions.

### System Design Choices
-   **UI/UX**: Dark-themed interface (`#121212 background`) using Tailwind CSS for focus.
-   **Technical Implementations**: Client-side ML with TensorFlow.js for pose detection, vanilla JavaScript for interactivity, Python for voice assistant and server.
-   **Feature Specifications**: Real-time pose analysis, voice commands, detailed pose scoring, and visual correction feedback.
-   **Core Poses**: Tadasana (Mountain Pose), Vrikshasana (Tree Pose), Namastey (Prayer Pose) are supported with reference images.

## External Dependencies

### Machine Learning & Computer Vision
-   **TensorFlow.js**: For browser-based ML inference.
-   **@tensorflow-models/pose-detection**: Pre-trained pose estimation models (MoveNet/BlazePose).

### Audio & Speech
-   **Tone.js**: Web audio synthesis for ambient sounds and feedback.
-   **speech_recognition** (Python): Utilizes Google Speech Recognition API for voice input.
-   **pyttsx3** (Python): Text-to-speech engine.

### Browser Automation
-   **Selenium WebDriver** (Python): For Chrome browser automation.
-   **Chrome browser**: Required for the assistant.

### UI Framework
-   **Tailwind CSS** (CDN): Utility-first CSS framework.

### Development Server
-   **Python http.server**: Built-in HTTP server for static files.

### API Integrations
-   **Google Speech Recognition API**: Used via the `speech_recognition` library.
-   **Gemini API (via `javascript_gemini` integration)**: For the Virtual Assistant feature (AI-powered yoga guidance).