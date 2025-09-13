import React from "react";
import ReactMarkdown from "react-markdown";
import rehypeRaw from "rehype-raw";
import remarkGfm from "remark-gfm";
import { TextReply } from "./TextReply";
import { AudioMessage } from "./Audio/AudioMessage";
import { ImageMessage } from "./Image/ImageMessage";
import { VideoMessage } from "./Video/VideoMessage";

export const MessageContent = ({ message }) => {
  const attachmentUrl = message.content.attachments ? message.content.attachments[0]?.url : '';

  if (message.reply?.is_reply) {
    return (
      <div className="p-1 rounded-lg">
        <TextReply replyToId={message.reply.reply_to} />
        <div className="text-sm border">
          <ReactMarkdown
            children={message.content.text}
            remarkPlugins={[remarkGfm]}
            rehypePlugins={[rehypeRaw]}
          />
        </div>
      </div>
    );
  }

  switch (message.content.type) {
    case "video":
      return (
        <div>
          <VideoMessage videoUrl={attachmentUrl} />
          <div className="text-sm">
            <ReactMarkdown
              children={message.content.text}
              remarkPlugins={[remarkGfm]}
              rehypePlugins={[rehypeRaw]}
            />
          </div>
        </div>
      );
    case "audio":
      return (
        <div>
          <AudioMessage audioUrl={attachmentUrl} />
          <div className="text-sm">
            <ReactMarkdown
              children={message.content.text}
              remarkPlugins={[remarkGfm]}
              rehypePlugins={[rehypeRaw]}
            />
          </div>
        </div>
      );
    case "image":
      return (
        <div>
          <ImageMessage imageUrl={attachmentUrl} />
          <div className="text-sm">
            <ReactMarkdown
              children={message.content.text}
              remarkPlugins={[remarkGfm]}
              rehypePlugins={[rehypeRaw]}
            />
          </div>
        </div>
      );
    default:
      return (
        <div className="text-sm">
          <ReactMarkdown
            children={message.content.text}
            remarkPlugins={[remarkGfm]}
            rehypePlugins={[rehypeRaw]}
          />
        </div>
      );
  }
};
