# Realtime Q&A Popup with Selenium and Flask Gemini Server

This project provides a complete solution for displaying real-time question and answer pairs from a Flask Gemini backend as a floating popup on any website using Selenium automation.  
It features a persistent 💡 icon that, when clicked, shows the latest scraped questions and their Gemini-provided answers, updating in real time—even after page reloads.

---

## Features

- **Automatic Scraping:** Extracts questions and options from any specified web page.
- **Gemini Integration:** Sends questions to your Flask Gemini API and stores/returns answers.
- **Realtime Popup:** Displays a floating 💡 icon; click to view/update the Q&A popup.
- **Robust Reload Handling:** Re-injects the icon and popup after page reloads or navigation.
- **Customizable:** Easily adjust update intervals, styling, or target URLs.

---

## Project Structure

```
.
├── qa_popup_reinject_on_reload.py    # Main Selenium script
├── server.py                        # Flask Gemini backend server
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

---

## Setup & Usage

### 1. Install Requirements

```bash
pip install -r requirements.txt
```

#### `requirements.txt` should include:
```
selenium
requests
flask
```

### 2. Start the Flask Gemini Server

Edit `server.py` with your Gemini API key if needed.

```bash
python server.py
```

- This exposes:
  - `POST /question` - Accepts a question (with options) and returns the Gemini answer.
  - `GET /answers` - Returns all Q&A pairs.

### 3. Run the Selenium Script

Edit the URL in `qa_popup_reinject_on_reload.py` if you want to scrape a different page.

```bash
python qa_popup_reinject_on_reload.py
```

- This will open a browser, scrape questions, send them to the server, and display a 💡 icon.
- The popup updates in real time as answers are received.
- The icon and popup will **reappear after any page reload or navigation**.

---

## Demo

![Demo Screenshot](demo_screenshot.png)

---

## Customization

- **Change Target Page:**  
  Edit the URL in the Selenium script:
  ```python
  driver.get('https://example.com')
  ```
- **Adjust Update Frequency:**  
  Change the `time.sleep()` values in the main loop.
- **Styling:**  
  Edit the injected JS/CSS in the Python script for a different look.

---

## Troubleshooting

- **Icon disappears after reload:**  
  This script automatically re-injects the icon/popup. If you still have issues, ensure your Selenium version is up-to-date.
- **CORS Issues:**  
  Make sure the Flask server allows requests from your browser (you may need to enable CORS for production).
- **Gemini API errors:**  
  Ensure your Gemini API key is valid and you have quota.

---

## License

MIT

---

## Credits

- [Gemini API](https://ai.google.dev/)
- [Selenium](https://www.selenium.dev/)
- [Flask](https://flask.palletsprojects.com/)
