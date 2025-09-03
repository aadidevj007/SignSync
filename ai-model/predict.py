#!/usr/bin/env python3
"""
SignSync Meet AI Model Prediction Script
Real-time sign language recognition using trained CNN model and MediaPipe Hands
"""

import os
import cv2
import numpy as np
import mediapipe as mp
import tensorflow as tf
import pickle
import json
from typing import Optional, Tuple, List
import time

class SignLanguagePredictor:
    def __init__(self, model_dir="./models"):
        self.model_dir = model_dir
        self.model = None
        self.label_encoder = None
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        
        # Load the latest trained model
        self.load_latest_model()
        
        # Prediction history for smoothing
        self.prediction_history = []
        self.history_size = 5
        
        print("SignSync Meet AI Predictor initialized!")
    
    def load_latest_model(self):
        """Load the latest trained model and label encoder"""
        try:
            # Check for latest model info
            latest_model_file = os.path.join(self.model_dir, "latest_model.json")
            
            if not os.path.exists(latest_model_file):
                print("No trained model found. Please run training first.")
                return
            
            with open(latest_model_file, 'r') as f:
                latest_info = json.load(f)
            
            model_path = latest_info['model']
            encoder_path = latest_info['encoder']
            
            # Load model
            print(f"Loading model from: {model_path}")
            self.model = tf.keras.models.load_model(model_path)
            
            # Load label encoder
            print(f"Loading label encoder from: {encoder_path}")
            with open(encoder_path, 'rb') as f:
                self.label_encoder = pickle.load(f)
            
            print("Model and encoder loaded successfully!")
            
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model = None
            self.label_encoder = None
    
    def extract_hand_landmarks(self, image: np.ndarray) -> Optional[np.ndarray]:
        """Extract hand landmarks from image using MediaPipe"""
        try:
            # Convert BGR to RGB
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Process image with MediaPipe
            results = self.hands.process(image_rgb)
            
            if results.multi_hand_landmarks:
                # Get landmarks for the first detected hand
                hand_landmarks = results.multi_hand_landmarks[0]
                
                # Extract 21 landmark points (x, y, z coordinates)
                landmarks = []
                for landmark in hand_landmarks.landmark:
                    landmarks.extend([landmark.x, landmark.y, landmark.z])
                
                return np.array(landmarks)
            else:
                return None
                
        except Exception as e:
            print(f"Error extracting landmarks: {e}")
            return None
    
    def predict_sign(self, landmarks: np.ndarray) -> Tuple[str, float]:
        """Predict sign language from hand landmarks"""
        if self.model is None or self.label_encoder is None:
            return "Model not loaded", 0.0
        
        try:
            # Reshape landmarks for model input
            landmarks_reshaped = landmarks.reshape(1, -1)
            
            # Make prediction
            prediction = self.model.predict(landmarks_reshaped, verbose=0)
            
            # Get predicted class and confidence
            predicted_class_idx = np.argmax(prediction[0])
            confidence = float(prediction[0][predicted_class_idx])
            
            # Decode class label
            predicted_class = self.label_encoder.inverse_transform([predicted_class_idx])[0]
            
            return predicted_class, confidence
            
        except Exception as e:
            print(f"Error during prediction: {e}")
            return "Error", 0.0
    
    def smooth_predictions(self, prediction: str, confidence: float) -> Tuple[str, float]:
        """Smooth predictions using history to reduce jitter"""
        # Add current prediction to history
        self.prediction_history.append((prediction, confidence))
        
        # Keep only recent predictions
        if len(self.prediction_history) > self.history_size:
            self.prediction_history.pop(0)
        
        # If we have enough history, use majority voting
        if len(self.prediction_history) >= 3:
            # Get most common prediction
            predictions = [p[0] for p in self.prediction_history]
            from collections import Counter
            most_common = Counter(predictions).most_common(1)[0]
            
            # Calculate average confidence for most common prediction
            avg_confidence = np.mean([p[1] for p in self.prediction_history if p[0] == most_common[0]])
            
            return most_common[0], avg_confidence
        
        # Return current prediction if not enough history
        return prediction, confidence
    
    def process_frame(self, frame: np.ndarray) -> Tuple[str, float, np.ndarray]:
        """Process a single frame and return prediction results"""
        # Extract hand landmarks
        landmarks = self.extract_hand_landmarks(frame)
        
        if landmarks is not None:
            # Make prediction
            prediction, confidence = self.predict_sign(landmarks)
            
            # Smooth predictions
            smoothed_prediction, smoothed_confidence = self.smooth_predictions(prediction, confidence)
            
            # Draw hand landmarks on frame
            annotated_frame = self.draw_landmarks(frame, landmarks)
            
            return smoothed_prediction, smoothed_confidence, annotated_frame
        else:
            # No hand detected
            return "No hand detected", 0.0, frame
    
    def draw_landmarks(self, frame: np.ndarray, landmarks: np.ndarray) -> np.ndarray:
        """Draw hand landmarks on the frame"""
        try:
            # Convert landmarks back to MediaPipe format for drawing
            h, w, _ = frame.shape
            
            # Create MediaPipe drawing utilities
            mp_drawing = mp.solutions.drawing_utils
            mp_drawing_styles = mp.solutions.drawing_styles
            
            # Convert landmarks to MediaPipe format
            hand_landmarks = self.mp_hands.HandLandmark
            landmarks_list = []
            
            for i in range(0, len(landmarks), 3):
                x, y, z = landmarks[i:i+3]
                # Convert normalized coordinates to pixel coordinates
                px, py = int(x * w), int(y * h)
                landmarks_list.append(mp_drawing.DrawingSpec(
                    color=(0, 255, 0), thickness=2, circle_radius=2
                ))
            
            # Draw landmarks
            annotated_frame = frame.copy()
            
            # Draw hand connections
            mp_drawing.draw_landmarks(
                annotated_frame,
                landmarks_list,
                self.mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style()
            )
            
            return annotated_frame
            
        except Exception as e:
            print(f"Error drawing landmarks: {e}")
            return frame
    
    def real_time_prediction(self, camera_index: int = 0):
        """Run real-time prediction from camera feed"""
        print("Starting real-time sign language prediction...")
        print("Press 'q' to quit, 's' to save current frame")
        
        cap = cv2.VideoCapture(camera_index)
        
        if not cap.isOpened():
            print("Error: Could not open camera")
            return
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("Error: Could not read frame")
                    break
                
                # Process frame
                prediction, confidence, annotated_frame = self.process_frame(frame)
                
                # Add prediction text to frame
                text = f"Prediction: {prediction} ({confidence:.2f})"
                cv2.putText(annotated_frame, text, (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                # Add instructions
                cv2.putText(annotated_frame, "Press 'q' to quit, 's' to save", 
                           (10, annotated_frame.shape[0] - 20), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                
                # Display frame
                cv2.imshow('SignSync Meet - Sign Language Recognition', annotated_frame)
                
                # Handle key presses
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('s'):
                    # Save current frame
                    timestamp = int(time.time())
                    filename = f"captured_frame_{timestamp}.jpg"
                    cv2.imwrite(filename, annotated_frame)
                    print(f"Frame saved as: {filename}")
                
                # Small delay to reduce CPU usage
                time.sleep(0.03)
                
        finally:
            cap.release()
            cv2.destroyAllWindows()
            print("Real-time prediction stopped")
    
    def predict_from_image(self, image_path: str) -> Tuple[str, float]:
        """Predict sign language from a single image"""
        try:
            # Load image
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Could not load image: {image_path}")
            
            # Extract landmarks
            landmarks = self.extract_hand_landmarks(image)
            
            if landmarks is not None:
                # Make prediction
                prediction, confidence = self.predict_sign(landmarks)
                return prediction, confidence
            else:
                return "No hand detected", 0.0
                
        except Exception as e:
            print(f"Error processing image {image_path}: {e}")
            return "Error", 0.0

def main():
    """Main function for testing the predictor"""
    # Initialize predictor
    predictor = SignLanguagePredictor()
    
    if predictor.model is None:
        print("❌ Model not loaded. Please train a model first.")
        return 1
    
    print("\n🎯 SignSync Meet AI Predictor Ready!")
    print("Choose an option:")
    print("1. Real-time camera prediction")
    print("2. Predict from image file")
    print("3. Exit")
    
    while True:
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            print("\nStarting real-time prediction...")
            predictor.real_time_prediction()
            
        elif choice == '2':
            image_path = input("Enter image path: ").strip()
            if os.path.exists(image_path):
                prediction, confidence = predictor.predict_from_image(image_path)
                print(f"\nPrediction: {prediction}")
                print(f"Confidence: {confidence:.2f}")
            else:
                print("❌ Image file not found!")
                
        elif choice == '3':
            print("👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")
    
    return 0

if __name__ == "__main__":
    exit(main())
