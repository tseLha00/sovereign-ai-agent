import { test, expect } from "@playwright/test";

test("UI smoke test: load page, send message, render reply, clear chat", async ({ page }) => {
  await page.route("**/v1/chat/completions", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        id: "chatcmpl-test-1",
        object: "chat.completion",
        created: Math.floor(Date.now() / 1000),
        model: "apertus-8b",
        choices: [
          {
            index: 0,
            message: {
              role: "assistant",
              content: "This is a mocked browser test response."
            },
            finish_reason: "stop"
          }
        ],
        usage: {
          prompt_tokens: null,
          completion_tokens: null,
          total_tokens: null
        }
      })
    });
  });

  await page.goto("/ui/");

  await expect(page.getByText("Sovereign AI Agent (Apertus)")).toBeVisible();
  await expect(page.getByText("Hello! How can I help you today?")).toBeVisible();

  const input = page.getByPlaceholder("Type your message...");
  await input.fill("Hello from Playwright");

  await page.getByRole("button", { name: /send/i }).click();

  await expect(page.getByText("Hello from Playwright")).toBeVisible();
  await expect(page.getByText("This is a mocked browser test response.")).toBeVisible();

  await page.getByRole("button", { name: /clear/i }).click();

  await expect(page.getByText("Hello! How can I help you today?")).toBeVisible();
  await expect(page.getByText("Hello from Playwright")).not.toBeVisible();
  await expect(page.getByText("This is a mocked browser test response.")).not.toBeVisible();
});