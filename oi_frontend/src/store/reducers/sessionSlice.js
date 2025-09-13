// sessionSlice.js
import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  user: null,
  isLoggedIn: false,
};

const sessionSlice = createSlice({
  name: "session",
  initialState,
  reducers: {
    setSessionUser(state, action) {
      state.user = action.payload;
      state.isLoggedIn = !!action.payload;
    },
    logout(state) {
      state.user = null;
      state.isLoggedIn = false;
      // Clear cookies (optional)
      document.cookie = "user_id=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    },
  },
});

export const { setSessionUser, logout } = sessionSlice.actions;
export default sessionSlice.reducer;
