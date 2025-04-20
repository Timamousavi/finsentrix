import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface Rumor {
  id: string;
  text: string;
  confidence: number;
  source: string;
  timestamp: string;
  status: 'unverified' | 'verified' | 'debunked';
  impact: string;
}

interface RumorsState {
  rumors: Rumor[];
  loading: boolean;
  error: string | null;
  selectedRumor: Rumor | null;
}

const initialState: RumorsState = {
  rumors: [],
  loading: false,
  error: null,
  selectedRumor: null,
};

const rumorsSlice = createSlice({
  name: 'rumors',
  initialState,
  reducers: {
    setRumors: (state, action: PayloadAction<Rumor[]>) => {
      state.rumors = action.payload;
    },
    addRumor: (state, action: PayloadAction<Rumor>) => {
      state.rumors.push(action.payload);
    },
    updateRumorStatus: (state, action: PayloadAction<{ id: string; status: Rumor['status'] }>) => {
      const rumor = state.rumors.find(r => r.id === action.payload.id);
      if (rumor) {
        rumor.status = action.payload.status;
      }
    },
    setSelectedRumor: (state, action: PayloadAction<Rumor | null>) => {
      state.selectedRumor = action.payload;
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload;
    },
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
    },
    resetRumors: (state) => {
      state.rumors = [];
      state.loading = false;
      state.error = null;
      state.selectedRumor = null;
    },
  },
});

export const {
  setRumors,
  addRumor,
  updateRumorStatus,
  setSelectedRumor,
  setLoading,
  setError,
  resetRumors,
} = rumorsSlice.actions;

export default rumorsSlice.reducer; 