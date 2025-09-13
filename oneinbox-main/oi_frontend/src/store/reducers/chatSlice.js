import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  messages: [],
  replyTarget: false,
};

const chatSlice = createSlice({
  name: "chat",
  initialState,
  reducers: {
    addMessages: (state, action) => {
      const newMessages = action.payload;

      // Remove duplicates before adding new messages
      const existingIds = new Set(state.messages.map((msg) => msg.id));
      const filteredMessages = newMessages.filter((msg) => !existingIds.has(msg.id));

      state.messages = [...state.messages, ...filteredMessages].sort(
        (a, b) => new Date(a.metadata.timestamp) - new Date(b.metadata.timestamp)
      );
    },

    clearMessages: (state) => {
      state.messages = [];
      state.replyTarget = false;
      state.replyToId = undefined;
    },

    addMessage: (state, action) => {
      const newMessage = action.payload;

      console.log("newMessage", newMessage)
      // Prevent adding duplicate messages
      const exists = state.messages.some((msg) => msg.id === newMessage.id);
      if (!exists) {
        state.messages.push(newMessage);
        state.messages.sort(
          (a, b) => new Date(a.metadata.timestamp) - new Date(b.metadata.timestamp)
        );
      }
    },

    setReplyTarget: (state, action) => {
      state.replyTarget = true;
      state.replyToId = action.payload;
    },

    clearReplyTarget: (state) => {
      state.replyTarget = false;
      state.replyToId = undefined;
    },

    updateMessage: (state, action) => {
      const updatedMessage = action.payload;
      const index = state.messages.findIndex((msg) => msg.id === updatedMessage.id);

      if (updatedMessage.metadata.status === "Deleted") {
        if (index !== -1) {
          state.messages.splice(index, 1); // Remove deleted message
        }
        return;
      }

      if (index !== -1) {
        state.messages[index] = updatedMessage; // Update existing message
      } else {
        state.messages.push(updatedMessage); // Add new message
      }

      state.messages.sort(
        (a, b) => new Date(a.metadata.timestamp) - new Date(b.metadata.timestamp)
      );
    },
  },
});

export const { addMessage, setReplyTarget, clearReplyTarget, updateMessage, addMessages, clearMessages } =
  chatSlice.actions;
export default chatSlice.reducer;
