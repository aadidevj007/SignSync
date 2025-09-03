import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { useProfile } from '../contexts/ProfileContext';
import { useEffect } from 'react';

const WelcomePage = () => {
  const navigate = useNavigate();
  const { currentUser } = useAuth();
  const { profile, loading } = useProfile();

  useEffect(() => {
    if (currentUser && !loading) {
      if (profile) {
        navigate('/dashboard');
      } else {
        navigate('/profile-setup');
      }
    }
  }, [currentUser, profile, loading, navigate]);

  const handleGetStarted = () => {
    navigate('/auth');
  };

  return (
    <div className="min-h-screen relative overflow-hidden">
      {/* Background with gradient overlay */}
      <div className="absolute inset-0 bg-gradient-to-br from-blue-900 via-purple-900 to-indigo-900">
        <div className="absolute inset-0 bg-black bg-opacity-50"></div>
      </div>

      {/* Animated background elements */}
      <div className="absolute inset-0">
        <div className="absolute top-20 left-20 w-72 h-72 bg-blue-400 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse"></div>
        <div className="absolute top-40 right-20 w-72 h-72 bg-purple-400 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse animation-delay-2000"></div>
        <div className="absolute -bottom-8 left-40 w-72 h-72 bg-pink-400 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse animation-delay-4000"></div>
      </div>

      {/* Main content */}
      <div className="relative z-10 flex flex-col items-center justify-center min-h-screen text-white px-4">
        {/* Logo and Title */}
        <div className="text-center mb-12 animate-fade-in">
          <div className="mb-6">
            <div className="w-24 h-24 mx-auto bg-white bg-opacity-20 rounded-full flex items-center justify-center backdrop-blur-sm">
              <svg className="w-12 h-12 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
          <h1 className="text-5xl md:text-7xl font-bold mb-4 bg-gradient-to-r from-white to-blue-200 bg-clip-text text-transparent">
            SignSync Meet
          </h1>
          <p className="text-xl md:text-2xl text-blue-100 max-w-2xl mx-auto leading-relaxed">
            AI-Powered Video Conferencing with Real-Time Sign Language Translation
          </p>
        </div>

        {/* Intro Video Section */}
        <div className="mb-12 max-w-4xl w-full animate-slide-up">
          <div className="bg-white bg-opacity-10 backdrop-blur-sm rounded-2xl p-8 border border-white border-opacity-20">
            <h2 className="text-2xl font-semibold mb-4 text-center">Welcome to the Future of Inclusive Communication</h2>
            <div className="aspect-video bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center">
              <div className="text-center">
                <svg className="w-16 h-16 mx-auto mb-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clipRule="evenodd" />
                </svg>
                <p className="text-white font-medium">Intro Video</p>
                <p className="text-blue-100 text-sm">Learn about SignSync Meet's features</p>
              </div>
            </div>
          </div>
        </div>

        {/* Features */}
        <div className="mb-12 grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl w-full animate-slide-up">
          <div className="text-center p-6 bg-white bg-opacity-10 backdrop-blur-sm rounded-xl border border-white border-opacity-20">
            <div className="w-16 h-16 mx-auto mb-4 bg-blue-500 rounded-full flex items-center justify-center">
              <svg className="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74a1 1 0 01.836.986V17a1 1 0 01-1 1h-2C7.82 18 2 12.18 2 5V3z" />
              </svg>
            </div>
            <h3 className="text-lg font-semibold mb-2">Real-Time Translation</h3>
            <p className="text-blue-100">Instant sign language to text and speech conversion</p>
          </div>

          <div className="text-center p-6 bg-white bg-opacity-10 backdrop-blur-sm rounded-xl border border-white border-opacity-20">
            <div className="w-16 h-16 mx-auto mb-4 bg-purple-500 rounded-full flex items-center justify-center">
              <svg className="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v3h8v-3z" />
              </svg>
            </div>
            <h3 className="text-lg font-semibold mb-2">Inclusive Design</h3>
            <p className="text-blue-100">Built for everyone, accessible to all</p>
          </div>

          <div className="text-center p-6 bg-white bg-opacity-10 backdrop-blur-sm rounded-xl border border-white border-opacity-20">
            <div className="w-16 h-16 mx-auto mb-4 bg-pink-500 rounded-full flex items-center justify-center">
              <svg className="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clipRule="evenodd" />
              </svg>
            </div>
            <h3 className="text-lg font-semibold mb-2">AI-Powered</h3>
            <p className="text-blue-100">Advanced machine learning for accurate recognition</p>
          </div>
        </div>

        {/* CTA Button */}
        <div className="animate-slide-up">
          <button
            onClick={handleGetStarted}
            className="px-8 py-4 bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white font-semibold text-lg rounded-full transition-all duration-300 transform hover:scale-105 hover:shadow-2xl focus:outline-none focus:ring-4 focus:ring-blue-300 focus:ring-opacity-50"
          >
            Get Started
          </button>
        </div>

        {/* Footer */}
        <footer className="absolute bottom-0 left-0 right-0 bg-black bg-opacity-30 backdrop-blur-sm py-6">
          <div className="text-center text-blue-100">
            <p className="text-sm">Created by Team SignSync</p>
            <div className="flex justify-center space-x-8 mt-2">
              <div className="text-center">
                <div className="w-12 h-12 mx-auto mb-2 bg-gray-600 rounded-full"></div>
                <p className="text-xs">John Doe</p>
                <p className="text-xs text-gray-300">Reg: 12345</p>
                <p className="text-xs text-gray-300">CSE</p>
              </div>
              <div className="text-center">
                <div className="w-12 h-12 mx-auto mb-2 bg-gray-600 rounded-full"></div>
                <p className="text-xs">Jane Smith</p>
                <p className="text-xs text-gray-300">Reg: 12346</p>
                <p className="text-xs text-gray-300">CSE</p>
              </div>
              <div className="text-center">
                <div className="w-12 h-12 mx-auto mb-2 bg-gray-600 rounded-full"></div>
                <p className="text-xs">Bob Johnson</p>
                <p className="text-xs text-gray-300">Reg: 12347</p>
                <p className="text-xs text-gray-300">CSE</p>
              </div>
              <div className="text-center">
                <div className="w-12 h-12 mx-auto mb-2 bg-gray-600 rounded-full"></div>
                <p className="text-xs">Alice Brown</p>
                <p className="text-xs text-gray-300">Reg: 12348</p>
                <p className="text-xs text-gray-300">CSE</p>
              </div>
            </div>
          </div>
        </footer>
      </div>
    </div>
  );
};

export default WelcomePage;
