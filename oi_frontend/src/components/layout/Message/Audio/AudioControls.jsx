import React from "react";
import { Play, Pause, Maximize2 } from "lucide-react";
import { formatTime } from "../../../../helper/utils";

// interface AudioControlsProps {
//   isPlaying: boolean;
//   togglePlay: () => void;
//   progress: number;
//   duration: number;
//   currentTime: number;
//   handleProgressChange: (e: React.MouseEvent<HTMLDivElement>) => void;
//   onExpand: () => void;
//   progressRef: React.RefObject<HTMLDivElement>;
// }

export const AudioControls= ({
  isPlaying,
  togglePlay,
  progress,
  duration,
  currentTime,
  handleProgressChange,
  onExpand,
  progressRef,
}) => (
  <div className="bg-black bg-opacity-70 p-2 rounded-lg flex items-center justify-between">
    <div className="flex items-center space-x-2 flex-grow">
      <button onClick={togglePlay} className="text-white">
        {isPlaying ? <Pause size={20} /> : <Play size={20} />}
      </button>
      <div
        ref={progressRef}
        onClick={handleProgressChange}
        className="flex-grow bg-gray-500 h-1 rounded-full cursor-pointer"
      >
        <div
          className="bg-blue-500 h-1 rounded-full"
          style={{ width: `${progress}%` }}
        />
      </div>
      <div className="text-white text-xs">
        {formatTime(currentTime)}/{formatTime(duration)}
      </div>
    </div>
    <button onClick={onExpand} className="text-white ml-2">
      <Maximize2 size={16} />
    </button>
  </div>
);
