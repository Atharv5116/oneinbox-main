import React from "react";
import { EllipsisVertical } from "lucide-react";

export const ChatHeader = ({ user }) => {
  
  // Function to open the Quick Entry form for Lead creation
  const handleCreateLead = () => {
    const baseUrl = window.location.origin;
    window.open(`${baseUrl}/app/lead/new`, "_blank");
  };

  return (
    <div className="   ">
      <div className="flex justify-between tems-center 
      p-2  w-[99%]    ">
        <div className="flex items-center   ">
        <img
          src={user.profile_picture_url || `https://hfhg-crm.frappe.cloud/files/default-profile-picture1.jpg`}
          alt={user.name || 'Default Image'}
          className="w-9 h-9 rounded-md mr-3"
          onError={(e) => e.target.src = 'https://hfhg-crm.frappe.cloud/files/default-profile-picture1.jpg'}
        />
          
          <h3 className="text-xl font-semibold">{user.name}</h3>
        </div>

        <button
          onClick={handleCreateLead}
          className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600"
        >
          Create Lead
        </button>
        {/* <div className="flex items-center cursor-pointer">
          <EllipsisVertical className="w-6 h-6" />
        </div> */}
      </div>
    </div>
  );
};
