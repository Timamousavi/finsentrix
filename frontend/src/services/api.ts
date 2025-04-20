import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

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

export const analyzeSentiment = async (text: string): Promise<any> => {
  try {
    const response = await api.post('/analyze', { text });
    return response.data;
  } catch (error) {
    console.error('Error analyzing sentiment:', error);
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