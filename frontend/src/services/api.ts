import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor for error handling
api.interceptors.request.use(
  (config) => {
    // Add any auth token here if needed
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // The request was made and the server responded with a status code
      // that falls out of the range of 2xx
      console.error('API Error:', error.response.data);
    } else if (error.request) {
      // The request was made but no response was received
      console.error('No response received:', error.request);
    } else {
      // Something happened in setting up the request that triggered an Error
      console.error('Error setting up request:', error.message);
    }
    return Promise.reject(error);
  }
);

export interface Rumor {
  id: string;
  text: string;
  confidence: number;
  type: string;
  timestamp: string;
}

export const detectRumors = async (text: string): Promise<Rumor[]> => {
  try {
    const response = await api.post('/rumors/detect', { text });
    return response.data;
  } catch (error) {
    console.error('Error detecting rumors:', error);
    throw error;
  }
};

export interface SentimentResult {
  text: string;
  sentiment: string;
  confidence: number;
  details: Record<string, number>;
}

export interface BatchSentimentResult {
  results: SentimentResult[];
}

export const analyzeSentiment = async (text: string, apiKey?: string): Promise<SentimentResult> => {
  try {
    const response = await api.post('/analyze', { text, api_key: apiKey });
    return response.data;
  } catch (error) {
    console.error('Error analyzing sentiment:', error);
    throw error;
  }
};

export const analyzeBatchSentiment = async (texts: string[], apiKey?: string): Promise<BatchSentimentResult> => {
  try {
    const response = await api.post('/analyze/batch', { texts, api_key: apiKey });
    return response.data;
  } catch (error) {
    console.error('Error analyzing batch sentiment:', error);
    throw error;
  }
};

export const getModelInfo = async (): Promise<any> => {
  try {
    const response = await api.get('/model/info');
    return response.data;
  } catch (error) {
    console.error('Error getting model info:', error);
    throw error;
  }
};

export const getApiInfo = async (): Promise<any> => {
  try {
    const response = await api.get('/');
    return response.data;
  } catch (error) {
    console.error('Error getting API info:', error);
    throw error;
  }
};

export const checkHealth = async (): Promise<boolean> => {
  try {
    const response = await api.get('/health');
    return response.data.status === 'healthy';
  } catch (error) {
    console.error('Health check failed:', error);
    return false;
  }
}; 