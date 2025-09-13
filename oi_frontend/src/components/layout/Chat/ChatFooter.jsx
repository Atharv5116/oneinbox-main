import React, { useRef, useState } from "react";
import Tiptap from "../../TextEditor/Tiptap";
import { useDispatch, useSelector } from "react-redux";
import { addMessage, clearReplyTarget, updateMessage } from "../../../store/reducers/chatSlice";
import { ReplyMessage } from "../Message/Replymessage";
import { useFrappePostCall, useFrappeEventListener } from "frappe-react-sdk";
import { getServerStyleTimestamp } from "../../../helper/utils";

export const ChatFooter = ({ user }) => {
  const [textContent, setTextContent] = useState("");
  const [fileUrl, setFileUrl] = useState(null);
  const dispatch = useDispatch();
  const editorRef = useRef(null);

  const { replyTarget, replyToId } = useSelector((state) => state.chat);

  useFrappeEventListener("one_message", (data) => {
    if (data.to === user.user_id || data.from === user.user_id) {
      console.log("Message received via real-time event:", data);
      dispatch(updateMessage(data));
    }
  });

  const handleClose = () => {
    dispatch(clearReplyTarget());
  };

  const { call: sendMessage, error: sendError, isValidating: isSending } = useFrappePostCall(
    "oneinbox.utils.api.messages.send_message"
  );

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!textContent && !fileUrl) {
      return;
    }

    const newMessage = {
      id: Date.now().toString(),
      type: fileUrl ? "file" : "text",
      content: textContent,
      replyTo: replyTarget ? replyToId : undefined,
      metadata: {
        status: "Sending",
        platform: user.platform,
        flow: "Outgoing",
        platform_id: user?.platform === "Messenger" ? "371024009436368" : "17841469373342139",
        timestamp: getServerStyleTimestamp()
      },
    };

    const payload = {
      recipient_id: user?.user_id,
      platform: user.platform,
      message_type: fileUrl ? "file" : "text",
      platform_id: user?.platform === "Messenger" ? "371024009436368" : "17841469373342139",
      message: fileUrl
        ? {
            attachment: {
              type: "file",
              url: fileUrl,
            },
          }
        : textContent,
    };

    try {
      const response = await sendMessage({ payload });
      console.log("Message sent successfully:", response);
      newMessage.id = response.message.request_id;
      dispatch(addMessage(newMessage));
    } catch (error) {
      console.error("Failed to send message:", error);
      dispatch(
        updateMessage({
          ...newMessage,
          metadata: { ...newMessage.metadata, status: "Failed" },
        })
      );
    }

    setTextContent("");
    setFileUrl(null);
    dispatch(clearReplyTarget());

    if (editorRef.current) {
      editorRef.current.clearContent();
    }
  };

  return (
    <div className="flex flex-col mb-4">
      {replyTarget && <ReplyMessage onClose={handleClose} />}
      <form onSubmit={handleSubmit}>
        <Tiptap
          ref={editorRef}
          content={textContent}
          onChange={(newContent) => setTextContent(newContent)}
          placeholder={`Message ${user.name}...`}
          setFileUrl={setFileUrl}
        />
      </form>
    </div>
  );
};
