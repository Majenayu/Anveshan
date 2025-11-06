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

**Supported Poses** (Simplified to 3 Core Poses):
1. **Tadasana (Mountain Pose)** - Beginner
   - Validates: Body alignment, feet position, shoulder level
   - Key checks: Side angles (165-180°), feet distance, shoulder symmetry
   - Reference image: `assets/poses/tadasana.jpg`

2. **Vrikshasana (Tree Pose)** - Beginner
   - Validates: Standing leg balance, raised foot position, hand placement
   - Key checks: Balance on one leg, foot placement on inner thigh, hands in prayer position
   - Reference image: `assets/poses/vrikshasana.jpg`

3. **Namastey (Prayer Pose)** - Beginner
   - Validates: Hand position at chest center, elbow angles, shoulder relaxation
   - Key checks: Hands together, elbow angles (80-110°), shoulder symmetry
   - Reference image: `assets/poses/namaste.png`

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

### Recent Changes (November 6, 2025)

#### Simplified Pose Library & Image-Based References (Latest - Session 2)
- **Reduced to 3 Core Poses**: Removed all poses except the essential beginner poses
  - Tadasana (Mountain Pose)
  - Vrikshasana (Tree Pose) 
  - Namastey (Prayer Pose)
- **Replaced Videos with Static Images**: Removed video reference system and replaced with generated reference images
  - All 3 poses now have professional AI-generated demonstration images
  - Images show correct form for pose validation
  - Stored in `assets/poses/` directory
  - Images use static img element instead of video element for better performance
- **Cleaned Up Assets**: Removed unused pose images and video directory
  - Deleted reference_videos directory
  - Removed images for deprecated poses (Downward Dog, Warrior III, Natarajasana, Baddha Konasana)

#### Posture Correction UX Enhancements (Session 1)
- **Reference Video Display**: Added video playback for reference poses
  - Displays correct form videos for Tadasana and Vrikshasana poses
  - Graceful fallback to placeholder emoji for poses without videos
  - Stored in `assets/reference_videos/` directory
  - Auto-plays on pose selection with proper error handling

- **Stabilized Suggestions System**: Implemented buffering to reduce rapid feedback changes
  - Suggestions now update every 5 frames (BUFFER_SIZE = 5) instead of every frame
  - Prevents jarring experience where corrections change too quickly for users to react
  - Maintains stable feedback message until user corrects their pose
  - Smoother user experience with predictable correction guidance

- **Real-Time Pose Scoring System**: Added 0-100 accuracy scoring with visual feedback
  - Deducts 15 points for red (major) errors, 8 points for yellow (minor) warnings
  - Rolling average over 30 frames (≈1 second) for smooth score display
  - Color-coded progress bar:
    - Green (85+): Excellent form
    - Blue/Yellow (70-84): Good form, minor adjustments
    - Orange (50-69): Needs improvement
    - Red (<50): Major corrections required
  - Real-time visual motivation to maintain correct posture
  - Score resets to 100 when starting each new pose

- **Improved Error Handling**: Added null checks for DOM elements to prevent crashes during AR initialization

#### Complete Platform Migration
- **Dashboard**: Full progress tracking with posture score, streak counter, calories burned widgets
- **Routine Page**: Personalized yoga sequences with wellness tracking (sleep, stress, hydration)
- **Virtual Assistant**: Gemini 2.5 Flash AI integration with markdown formatting for yoga/wellness guidance
- **Asana Library**: Complete pose database with benefits, precautions, and targeted areas
- **AR Correction**: Real-time camera feedback with pose validation (MIN_CONFIDENCE bug fixed)
- **Responsive Design**: Mobile-first with Tailwind CSS breakpoints (md:) for seamless Android/laptop experience
- **Voice Commands**: Browser Speech Recognition API for hands-free navigation ("go to dashboard", "start routine", etc.)
- **Security**: Removed hardcoded API keys, now uses environment variables (__gemini_api_key) only

### Recent Bug Fixes (November 6, 2025)
- **AR Skeleton Drawing Fix** (Critical):
  - Fixed runtime errors in skeleton drawing where `this.keypointIndices` and `this.SKELETON_CONNECTIONS` were undefined
  - Changed to use module-level `keypointIndices` and `SKELETON_CONNECTIONS` constants
  - Fixed keypoint access from `.find(k => k.id === i)` to direct array access `keypoints[i]`
  - Added null checks for `corrections` and `affectedKeypoints` parameters to prevent crashes
  - Skeleton now renders properly with color-coded feedback on live video feed
- **Reference Pose Display Restoration**:
  - Re-implemented side-by-side reference pose display in AR correction mode
  - Shows pose name, targeted body parts, benefits, and precautions
  - Reference panel appears automatically when user selects a pose
