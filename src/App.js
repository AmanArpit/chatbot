import React, { useState } from "react";
import axios from "axios";

const App = () => {
  const [message, setMessage] = useState("");
  const [response, setResponse] = useState(null);

  const handleSend = async () => {
    const res = await axios.post("https://chatbot-lg9o.onrender.com", {
      message: message,
    });
    setResponse(res.data);
  };

  return (
    <div>
      <h1>Human-Like Chatbot</h1>
      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Type your message"
      />
      <button onClick={handleSend}>Send</button>

      {response && (
        <div>
          <h2>Face Output:</h2>
          <img src={response.face_url} alt="Face" width="400" />
          <h2>Audio Output:</h2>
          <audio controls src={response.audio_url}></audio>
        </div>
      )}
    </div>
  );
};

export default App;


