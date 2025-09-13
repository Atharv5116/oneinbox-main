// import { type } from "@tiptap/react";
import { SendHorizontal, Link } from "lucide-react";

import { buttonConfigs } from "./ButtonConfig";

// type ToolbarProps = {
//   editor: Editor | null;
//   content: string;
//   handleImageUpload: (file: File) => void;
//   handleVideoUpload: (file: File) => void;
//   handleAudioUpload: (file: File) => void;
// };

const Toolbar= ({
  editor,
  content,
  handleImageUpload,
  handleVideoUpload,
  handleAudioUpload,
}) => {
  if (!editor) return null;

  const handleFileUpload = () => {
    const input = document.createElement("input");
    input.type = "file";
    input.accept = "image/*,video/*,audio/*";
    input.onchange = (event) => {
      const file = (event.target).files?.[0];
      if (file) {
        if (file.type.startsWith("image/")) {
          handleImageUpload(file);
        } else if (file.type.startsWith("video/")) {
          handleVideoUpload(file);
        } else if (file.type.startsWith("audio/")) {
          handleAudioUpload(file);
        } else {
          console.error("Unsupported file type:", file.type);
        }
      }
    };
    input.click();
  };

  return (
    <div
      className="px-4 py-3 rounded-br-md rounded-bl-md flex justify-between items-start
     gap-5 w-full flex-wrap border border-gray-200 bg-gray-100 "
    >
      <div className="flex justify-start items-center gap-5 w-full lg:w-10/12 flex-wrap">
        {buttonConfigs.map(
          ({ type, command, icon, activeType, customClass, ariaLabel }) => (
            <button
              key={type}
              onClick={(e) => {
                e.preventDefault();
                command(editor);
              }}
              className={
                activeType && editor.isActive(activeType)
                  ? "bg-gray-400 text-white p-1 rounded-lg"
                  : `font-semibold ${customClass ?? ""}`
              }
              aria-label={ariaLabel}
            >
              {icon}
            </button>
          )
        )}
        <button onClick={handleFileUpload} aria-label="Insert Image">
          <Link size={17} />
        </button>
      </div>
      {content && (
        <button type="submit" className="px-1 rounded-md">
          <SendHorizontal className="text-gray-600" />
        </button>
      )}
    </div>
  );
};

export default Toolbar;
