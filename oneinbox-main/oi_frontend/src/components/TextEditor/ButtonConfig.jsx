import {
  Bold,
  Strikethrough,
  Italic,
  List,
  ListOrdered,
  Underline,
  Quote,
  Undo,
  Redo,
  Code,
} from "lucide-react";
// import { type } from "@tiptap/react";

// type ButtonConfig = {
  // type: string;
  // command: (editor: Editor) => void;
  // icon: JSX.Element;
  // activeType?: string;
  // customClass?: string;
  // ariaLabel: string;
// };

export const buttonConfigs = [
  {
    type: "bold",
    command: (editor) => editor.chain().focus().toggleBold().run(),
    icon: <Bold className="w-4 h-4" />,
    activeType: "bold",
    ariaLabel: "Bold",
  },
  {
    type: "italic",
    command: (editor) => editor.chain().focus().toggleItalic().run(),
    icon: <Italic className="w-4 h-4" />,
    activeType: "italic",
    ariaLabel: "Italic",
  },
  {
    type: "underline",
    command: (editor) => editor.chain().focus().toggleUnderline().run(),
    icon: <Underline className="w-4 h-4" />,
    activeType: "underline",
    ariaLabel: "Underline",
  },
  {
    type: "strike",
    command: (editor) => editor.chain().focus().toggleStrike().run(),
    icon: <Strikethrough className="w-4 h-4" />,
    activeType: "strike",
    ariaLabel: "Strikethrough",
  },
  {
    type: "bulletList",
    command: (editor) => editor.chain().focus().toggleBulletList().run(),
    icon: <List className="w-4 h-4" />,
    activeType: "bulletList",
    ariaLabel: "Bullet List",
  },
  {
    type: "orderedList",
    command: (editor) => editor.chain().focus().toggleOrderedList().run(),
    icon: <ListOrdered className="w-4 h-4" />,
    activeType: "orderedList",
    ariaLabel: "Ordered List",
  },
  {
    type: "blockquote",
    command: (editor) => editor.chain().focus().toggleBlockquote().run(),
    icon: <Quote className="w-4 h-4" />,
    activeType: "blockquote",
    ariaLabel: "Blockquote",
  },
  {
    type: "code",
    command: (editor) => editor.chain().focus().toggleCode().run(),
    icon: <Code className="w-4 h-4" />,
    activeType: "code",
    ariaLabel: "Code",
  },
  {
    type: "undo",
    command: (editor) => editor.chain().focus().undo().run(),
    icon: <Undo className="w-4 h-4" />,
    customClass: "hover:bg-gray-400 hover:text-white p-1 hover:rounded-lg",
    ariaLabel: "Undo",
  },
  {
    type: "redo",
    command: (editor) => editor.chain().focus().redo().run(),
    icon: <Redo className="w-4 h-4" />,
    customClass: "hover:bg-gray-700 hover:text-white p-1 hover:rounded-lg",
    ariaLabel: "Redo",
  },
];
