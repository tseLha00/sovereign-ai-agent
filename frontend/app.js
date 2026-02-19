const chatEl = document.getElementById("chat");
const formEl = document.getElementById("form");
const inputEl = document.getElementById("input");
const sendBtn = document.getElementById("sendBtn");
const clearBtn = document.getElementById("clearBtn");
const errorEl = document.getElementById("error");

let messages = [];

function showError(text) {
  errorEl.textContent = text;
  errorEl.classList.remove("hidden");
}

function clearError() {
  errorEl.textContent = "";
  errorEl.classList.add("hidden");
}

function render() {
  chatEl.innerHTML = "";
  for (const m of messages) {
    const row = document.createElement("div");
    row.className = `msg ${m.role}`;
    const bubble = document.createElement("div");
    bubble.className = "bubble";
    bubble.textContent = m.content;
    row.appendChild(bubble);
    chatEl.appendChild(row);
  }
  chatEl.scrollTop = chatEl.scrollHeight;
}

function add(role, content) {
  messages.push({ role, content });
  render();
}

async function sendMessage(text) {
  clearError();
  add("user", text);

  // UX latency mitigation
  sendBtn.disabled = true;
  inputEl.disabled = true;
  add("assistant", "…thinking");

  const payload = {
    model: "apertus-8b",
    messages: [
      { role: "system", content: "You are a helpful assistant." },
      ...messages.filter(m => m.content !== "…thinking").map(m => ({ role: m.role, content: m.content }))
    ],
    stream: false
  };

  try {
    const res = await fetch("/v1/chat/completions", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await res.json();

    // remove thinking bubble
    messages = messages.filter(m => m.content !== "…thinking");

    if (!res.ok) {
      const msg = data?.error?.message || `Request failed (${res.status})`;
      showError(msg);
      add("assistant", "Error. Please try again.");
      return;
    }

    const content = data?.choices?.[0]?.message?.content ?? "(no content)";
    add("assistant", content);

  } catch (e) {
    messages = messages.filter(m => m.content !== "…thinking");
    showError("Network error. Is the backend running?");
    add("assistant", "Error. Please try again.");
  } finally {
    sendBtn.disabled = false;
    inputEl.disabled = false;
    inputEl.focus();
  }
}

formEl.addEventListener("submit", (e) => {
  e.preventDefault();
  const text = inputEl.value.trim();
  if (!text) return;
  inputEl.value = "";
  sendMessage(text);
});

clearBtn.addEventListener("click", () => {
  messages = [];
  clearError();
  render();
  inputEl.focus();
});

render();
