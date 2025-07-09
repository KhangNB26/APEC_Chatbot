const API_BASE = "/api";

const chat = document.getElementById("chat");
const form = document.getElementById("chat-form");
const input = document.getElementById("question-input");
const quickRepliesContainer = document.getElementById("quick-replies");


const quickReplies = [
  "Today Event",
  "How to get to Gyeongju",
  "APEC 2025 Overview",
];

// Render quick replies on page load
function showQuickReplies() {
  quickRepliesContainer.innerHTML = ""; // Clear cũ
  quickReplies.forEach((text) => {
    const btn = document.createElement("button");
    btn.classList.add("quick-reply-btn");
    btn.textContent = text;
    btn.addEventListener("click", () => {
      input.value = text;
      form.dispatchEvent(new Event("submit")); // Giả lập submit
    });
    quickRepliesContainer.appendChild(btn);
  });
}

showQuickReplies();

// Add message to chat
function addMessage(content, role = "bot") {
  const div = document.createElement("div");
  div.classList.add("message", role);
  div.textContent = content;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const question = input.value.trim();
  if (!question) return;

  addMessage(question, "user");
  input.value = "";
  input.focus();

  try {
    const res = await fetch(`${API_BASE}/ask`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ question }),
  });
    if (!res.ok) throw new Error(`Server error: ${res.status}`);
    const data = await res.json();
    addMessage(data.answer, "bot");
  } catch (err) {
    console.error(err);
    addMessage("⚠️ Oops! Something went wrong.");
  }
});
