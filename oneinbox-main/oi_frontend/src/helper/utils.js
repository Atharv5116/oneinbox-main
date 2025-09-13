import { format } from "date-fns";

// Format time in MM:SS
export const formatTime = (timeInSeconds) => {
  const minutes = Math.floor(timeInSeconds / 60);
  const seconds = Math.floor(timeInSeconds % 60);
  return `${minutes.toString().padStart(2, "0")}:${seconds
    .toString()
    .padStart(2, "0")}`;
};

export const getServerStyleTimestamp = () => {
  const date = new Date();
  const pad = (num, size = 2) => String(num).padStart(size, "0");

  const year = date.getFullYear();
  const month = pad(date.getMonth() + 1);
  const day = pad(date.getDate());
  const hours = pad(date.getHours());
  const minutes = pad(date.getMinutes());
  const seconds = pad(date.getSeconds());
  // JavaScript only gives milliseconds, so we’ll format three digits:
  const ms = String(date.getMilliseconds()).padStart(3, "0");

  // Returns something like "2025-02-06 23:55:13.626"
  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}.${ms}`;
}

 
export const formattedTime = (timestamp)=> {
  return format(new Date(timestamp), "hh:mm a");
};
