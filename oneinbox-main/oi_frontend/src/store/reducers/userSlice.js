import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  users: [],
  selectedUserId: null,
  loading: true,
  error: null,
};

const userSlice = createSlice({
  name: "user",
  initialState,
  reducers: {
    setUsers: (state, action) => {
      state.users = action.payload.slice().sort(
        (a, b) => new Date(b.last_interaction_timestamp) - new Date(a.last_interaction_timestamp)
      );
      state.loading = false;
      state.error = null;
    },
    setSelectedUserId: (state, action) => {
      state.selectedUserId = action.payload;
    },
    setLoading: (state, action) => {
      state.loading = action.payload;
    },
    setError: (state, action) => {
      state.error = action.payload;
      state.loading = false;
    },
    updateUser: (state, action) => {
      const updatedUser = action.payload;
      const index = state.users.findIndex((user) => user.user_id === updatedUser.user_id);
      if (index !== -1) {
        state.users[index] = { ...state.users[index], ...updatedUser };
      } else {
        state.users.push(updatedUser);
      }
      state.users = state.users.slice().sort(
        (a, b) => new Date(b.last_interaction_timestamp) - new Date(a.last_interaction_timestamp)
      );
    },
  },
});

export const { setUsers, setSelectedUserId, setLoading, setError, updateUser } = userSlice.actions;
export default userSlice.reducer;
