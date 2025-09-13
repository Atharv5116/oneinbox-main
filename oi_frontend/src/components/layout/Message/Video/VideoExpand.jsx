import React from "react";
import { X } from "lucide-react";

// interface VideoExpandedViewProps {
//   videoUrl: string;
//   toggleExpand: () => void;
//   videoRef: React.RefObject<HTMLVideoElement>;
// }

export const VideoExpandedView= ({
  videoUrl,
  toggleExpand,
  videoRef,
}) => {
  return (
    <div
      className="fixed inset-0 bg-black bg-opacity-90 z-50 flex flex-col items-center justify-center"
      onClick={(e) => {
        // Prevent closing if clicking on video or controls
        if ((e.target).tagName !== "VIDEO") {
          toggleExpand();
        }
      }}
    >
      {/* Close Button */}
      <button
        onClick={toggleExpand}
        className="absolute top-4 right-4 text-white bg-blue-200 bg-opacity-50 rounded-full p-2"
      >
        <X size={24} />
      </button>

      {/*   Video Container */}
      <div className="relative w-full max-w-4xl">
        <video
          ref={videoRef}
          src={videoUrl}
          className="w-full max-h-[80vh] rounded-lg"
          controls
        />
      </div>
    </div>
  );
};
