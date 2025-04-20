import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { detectEvents } from '../../services/api';

interface EventState {
  text: string;
  events: any[];
  loading: boolean;
  error: string | null;
}

const initialState: EventState = {
  text: '',
  events: [],
  loading: false,
  error: null,
};

export const detectMarketEvents = createAsyncThunk(
  'events/detect',
  async (text: string) => {
    const response = await detectEvents(text);
    return response;
  }
);

const eventSlice = createSlice({
  name: 'events',
  initialState,
  reducers: {
    setText: (state, action) => {
      state.text = action.payload;
    },
    clearEvents: (state) => {
      state.events = [];
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(detectMarketEvents.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(detectMarketEvents.fulfilled, (state, action) => {
        state.loading = false;
        state.events = action.payload;
      })
      .addCase(detectMarketEvents.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to detect events';
      });
  },
});

export const { setText, clearEvents } = eventSlice.actions;
export default eventSlice.reducer; 