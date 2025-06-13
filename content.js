chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.type === "ANSWER") {
    let answerBox = document.createElement("div");
    answerBox.style = `
      position: fixed; top: 10px; right: 10px; z-index: 99999;
      background: #fff; border: 2px solid #007bff; padding: 20px; font-size: 18px;
      box-shadow: 0 0 10px #0003; max-width: 400px;
    `;
    answerBox.innerText = "Answer: " + msg.answer;
    document.body.appendChild(answerBox);

    setTimeout(() => answerBox.remove(), 15000);
  }
});
