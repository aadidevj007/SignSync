import { initializeApp } from 'firebase/app';
import { getAuth, GoogleAuthProvider } from 'firebase/auth';
import { getFirestore } from 'firebase/firestore';
import { getStorage } from 'firebase/storage';

const firebaseConfig = {
  apiKey: "AIzaSyDgPVqTrWmh-fSwadDcQU3YGNlAKpu1h9w",
  authDomain: "signsync-meet.firebaseapp.com",
  projectId: "signsync-meet",
  storageBucket: "signsync-meet.firebasestorage.app",
  messagingSenderId: "774712370796",
  appId: "1:774712370796:web:ed9cbe86d012beda515a49",
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firebase services
export const auth = getAuth(app);
export const db = getFirestore(app);
export const storage = getStorage(app);
export const googleProvider = new GoogleAuthProvider();

// Configure Google Auth Provider
googleProvider.setCustomParameters({
  prompt: 'select_account'
});

export default app;
