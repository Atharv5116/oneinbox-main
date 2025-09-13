import React, { useEffect, useRef, useState } from "react";
import { ChevronDown, XCircle, Loader2, Check, CheckCheck } from "lucide-react";
import { useDispatch } from "react-redux";
import { setReplyTarget } from "../../../store/reducers/chatSlice";
import { ReplyMenu } from "./ReplyMenu";
import { MessageContent } from "./MessageContent";
import { formattedTime } from "../../../helper/utils";

export const SenderMessage = ({ message }) => {
  const dispatch = useDispatch();
  const [openReplyMenu, setOpenReplyMenu] = useState(null);
  const replyMenuRef = useRef(null);
  

  const handleReplyClick = (messageId) => {
    console.log('handle reploy menu button', messageId)
    if (!messageId) return; // Prevent actions on invalid message IDs
    dispatch(setReplyTarget(messageId));
    setOpenReplyMenu(null);
  };

  const toggleReplyMenu = (messageId) => {
    setOpenReplyMenu((prev) => (prev === messageId ? null : messageId));
  };

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (
        replyMenuRef.current &&
        !replyMenuRef.current.contains(event.target)
      ) {
        setOpenReplyMenu(null);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  // Tooltip messages for each status
  const statusMessages = {
    Sending: "Sending...",
    Sent: "Sent",
    Delivered: "Delivered",
    Read: "Read",
    Failed: "Failed to Send."
  };

  // Function to render the status icon with tooltip
  const renderStatusIcon = () => {
    const status = message.metadata.status;
    const statusIcon = {
      Sending: <Loader2 className="w-4 h-4 animate-spin text-gray-400" />,
      Sent: <Check className="w-4 h-4 text-gray-500" />,
      Delivered: <CheckCheck className="w-4 h-4 text-gray-500" />,
      Read: <CheckCheck className="w-4 h-4 text-blue-500" />,
      Failed: <XCircle className="w-4 h-4 text-red-500 cursor-pointer" />
    }[status];

    return (
      <div className="relative group flex items-center">
        {statusIcon}
        <div
          className="absolute right-0 bottom-full mb-1 px-2 py-1 bg-black text-white text-xs rounded-md opacity-0 
                     group-hover:opacity-100 transition-opacity duration-200 whitespace-nowrap"
        >
          {statusMessages[status]}
        </div>
      </div>
    );
  };

  return (
    <div className="mb-3 flex justify-end p-1">
      <div className="flex flex-col items-start relative p-1 max-w-[55%] mr-5">
        <div className="flex flex-col p-2 bg-blue-100 rounded-lg w-full border border-blue-200">
          <div className="flex group relative">
            <MessageContent message={message} />
            {/* <div
              className="flex items-center cursor-pointer opacity-0 group-hover:opacity-100 transition-opacity duration-200 h-fit"
              onClick={() => toggleReplyMenu(message.id)}
            >
              <ChevronDown className="w-4 h-4 ml-4" />
            </div> */}
            {openReplyMenu === message.id && (
              <ReplyMenu
                replyMenuRef={replyMenuRef}
                messageId={message.id}
                handleReplyClick={handleReplyClick}
                status={message.metadata.status}
                flow="outgoing"
              />
            )}
          </div>
          {message.reaction?.emoji && (
            <div
              style={{ fontSize: "13px" }}
              className="absolute bg-blue-300 left-4 bottom-7 rounded-xl"
            >
              {message.reaction.emoji}
            </div>
          )}
        </div>
        <div
          className={`flex justify-between w-full p-1 ${
            message.reaction?.emoji ? "mt-2" : "mt-1"
          }`}
        >
          <h6 style={{ fontSize: "10px" }} className="text-gray-500 justify-items-start">
            {formattedTime(message.metadata.timestamp)}
          </h6>
          {renderStatusIcon()}
        </div>
      </div>
    </div>
  );
};
