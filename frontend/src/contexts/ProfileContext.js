import React, { createContext, useContext, useState, useEffect } from 'react';
import { useAuth } from './AuthContext';

const ProfileContext = createContext();

export function useProfile() {
  return useContext(ProfileContext);
}

export function ProfileProvider({ children }) {
  const { currentUser, getUserProfile } = useAuth();
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (currentUser) {
      loadProfile();
    } else {
      setProfile(null);
      setLoading(false);
    }
  }, [currentUser]);

  const loadProfile = async () => {
    try {
      setLoading(true);
      const userProfile = await getUserProfile(currentUser.uid);
      setProfile(userProfile);
    } catch (error) {
      console.error('Error loading profile:', error);
      setProfile(null);
    } finally {
      setLoading(false);
    }
  };

  const updateProfile = (newProfileData) => {
    setProfile(prev => ({ ...prev, ...newProfileData }));
  };

  const value = {
    profile,
    loading,
    updateProfile,
    loadProfile
  };

  return (
    <ProfileContext.Provider value={value}>
      {children}
    </ProfileContext.Provider>
  );
}
