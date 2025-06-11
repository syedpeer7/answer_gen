const GEMINI_API_KEY = "AIzaSyCPxYEmoEf0CNHWXO8yIKKATzgoYEpby-E"; // Replace with your Gemini API key

// Create context menu item for selected text
chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "get-answer",
    title: "Get Answer to Selected Question",
    contexts: ["selection"]
  });
});

// Listen for context menu click
chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === "get-answer" && info.selectionText) {
    // Send selected text to Gemini API
    fetch(
      `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${GEMINI_API_KEY}`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          contents: [
            {
              parts: [{ text: info.selectionText }]
            }
          ]
        })
      }
    )
      .then(res => res.json())
      .then(data => {
        let answer = "No answer found.";
        try {
          answer = data.candidates[0].content.parts[0].text;
        } catch (e) {
          answer = "Could not extract answer from Gemini API response.";
        }
        // Send answer to content script to display
        chrome.tabs.sendMessage(tab.id, { type: "ANSWER", answer });
      });
  }
});