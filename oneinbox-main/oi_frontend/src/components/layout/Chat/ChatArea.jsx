import React from "react";
import { ChatHeader } from "./ChatHeader";
import { ChatBody } from "./ChatBody";
import { ChatFooter } from "./ChatFooter";
// import { ChatAreaProps } from "../../../types";


export const ChatArea= ({ selectedUser }) => (
  <div className="flex flex-col h-full w-full">
    {selectedUser ? (
      <>
        <ChatHeader user={selectedUser} />
        <div className=" flex items-center justify-center"  >
        <div className="h-[1px] bg-gray-200 w-[99%] " />
        </div>
        <div className="flex-1 overflow-auto p-2">
          <ChatBody user={selectedUser}/>
        </div>
        <ChatFooter  user={selectedUser}  />
      </>
    ) : (
      <div className="flex-1 flex justify-center items-center">
        Select a user to chat
      </div>
    )}
  </div>
);
