/**
 * Utility to check if backend is available
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export async function checkBackendConnection(): Promise<{
  isConnected: boolean;
  message: string;
  modelReady: boolean;
}> {
  try {
    console.log('🔍 Checking backend connection at:', API_BASE_URL);
    
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 5000); // 5 second timeout
    
    const response = await fetch(`${API_BASE_URL}/health`, {
      method: 'GET',
      signal: controller.signal,
    });
    
    clearTimeout(timeoutId);
    
    if (!response.ok) {
      return {
        isConnected: false,
        message: `Backend responded with status ${response.status}`,
        modelReady: false,
      };
    }
    
    const data = await response.json();
    console.log('✅ Backend health check:', data);
    
    return {
      isConnected: true,
      message: data.model_ready ? 'Backend is ready!' : 'Backend is starting...',
      modelReady: data.model_ready || false,
    };
  } catch (error) {
    console.error('❌ Backend connection failed:', error);
    
    if (error instanceof Error) {
      if (error.name === 'AbortError') {
        return {
          isConnected: false,
          message: 'Backend connection timeout. Server might be starting or not running.',
          modelReady: false,
        };
      }
      
      if (error.message.includes('fetch')) {
        return {
          isConnected: false,
          message: `Cannot connect to ${API_BASE_URL}. Make sure backend is running: python main.py`,
          modelReady: false,
        };
      }
    }
    
    return {
      isConnected: false,
      message: 'Unknown connection error',
      modelReady: false,
    };
  }
}

