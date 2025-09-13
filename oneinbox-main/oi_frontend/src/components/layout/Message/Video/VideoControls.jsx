import React from "react";
import { Play, Pause, Maximize2 } from "lucide-react";

// interface VideoControlsProps {
//   isPlaying: boolean;
//   toggleVideoPlay: () => void;
//   progress: number;
//   duration: number;
//   currentTime: number;
//   handleProgressChange: (e: React.MouseEvent<HTMLDivElement>) => void;
//   toggleExpand: () => void;
//   formatTime: (time: number) => string;
// }

export const VideoControls = ({
  isPlaying,
  toggleVideoPlay,
  progress,
  duration,
  currentTime,
  handleProgressChange,
  toggleExpand,
  formatTime,
}) => {
  return (
    <div className="bg-black bg-opacity-70 p-2 rounded-b-lg flex items-center justify-between">
      <div className="flex items-center space-x-2 flex-grow">
        {/* Play/Pause Button */}
        <button onClick={toggleVideoPlay} className="text-white">
          {isPlaying ? <Pause size={20} /> : <Play size={20} />}
        </button>

        {/* Progress Bar */}
        <div
          onClick={handleProgressChange}
          className="flex-grow bg-gray-500 h-1 rounded-full cursor-pointer"
        >
          <div
            className="bg-blue-500 h-1 rounded-full"
            style={{ width: `${progress}%` }}
          />
        </div>

        {/* Time Display */}
        <div className="text-white text-xs">
          {formatTime(currentTime)}/{formatTime(duration)}
        </div>
      </div>

      {/* Expand Button */}
      <button onClick={toggleExpand} className="text-white ml-2">
        <Maximize2 size={16} />
      </button>
    </div>
  );
};
