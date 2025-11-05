# SUNDAY - Yoga Wellness Platform

## Overview

SUNDAY is an AI-powered yoga wellness platform that combines voice interaction with real-time pose detection and correction. The system uses a Python-based voice assistant (named "Sunday") to interact with users through a web interface that provides AR-based yoga pose correction using TensorFlow.js pose detection models. The platform features a dark-themed UI, real-time camera-based pose analysis, and audio feedback for wellness coaching.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture

**Problem**: Need to provide an interactive, camera-based yoga pose correction system that runs entirely in the browser without requiring backend processing.

**Solution**: Client-side web application using vanilla JavaScript with TensorFlow.js for ML inference.

**Key Components**:
- **TensorFlow.js Pose Detection**: Real-time pose estimation running directly in the browser
- **Tailwind CSS**: Utility-first CSS framework for dark-themed, responsive UI
- **Tone.js**: Audio synthesis library for feedback and ambient sounds
- **Camera Access**: WebRTC-based camera streaming for pose analysis

**Design Rationale**: Browser-based ML processing eliminates latency from server roundtrips and maintains user privacy by keeping video data local. The dark theme (#121212 background) provides better focus during yoga sessions.

### Backend Architecture

**Problem**: Need to serve static web content and provide voice-controlled interaction with the yoga platform.

**Solution**: Dual-component architecture with a simple HTTP server and a Selenium-based voice assistant.

**Components**:

1. **HTTP Server** (`server.py`)
   - Simple Python HTTP server serving static files on port 5000
   - Custom headers to prevent caching for development
   - No-framework approach for minimal dependencies

2. **Voice Assistant** (`assistant.py`)
   - Speech recognition using `speech_recognition` library
   - Wake word detection ("sunday") for hands-free operation
   - Text-to-speech using `pyttsx3` for audio responses
   - Selenium WebDriver for browser automation and interaction

**Design Pattern**: The voice assistant runs as a separate process that controls a Chrome browser instance, allowing voice commands to interact with the web-based yoga platform. This separation enables the platform to work standalone while the assistant provides enhanced voice-controlled features.

### Data Storage

**Problem**: Need to maintain conversation history and system status across sessions.

**Solution**: File-based JSON storage for lightweight persistence.

**Storage Components**:
- `sunday_status.json`: Tracks assistant state and configuration
- `conversation_log.txt`: Logs user interactions and system events

**Rationale**: File-based storage is sufficient for single-user desktop application without need for complex database infrastructure.

### Voice Interaction System

**Problem**: Provide hands-free, natural language interaction during yoga sessions.

**Solution**: Wake word-activated voice assistant with calibrated microphone settings.

**Implementation Details**:
- Dynamic energy threshold adjustment for varying ambient noise
- Pause threshold of 1.0 seconds for natural speech patterns
- Threading model for concurrent listening and browser control
- Energy threshold set to 3000 for optimal sensitivity

**Alternatives Considered**: Cloud-based speech recognition was considered but rejected to maintain privacy and reduce latency.

### Browser Automation Layer

**Problem**: Bridge voice commands to web application interactions.

**Solution**: Selenium WebDriver with Chrome in automation mode.

**Chrome Configuration**:
- Fake media stream for testing without physical camera
- Disabled web security for development flexibility
- No sandbox mode for containerized environments
- Autoplay policy bypass for audio feedback
- Hidden automation flags for cleaner UI experience

**Rationale**: Selenium provides robust control over the web interface, enabling the voice assistant to trigger actions, read status, and manage the yoga session programmatically.

## External Dependencies

### Machine Learning & Computer Vision
- **TensorFlow.js** (v3.13.0): Browser-based ML inference for pose detection
- **@tensorflow-models/pose-detection** (v2.0.0): Pre-trained pose estimation models (MoveNet/BlazePose)

### Audio & Speech
- **Tone.js** (v14.8.49): Web audio synthesis for ambient sounds and feedback
- **speech_recognition** (Python): Google Speech Recognition API for voice input
- **pyttsx3** (Python): Text-to-speech engine for voice responses

### Browser Automation
- **Selenium WebDriver** (Python): Chrome browser automation
- Chrome browser required for running the assistant

### UI Framework
- **Tailwind CSS** (CDN): Utility-first CSS framework for responsive dark theme

### Development Server
- **Python http.server**: Built-in HTTP server for static file serving
- Port 5000 default configuration

### System Requirements
- Microphone access for voice control
- Webcam access for pose detection
- Chrome browser for assistant automation
- Python 3.x runtime environment

### API Integrations
- Google Speech Recognition API (via speech_recognition library)
- No external API keys required for basic functionality
- All pose detection runs client-side

## AR Pose Correction System

### Overview
The AR correction system provides real-time visual feedback on yoga pose accuracy using MoveNet pose detection and color-coded skeleton overlay.

### Pose Validation Architecture

**Problem**: Need to provide accurate, real-time feedback on pose correctness for 4 different yoga poses with varying difficulty levels.

**Solution**: Angle-based validation system with normalized scoring (0-100%) and color-coded visual feedback.

**Supported Poses**:
1. **Tadasana (Mountain Pose)** - Beginner
   - Validates: Body alignment, feet position, shoulder level
   - Key checks: Side angles (165-180°), feet distance, shoulder symmetry

2. **Adho Mukha Svanasana (Downward Dog)** - Intermediate
   - Validates: Inverted V shape, leg straightness, hip elevation, hand/feet balance
   - Key checks: Hip-shoulder-wrist angle (60-90°), leg extension (160-180°)

3. **Virabhadrasana III (Warrior III)** - Advanced
   - Validates: Standing leg straightness, torso horizontal alignment, lifted leg extension, hip level
   - Key checks: Balance, body parallel to ground, hip squaring

4. **Namastey (Prayer Pose)** - Beginner
   - Validates: Hand position at chest center, elbow angles, shoulder relaxation
   - Key checks: Hands together, elbow angles (80-110°), shoulder symmetry

### Scoring System

**Design**: Normalized percentage-based scoring with dynamic color feedback

**Scoring Formula**:
```javascript
finalScore = (overallScore / (checks * 25)) * 100
```

**Key Features**:
- Each validation check contributes up to 25 points
- Final score normalized to 0-100% regardless of number of checks performed
- Handles low-confidence keypoints gracefully by adjusting denominator
- Ensures 100% score is attainable when all available checks pass perfectly

**Color Coding**:
- **Green** (#10B981): Score ≥ 80% - Pose is correct
- **Yellow-Green** (#84cc16): Score 60-80% - Minor adjustments needed
- **Orange** (#FFC107): Score 40-60% - Moderate corrections required
- **Light Orange** (#FB923C): Score 20-40% - Significant corrections needed
- **Red** (#EF4444): Score < 20% - High risk, major form issues

### Real-Time Feedback

**Visual Overlay**:
- Skeleton rendered on video feed using MoveNet's 17 keypoints
- Skeleton color changes based on pose accuracy score
- Keypoints displayed as filled circles with white outlines
- Connections drawn as colored lines between joints

**Text Feedback**:
- Real-time score percentage display
- Specific correction suggestions per body part
- Check marks (✓) for correct positions
- Warning symbols (⚠) for minor issues
- Error symbols (✗) for major corrections needed

### Technical Implementation

**Pose Detection**:
- MoveNet SinglePose Lightning model for speed
- Minimum confidence threshold: 0.3 for keypoint validity
- 60 FPS target for smooth real-time tracking
- Mirrored video feed for natural user experience

**Angle Calculation**:
- Three-point angle calculation using atan2
- Handles 0-360° range with normalization
- Distance calculations for position validation
- Relative measurements for device-independent validation

**Performance Optimization**:
- Client-side inference eliminates network latency
- RequestAnimationFrame for smooth rendering
- Canvas overlay prevents video reprocessing
- Efficient skeleton connection algorithm

### Recent Changes (November 5, 2025)
- **Side-by-Side Reference Pose Display**: Added reference pose images alongside user's camera feed in AR correction mode
  - Users now see correct pose reference image next to their live camera feed
  - Reference images for all 4 poses (Tadasana, Downward Dog, Warrior III, Namaste)
  - Responsive grid layout: side-by-side on desktop, stacked on mobile
  - Reference images stored in `assets/poses/` directory
- **Detailed Correction Guidance Panel**: Added instructive feedback panel with step-by-step corrections
  - New panel displays below reference image with detailed, color-coded guidance
  - Each feedback item shows both WHAT to correct and HOW to correct it
  - Green (success), Yellow (warning), and Red (error) color coding for clarity
  - Scrollable panel for multiple correction points
- **Camera Optimization**: Enhanced camera settings for smooth pose tracking
  - Resolution increased to 1280x720 for better pose detection accuracy
  - Frame rate optimized: 30fps ideal, 60fps maximum for smooth tracking
  - Improved video quality reduces false positives in pose validation
- **Fixed Scoring Accuracy** (Critical Fix):
  - Fixed random scoring issue caused by using low-confidence keypoints
  - ALL keypoints now checked for minimum confidence before use in calculations
  - Scoring normalized against total possible score (100) for consistency
  - Partial pose detection now properly warns users and gives accurate percentages
  - Example: If only 1 of 4 checks detects 60%, score is 15% (not 60%), accurately reflecting incomplete pose
- **Improved Validation Logic**:
  - Tadasana validation completely rewritten with detailed feedback
  - Confidence checks prevent "random" angles from undetected keypoints
  - Users warned when fewer than 3 of 4 body parts detected
  - Clear instructions on repositioning for better camera visibility