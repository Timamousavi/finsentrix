import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface AnalysisState {
  text: string;
  sentiment: string;
  confidence: number;
  loading: boolean;
  error: string | null;
}

const initialState: AnalysisState = {
  text: '',
  sentiment: '',
  confidence: 0,
  loading: false,
  error: null,
};

const analysisSlice = createSlice({
  name: 'analysis',
  initialState,
  reducers: {
    setText: (state, action: PayloadAction<string>) => {
      state.text = action.payload;
    },
    setSentiment: (state, action: PayloadAction<string>) => {
      state.sentiment = action.payload;
    },
    setConfidence: (state, action: PayloadAction<number>) => {
      state.confidence = action.payload;
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload;
    },
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
    },
    resetAnalysis: (state) => {
      state.text = '';
      state.sentiment = '';
      state.confidence = 0;
      state.loading = false;
      state.error = null;
    },
  },
});

export const {
  setText,
  setSentiment,
  setConfidence,
  setLoading,
  setError,
  resetAnalysis,
} = analysisSlice.actions;

export default analysisSlice.reducer; 