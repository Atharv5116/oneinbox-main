import {
  MarkdownSerializer,
  defaultMarkdownSerializer,
} from "prosemirror-markdown";

export const customMarkdownSerializer = new MarkdownSerializer(
  {
    ...defaultMarkdownSerializer.nodes,
    video(state, node) { 
      const { src, alt = "", title = "" } = node.attrs;
      const altText = alt ? `[${alt}]` : "[]";
      const titleText = title ? ` "${title}"` : "";
      state.write(`!video${altText}(${src}${titleText})`);
    },
    audio(state, node) {
      const { src, alt = "", title = "" } = node.attrs;
      const altText = alt ? `[${alt}]` : "[]";
      const titleText = title ? ` "${title}"` : "";
      state.write(`!audio${altText}(${src}${titleText})`);
    },
    text(state, node) {
      state.text(node.text || "", false);
    },
  },
  {
    bold: {
      open: "**",
      close: "**",
      mixable: true,
      expelEnclosingWhitespace: true,
    },
    italic: {
      open: "_",
      close: "_",
      mixable: true,
      expelEnclosingWhitespace: true,
    },
    underline: {
      open: "<u>",
      close: "</u>",
      mixable: true,
    },
    strike: {
      open: "~~",
      close: "~~",
      mixable: true,
      expelEnclosingWhitespace: true,
    },
    code: {
      open: "`",
      close: "`",
      mixable: true,
      expelEnclosingWhitespace: true,
    },
  }
);
