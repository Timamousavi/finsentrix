import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { detectRumors } from '../../services/api';

interface RumorState {
  text: string;
  rumors: any[];
  loading: boolean;
  error: string | null;
}

const initialState: RumorState = {
  text: '',
  rumors: [],
  loading: false,
  error: null,
};

export const detectMarketRumors = createAsyncThunk(
  'rumors/detect',
  async (text: string) => {
    const response = await detectRumors(text);
    return response;
  }
);

const rumorSlice = createSlice({
  name: 'rumors',
  initialState,
  reducers: {
    setText: (state, action) => {
      state.text = action.payload;
    },
    clearRumors: (state) => {
      state.rumors = [];
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(detectMarketRumors.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(detectMarketRumors.fulfilled, (state, action) => {
        state.loading = false;
        state.rumors = action.payload;
      })
      .addCase(detectMarketRumors.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to detect rumors';
      });
  },
});

export const { setText, clearRumors } = rumorSlice.actions;
export default rumorSlice.reducer; 