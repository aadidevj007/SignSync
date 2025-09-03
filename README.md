# 📌 SignSync Meet: AI-Powered Video Conferencing with Sign Language Translation

An inclusive video conferencing platform that provides real-time bidirectional sign language translation using AI and MediaPipe technology.

## 🌟 Features

- **Real-time Video Conferencing** - Built with Jitsi Meet SDK
- **AI-Powered Sign Language Recognition** - MediaPipe + CNN for gesture detection
- **Bidirectional Translation** - Speech-to-text, text-to-sign, and sign-to-text
- **Firebase Authentication** - Email/password and Google Sign-In
- **Responsive Design** - Beautiful UI with TailwindCSS
- **Real-time Communication** - Socket.IO for instant updates
- **Profile Management** - User profiles with photo uploads

## 🏗️ Project Structure

```
SignSyncMeet/
├── frontend/                 # React + Firebase + Jitsi
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/          # Application pages
│   │   ├── contexts/       # React contexts
│   │   └── utils/          # Utility functions
│   ├── public/             # Static assets
│   └── package.json        # Frontend dependencies
├── backend/                 # Flask + SocketIO APIs
│   ├── app.py              # Main Flask application
│   ├── requirements.txt    # Python dependencies
│   └── env.example        # Environment variables template
├── ai-model/               # MediaPipe + CNN implementation
│   ├── train_model.py      # Model training script
│   └── predict.py          # Real-time prediction script
├── gesture-videos/         # Sample sign language videos
└── README.md               # This file
```

## 🚀 Quick Start

### Prerequisites

- **Node.js** (v16 or higher)
- **Python** (v3.8 or higher)
- **Firebase Account** (for authentication and hosting)
- **Git** (for version control)

### 1. Clone the Repository

```bash
git clone <repository-url>
cd SignSyncMeet
```

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create Firebase project and update configuration
# Copy your Firebase config to src/firebase.js

# Start development server
npm start
```

**Firebase Configuration:**
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project
3. Enable Authentication (Email/Password + Google)
4. Enable Firestore Database
5. Enable Storage
6. Copy config to `src/firebase.js`

### 3. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp env.example .env
# Edit .env with your configuration

# Start Flask server
python app.py
```

**Environment Variables:**
- `SECRET_KEY`: Flask secret key
- `FIREBASE_*`: Firebase service account credentials
- `PORT`: Backend port (default: 5000)

### 4. AI Model Setup

```bash
cd ai-model

# Install additional dependencies
pip install mediapipe opencv-python tensorflow scikit-learn

# Prepare training data (optional)
# Place ASL images in data/ directory organized by letter

# Train the model
python train_model.py

# Test real-time prediction
python predict.py
```

## 🔧 Configuration

### Firebase Setup

1. **Authentication:**
   - Enable Email/Password authentication
   - Enable Google Sign-In
   - Add authorized domains

2. **Firestore Rules:**
```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
  }
}
```

3. **Storage Rules:**
```javascript
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    match /profile-photos/{userId}/{allPaths=**} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
  }
}
```

### Backend Configuration

1. **Firebase Admin SDK:**
   - Download service account key from Firebase Console
   - Update path in `app.py`

2. **CORS Settings:**
   - Update `cors_allowed_origins` in `app.py` for production

## 🚀 Deployment

### Frontend (Firebase Hosting)

```bash
cd frontend

# Build production version
npm run build

# Install Firebase CLI
npm install -g firebase-tools

# Login to Firebase
firebase login

# Initialize Firebase hosting
firebase init hosting

# Deploy
firebase deploy
```

### Backend (Render/Railway)

1. **Render:**
   - Connect GitHub repository
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `python app.py`
   - Add environment variables

2. **Railway:**
   - Connect GitHub repository
   - Set Python runtime
   - Add environment variables
   - Deploy automatically

### Environment Variables for Production

```bash
# Flask
SECRET_KEY=your-production-secret-key
FLASK_DEBUG=False
PORT=10000

# Firebase (use service account key file)
FIREBASE_SERVICE_ACCOUNT_PATH=./serviceAccountKey.json

# AI Model
MODEL_PATH=./ai-model/sign_language_model.h5
```

## 🧠 AI Model Training

### Data Preparation

1. **Collect ASL Images:**
   - Organize by letter (A, B, C, etc.)
   - Multiple angles and lighting conditions
   - Clean background, clear hand gestures

2. **Data Structure:**
```
data/
├── A/
│   ├── a1.jpg
│   ├── a2.jpg
│   └── ...
├── B/
│   ├── b1.jpg
│   └── ...
└── ...
```

### Training Process

```bash
cd ai-model

# Train with custom parameters
python train_model.py --epochs 200 --batch-size 64

# Monitor training progress
# Check models/ directory for saved models
```

### Model Performance

- **Target Accuracy**: >90% on test set
- **Training Time**: 2-4 hours on GPU
- **Model Size**: <50MB for web deployment

## 🔌 API Endpoints

### Authentication Required Endpoints

- `POST /api/speech-to-text` - Convert speech to text
- `POST /api/text-to-sign` - Convert text to sign language
- `POST /api/sign-to-text` - Recognize sign language gestures

### Public Endpoints

- `GET /` - API status
- `GET /api/health` - Health check

### WebSocket Events

- `connect` - Client connection
- `join_meeting` - Join video meeting
- `translation_request` - Request translation
- `translation_result` - Translation result

## 🧪 Testing

### Frontend Testing

```bash
cd frontend
npm test
```

### Backend Testing

```bash
cd backend
python -m pytest tests/
```

### AI Model Testing

```bash
cd ai-model
python predict.py
# Choose option 1 for real-time testing
```

## 🐛 Troubleshooting

### Common Issues

1. **Firebase Connection Error:**
   - Check Firebase config in `src/firebase.js`
   - Verify service account credentials

2. **Jitsi Meet Not Loading:**
   - Check browser console for errors
   - Verify network connectivity
   - Check Jitsi Meet external API

3. **AI Model Not Working:**
   - Ensure model files exist in `ai-model/models/`
   - Check Python dependencies
   - Verify MediaPipe installation

4. **Socket.IO Connection Issues:**
   - Check backend server status
   - Verify CORS settings
   - Check network firewall

### Debug Mode

```bash
# Frontend
REACT_APP_DEBUG=true npm start

# Backend
FLASK_DEBUG=True python app.py
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push branch: `git push origin feature-name`
5. Submit pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Team

**SignSync Meet Development Team:**
- **John Doe** - Reg: 12345, CSE
- **Jane Smith** - Reg: 12346, CSE  
- **Bob Johnson** - Reg: 12347, CSE
- **Alice Brown** - Reg: 12348, CSE

## 🙏 Acknowledgments

- **MediaPipe** - Hand landmark detection
- **Jitsi Meet** - Video conferencing platform
- **Firebase** - Authentication and hosting
- **TensorFlow** - Machine learning framework
- **TailwindCSS** - UI framework

## 📞 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

---

**Made with ❤️ for inclusive communication**
