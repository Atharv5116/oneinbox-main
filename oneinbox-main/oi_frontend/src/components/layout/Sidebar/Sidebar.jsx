import React, { useEffect, useState, useCallback, useRef } from "react";
import { useDispatch, useSelector } from "react-redux";
import { SidebarHeader } from "./SidebarHeader";
import { UserItem } from "./UserItem";
import { useFrappeGetCall, useFrappePostCall, useFrappeEventListener } from "frappe-react-sdk";
import { setUsers, setSelectedUserId, setLoading, setError, updateUser } from "../../../store/reducers/userSlice";

export const Sidebar = ({ onUserSelect }) => {
  const dispatch = useDispatch();
  const { users, selectedUserId, loading, error } = useSelector((state) => state.user);

  const [page, setPage] = useState(1);
  const [hasNext, setHasNext] = useState(true);
  const [loadingMore, setLoadingMore] = useState(false);

  const fetchUsers = {
    limit: 20,
    page,
    order: "desc",
  };

  // Using useFrappeGetCall to fetch users
  const { data, error: apiError, isValidating } = useFrappeGetCall(
    "oneinbox.utils.api.messages.fetch_users",
    fetchUsers
  );

  const { call: resetUnreadCount } = useFrappePostCall("oneinbox.utils.api.messages.reset_unread_count");

  useEffect(() => {
    if (isValidating) {
      dispatch(setLoading(true)); // Set loading to true while fetching
    }

    if (data?.message?.data) {
      dispatch(setUsers(data.message.data)); // Update users state

      // Check if more pages remain
      const { has_next } = data.message.pagination || {};
      setHasNext(has_next);
    }

    if (apiError) {
      dispatch(setError(apiError.message || "Failed to fetch users.")); // Set error message
    }
  }, [data, apiError, isValidating, dispatch]);

  useFrappeEventListener("user_update", (data) => {
    dispatch(updateUser(data));
  });

  const handleUserSelect = async (user) => {
    dispatch(setSelectedUserId(user.user_id));
    onUserSelect(user);

    try {
      await resetUnreadCount({ user_id: user.user_id, platform: user.platform });
    } catch (error) {
      console.error("Failed to reset unread count:", error);
    }
  };

  // Container ref to handle scrolling
  const sidebarRef = useRef(null);

  // On scroll, if we reach bottom, load more users
  const handleScroll = useCallback(
    (event) => {
      if (!hasNext || loadingMore) return;
      const { scrollTop, scrollHeight, clientHeight } = event.currentTarget;
      if (scrollHeight - scrollTop === clientHeight) {
        // we are at bottom, load next page
        setLoadingMore(true);
        setPage((prev) => prev + 1);
      }
    },
    [hasNext, loadingMore]
  );

  useEffect(() => {
    if (loadingMore) {
      // Fetch more users when loadingMore is true
      fetchUsers.page = page;
      fetchUsers.limit = 20;
    }
  }, [loadingMore, page]);

  // Display error state
  if (error) {
    return (
      <div className="w-64 h-screen flex items-center justify-center text-red-500">
        <div>Error: {error}</div>
      </div>
    );
  }

  // Display loading state
  if (loading && page === 1) {
    return (
      <div className="w-64 h-screen flex items-center justify-center text-gray-500">
        <div>Loading...</div>
      </div>
    );
  }

  return (
    <div>
      <div className="w-64 h-screen bg-gray-100 border border-gray-100 text-black-300 flex flex-col">
        <SidebarHeader />
        <div className="flex items-center justify-center">
          <div className="h-[1px] bg-gray-300 w-[95%]" />
        </div>
        <div className="flex-1 overflow-y-auto" ref={sidebarRef} onScroll={handleScroll}>
          <div className="px-2 py-3">
            <div className="mt-6">
              <div className="mt-3 space-y-1">
                {users.map((user) => (
                  <UserItem
                    key={user.user_id}
                    user={user}
                    onUserSelect={handleUserSelect}
                    isSelected={user.user_id === selectedUserId}
                    unreadCount={user.unread_count || 0}
                  />
                ))}
              </div>
              {loadingMore && (
                <div className="text-center text-gray-500 mt-2">
                  Loading more users...
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
