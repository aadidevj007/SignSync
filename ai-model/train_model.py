#!/usr/bin/env python3
"""
SignSync Meet AI Model Training Script
Trains a CNN model for American Sign Language (ASL) recognition using MediaPipe Hands
"""

import os
import cv2
import numpy as np
import mediapipe as mp
import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pickle
import json
from datetime import datetime

class SignLanguageTrainer:
    def __init__(self, data_path="./data", model_path="./models"):
        self.data_path = data_path
        self.model_path = model_path
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=True,
            max_num_hands=1,
            min_detection_confidence=0.5
        )
        
        # Create directories if they don't exist
        os.makedirs(self.data_path, exist_ok=True)
        os.makedirs(self.model_path, exist_ok=True)
        
        # ASL alphabet (A-Z, excluding J and Z which require motion)
        self.asl_letters = [chr(i) for i in range(65, 91) if i not in [74, 90]]
        self.num_classes = len(self.asl_letters)
        
        print(f"Training model for {self.num_classes} ASL letters: {self.asl_letters}")
    
    def extract_hand_features(self, image_path):
        """Extract hand landmarks using MediaPipe"""
        try:
            image = cv2.imread(image_path)
            if image is None:
                return None
            
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
            print(f"Error processing {image_path}: {e}")
            return None
    
    def load_dataset(self):
        """Load and preprocess the dataset"""
        print("Loading dataset...")
        
        features = []
        labels = []
        
        for letter in self.asl_letters:
            letter_path = os.path.join(self.data_path, letter)
            if not os.path.exists(letter_path):
                print(f"Warning: No data found for letter {letter}")
                continue
            
            print(f"Processing letter {letter}...")
            
            # Process each image in the letter directory
            for filename in os.listdir(letter_path):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    image_path = os.path.join(letter_path, filename)
                    landmarks = self.extract_hand_features(image_path)
                    
                    if landmarks is not None:
                        features.append(landmarks)
                        labels.append(letter)
        
        if not features:
            raise ValueError("No valid data found. Please ensure your data directory contains images.")
        
        # Convert to numpy arrays
        X = np.array(features)
        y = np.array(labels)
        
        print(f"Dataset loaded: {len(X)} samples, {len(np.unique(y))} classes")
        print(f"Feature shape: {X.shape}")
        
        return X, y
    
    def create_model(self, input_shape):
        """Create CNN model architecture"""
        model = models.Sequential([
            # Input layer
            layers.Input(shape=input_shape),
            
            # Dense layers for landmark processing
            layers.Dense(256, activation='relu'),
            layers.Dropout(0.3),
            layers.Dense(128, activation='relu'),
            layers.Dropout(0.3),
            layers.Dense(64, activation='relu'),
            layers.Dropout(0.2),
            
            # Output layer
            layers.Dense(self.num_classes, activation='softmax')
        ])
        
        # Compile model
        model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def train_model(self, X, y, epochs=100, batch_size=32):
        """Train the model"""
        print("Creating and training model...")
        
        # Encode labels
        label_encoder = LabelEncoder()
        y_encoded = label_encoder.fit_transform(y)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
        )
        
        # Create model
        model = self.create_model(X_train.shape[1:])
        
        # Print model summary
        model.summary()
        
        # Training callbacks
        callbacks = [
            tf.keras.callbacks.EarlyStopping(
                monitor='val_loss', 
                patience=10, 
                restore_best_weights=True
            ),
            tf.keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss', 
                factor=0.5, 
                patience=5, 
                min_lr=1e-7
            )
        ]
        
        # Train model
        history = model.fit(
            X_train, y_train,
            validation_data=(X_test, y_test),
            epochs=epochs,
            batch_size=batch_size,
            callbacks=callbacks,
            verbose=1
        )
        
        # Evaluate model
        test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)
        print(f"\nTest accuracy: {test_accuracy:.4f}")
        print(f"Test loss: {test_loss:.4f}")
        
        return model, label_encoder, history
    
    def save_model(self, model, label_encoder, history):
        """Save the trained model and metadata"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save model
        model_path = os.path.join(self.model_path, f"sign_language_model_{timestamp}.h5")
        model.save(model_path)
        print(f"Model saved to: {model_path}")
        
        # Save label encoder
        encoder_path = os.path.join(self.model_path, f"label_encoder_{timestamp}.pkl")
        with open(encoder_path, 'wb') as f:
            pickle.dump(label_encoder, f)
        print(f"Label encoder saved to: {encoder_path}")
        
        # Save training history
        history_path = os.path.join(self.model_path, f"training_history_{timestamp}.json")
        with open(history_path, 'w') as f:
            json.dump(history.history, f, indent=2)
        print(f"Training history saved to: {history_path}")
        
        # Save latest model paths
        latest_paths = {
            'model': model_path,
            'encoder': encoder_path,
            'history': history_path,
            'timestamp': timestamp
        }
        
        latest_paths_file = os.path.join(self.model_path, "latest_model.json")
        with open(latest_paths_file, 'w') as f:
            json.dump(latest_paths, f, indent=2)
        
        return latest_paths
    
    def run_training(self, epochs=100, batch_size=32):
        """Run the complete training pipeline"""
        try:
            print("Starting SignSync Meet AI Model Training...")
            print("=" * 50)
            
            # Load dataset
            X, y = self.load_dataset()
            
            # Train model
            model, label_encoder, history = self.train_model(X, y, epochs, batch_size)
            
            # Save model
            latest_paths = self.save_model(model, label_encoder, history)
            
            print("\nTraining completed successfully!")
            print("=" * 50)
            print(f"Model saved to: {latest_paths['model']}")
            print(f"Label encoder saved to: {latest_paths['encoder']}")
            
            return latest_paths
            
        except Exception as e:
            print(f"Training failed: {e}")
            raise

def main():
    """Main function to run training"""
    # Initialize trainer
    trainer = SignLanguageTrainer()
    
    # Run training
    try:
        latest_paths = trainer.run_training(epochs=100, batch_size=32)
        print("\n🎉 Training completed successfully!")
        print(f"📁 Model files saved in: {trainer.model_path}")
        
    except Exception as e:
        print(f"\n❌ Training failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
