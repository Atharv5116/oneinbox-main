import React from "react";
import { CircleX } from "lucide-react";
import { useSelector } from "react-redux";
import { ChatData, users } from "../../../data";

export const ReplyMessage = ({ onClose }) => {
  const replyToId = useSelector((state) => state.chat.replyToId);
  const replyMessage = useSelector((state) =>
    state.chat.messages.find((message) => message.id === replyToId)
  );

  const user = users.data.find(
    (user) =>
      user.user_id === replyMessage?.from || user.user_id === replyMessage?.to
  );

  const userName = user ? user.name : "Unknown";

  if (!replyMessage) return null;

  return (
    <div className="p-1 border flex gap-2 bg-blue-50 border-blue-100 text-xs max-w-[70%]  rounded-t-md ml-4">
      <div className="h-auto border ml-1 border-blue-200  "></div>
      <div className="w-full">
        <div className="w-full flex justify-between">
          <div className="rounded-lg p-1 flex w-fit gap-2 items-center justify-around ">
            <span className="font-semibold text-xs">{userName}</span>
          </div>
          <button onClick={onClose}>
            <CircleX className="w-4 h-4 " />
          </button>
        </div>
        <div className="p-1 items-center">{replyMessage.content.text}</div>
      </div>
    </div>
  );
};
