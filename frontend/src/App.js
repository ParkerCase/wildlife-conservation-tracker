import React, { useState, useEffect } from 'react';
import { Shield } from 'lucide-react';
import Login from './components/Login';
import WildlifeDashboard from './components/WildlifeDashboard';
import './index.css';

const App = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [authError, setAuthError] = useState('');
  const [isLoading, setIsLoading] = useState(true);

  // Check if user is already logged in (from localStorage)
  useEffect(() => {
    const checkAuthStatus = () => {
      try {
        const authData = localStorage.getItem('wildguard_auth');
        if (authData) {
          const { token, expiry } = JSON.parse(authData);
          if (Date.now() < expiry) {
            console.log('User already authenticated, loading dashboard...');
            setIsAuthenticated(true);
          } else {
            console.log('Auth token expired, removing...');
            localStorage.removeItem('wildguard_auth');
          }
        }
      } catch (error) {
        console.error('Error checking auth status:', error);
        localStorage.removeItem('wildguard_auth');
      }
      setIsLoading(false);
    };

    checkAuthStatus();
  }, []);

  // Handle login with username/password
  const handleLogin = async (credentials) => {
    console.log('Login attempt for username:', credentials.username);
    setAuthError('');

    try {
      // Simple username/password authentication
      // You can replace this with your actual authentication logic
      const validCredentials = {
        username: 'admin',
        password: 'wildguard2025',
        // Add more valid credentials as needed
        alternativeUsers: [
          { username: 'wildguard', password: 'conservation2025' },
          { username: 'parker', password: 'wildlife123' },
          { username: 'demo', password: 'demo123' },
          { username: 'conservation', password: 'tracker123' },
          { username: 'wildlife', password: 'guard2025' }
        ]
      };

      const isValidUser = 
        (credentials.username === validCredentials.username && credentials.password === validCredentials.password) ||
        validCredentials.alternativeUsers.some(user => 
          user.username === credentials.username && user.password === credentials.password
        );

      if (isValidUser) {
        // Create session token
        const sessionData = {
          username: credentials.username,
          token: `wildguard_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
          loginTime: Date.now(),
          expiry: Date.now() + (24 * 60 * 60 * 1000) // 24 hours
        };

        // Store in localStorage
        localStorage.setItem('wildguard_auth', JSON.stringify(sessionData));
        
        console.log('Login successful for user:', credentials.username);
        setIsAuthenticated(true);
        setAuthError('');
      } else {
        console.log('Login failed: Invalid credentials');
        throw new Error('Invalid username or password');
      }
    } catch (error) {
      console.error('Login error:', error);
      setAuthError(error.message);
      throw error;
    }
  };

  // Handle logout
  const handleLogout = () => {
    console.log('User logging out...');
    localStorage.removeItem('wildguard_auth');
    setIsAuthenticated(false);
    setAuthError('');
  };

  // Loading screen
  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <Shield size={48} className="text-blue-600 mx-auto mb-4 animate-pulse" />
          <h1 className="text-2xl font-bold text-gray-900 mb-2">WildGuard AI</h1>
          <p className="text-gray-600 mb-4">Initializing wildlife protection platform...</p>
          <div className="flex items-center justify-center space-x-2">
            <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce"></div>
            <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
            <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
          </div>
        </div>
      </div>
    );
  }

  // Show login screen if not authenticated
  if (!isAuthenticated) {
    return <Login onLogin={handleLogin} error={authError} />;
  }

  // Show enhanced dashboard if authenticated with real Supabase data
  return (
    <div className="app">
      <WildlifeDashboard onLogout={handleLogout} />
    </div>
  );
};

export default App;
