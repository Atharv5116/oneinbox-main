import { useEffect, useState } from "react";
import { useSelector, useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";
import { setSessionUser } from "./store/reducers/sessionSlice";

const RequireAuth = ({ children }) => {
  const isLoggedIn = useSelector((state) => state.session.isLoggedIn);
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const [authChecked, setAuthChecked] = useState(false);

  // console.log("Session User:", sessionUser);

  useEffect(() => {
    // Check session user from cookies
    const sessionUser = getSessionUserFromCookies();
    if (sessionUser) {
      dispatch(setSessionUser(sessionUser));
    } else {
      dispatch(setSessionUser(null));
    }
    setAuthChecked(true); // Auth check complete
  }, [dispatch]);

  // While authentication is being checked, render nothing
  if (!authChecked) {
    console.log("Checking authentication...");
    return null; // Render nothing while checking auth
  }

  if (!isLoggedIn) {
    window.location.href =  "/login?redirect-to=/oneinbox";
    return null;
  }

  return children;
};

// Helper function to get the session user from cookies
const getSessionUserFromCookies = () => {
  try {
    const cookies = document.cookie.split("; ").reduce((acc, cookie) => {
      const [key, value] = cookie.split("=");
      acc[key] = value;
      return acc;
    }, {});
    return cookies.user_id && cookies.user_id !== "Guest" ? { id: cookies.user_id } : null;
  } catch (error) {
    console.error("Error accessing cookies:", error);
    return null;
  }
};

export default RequireAuth;