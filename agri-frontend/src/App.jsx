// import { useEffect, useRef, useState } from "react";
// import axios from "axios";

// const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8080";

// function App() {
//   const [messages, setMessages] = useState([
//     { role: "assistant", text: "Namaste! Ask any agriculture question in your language." }
//   ]);
//   const [input, setInput] = useState("");
//   const [loading, setLoading] = useState(false);
//   const [error, setError] = useState("");
//   const listEndRef = useRef(null);
//   const [location, setLocation] = useState(null);

//   useEffect(() => {
//     listEndRef.current?.scrollIntoView({ behavior: "smooth" });
//   }, [messages, loading]);
//   useEffect(() => {
//   if (navigator.geolocation) {
//     navigator.geolocation.getCurrentPosition(
//       (pos) => {
//         setLocation({
//           lat: pos.coords.latitude,
//           lon: pos.coords.longitude
//         });
//       },
//       (err) => {
//         console.warn("Location access denied:", err.message);
//       }
//     );
//   }
// }, []);



//   const ask = async (e) => {
//   e.preventDefault();
//   const q = input.trim();
//   if (!q) return;
//   setError("");
//   setMessages((m) => [...m, { role: "user", text: q }]);
//   setInput("");
//   setLoading(true);
//   try {
//     const res = await axios.post(`${API_BASE}/answer`, {
//       question: q,
//       location // send location object if available
//     }, { timeout: 60000 });
//     const ans = res?.data?.answer ?? "No answer received.";
//     setMessages((m) => [...m, { role: "assistant", text: ans }]);
//   } catch (err) {
//     const msg = err?.response?.data?.detail || err.message || "Request failed";
//     setError(msg);
//     setMessages((m) => [...m, { role: "assistant", text: "Sorry, I couldn’t process that." }]);
//   } finally {
//     setLoading(false);
//   }
// };

  

//   return (
//     <div style={styles.container}>
//       <header style={styles.header}>
//         Agri Advisor
//         <span style={styles.sub}> - RAG + Gemini - India-ready</span>
//       </header>

//       <main style={styles.chat}>
//         {messages.map((m, i) => (
//           <div key={i} style={{ ...styles.bubble, ...(m.role === "user" ? styles.user : styles.assistant) }}>
//             {m.text}
//           </div>
//         ))}
//         {loading && <div style={{ ...styles.bubble, ...styles.assistant }}>Thinking…</div>}
//         <div ref={listEndRef} />
//       </main>

//       {error && <div style={styles.error}>{error}</div>}

//       <form onSubmit={ask} style={styles.inputRow}>
//         <input
//           style={styles.input}
//           placeholder="e.g., अगले हफ्ते के तापमान से मेरी टमाटर फसल पर क्या असर पड़ेगा?"
//           value={input}
//           onChange={(e) => setInput(e.target.value)}
//         />
//         <button style={styles.button} type="submit" disabled={loading}>
//           Ask
//         </button>
//       </form>

//       <footer style={styles.footer}>
//         Tips: Ask about irrigation timing, seed varieties, pest risk, mandi prices, or policy eligibility.
//       </footer>
//     </div>
//   );
// }

// const styles = {
//   container: { display: "flex", flexDirection: "column", height: "100vh", background: "#0b1726", color: "#e7eef7" },
//   header: { padding: "12px 16px", fontWeight: 700, borderBottom: "1px solid #1f2b3b" },
//   sub: { color: "#7aa2f7", fontWeight: 400, marginLeft: 6, fontSize: 14 },
//   chat: { flex: 1, overflowY: "auto", padding: 16, display: "flex", flexDirection: "column", gap: 8 },
//   bubble: { maxWidth: "75%", padding: "10px 12px", borderRadius: 12, whiteSpace: "pre-wrap", lineHeight: 1.4 },
//   user: { alignSelf: "flex-end", background: "#244d8a" },
//   assistant: { alignSelf: "flex-start", background: "#13233a" },
//   inputRow: { display: "flex", gap: 8, padding: 12, borderTop: "1px solid #1f2b3b" },
//   input: { flex: 1, padding: "10px 12px", borderRadius: 8, border: "1px solid #1f2b3b", background: "#0f1b2d", color: "#e7eef7" },
//   button: { padding: "10px 16px", borderRadius: 8, border: "none", background: "#7aa2f7", color: "#0b1726", fontWeight: 700, cursor: "pointer" },
//   error: { color: "#ffb4a9", padding: "4px 16px" },
//   footer: { padding: "8px 16px", color: "#9fb3d2", fontSize: 12 }
// };

// export default App;
