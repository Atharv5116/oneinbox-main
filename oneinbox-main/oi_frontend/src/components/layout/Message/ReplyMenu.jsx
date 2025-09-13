import React from "react";

export const ReplyMenu = ({ replyMenuRef, messageId, handleReplyClick, flow, status }) => {
  const isDisabled = status === "Sending" || status !== "Failed";

  return (
    <div
      ref={replyMenuRef}
      className={`absolute ${
        flow === "incoming" ? "left-12 -top-2" : "right-7 top-0"
      } bg-gray-100 shadow-md border rounded-md p-2 w-40 z-50`}
    >
      {/* Reply Button */}
      <button
        onClick={() => !isDisabled && handleReplyClick(messageId)}
        disabled={isDisabled}
        className={`text-sm p-1 w-full text-left rounded-md 
          ${isDisabled ? "text-gray-400 cursor-not-allowed" : "hover:bg-gray-200 cursor-pointer"}
        `}
      >
        Reply
      </button>

      {/* React Button */}
      <button
        disabled={isDisabled}
        className={`text-sm p-1 w-full text-left rounded-md 
          ${isDisabled ? "text-gray-400 cursor-not-allowed" : "hover:bg-gray-200 cursor-pointer"}
        `}
      >
        React
      </button>
    </div>
  );
};
