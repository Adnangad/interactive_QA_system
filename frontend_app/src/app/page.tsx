'use client'
import { useState, useEffect } from "react";
import LoadingSpinner from "./loading";

interface ChatMessage {
  user?: string;
  chat_bot?: string;
}

export default function Home() {
  const [query, SetQuery] = useState("");
  const [error, SetError] = useState("");
  const [loading, SetLoading] = useState(false);
  const [response, SetResponse] = useState<ChatMessage[]>([]);

  // Fetch chat history on mount
  useEffect(() => {
    async function get_data() {
      try {
        const url = "http://127.0.0.1:8000/history";
        const resp = await fetch(url, {
          method: "GET",
          headers: { "Content-Type": "application/json" }
        });
        const data = await resp.json();
        console.log("DATA IS:: ", data);
        SetResponse(data);
      } catch (error: any) {
        console.log(error);
        SetError("An error occurred while fetching chat history");
      }
    }
    get_data()
  }, [])

  // Handle sending prompt
  async function promptChat(event: React.MouseEvent<HTMLButtonElement>) {
    event.preventDefault();
    SetLoading(true);
    SetError(""); // reset error on each attempt

    if (!query.trim()) {
      SetError("Kindly input a valid prompt");
      SetLoading(false);
      return;
    }

    try {
      const resp = await fetch("http://127.0.0.1:8000/prompt", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });

      if (resp.ok) {
        const data: ChatMessage = await resp.json();
        console.log("RESPONSE IS::: ", data);

        // append new messages to chat
        SetResponse(prev => [...prev, data]);
        SetQuery(""); // clear input
      } else {
        console.log("Error status:", resp.status);
        SetError("Something went wrong while fetching response");
      }
    } catch (error: any) {
      console.log(error);
      SetError("Unable to Respond at this time, Kindly try again later");
    } finally {
      SetLoading(false);
    }
  }

  return (
    <div className="font-sans grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-2 sm:p-20">
      <div className="w-full h-15 rounded items-center justify-items-center pt-4">
        <h2 className="text-2xl">Chatgpt</h2>
      </div>

      {/* Chat window */}
      <div className="w-full h-auto px-6 py-4 overflow-y-auto mt-0">
        {response.length > 0 ? (
          <ul>
            {response.map((dat, index) => (
              <li key={index} className="mb-4">
                {dat.user && (
                  <p className="text-lg bg-blue-500 text-white p-2 py-5 rounded-xl float-right clear-both max-w-xs">
                    {dat.user}
                  </p>
                )}
                {dat.chat_bot && (
                  <h3 className="text-lg bg-gray-400 p-2 rounded-xl float-left clear-both w-full pt-3 mt-5">
                    {dat.chat_bot}
                  </h3>
                )}
              </li>
            ))}
          </ul>
        ) : (
          <p>Welcome to chat</p>
        )}
      </div>

      {/* Input Footer */}
      <footer className="w-full h-auto pr-40 pl-40">
        {loading ? (
          <LoadingSpinner />
        ) : (
          <div className="flex items-center w-full border rounded-2xl overflow-hidden">
            <input
              type="text"
              placeholder="Ask Anything..."
              className="flex-grow px-4 p-2 outline-none"
              value={query}
              onChange={(e) => SetQuery(e.target.value)}
            />
            <button
              className="bg-blue-600 text-white px-4 py-2 hover:bg-blue-700 hover:cursor-pointer"
              onClick={promptChat}
            >
              Go
            </button>
          </div>
        )}
        {error && <p className="text-red-600 mt-2">{error}</p>}
      </footer>
    </div>
  );
}
