import { configureStore } from "@reduxjs/toolkit";
import chatReducer from "./reducers/chatSlice";
import themeReducer from "./reducers/themeSlice";
import sessionReducer from "./reducers/sessionSlice";
import userReducer from "./reducers/userSlice";

const store = configureStore({
  reducer: {
    chat: chatReducer,
    theme: themeReducer,
    session: sessionReducer,
    user: userReducer,
  },
});

// export type RootState = ReturnType<typeof store.getState>;
// export type AppDispatch = typeof store.dispatch;

export default store;
