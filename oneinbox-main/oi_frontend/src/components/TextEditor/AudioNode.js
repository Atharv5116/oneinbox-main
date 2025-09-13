import { Node, mergeAttributes } from "@tiptap/core";

export const Audio = Node.create({
  name: "audio",

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
    };
  },

  parseHTML() {
    return [
      {
        tag: "audio",
      },
    ];
  },

  renderHTML({ HTMLAttributes }) {
    const styledAttributes = {
      ...HTMLAttributes,
      style:
        "border-radius: 25px; margin-bottom: 15px; border: 0.5px solid #C8E6FF; max-width: 100%; display: block;",
    };

    return ["audio", mergeAttributes(styledAttributes)];
  },

  addCommands() {
    return {
      setAudio:
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
