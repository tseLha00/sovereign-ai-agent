import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./frontend/e2e",
  timeout: 30_000,
  reporter: "list",
  use: {
    baseURL: "http://127.0.0.1:8000",
    headless: true
  }
});