export const config = {
  api: {
    baseUrl: process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000',
    timeout: 30000, // 30 seconds
    retryAttempts: 3,
  },
  features: {
    enableApiKey: process.env.REACT_APP_ENABLE_API_KEY === 'true',
    enableBatchAnalysis: process.env.REACT_APP_ENABLE_BATCH_ANALYSIS === 'true',
  },
  ui: {
    defaultLanguage: process.env.REACT_APP_DEFAULT_LANGUAGE || 'en',
    theme: {
      primaryColor: '#1890ff',
      secondaryColor: '#52c41a',
    },
  },
}; 