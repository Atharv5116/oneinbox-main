import { Node, mergeAttributes } from "@tiptap/core";

export const Video = Node.create({
  name: "video",

  group: "block",

  atom: true,

  selectable: true,

  draggable: true,

  addAttributes() {
    return {
      src: {
        default: null,
      },
      controls: {
        default: true,
      },
      width: {
        default: "150px",
      },
      height: {
        default: "auto",
      },
    };
  },

  parseHTML() {
    return [
      {
        tag: "video",
      },
    ];
  },

  renderHTML({ HTMLAttributes }) {
    const styledAttributes = {
      ...HTMLAttributes,
      style:
        "border-radius: 8px; margin-bottom: 15px; border: 0.5px solid #0056b3; max-width: 100%; display: block;",
    };

    return ["video", mergeAttributes(styledAttributes)];
  },

  addCommands() {
    return {
      setVideo:
        (options) =>
        ({ commands }) => {
          return commands.insertContent({
            type: this.name,
            attrs: options,
          });
        },
    };
  },
});
