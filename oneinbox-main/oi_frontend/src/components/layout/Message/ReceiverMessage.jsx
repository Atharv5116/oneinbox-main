import React, { useState, useEffect, useRef } from "react";
import { ChevronDown } from "lucide-react";
import { useDispatch } from "react-redux";
import { setReplyTarget } from "../../../store/reducers/chatSlice";
// import { ReceiverMessageProps } from "../../../types";
import { MessageContent } from "./MessageContent";
import { ReplyMenu } from "./ReplyMenu";
import { formattedTime } from "../../../helper/utils";

export const ReceiverMessage = ({
  message,
}) => {
  const dispatch = useDispatch();
  const [openReplyMenu, setOpenReplyMenu] = useState(null);
  const replyMenuRef = useRef(null);

  const handleReplyClick = (messageId) => {
    dispatch(setReplyTarget(messageId));
    console.log("Reply clicked for messageId:", messageId);
    setOpenReplyMenu(null);
  };

  const toggleReplyMenu = (messageId) => {
    setOpenReplyMenu((prev) => (prev === messageId ? null : messageId));
  };

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (
        replyMenuRef.current &&
        !replyMenuRef.current.contains(event.target )
      ) {
        setOpenReplyMenu(null);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  return (
    <div className="mb-2 relative ml-3">
      <div
        className="bg-blue-50 flex-col items-start p-2 
      max-w-[55%] w-fit rounded-md relative mb-1 px-2 border border-blue-100"
      >
        <div className="flex flex-col w-full">
          <div className="flex group">
            <MessageContent message={message} />
            <div className="relative flex items-center h-fit">
              <div
                className="flex items-center cursor-pointer opacity-0 group-hover:opacity-100 transition-opacity duration-200"
                onClick={() => toggleReplyMenu(message.message_id)}
              >
                <ChevronDown className="w-4 h-4 ml-4" />
              </div>
              {openReplyMenu === message.message_id && (
                <ReplyMenu
                  replyMenuRef={replyMenuRef}
                  messageId={message.message_id}
                  handleReplyClick={handleReplyClick}
                  flow="incoming"
                />
              )}
            </div>
          </div>
        </div>
        {message.reaction?.emoji && (
          <div
            style={{ fontSize: "13px" }}
            className="absolute bg-blue-300 left-3 -bottom-2 rounded-xl"
          >
            {message.reaction.emoji}
          </div>
        )}
      </div>
      <div
        className={`flex items-center justify-start ${
          message.reaction?.emoji ? "mt-3" : "mt-1"
        }`}
      >
        <h6 style={{ fontSize: "10px" }} className="text-gray-500">
          {formattedTime(message.metadata.timestamp)}
        </h6>
      </div>
    </div>
  );
};
