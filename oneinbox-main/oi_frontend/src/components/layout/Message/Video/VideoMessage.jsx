import React, { useState, useEffect, useRef } from "react";
// import { VideoMessageProps } from "../../../../types";
import { VideoExpandedView } from "./VideoExpand";
import { VideoControls } from "./VideoControls";
import { formatTime } from "../../../../helper/utils";

export const VideoMessage = ({ videoUrl }) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [progress, setProgress] = useState(0);
  const [duration, setDuration] = useState(0);
  const [isExpanded, setIsExpanded] = useState(false);
  const videoRef = useRef(null);
  const progressRef = useRef(null);

  const toggleVideoPlay = () => {
    if (videoRef.current) {
      if (isPlaying) {
        videoRef.current.pause();
      } else {
        videoRef.current.play();
      }
      setIsPlaying(!isPlaying);
    }
  };

  const handleProgressChange = (e) => {
    if (progressRef.current && videoRef.current) {
      const progressBar = progressRef.current;
      const clickPosition = e.nativeEvent.offsetX;
      const progressBarWidth = progressBar.clientWidth;
      const percentage = (clickPosition / progressBarWidth) * 100;

      const time = (percentage / 100) * duration;
      videoRef.current.currentTime = time;
      setProgress(percentage);
    }
  };

  const toggleExpand = () => {
    setIsExpanded(!isExpanded);

    // Pause video when closing expanded view
    if (isExpanded && videoRef.current) {
      videoRef.current.pause();
      setIsPlaying(false);
    }
  };

  useEffect(() => {
    const videoElement = videoRef.current;

    const updateProgress = () => {
      if (videoElement) {
        const progressPercent =
          (videoElement.currentTime / videoElement.duration) * 100;
        setProgress(progressPercent);
      }
    };

    const handleMetaLoaded = () => {
      if (videoElement) {
        setDuration(videoElement.duration);
      }
    };

    if (videoElement) {
      videoElement.addEventListener("timeupdate", updateProgress);
      videoElement.addEventListener("loadedmetadata", handleMetaLoaded);
      videoElement.addEventListener("ended", () => setIsPlaying(false));
    }

    return () => {
      if (videoElement) {
        videoElement.removeEventListener("timeupdate", updateProgress);
        videoElement.removeEventListener("loadedmetadata", handleMetaLoaded);
        videoElement.removeEventListener("ended", () => setIsPlaying(false));
      }
    };
  }, []);

  // const videoUrl = message.content.attachments[0].url;

  if (isExpanded) {
    // console.log(videoUrl)
    return (
      <VideoExpandedView
        videoUrl={videoUrl.startsWith("http") 
          ? videoUrl 
          : `https://hfhg-crm.frappe.cloud${videoUrl}`}
        toggleExpand={toggleExpand}
        videoRef={videoRef}
      />
    );
  }

  return (
    <div>
      <div className="mb-2">
        <div className="bg-[#f7f7f7] flex-col items-start p-1 max-w-[70%] w-fit rounded-lg relative">
          {/* Video Content */}
          <div className="flex flex-col w-full">
            <div className="flex group relative">
              {/* Video Player */}
              <div className="relative w-[300px]">
                <video
                  ref={videoRef}
                  src={videoUrl.startsWith("http") 
                    ? videoUrl 
                    : `https://hfhg-crm.frappe.cloud${videoUrl}`}
                  className="max-w-[300px] max-h-[400px] rounded-t-lg"
                />

                {/* Video Controls */}
                <VideoControls
                  isPlaying={isPlaying}
                  toggleVideoPlay={toggleVideoPlay}
                  progress={progress}
                  duration={duration}
                  currentTime={videoRef.current?.currentTime || 0}
                  handleProgressChange={handleProgressChange}
                  toggleExpand={toggleExpand}
                  formatTime={formatTime}
                />
              </div>
              <div></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
