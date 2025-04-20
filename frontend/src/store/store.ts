import { configureStore } from '@reduxjs/toolkit';
import sentimentReducer from './slices/sentimentSlice';
import eventReducer from './slices/eventSlice';
import rumorReducer from './slices/rumorSlice';

export const store = configureStore({
  reducer: {
    sentiment: sentimentReducer,
    events: eventReducer,
    rumors: rumorReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch; 