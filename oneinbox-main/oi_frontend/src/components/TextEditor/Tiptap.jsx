import { useEditor, EditorContent } from "@tiptap/react";
import StarterKit from "@tiptap/starter-kit";
import Toolbar from "./Toolbar";
import Underline from "@tiptap/extension-underline";
import { useEffect, useState, useImperativeHandle, forwardRef } from "react";
import { customMarkdownSerializer } from "./customMarkdownSerializer";
import Image from "@tiptap/extension-image";
import { Video } from "./VideoNode";
import { Audio } from "./AudioNode";
import { useFrappePostCall } from "frappe-react-sdk";


const Tiptap = forwardRef(({ onChange, content, placeholder, setFileUrl }, ref) => {
  const [isFocused, setIsFocused] = useState(false);

  // const handleImageUpload = async (file) => {
  //   const reader = new FileReader();
  //   reader.onload = () => {
  //     if (reader.result) {
  //       editor
  //         ?.chain()
  //         .focus()
  //         .setImage({src: reader.result.toString()})
  //         .run();
  //     }
  //   };

  //   reader.readAsDataURL(file);
  // };

  // const handleVideoUpload = async (file) => {
  //   const reader = new FileReader();
  //   reader.onload = () => {
  //     if (reader.result) {
  //       editor
  //         ?.chain()
  //         .focus()
  //         .setVideo({ src: reader.result.toString(), controls: true })
  //         .run();
  //     }
  //   };
  //   reader.readAsDataURL(file);
  // };
  // const handleAudioUpload = async (file) => {
  //   const reader = new FileReader();
  //   reader.onload = () => {
  //     if (reader.result) {
  //       editor
  //         ?.chain()
  //         .focus()
  //         .setAudio({ src: reader.result.toString(), controls: true })
  //         .run();
  //     }
  //   };
  //   reader.readAsDataURL(file);
  // };

  const { call: uploadFileApi, error: uploadError, isValidating: isUploading } = useFrappePostCall(
    "oneinbox.utils.api.messages.upload_file" // Replace with the actual file upload API endpoint
  );

  const uploadFile = async (file, uploadFileApi) => {
    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await uploadFileApi({ payload: formData });

      if (response?.message?.file_url.url) {
        return {
          url: response.message.file_url.url, // File URL
          type: "type"
        };
      } else {
        throw new Error("Failed to upload file");
      }
    } catch (error) {
      console.error("File upload error:", error);
      throw error;
    }
  };

  

  const handleFileUpload = async (file) => {
    try {
      const uploadedFile = await uploadFile(file, uploadFileApi);

      if (uploadedFile) {
        setFileUrl(uploadedFile.url)
        // Update editor or state based on file type
        // if (uploadedFile.type === "image") {
        //   editor?.chain().focus().setImage({ src: uploadedFile.url }).run();
        //   setImageUrl(uploadedFile.url);
        // } else if (uploadedFile.type === "video") {
        //   editor?.chain().focus().setVideo({ src: uploadedFile.url }).run();
        //   setVideoUrl(uploadedFile.url);
        // } else if (uploadedFile.type === "audio") {
        //   editor?.chain().focus().setAudio({ src: uploadedFile.url }).run();
        //   setAudioUrl(uploadedFile.url);
        // }
      }
    } catch (error) {
      console.error("Failed to handle file upload:", error);
    }
  };


  const handleChange = () => {
    if (!editor) return;
    const doc = editor?.state.doc;
    const markdownContent = customMarkdownSerializer.serialize(doc);

    const imageNodes = editor
      ?.getJSON()
      ?.content?.filter((node) => node.type === "image");
    const imageUrl = imageNodes?.map((node) => node.attrs.src) || [];

    const videoNodes = editor
      ?.getJSON()
      ?.content?.filter((node) => node.type === "video");
    const videoUrl = videoNodes?.map((node) => node.attrs.src) || [];

    const audioNodes = editor
      ?.getJSON()
      ?.content?.filter((node) => node.type === "audio");
    const audioUrl = audioNodes?.map((node) => node.attrs.src) || [];

    const cleanedMarkdownContent = markdownContent
      .replace(/!video(\[.*?\])?\(.*?\)|!audio(\[.*?\])?\(.*?\)/g, "")
      .trim();
    onChange({
      text: cleanedMarkdownContent,
      imageUrl,
      videoUrl,
      audioUrl,
    });
  };

  const editor = useEditor({
    extensions: [
      StarterKit,
      Underline,
      Image.extend({
        addAttributes() {
          return {
            src: {},
            alt: {
              default: null,
            },
            title: {
              default: null,
            },
            width: {
              default: "150px",
            },
            height: {
              default: "auto",
            },
          };
        },
        renderHTML({ HTMLAttributes }) {
          return [
            "img",
            {
              ...HTMLAttributes,
              style:
                "border-radius: 8px; margin-bottom: 15px; border: 0.5px solid #0056b3;",
            },
          ];
        },
      }),
      Video,
      Audio,
    ],
    editorProps: {
      attributes: {
        class:
          "flex flex-col px-4 py-3 justify-start border-t border-r border-l border-gray-200 rounded-tl-md rounded-tr-md items-start w-full gap-2 text-sm pt-4 outline-none",
      },
    },
    onUpdate: handleChange,
    content,
  });

  //  clearContent method via ref for the editor
  useImperativeHandle(ref, () => ({
    clearContent() {
      editor?.commands.clearContent();
    },
  }));

  // Effect to manage focus state
  useEffect(() => {
    if (editor) {
      const handleFocus = () => setIsFocused(true);
      const handleBlur = () => setIsFocused(false);

      editor.on("focus", handleFocus);
      editor.on("blur", handleBlur);

      return () => {
        editor.off("focus", handleFocus);
        editor.off("blur", handleBlur);
      };
    }
  }, [editor]);

  return (
    <div className="relative px-4 w-[97%]">
      <div className="relative">
        {!isFocused && !content && (
          <div className="absolute left-4 top-3 text-gray-700 pointer-events-none">
            {placeholder}
          </div>
        )}
        <EditorContent
          style={{
            whiteSpace: "pre-line",
            maxWidth: "100%",
            width: "100%",
            wordWrap: "break-word",
          }}
          editor={editor}
        />
      </div>
      <Toolbar editor={editor} content={content} handleFileUpload={handleFileUpload} />
    </div>
  );
});

export default Tiptap;