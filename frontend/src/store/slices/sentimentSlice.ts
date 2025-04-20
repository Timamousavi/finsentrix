import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';

interface SentimentState {
  loading: boolean;
  error: string | null;
  result: {
    sentiment: string;
    confidence: number;
    keywords: string[];
  } | null;
}

const initialState: SentimentState = {
  loading: false,
  error: null,
  result: null,
};

export const analyzeText = createAsyncThunk(
  'sentiment/analyzeText',
  async (text: string) => {
    const response = await axios.post('/api/analyze', { text });
    return response.data;
  }
);

const sentimentSlice = createSlice({
  name: 'sentiment',
  initialState,
  reducers: {
    clearResult: (state) => {
      state.result = null;
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(analyzeText.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(analyzeText.fulfilled, (state, action) => {
        state.loading = false;
        state.result = action.payload;
      })
      .addCase(analyzeText.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'An error occurred';
      });
  },
});

export const { clearResult } = sentimentSlice.actions;
export default sentimentSlice.reducer; 