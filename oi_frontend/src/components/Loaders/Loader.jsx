import React from "react";
import "./loader.css";

export const Loader = () => {
  return (
    <div className="flex items-center justify-center h-screen w-screen fixed top-0 left-0 bg-white bg-opacity-80">
    <div className="loader"></div>
  </div>
  );
};
