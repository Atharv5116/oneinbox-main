import React from "react";
import { X } from "lucide-react";

// interface ImageExpandedViewProps {
//   imageUrl: string;
//   toggleExpand: () => void;
// }

export const ImageExpandedView= ({
  imageUrl,
  toggleExpand,
}) => {
  return (
    <div
      className="fixed inset-0 bg-black bg-opacity-90 z-50 flex flex-col items-center justify-center"
      onClick={(e) => {
        // Prevent closing when clicking on the image
        if ((e.target).tagName !== "IMG") {
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

      {/* Expanded Image Container */}
      <div className="relative w-full max-w-4xl">
        <img
          src={imageUrl}
          alt="Expanded Image"
          className="w-full max-h-[80vh] rounded-lg object-contain"
        />
      </div>
    </div>
  );
};
