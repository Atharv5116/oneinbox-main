import React, { useEffect, useRef, useCallback, useState, Suspense } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useFrappeGetCall } from "frappe-react-sdk";
import { addMessages, clearMessages } from "../../../store/reducers/chatSlice";
import { Loader } from "../../Loaders/Loader";
import { DateSeparator } from "./DateSeparator";
import { SenderMessage } from "../Message/SenderMessage";
import { ReceiverMessage } from "../Message/ReceiverMessage";
import { EditorMessage } from "../Editor/EditorMessage";

export const ChatBody = ({ user }) => {
  const dispatch = useDispatch();
  const messages = useSelector((state) => state.chat.messages);

  // Pagination
  const [page, setPage] = useState(1);
  const [hasNext, setHasNext] = useState(true);
  const [loadingMore, setLoadingMore] = useState(false);

  // Fetch messages
  const {
    data,
    error: apiError,
    isValidating // from useFrappeGetCall
  } = useFrappeGetCall(
    "oneinbox.utils.api.messages.fetch_messages",
    {
      user_id: user?.user_id,
      platform: user?.platform,
      platform_id:
        user?.platform === "Messenger" ? "371024009436368" : "17841469373342139",
      limit: 100,
      page,
      order: "desc"
    },
  );

  // Container ref to handle scrolling
  const chatRef = useRef(null);

  useEffect(() => {
    dispatch(clearMessages());
    setPage(1); // Reset page to 1 when user changes
  }, [user, dispatch]);

  // When data arrives
  useEffect(() => {
    if (data?.message?.data) {
      dispatch(addMessages(data.message.data)); // merges into Redux

      // Check if more pages remain
      const { has_next } = data.message.pagination || {};
      setHasNext(has_next);

      // If this is the FIRST load (page = 1),
      // auto-scroll to the bottom:
      if (page === 1) {
        setTimeout(scrollToBottom, 100); // Delay to ensure messages are rendered
      }
      // If we are loading older messages (page > 1),
      // preserve the scroll position
    }
    setLoadingMore(false);
  }, [data, dispatch, page, user]);

  // Auto-scroll to bottom helper
  const scrollToBottom = useCallback(() => {
    if (chatRef.current) {
      chatRef.current.scrollTop = chatRef.current.scrollHeight;
    }
  }, []);

  // On scroll, if we reach top, load older messages
  const handleScroll = useCallback(
    (event) => {
      if (!hasNext || loadingMore) return;
      const { scrollTop } = event.currentTarget;
      if (scrollTop === 0) {
        // we are at top, load next page
        setLoadingMore(true);
        setPage((prev) => prev + 1);
      }
    },
    [hasNext, loadingMore]
  );

  // Render states
  if (isValidating && page === 1) {
    // If it's the initial load, show a loader
    return <Loader />;
  }

  if (apiError) {
    return (
      <div className="text-center text-red-500">
        <p>Failed to load messages. Please try again later.</p>
        <pre>{apiError.message}</pre>
      </div>
    );
  }

  // If no messages at all
  if (!messages || messages.length === 0) {
    return (
      <>
        <div className="flex flex-col h-full" ref={chatRef}>
          <p className="m-auto text-gray-500">No messages available.</p>
        </div>
        <EditorMessage />
      </>
    );
  }

  return (
    <>
      <div
        className="flex flex-col h-full overflow-y-auto scrolling-touch"
        ref={chatRef}
        onScroll={handleScroll}
      >
        {messages.map((message, index) => {
          const showDateSeparator =
            index === 0 ||
            new Date(message.metadata.timestamp).toDateString() !==
              new Date(messages[index - 1].metadata.timestamp).toDateString();

          return (
            <React.Fragment key={message.id}>
              {showDateSeparator && (
                <DateSeparator date={message.metadata.timestamp} />
              )}
              {message.metadata.flow === "Incoming" ? (
                <ReceiverMessage message={message} />
              ) : (
                <SenderMessage message={message} />
              )}
            </React.Fragment>
          );
        })}
        {loadingMore && <Loader />}
        <div className="pt-4" />
      </div>
      <Suspense fallback={<div>Loading Editor...</div>}>
        <EditorMessage scrollToBottom={scrollToBottom} />
      </Suspense>
    </>
  );
};
