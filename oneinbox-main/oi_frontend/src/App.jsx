import { lazy, Suspense, useState, useTransition } from "react";
import './App.css';
import { FrappeProvider } from 'frappe-react-sdk';
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { Provider, useSelector, useDispatch } from "react-redux"; // Import Provider
import store from "./store/store"; // Import the Redux store
import RequireAuth from "./RequireAuth";
import {Sidebar} from "./components/layout/Sidebar/Sidebar";
import {ChatArea} from "./components/layout/Chat/ChatArea";


function App() {
  const [selectedUser, setSelectedUser] = useState(null);

  const handleUserSelect = (user) => {
    setSelectedUser(user); // Update selected user when a user is clicked
  };
  const getSiteName = () => {
  if (window.frappe?.boot?.versions?.frappe.startsWith('14')) {
    return import.meta.env.VITE_SITE_NAME
  }
  else {
    return window.frappe?.boot?.sitename ?? import.meta.env.VITE_SITE_NAME
  }
}

  return (
    <FrappeProvider
      // url={window.location.origin}
      socketPort={import.meta.env.VITE_SOCKET_PORT ? import.meta.env.VITE_SOCKET_PORT : undefined}      
      // tokenParams={{
      //   useToken: true,
      // }}
      siteName={getSiteName()}
    >
      <Provider store={store}>
        <Router>
          <Routes>
            <Route
              path="/oneinbox"
              element={
                <RequireAuth>
                  <div className="flex h-screen">
                    <Sidebar onUserSelect={handleUserSelect} />
                    <div className="flex-1">
                      {selectedUser ? (
                        <ChatArea selectedUser={selectedUser} />
                      ) : (
                        <div className="p-4 text-center">
                          Please select a user to start chatting.
                        </div>
                      )}
                    </div>
                  </div>
                </RequireAuth>
              }
            />
            {/* Redirect invalid routes to /oneinbox */}
            <Route path="*" element={<Navigate to="/oneinbox" replace />} />
          </Routes>
        </Router>
      </Provider>
    </FrappeProvider>
  );
}

export default App;
