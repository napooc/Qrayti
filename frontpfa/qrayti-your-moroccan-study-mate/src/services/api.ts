/**
 * API Service for Qrayti Backend
 * Connects frontend to the FastAPI backend with microsoft/phi-2 model
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Log API URL on load for debugging
console.log('🔌 API Base URL:', API_BASE_URL);

export interface UploadPDFResponse {
  fileName: string;
  content: string;
  pageCount: number;
}

export interface QuizQuestion {
  id: number;
  question: string;
  options: string[];
  correctIndex: number;
  explanation: string;
  explanationDarija: string;
}

export interface QuizResponse {
  questions: QuizQuestion[];
}

export interface KeyTerm {
  term: string;
  definition: string;
  definitionDarija: string;
}

export interface SummarySection {
  title: string;
  content: string;
  keyTerms: KeyTerm[];
  essentialPoints: string[];
}

export interface SummaryResponse {
  sections: SummarySection[];
}

/**
 * Upload a PDF file and extract its text content
 */
export async function uploadPDF(file: File): Promise<UploadPDFResponse> {
  console.log('📤 Uploading PDF:', file.name, `(${(file.size / 1024 / 1024).toFixed(2)} MB)`);
  
  // Check file size (max 50MB)
  const MAX_SIZE = 50 * 1024 * 1024; // 50MB
  if (file.size > MAX_SIZE) {
    throw new Error(`File too large. Maximum size is 50MB. Your file is ${(file.size / 1024 / 1024).toFixed(2)}MB`);
  }
  
  const formData = new FormData();
  formData.append('file', file);

  try {
    // Create abort controller for timeout
    const controller = new AbortController();
    const timeoutId = setTimeout(() => {
      controller.abort();
    }, 60000); // 60 second timeout for upload + extraction

    const response = await fetch(`${API_BASE_URL}/api/upload-pdf`, {
      method: 'POST',
      body: formData,
      mode: 'cors',
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    console.log('📥 Upload response status:', response.status);

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Upload failed' }));
      console.error('❌ Upload error:', error);
      throw new Error(error.detail || 'Failed to upload PDF');
    }

    const data = await response.json();
    console.log('✅ Upload successful:', data.fileName, `(${data.pageCount} pages)`);
    return data;
  } catch (error) {
    console.error('❌ Upload fetch error:', error);
    
    if (error instanceof Error && error.name === 'AbortError') {
      throw new Error(
        'Upload timed out. The file might be too large or the server is slow. ' +
        'Try a smaller PDF or check your connection.'
      );
    }
    
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error(
        `Cannot connect to backend at ${API_BASE_URL}. ` +
        'Make sure the server is running: cd backend && python main.py'
      );
    }
    
    if (error instanceof Error) {
      throw error;
    }
    throw new Error('Failed to upload PDF. Please check your connection.');
  }
}

/**
 * Generate a quiz from the provided content
 */
export async function generateQuiz(
  content: string,
  numQuestions: number = 5
): Promise<QuizResponse> {
  console.log('🧠 Generating quiz, content length:', content.length, 'questions:', numQuestions);
  
  try {
    // Create abort controller for timeout - reduced to 60 seconds for faster feedback
    const controller = new AbortController();
    const timeoutId = setTimeout(() => {
      controller.abort();
    }, 60000); // 60 second timeout for quiz generation

    const response = await fetch(`${API_BASE_URL}/api/generate-quiz`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        content,
        num_questions: numQuestions,
      }),
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    console.log('📥 Quiz response status:', response.status);

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Quiz generation failed' }));
      console.error('❌ Quiz error:', error);
      throw new Error(error.detail || 'Failed to generate quiz');
    }

    const data = await response.json();
    console.log('✅ Quiz generated:', data.questions?.length, 'questions');
    return data;
  } catch (error) {
    console.error('❌ Quiz fetch error:', error);
    
    if (error instanceof Error && error.name === 'AbortError') {
      throw new Error(
        'Quiz generation timed out after 60 seconds. ' +
        'The server might be slow or the model is not responding. ' +
        'Please check backend logs and restart the server if needed.'
      );
    }
    
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error(
        `Cannot connect to backend at ${API_BASE_URL}. ` +
        'Make sure the server is running: cd backend && python main.py'
      );
    }
    
    if (error instanceof Error) {
      throw error;
    }
    throw new Error('Failed to generate quiz. Please check your connection.');
  }
}

/**
 * Generate a summary from the provided content
 */
export async function generateSummary(content: string): Promise<SummaryResponse> {
  console.log('🧠 Generating summary, content length:', content.length);
  
  try {
    // Create abort controller for timeout - reduced to 60 seconds for faster feedback
    const controller = new AbortController();
    const timeoutId = setTimeout(() => {
      controller.abort();
    }, 60000); // 60 second timeout for summary generation

    const response = await fetch(`${API_BASE_URL}/api/generate-summary`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ content }),
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    console.log('📥 Summary response status:', response.status);

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Summary generation failed' }));
      console.error('❌ Summary error:', error);
      throw new Error(error.detail || 'Failed to generate summary');
    }

    const data = await response.json();
    console.log('✅ Summary generated:', data.sections?.length, 'sections');
    return data;
  } catch (error) {
    console.error('❌ Summary fetch error:', error);
    
    if (error instanceof Error && error.name === 'AbortError') {
      throw new Error(
        'Summary generation timed out after 60 seconds. ' +
        'The server might be slow or the model is not responding. ' +
        'Please check backend logs and restart the server if needed.'
      );
    }
    
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error(
        `Cannot connect to backend at ${API_BASE_URL}. ` +
        'Make sure the server is running: cd backend && python main.py'
      );
    }
    
    if (error instanceof Error) {
      throw error;
    }
    throw new Error('Failed to generate summary. Please check your connection.');
  }
}

/**
 * Check if the backend is healthy and ready
 */
export async function checkHealth(): Promise<{
  status: string;
  model_type: string;
  model_ready: boolean;
}> {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    
    if (!response.ok) {
      throw new Error('Backend is not responding');
    }

    return await response.json();
  } catch (error) {
    throw new Error('Cannot connect to backend. Make sure the server is running.');
  }
}

