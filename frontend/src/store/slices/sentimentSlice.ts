import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { analyzeText } from '../../services/api';

interface SentimentState {
  text: string;
  result: any;
  loading: boolean;
  error: string | null;
}

const initialState: SentimentState = {
  text: '',
  result: null,
  loading: false,
  error: null,
};

export const analyzeSentiment = createAsyncThunk(
  'sentiment/analyze',
  async (text: string) => {
    const response = await analyzeText(text);
    return response;
  }
);

const sentimentSlice = createSlice({
  name: 'sentiment',
  initialState,
  reducers: {
    setText: (state, action) => {
      state.text = action.payload;
    },
    clearResult: (state) => {
      state.result = null;
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(analyzeSentiment.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(analyzeSentiment.fulfilled, (state, action) => {
        state.loading = false;
        state.result = action.payload;
      })
      .addCase(analyzeSentiment.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to analyze sentiment';
      });
  },
});

export const { setText, clearResult } = sentimentSlice.actions;
export default sentimentSlice.reducer; 