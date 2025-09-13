import React from "react";
import { format, isToday, isYesterday, parseISO } from "date-fns";

/**
 * Safely parse a date string and format it as:
 *   - "Today" if isToday
 *   - "Yesterday" if isYesterday
 *   - "dd-MM-yyyy" otherwise
 */
function getFormattedDate(dateStr) {
  // Often Frappe might return a date like "2025-02-06 23:55:13.626099"
  // so we convert the first space to 'T' for parseISO
  let isoLikeStr = dateStr.includes("T")
    ? dateStr
    : dateStr.replace(" ", "T");

  let parsedDate;
  try {
    parsedDate = parseISO(isoLikeStr);
  } catch (error) {
    // If parse fails for some reason, just return the raw string
    return dateStr;
  }

  const currentYear = new Date().getFullYear();
  const messageYear = parsedDate.getFullYear();

  if (isToday(parsedDate)) {
    return "Today";
  } else if (isYesterday(parsedDate)) {
    return "Yesterday";
  } else if (currentYear === messageYear) {
    return format(parsedDate, "dd MMM");
  } else {
    return format(parsedDate, "dd/MM/yyyy");
  }
}

export const DateSeparator = ({ date }) => {
  // Convert the timestamp into our display string
  const formattedDate = getFormattedDate(date);

  return (
    <div className="flex items-center mb-2">
      {/* Left line */}
      <div className="flex-grow h-[1px] bg-gray-300 mr-2" />
      {/* Date Text */}
      <h6 className="text-xs text-gray-500">{formattedDate}</h6>
      {/* Right line */}
      <div className="flex-grow h-[1px] bg-gray-300 ml-2" />
    </div>
  );
};
