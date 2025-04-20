import { configureStore } from '@reduxjs/toolkit';
import analysisReducer from './features/analysis/analysisSlice';
import eventsReducer from './features/events/eventsSlice';
import rumorsReducer from './features/rumors/rumorsSlice';
import settingsReducer from './features/settings/settingsSlice';

export const store = configureStore({
  reducer: {
    analysis: analysisReducer,
    events: eventsReducer,
    rumors: rumorsReducer,
    settings: settingsReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch; 