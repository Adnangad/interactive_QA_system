'use client'
import Image from "next/image";
import { useState, useEffect } from "react";
import LoadingSpinner from "./loading";

const useTypewriter = (text: string, speed = 20) => {
  const [displayText, setDisplayText] = useState('');

  useEffect(() => {
    let i = 0;
    const typeCharacter = () => {
      if (i < text.length) {
        setDisplayText(prevText => prevText + text.charAt(i));
        i++;
        setTimeout(typeCharacter, speed);
      }
    };

    typeCharacter();
  }, [text, speed]);

  return displayText;
};

export default function Home() {
  const [query, SetQuery] = useState("");
  const [error, SetError] = useState("");
  const [loading, SetLoading] = useState(false);
  const [response, SetResponse] = useState([]);
  const tempData = [{ user: "Hello, how are you?", chat_bot: "I am doing well bg-blue-500 rounded items-center justify-items-center pt-4" }]
  //const typedText = useTypewriter("Welcome, Whats on your mind?", 50);

  useEffect(() => {
    async function get_data() {
      try {
        const url = "http://localhost:2189/prompt";
        const resp = await fetch(url, {
          method: "GET",
          headers: { "Content-Type": "application/json" }
        });
        const data = await resp.json();
        SetResponse(data);
      } catch (error: any) {
        console.log(error);
        SetError("An error occured while fetching chat history");
      }
    }
    get_data()
  }, [])

  async function promptChat(event: Event) {
    SetLoading(true)
    event.preventDefault()
    const url = "http://localhost:2189/prompt";
    if (query.length < 1) {
      SetError("Kindly input a valid prompt");
    }
    try {
      const resp = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(query),
      });
      if (resp.status == 200) {
        const data = await resp.json()
        SetResponse(data);
      }
      else {
        console.log(resp.status)
      }
    } catch (error: any) {
      console.log(error);
      SetError("Unable to Respond at this time, Kindly try again later");
    }

  }

  return (
    <div className="font-sans grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-2 pb-0 gap-4 sm:p-20">
      <div className="w-full h-15 bg-blue-500 rounded items-center justify-items-center pt-4">
        <h2 className="text-2xl">Chatgpt</h2>
      </div>
      <div className="w-full h-auto border px-6 py-4 overflow-y-auto max-h-[70vh]">
        <ul>
          {tempData.map((dat, index) => (
            <li key={index} className="mb-4">
              {dat.user && (
                <p className="text-lg bg-blue-500 text-white p-2 rounded-xl float-right clear-both max-w-xs">
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
      </div>
      <footer className="w-full h-auto pr-40 pl-40">
        {loading ? (
          <LoadingSpinner></LoadingSpinner>
        ) : (
          <input className="w-full h-10 bg-gray-500 rounded-2xl" placeholder="Ask Anything"></input>
        )}
      </footer>
    </div>
  );
}
