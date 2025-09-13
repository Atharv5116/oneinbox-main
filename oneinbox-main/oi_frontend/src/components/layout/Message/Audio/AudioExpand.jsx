import React from "react";
import { X, Music } from "lucide-react";

// interface AudioExpandedViewProps {
//   audioRef: React.RefObject<HTMLAudioElement>;
//   toggleExpand: () => void;
//   audioSrc: string;
// }

export const AudioExpandedView = ({
  audioRef,
  toggleExpand,
  audioSrc,
}) => {
  return (
    <div
      className="fixed inset-0 bg-black bg-opacity-90 z-50 flex flex-col items-center justify-center"
      onClick={(e) => {
        if (!(e.target ).closest("audio")) {
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

      {/*  Audio Container */}
      <div className="relative w-full max-w-2xl bg-blue-100 rounded-lg p-6 flex items-center space-x-4 border border-blue-300">
        {/* Music Icon */}
        <div className="bg-blue-200 items-center justify-center rounded-full p-4">
          <Music size={48} className="text-white" />
        </div>

        {/* Audio Player */}
        <div className="flex-grow">
          <audio ref={audioRef} src={audioSrc} className="w-full" controls />
        </div>
      </div>
    </div>
  );
};