- **Correction Log & Suggestions Panel Restoration**:
  - Re-implemented detailed correction log panel with last 5 unique corrections
  - Color-coded feedback: ✓ (green) for correct, ⚠ (yellow) for warnings, ✗ (red) for errors
  - Auto-scrolls to latest correction for better UX
  - Prevents duplicate logging of same correction message
- **AR Correction MIN_CONFIDENCE Fix**:
  - Fixed bug where `this.MIN_CONFIDENCE` was undefined, causing all low-confidence keypoints to pass validation
  - Changed to module-level `MIN_CONFIDENCE` constant for proper pose detection threshold
  - Now properly filters keypoints with score < 0.3 for accurate pose feedback

### Previous Changes (November 5, 2025)
- **Side-by-Side Reference Pose Display**: Added reference pose images alongside user's camera feed in AR correction mode
- **Detailed Correction Guidance Panel**: Added instructive feedback panel with step-by-step corrections
- **Camera Optimization**: Enhanced camera settings for smooth pose tracking (1280x720, 30-60fps)
- **Fixed Scoring Accuracy**: Confidence checks prevent "random" angles from undetected keypoints
- **Improved Validation Logic**: Tadasana validation rewritten with detailed feedback

## Usage Instructions

### Running the Web Platform

The yoga web platform runs automatically via the configured workflow. The server is already running on port 5000.

**Access the platform:**
- Click the "Open Website" button in the Replit interface
- Or navigate to the provided Replit URL in your browser

**Web Platform Features:**
1. **Dashboard** - View your progress, streak, and wellness metrics
2. **Asana Library** - Browse all available yoga poses with descriptions
3. **AR Correction** - Real-time camera-based pose correction (requires camera permission)
4. **Virtual Assistant** - Ask yoga questions to the AI (requires Gemini API key)

**Browser Voice Control (Built-in):**
- Click the microphone button in the top-right corner of the web interface
- Say commands like "go to dashboard", "open pose library", "start posture correction"
- This works entirely in the browser - no additional setup needed

### Running the Sunday AI Voice Assistant (Optional)

The Sunday AI Voice Assistant (`assistant.py`) provides advanced voice control with wake word detection.

**Important:** This requires:
- Microphone access
- Chrome browser installed
- Active internet connection
- Ability to run desktop applications

**To run the assistant locally:**
1. Open a new Shell terminal
2. Run: `python assistant.py`
3. The assistant will:
   - Calibrate your microphone
   - Open a Chrome browser window with the yoga platform
   - Start listening for the wake word "Sunday"

**Voice Commands:**
- Say "Sunday" to activate the assistant
- Follow with commands like:
  - "Sunday, open pose library"
  - "Sunday, start posture correction"
  - "Sunday, show my routine"
  - "Sunday, go to dashboard"
  - "Sunday, stop" (to shutdown)

**Features:**
- Wake word detection for hands-free operation
- Text-to-speech responses with natural acknowledgements
- Browser automation for seamless navigation
- Conversation logging to `conversation_log.txt`
- Status tracking in `sunday_status.json`

**Note:** The voice assistant may have limited functionality in the Replit web environment. For full functionality, consider running the project locally on your computer.

### Integrations

**Gemini API (Virtual Assistant Feature):**
- The Virtual Assistant tab uses Gemini 2.5 Flash for AI-powered yoga guidance
- To enable this feature, set up the Gemini integration using Replit's integration system
- The integration ID is: `javascript_gemini`
- Once configured, you can ask questions about yoga poses, wellness, nutrition, and more

### Troubleshooting

**Camera not working:**
- Ensure you've granted camera permissions in your browser
- Try refreshing the page
- Check if another application is using the camera

**Voice commands not working (Browser):**
- Ensure you've granted microphone permissions
- Check browser compatibility (Chrome, Edge recommended)
- Click the microphone button to activate listening

**Voice assistant (Python) not starting:**
- Verify Chrome is installed
- Check microphone permissions
- Review `conversation_log.txt` for error messages
- Ensure all Python packages are installed

**Virtual Assistant returning errors:**
- Set up the Gemini integration properly
- Check that the API key is configured
- Verify internet connection

### Development Workflow

**File Structure:**
- `server.py` - HTTP server for the web platform
- `assistant.py` - Python voice assistant with wake word detection
- `index.html` - Main web application
- `assets/poses/` - Reference images for yoga poses
- `README.md` - Comprehensive project documentation

**Making Changes:**
- Edit files directly in the Replit editor
- The server automatically restarts when files change
- Refresh your browser to see web platform updates
- Restart the voice assistant manually if you change `assistant.py`

**Logs:**
- Server logs appear in the workflow console
- Voice assistant logs are written to `conversation_log.txt`
- Browser console logs are accessible via browser developer tools