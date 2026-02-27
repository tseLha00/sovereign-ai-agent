const { useEffect, useMemo, useRef, useState } = React;
const {
  ThemeProvider,
  createTheme,
  CssBaseline,
  AppBar,
  Toolbar,
  Typography,
  Box,
  Container,
  Paper,
  Chip,
  TextField,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Stack
} = MaterialUI;

const LANGUAGE_OPTIONS = ["English", "German", "French", "Italian"];
const TEMP_OPTIONS = ["0.2", "0.5", "0.7", "1.0"];

function buildSystemPrompt(language) {
  return [
    "You are a helpful assistant.",
    `Reply only in ${language}.`,
    "Do not repeat previous answers.",
    "Do not repeat the user's message.",
    "Do not include role labels like USER: or ASSISTANT:.",
    "Answer naturally and clearly."
  ].join(" ");
}

function initialGreeting(language) {
  const greetings = {
    English: "Hello! How can I help you today?",
    German: "Hallo! Wie kann ich Ihnen heute helfen?",
    French: "Bonjour ! Comment puis-je vous aider aujourd'hui ?",
    Italian: "Ciao! Come posso aiutarti oggi?"
  };

  return greetings[language] || greetings.English;
}

function MessageBubble({ role, content }) {
  const isUser = role === "user";

  return (
    <Box
      sx={{
        display: "flex",
        justifyContent: isUser ? "flex-end" : "flex-start",
        width: "100%"
      }}
    >
      <Paper
        elevation={0}
        sx={{
          maxWidth: "78%",
          px: 2,
          py: 1.5,
          borderRadius: 3,
          color: "#e8eefc",
          backgroundColor: isUser ? "rgba(90,167,255,.18)" : "rgba(255,255,255,.12)",
          border: isUser
            ? "1px solid rgba(90,167,255,.35)"
            : "1px solid rgba(255,255,255,.10)"
        }}
      >
        <Chip
          size="small"
          label={isUser ? "User" : "Assistant"}
          sx={{
            mb: 1,
            height: 24,
            color: "#d8e7ff",
            backgroundColor: isUser
              ? "rgba(90,167,255,.15)"
              : "rgba(255,255,255,.08)",
            border: "1px solid rgba(90,167,255,.35)"
          }}
        />
        <Typography
          variant="body1"
          sx={{
            whiteSpace: "pre-wrap",
            lineHeight: 1.6,
            wordBreak: "break-word"
          }}
        >
          {content}
        </Typography>
      </Paper>
    </Box>
  );
}

