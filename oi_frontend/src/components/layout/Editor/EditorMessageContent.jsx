import React from "react";
import ReactMarkdown from "react-markdown";
import rehypeRaw from "rehype-raw";
import remarkGfm from "remark-gfm";
import { TextReply } from "../Message/TextReply";
import { ImageMessage } from "../Message/Image/ImageMessage";
import { VideoMessage } from "../Message/Video/VideoMessage";
import { AudioMessage } from "../Message/Audio/AudioMessage";

const EditorMessageContent= ({ message }) => {
  const imageUrl = message.content.text?.imageUrl || [];
  const videoUrl = message.content.text?.videoUrl || [];
  const audioUrl = message.content.text?.audioUrl || [];
  const text = message.content.text || "";

  return (
    <>
      {message.type === "reply" ? (
        <div className="p-1 rounded-lg">
          <TextReply replyToId={message.replyTo?.toString() || ""} />
          <div className="text-sm">
            <ReactMarkdown
              children={text}
              remarkPlugins={[remarkGfm]}
              rehypePlugins={[rehypeRaw]}
            />
          </div>
        </div>
      ) : (
        <div className="flex flex-col-reverse">
          <div className="text-sm w-fit  ">
            {message.content.text && (
              <ReactMarkdown
                children={text}
                remarkPlugins={[remarkGfm]}
                rehypePlugins={[rehypeRaw]}
              />
            )}
          </div>
          <div className="rounded-lg w-[300px] ">
            {imageUrl && imageUrl.length > 0 && (
              <ImageMessage imageUrl={imageUrl} />
            )}
          </div>
          <div className="rounded-lg w-[300px] ">
            {videoUrl && videoUrl.length > 0 && (
              <VideoMessage videoUrl={videoUrl} />
            )}
          </div>
          <div className="rounded-lg w-[300px] ">
            {audioUrl && audioUrl.length > 0 && (
              <AudioMessage audioUrl={audioUrl} />
            )}
          </div>
        </div>
      )}
    </>
  );
};

export default EditorMessageContent;
