import React, { useState, useEffect, useRef } from "react";
import { Music } from "lucide-react";
import { AudioControls } from "./AudioControls";
import { AudioExpandedView } from "./AudioExpand";
// import { AudioMessageProps } from "../../../../types";

export const AudioMessage= ({ audioUrl }) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [progress, setProgress] = useState(0);
  const [duration, setDuration] = useState(0);
  const [isExpanded, setIsExpanded] = useState(false);
  const audioRef = useRef(null);
  const progressRef = useRef(null);
  // const audioUrl = message.content.attachments[0].url;
  const toggleAudioPlay = () => {
    if (audioRef.current) {
      if (isPlaying) {
        audioRef.current.pause();
      } else {
        audioRef.current.play();
      }
      setIsPlaying(!isPlaying);
    }
  };

  const handleProgressChange = (e) => {
    if (progressRef.current && audioRef.current) {
      const progressBar = progressRef.current;
      const clickPosition = e.nativeEvent.offsetX;
      const progressBarWidth = progressBar.clientWidth;
      const percentage = (clickPosition / progressBarWidth) * 100;

      const time = (percentage / 100) * duration;
      audioRef.current.currentTime = time;
      setProgress(percentage);
    }
  };

  const toggleExpand = () => {
    setIsExpanded(!isExpanded);

    // Pause audio when closing expanded view
    if (isExpanded && audioRef.current) {
      audioRef.current.pause();
      setIsPlaying(false);
    }
  };

  useEffect(() => {
    const audioElement = audioRef.current;

    const updateProgress = () => {
      if (audioElement) {
        const progressPercent =
          (audioElement.currentTime / audioElement.duration) * 100;
        setProgress(progressPercent);
      }
    };

    const handleMetaLoaded = () => {
      if (audioElement) {
        setDuration(audioElement.duration);
      }
    };

    if (audioElement) {
      audioElement.addEventListener("timeupdate", updateProgress);
      audioElement.addEventListener("loadedmetadata", handleMetaLoaded);
      audioElement.addEventListener("ended", () => setIsPlaying(false));
    }

    return () => {
      if (audioElement) {
        audioElement.removeEventListener("timeupdate", updateProgress);
        audioElement.removeEventListener("loadedmetadata", handleMetaLoaded);
        audioElement.removeEventListener("ended", () => setIsPlaying(false));
      }
    };
  }, []);

  // expanded view
  if (isExpanded) {
    return (
      <AudioExpandedView
        audioRef={audioRef}
        toggleExpand={toggleExpand}
        audioSrc={audioUrl.startsWith("http") 
                  ? audioUrl 
                  : `https://hfhg-crm.frappe.cloud${audioUrl}`}
      />
    );
  }

  return (
    <div>
      <div className="mb-2 ">
        <div
          className="bg-blue-200 flex-col items-start 
        p-1  w-fit rounded-lg relative"
        >
          {/* Audio Content */}
          <div className="flex flex-col w-full">
            <div className="flex group relative">
              {/* Audio Player */}
              <div className="relative w-[300px]">
                {/* Music Icon */}
                <div className="bg-blue-300 rounded-full p-3 mx-auto w-fit mb-2">
                  <Music size={24} className="text-gray-600" />
                </div>

                {/* Audio Controls */}
                <AudioControls
                  isPlaying={isPlaying}
                  togglePlay={toggleAudioPlay}
                  progress={progress}
                  duration={duration}
                  currentTime={audioRef.current?.currentTime || 0}
                  handleProgressChange={handleProgressChange}
                  onExpand={toggleExpand}
                  progressRef={progressRef}
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Hidden Audio Element for Playback */}
      <audio ref={audioRef} src={audioUrl.startsWith("http") ? audioUrl : `https://hfhg-crm.frappe.cloud${audioUrl}`} className="hidden" />
    </div>
  );
};
