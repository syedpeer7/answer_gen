from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
import requests
import time
import json

options = webdriver.ChromeOptions()
# options.add_argument("--headless")
driver = webdriver.Chrome(options=options)
driver.get('https://ays-pro.com/blog/free-general-knowledge-questions')
time.sleep(3)

inject_icon_script = """
(function(){
    if(document.getElementById('qa-answers-icon')) document.getElementById('qa-answers-icon').remove();
    if(document.getElementById('qa-answers-popup')) document.getElementById('qa-answers-popup').remove();

    const icon = document.createElement('div');
    icon.id = 'qa-answers-icon';
    icon.innerText = '💡';
    icon.style.cssText = `
        position:fixed;bottom:30px;right:30px;width:48px;height:48px;border-radius:50%;
        background:#00796b;color:#fff;font-size:32px;display:flex;align-items:center;justify-content:center;
        box-shadow:0 4px 16px rgba(0,0,0,0.25);cursor:pointer;z-index:99999;transition:background 0.2s;
    `;
    icon.onmouseover = () => icon.style.background = "#26a69a";
    icon.onmouseout = () => icon.style.background = "#00796b";

    const popup = document.createElement('div');
    popup.id = 'qa-answers-popup';
    popup.style.cssText = `
        position: fixed; bottom: 90px; right: 30px; width: 500px; max-height: 70vh; background: #fff;
        border-radius: 12px; box-shadow: 0 8px 32px rgba(0,0,0,0.18); color: #333; z-index: 100000;
        display: none; overflow-y: auto; padding: 24px 20px 20px 20px; font-family: Arial,sans-serif;
    `;

    const closeBtn = document.createElement('button');
    closeBtn.innerText = '✖';
    closeBtn.style.cssText = `
        position: absolute; top: 10px; right: 14px; border: none; background: transparent; color: #888;
        font-size: 20px; cursor: pointer;
    `;
    closeBtn.onclick = () => popup.style.display = 'none';
    popup.appendChild(closeBtn);

    const title = document.createElement('h3');
    title.innerText = 'Questions & Answers';
    title.style.cssText = "margin-top: 0; margin-bottom: 16px; color: #00796b;";
    popup.appendChild(title);

    const container = document.createElement('div');
    container.id = 'qa-answers-container';
    popup.appendChild(container);

    icon.onclick = () => {
        popup.style.display = (popup.style.display === 'none' || popup.style.display === '') ? 'block' : 'none';
    };

    document.body.appendChild(icon);
    document.body.appendChild(popup);

    container.innerHTML = '<div style="color:#888">No answers found yet.</div>';
})();
"""

def inject_if_missing():
    try:
        is_present = driver.execute_script("return !!document.getElementById('qa-answers-icon');")
        if not is_present:
            driver.execute_script(inject_icon_script)
            print("Icon re-injected after reload or navigation.")
    except WebDriverException:
        # Page might still be loading, wait and retry in main loop
        pass

def extract_questions_and_options():
    qa_list = []
    try:
        questions = driver.find_elements(By.TAG_NAME, 'p')
        for idx, q_el in enumerate(questions):
            question = q_el.text.strip()
            if "?" not in question:
                continue
            try:
                ol = q_el.find_element(By.XPATH, 'following-sibling::ol[1]')
                options = [
                    li.text.strip()
                    for li in ol.find_elements(By.TAG_NAME, 'li')
                    if "correct answer" not in li.text.strip().lower()
                ]
            except Exception:
                continue
            if options:
                qa_list.append({
                    'question': question,
                    'options': options
                })
    except WebDriverException:
        # DOM is not ready, will retry in main loop
        pass
    return qa_list

def send_with_retry(prompt, max_retries=5):
    url = "http://localhost:5000/question"
    payload = {"question": prompt}
    delay = 2
    for attempt in range(max_retries):
        try:
            resp = requests.post(url, json=payload)
            if resp.status_code == 429:
                time.sleep(delay)
                delay *= 2
                continue
            resp.raise_for_status()
            try:
                return resp.json().get("answer", "No answer")
            except Exception:
                return resp.text
        except requests.exceptions.RequestException:
            time.sleep(delay)
            delay *= 2
    return "Failed after retries"

def fetch_all_qa_pairs():
    try:
        resp = requests.get("http://localhost:5000/answers")
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return []

def update_popup(qa_pairs_with_answers):
    if not qa_pairs_with_answers:
        html_content = '<div style="color:#888">No answers found yet.</div>'
    else:
        blocks = []
        for idx, qa in enumerate(qa_pairs_with_answers):
            lines = qa['question'].split('\n')
            q_main = lines[0]
            q_opts = lines[1:]
            options_html = ""
            if q_opts:
                options_html = '<div style="margin:8px 0 6px 0; font-size: 15px;"><b>Options:</b><ul style="margin:4px 0 0 18px;">' + \
                    ''.join(f"<li style='margin-bottom:2px'>{opt}</li>" for opt in q_opts) + '</ul></div>'
            block = f"""
            <div style="margin-bottom: 18px; padding-bottom: 10px; border-bottom: 1px solid #eee;">
                <div style="font-weight:600; color:#222;">{idx+1}. {q_main}</div>
                {options_html}
                <div style="color: #388e3c; margin-top: 4px;">Answer: <b>{qa['answer']}</b></div>
            </div>
            """
            blocks.append(block)
        html_content = "".join(blocks)

    update_script = f"""
    (function(){{
        var container = document.getElementById('qa-answers-container');
        if(container) {{
            container.innerHTML = `{html_content}`;
        }}
    }})();
    """
    try:
        driver.execute_script(update_script)
    except WebDriverException:
        # DOM is not ready, will retry in main loop
        pass

while True:
    try:
        # Make sure icon/popup are present after reload/navigation
        inject_if_missing()
        # Scrape questions and options
        qa_pairs = extract_questions_and_options()
        for qa in qa_pairs:
            prompt = qa["question"] + "\n" + "\n".join(qa["options"])
            send_with_retry(prompt)
            # Update popup after each answer is sent/received
            qa_pairs_with_answers = fetch_all_qa_pairs()
            update_popup(qa_pairs_with_answers)
            time.sleep(1)
        # Make sure popup is up-to-date at the end of each full scrape cycle
        qa_pairs_with_answers = fetch_all_qa_pairs()
        update_popup(qa_pairs_with_answers)
        print("Popup updated with all Q&A (real-time)!")
        time.sleep(10)  # Check more frequently for reload/navigation
    except WebDriverException:
        # Page reloaded or navigated; wait, then re-inject and continue
        print("Page reload or navigation detected, waiting for DOM to be ready...")
        time.sleep(2)
        continue