function App() {
  const [language, setLanguage] = useState("English");
  const [temperature, setTemperature] = useState("0.2");
  const [messages, setMessages] = useState([
    { role: "assistant", content: initialGreeting("English") }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const chatRef = useRef(null);

  useEffect(() => {
    if (chatRef.current) {
      chatRef.current.scrollTop = chatRef.current.scrollHeight;
    }
  }, [messages, loading]);

  const canSend = useMemo(() => {
    return input.trim().length > 0 && !loading;
  }, [input, loading]);

  async function handleSend() {
    const text = input.trim();
    if (!text || loading) return;

    const nextUserMessage = { role: "user", content: text };
    const nextMessages = [...messages, nextUserMessage];

    setMessages(nextMessages);
    setInput("");
    setError("");
    setLoading(true);

    const payload = {
      model: "apertus-8b",
      messages: [
        {
          role: "system",
          content: buildSystemPrompt(language)
        },
        ...nextMessages
      ],
      temperature: Number(temperature),
      max_tokens: 256,
      stream: false
    };

    try {
      const res = await fetch("/v1/chat/completions", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data?.error?.message || `Request failed (${res.status})`);
      }

      const content =
        data?.choices?.[0]?.message?.content?.trim() || "(no content)";

      setMessages((prev) => [...prev, { role: "assistant", content }]);
    } catch (err) {
      setError(err?.message || "Request failed.");
    } finally {
      setLoading(false);
    }
  }

  function handleClear() {
    setMessages([{ role: "assistant", content: initialGreeting(language) }]);
    setInput("");
    setError("");
    setLoading(false);
  }

  function onSubmit(e) {
    e.preventDefault();
    handleSend();
  }

  const theme = createTheme({
    palette: {
      mode: "dark",
      background: {
        default: "#08111f",
        paper: "#0d1b31"
      },
      primary: {
        main: "#2f8cff"
      }
    },
    typography: {
      fontFamily: "Roboto, system-ui, sans-serif"
    }
  });

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />

      <Box sx={{ minHeight: "100vh", background: "#08111f" }}>
        <AppBar
          position="static"
          elevation={0}
          sx={{
            background: "transparent",
            borderBottom: "1px solid rgba(255,255,255,.08)"
          }}
        >
          <Toolbar sx={{ justifyContent: "space-between" }}>
            <Typography variant="h5" fontWeight={700}>
              Sovereign AI Agent (Apertus)
            </Typography>

            <Button
              variant="outlined"
              onClick={handleClear}
              sx={{
                borderRadius: 2,
                fontWeight: 700
              }}
            >
              Clear
            </Button>
          </Toolbar>
        </AppBar>

        <Container maxWidth="lg" sx={{ py: 3 }}>
          <Paper
            ref={chatRef}
            elevation={0}
            sx={{
              minHeight: "56vh",
              maxHeight: "56vh",
              overflowY: "auto",
              p: 2,
              borderRadius: 3,
              backgroundColor: "rgba(13,27,49,.95)",
              border: "1px solid rgba(255,255,255,.08)",
              display: "flex",
              flexDirection: "column",
              gap: 2
            }}
          >
            {messages.map((msg, index) => (
              <MessageBubble
                key={`${msg.role}-${index}`}
                role={msg.role}
                content={msg.content}
              />
            ))}

            {loading && (
              <MessageBubble role="assistant" content="Thinking…" />
            )}
          </Paper>

          {error && (
            <Paper
              elevation={0}
              sx={{
                mt: 2,
                p: 1.5,
                borderRadius: 2,
                border: "1px solid rgba(255,107,107,.5)",
                backgroundColor: "rgba(255,107,107,.12)",
                color: "#fff"
              }}
            >
              <Typography variant="body2">{error}</Typography>
            </Paper>
          )}

          <Stack direction={{ xs: "column", md: "row" }} spacing={2} sx={{ mt: 2 }}>
            <FormControl fullWidth>
              <InputLabel id="language-label">Language</InputLabel>
              <Select
                labelId="language-label"
                value={language}
                label="Language"
                onChange={(e) => setLanguage(e.target.value)}
              >
                {LANGUAGE_OPTIONS.map((option) => (
                  <MenuItem key={option} value={option}>
                    {option}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>

            <FormControl fullWidth>
              <InputLabel id="temperature-label">Temperature</InputLabel>
              <Select
                labelId="temperature-label"
                value={temperature}
                label="Temperature"
                onChange={(e) => setTemperature(e.target.value)}
              >
                {TEMP_OPTIONS.map((option) => (
                  <MenuItem key={option} value={option}>
                    {option}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Stack>

          <Box
            component="form"
            onSubmit={onSubmit}
            sx={{
              mt: 2,
              display: "flex",
              gap: 2,
              alignItems: "stretch"
            }}
          >
            <TextField
              fullWidth
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your message..."
              disabled={loading}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  handleSend();
                }
              }}
            />
            <Button
              type="submit"
              variant="contained"
              disabled={!canSend}
              sx={{
                minWidth: 120,
                borderRadius: 2,
                fontWeight: 700
              }}
            >
              Send
            </Button>
          </Box>

          <Typography
            variant="body2"
            sx={{
              mt: 2,
              color: "rgba(232,238,252,.75)",
              fontFamily: "monospace"
            }}
          >
            API: POST /v1/chat/completions (Apertus 8B via llama.cpp)
          </Typography>
        </Container>
      </Box>
    </ThemeProvider>
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(<App />);