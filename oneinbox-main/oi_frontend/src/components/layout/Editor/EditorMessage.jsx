import React from "react";
import { ChevronDown } from "lucide-react";
import { useDispatch, useSelector } from "react-redux";
import { setReplyTarget } from "../../../store/reducers/chatSlice";
import { format } from "date-fns";
import EditorMessageContent from "./EditorMessageContent";

export const EditorMessage = () => {
  const dispatch = useDispatch();
  const replyTarget = useSelector((state) => state.chat.replyTarget); // Only track replyTarget
  
  const handleReplyClick = (messageId) => {
    dispatch(setReplyTarget(messageId));
  };

  const formatTime = () => format(new Date(), "h:mm a");
  
  return (
    <div className="mr-1">
      {replyTarget && (
        <div
          className="mb-3 flex flex-col items-end justify-end"
        >
          <div className="border-blue-200 flex flex-col items-start p-1 max-w-[55%] mr-5 rounded-md">
            <div className="flex flex-col rounded-md p-2 w-full bg-blue-100 ">
              <div className="flex items-center justify-end"></div>
              <div className="flex group w-fit">
                <EditorMessageContent message={replyTarget} />
                <div
                  className="flex items-center max-h-fit cursor-pointer opacity-0 group-hover:opacity-100 transition-opacity duration-200"
                  onClick={() => handleReplyClick(null)} // Remove reply on click
                >
                  <ChevronDown className="w-4 h-4 ml-4" />
                </div>
              </div>
            </div>
            <div className="flex items-center mt-1">
              <h6 style={{ fontSize: "10px" }} className="text-gray-500">
                {formatTime()}
              </h6>
            </div>
          </div>
        </div>
      )}
      {/* Here goes the actual input field for sending messages */}
      {/* <div className="p-2 border-t">
        <input
          type="text"
          className="w-full border rounded-md p-2"
          placeholder="Type a message..."
        />
      </div> */}
    </div>
  );
};