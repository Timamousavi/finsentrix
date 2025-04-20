import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface Event {
  id: string;
  type: string;
  description: string;
  timestamp: string;
  confidence: number;
  impact: string;
}

interface EventsState {
  events: Event[];
  loading: boolean;
  error: string | null;
  selectedEvent: Event | null;
}

const initialState: EventsState = {
  events: [],
  loading: false,
  error: null,
  selectedEvent: null,
};

const eventsSlice = createSlice({
  name: 'events',
  initialState,
  reducers: {
    setEvents: (state, action: PayloadAction<Event[]>) => {
      state.events = action.payload;
    },
    addEvent: (state, action: PayloadAction<Event>) => {
      state.events.push(action.payload);
    },
    removeEvent: (state, action: PayloadAction<string>) => {
      state.events = state.events.filter(event => event.id !== action.payload);
    },
    setSelectedEvent: (state, action: PayloadAction<Event | null>) => {
      state.selectedEvent = action.payload;
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload;
    },
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
    },
    resetEvents: (state) => {
      state.events = [];
      state.loading = false;
      state.error = null;
      state.selectedEvent = null;
    },
  },
});

export const {
  setEvents,
  addEvent,
  removeEvent,
  setSelectedEvent,
  setLoading,
  setError,
  resetEvents,
} = eventsSlice.actions;

export default eventsSlice.reducer; 