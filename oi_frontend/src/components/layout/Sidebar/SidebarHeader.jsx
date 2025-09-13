import React, {useState, useEffect} from "react";
import { Moon, Search, ArrowLeft, Home } from "lucide-react";

export const SidebarHeader = () => {

  // handle back button click and navigate to the previous page
  // if no history found then display the back button
  const [showBackButton, setShowBackButton] = useState(false);
  const [showHomeButton, setShowHomeButton] = useState(false);
  useEffect(() => {
    const referrer = document.referrer;
    const currentOrigin = window.location.origin;
    
    if (referrer && new URL(referrer).origin === currentOrigin && window.history.length > 1) {
      setShowBackButton(true);
    } else {
      setShowHomeButton(true);
    }
  }, [])

  const handleBackButtonClick = () => {
    if (window.history.length > 1) {
      window.history.back()
    }
  }

  const handleHomeButtonClick = () => {
    window.location.href = `${window.location.origin}/app`;
  };

  return (
    <div className="p-2.5 flex items-center">
      {showBackButton && <button className="p-2 hover:bg-gray-300 rounded-md" onClick={handleBackButtonClick}>
        <ArrowLeft />
      </button>}

      {showHomeButton && (
        <button className="p-2 hover:bg-gray-300 rounded-md" onClick={handleHomeButtonClick}>
          <Home />
        </button>
      )}

      <span className="text-xl font-semibold cursor-pointer ">Oneinbox</span>
      <div className="ml-auto flex items-center space-x-2">
        <button className="p-2 hover:bg-gray-300 rounded-md">
          {/* <Search className="w-4 h-4" /> */}
        </button>
        <button className="p-2 hover:bg-gray-300 rounded-md">
          {/* <Moon className="w-4 h-4" /> */}
        </button>
      </div>
    </div>
  );
};
