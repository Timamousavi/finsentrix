import axios from 'axios';

// Use relative URL when in development, absolute URL in production
const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? process.env.REACT_APP_API_BASE_URL 
  : 'http://localhost:8000';  // FastAPI default port

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  // Add timeout
  timeout: 30000,
});

// Add request interceptor for error handling
api.interceptors.request.use(
  (config) => {
    console.log('Making request to:', config.url);
    return config;
  },
  (error) => {
    console.error('Request error:', error);
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
      console.error('Status:', error.response.status);
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

export const detectRumors = async (input: string | Array<{ text: string; timestamp: string }>): Promise<Rumor[]> => {
  try {
    const payload = typeof input === 'string' ? { text: input } : input;
    const endpoint = typeof input === 'string' ? '/rumors/detect' : '/analyze/rumors';
    const response = await api.post(endpoint, payload);
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
  details?: Record<string, number>;
}

export interface Event {
  timestamp: string;
  text: string;
  type: string;
  sentiment_impact: number;
}

export interface TimelineData {
  events: Event[];
  sentiment_data: Array<{
    timestamp: string;
    sentiment_score: number;
  }>;
  visualization?: string;
}

export interface ApiInfo {
  version: string;
  created_at: string;
  last_updated: string;
  performance_metrics: Record<string, number>;
  supported_languages: string[];
  supported_markets: string[];
  supported_regions: string[];
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

export const getApiInfo = async (): Promise<ApiInfo> => {
  try {
    const response = await api.get('/model/info');
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

export const getTimeline = async (startTime?: Date, endTime?: Date): Promise<TimelineData> => {
  try {
    const params = new URLSearchParams();
    if (startTime) {
      params.append('start_time', startTime.toISOString());
    }
    if (endTime) {
      params.append('end_time', endTime.toISOString());
    }
    
    const response = await api.get(`/timeline?${params.toString()}`);
    return response.data.timeline;
  } catch (error) {
    console.error('Error getting timeline:', error);
    throw error;
  }
};

export const getRecentAnalyses = async (limit: number = 10): Promise<SentimentResult[]> => {
  try {
    const response = await api.get(`/analyze/recent?limit=${limit}`);
    return response.data;
  } catch (error) {
    console.error('Error getting recent analyses:', error);
    throw error;
  }
}; 