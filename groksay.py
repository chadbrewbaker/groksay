from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import subprocess

# Set up Chrome options to attach to an existing Chrome session
# Note: First, launch Chrome with remote debugging: 
# brew install chromedriver
# xattr -d com.apple.quarantine /opt/homebrew/bin/chromedriver
# /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir=$(mktemp -d)
# Navigate to the chat page in that Chrome window.

chrome_options = Options()
chrome_options.debugger_address = "127.0.0.1:9222"  # Default port; change if needed

# Initialize the WebDriver attached to the existing session
# Assumes ChromeDriver is installed via Homebrew (brew install --cask chromedriver)
driver = webdriver.Chrome(options=chrome_options)

# Ensure we're on the Grok chat page (if not, uncomment the next line)
# driver.get("https://x.com/i/grok")

# Wait for the chat input field to load
input_field = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//textarea[contains(@placeholder, 'Ask')]"))
)

# Clear the input if needed and type the message
input_field.clear()
message = "Hello, this is a test message!"
input_field.send_keys(message)

# Send the message by pressing Enter
input_field.send_keys(Keys.ENTER)

# Wait for the response to load (e.g., by waiting for a new element or time delay; adjust as needed)
time.sleep(30)  # Simple delay; replace with better wait if possible

# Find all copy buttons and click the last one (assuming it's for the latest response)
copy_buttons = driver.find_elements(By.XPATH, '//button[@aria-label="Copy text"]')
if copy_buttons:
    copy_buttons[-1].click()
    time.sleep(1)  # Brief wait for clipboard to update

    # Use pbpaste to get the clipboard content
    response = subprocess.run(['pbpaste'], capture_output=True, text=True).stdout.strip()
    print("Grok's Response:", response)
else:
    print("No copy button found.")

# Wait to observe (optional)
time.sleep(5)

# Note: Do not quit the driver if you want to keep the browser open
# driver.quit()
