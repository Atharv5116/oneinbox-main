import React from "react";
import { format, isToday, isYesterday } from "date-fns";
import { platformIcons } from "../../../data";
// import { UserItemProps } from "../../../types;
// import Instagram  from "../../../assets";

export const UserItem = ({
  user,
  onUserSelect,
  isSelected,
  unreadCount,
}) => {
  const lastInteraction = new Date(user.last_interaction_timestamp);
  let formattedTime;

  const currentYear = new Date().getFullYear();
  const messageYear = lastInteraction.getFullYear();

  if (isToday(lastInteraction)) {
    formattedTime = format(lastInteraction, "hh:mm a");
  } else if (isYesterday(lastInteraction)) {
    formattedTime = "Yesterday";
  } else if (currentYear === messageYear) {
    formattedTime = format(lastInteraction, "dd MMM");
  } else {
    formattedTime = format(lastInteraction, "dd/MM/yy");
  }

  // Define platform-specific image sources
  const platformImageMap = {
    Instagram: "https://hfhg-crm.frappe.cloud/files/instagram icon.png", // Path to Instagram icon in the assets folder
    Messenger: "https://hfhg-crm.frappe.cloud/files/messenger logo icon.png", // Path to Messenger icon in the assets folder
  };

  // // Fallback for other platforms or undefined platform
  const platformIcon =
    platformImageMap[user.platform];


  return (
    <div
      className={`flex p-2 items-center rounded-md cursor-pointer mb-1 ${
        isSelected ? "bg-gray-200" : "hover:bg-gray-200"
      }`}
      onClick={() => onUserSelect(user)}
    >
      <div className="relative">
        {/* {console.log(user.profile_picture_url)} */}
        <img
          src={user.profile_picture_url || `https://hfhg.redsofterp.com/files/default-profile-picture1.jpg`}
          alt={user.name || 'Default Image'}
          className="w-11 h-10 rounded-md object-cover"
          onError={(e) => e.target.src = 'https://hfhg.redsofterp.com/files/default-profile-picture1.jpg'}
        />
        {/* <span
            className={`absolute top-0 left-0 w-2.5 h-2.5 rounded-md border-2 border-white ${
              user.status === "online"
                ? "bg-green-500"
                : user.status === "away"
                ? "bg-yellow-500"
                : "bg-gray-400"
            }`}
          /> */}

        <img
          src={platformIcon}
          alt={user.platform}
          className="absolute -bottom-1 -right-1 w-5 h-5 object-contain"
          />
      </div>
      <div className="flex flex-col justify-between w-full ml-3">
        <div className="flex justify-between items-center">
          <span className="text-sm text-gray-700">{user.name}</span>
          {unreadCount > 0 && (
            <div className="bg-red-500 text-white ms-1 text-xs rounded-full px-1 flex items-center justify-center">
              {unreadCount}
            </div>
          )}
        </div>
        <div className="flex justify-between items-center">
          <span className="text-xs text-gray-500">{user.username}</span>
          <span style={{ fontSize: "11px" }} className="text-gray-400">
            {formattedTime}
          </span>
        </div>
      </div>
    </div>
  );
};
