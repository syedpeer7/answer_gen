from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import time

# Start Selenium (headless for performance)
driver = webdriver.Chrome(options=webdriver.ChromeOptions().add_argument('--headless'))
driver.get('https://ays-pro.com/blog/free-general-knowledge-questions')  # Replace with logic to get active tab

def extract_questions():
    # Example: find elements likely to be questions
    elements = driver.find_elements(By.XPATH, "//*[contains(text(), '?']")
    questions = [el.text for el in elements]
    return questions

while True:
    questions = extract_questions()
    for q in questions:
        # Send question to local server or extension (e.g., via HTTP POST)
        requests.post("http://localhost:5000/question", json={"question": q})
    time.sleep(5)
