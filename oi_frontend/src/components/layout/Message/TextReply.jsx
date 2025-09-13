import React from "react";
import { ChatData, users } from "../../../data";
// import { TextReplyProps } from "../../../types";

export const TextReply = ({ replyToId }) => {
  const replyMessage = ChatData.data.find(
    (chat) => chat.message_id === replyToId
  );

  const user = users.data.find(
    (user) =>
      user.user_id === replyMessage?.from || user.user_id === replyMessage?.to
  );

  const userName = user ? user.name : "Unknown";
  if (!replyMessage) return null;

  return (
    <div className="p-1 border flex gap-2 bg-white border-grey-300 text-xs max-w-full rounded-md">
      <div className="h-auto border ml-1 border-blue-100"></div>
      <div className="w-full">
        <div className="w-full flex justify-between">
          <div className="rounded-lg p-1 flex w-fit gap-2 items-center justify-around">
            <span className="font-semibold text-xs">
              {userName || "Unknown"}
            </span>
          </div>
        </div>
        <div className="p-1 items-center">
          {replyMessage.content.text || "Unsupported message type"}
        </div>
      </div>
    </div>
  );
};
