import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import time

# Define the Chrome binary location explicitly
chrome_binary_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"  # Adjust if necessary

# Set options for the undetected Chrome driver
options = uc.ChromeOptions()
options.binary_location = chrome_binary_path

# Start the undetected Chrome browser with the specified options
driver = uc.Chrome(options=options)

# URL and credentials
url = "https://www.producthunt.com/"
email = "tim.schmid.student@gmail.com"
password = "Singapur2020"
method = "google"

# Visit the website
driver.get(url)

def safe_find_element(by, value, timeout=10):
    """Helper function to safely find an element with retry on stale reference."""
    wait = WebDriverWait(driver, timeout)
    while True:
        try:
            return wait.until(EC.presence_of_element_located((by, value)))
        except StaleElementReferenceException:
            print("Element went stale, retrying...")

# Locate and click the login button
login_button = safe_find_element(By.XPATH, "//li[contains(@class, 'styles_submit__58ZM_') and .//button[contains(text(), 'Sign in')]]//button")
login_button.click()

# Locate and click the Google login button
login_method_button = safe_find_element(By.XPATH, "//button[@data-test='login-with-google']")
login_method_button.click()

# Enter the email
email_input = safe_find_element(By.XPATH, "//input[@type='email' and @class='whsOnd zHQkBf']")
email_input.send_keys(email)

# Click the "Next" button
next_button = safe_find_element(By.XPATH, "//button[@data-idom-class='nCP5yc AjY5Oe DuMIQc LQeN7 BqKGqe Jskylb TrZEUc lw1w4b']")
next_button.click()

time.sleep(2)

# Enter the password
password_input = safe_find_element(By.XPATH, "//input[@type='password' and @class='whsOnd zHQkBf']")
password_input.send_keys(password)

next_button = safe_find_element(By.XPATH, "//button[@data-idom-class='nCP5yc AjY5Oe DuMIQc LQeN7 BqKGqe Jskylb TrZEUc lw1w4b']")
next_button.click()

time.sleep(2)

# Click the "Weiter" button
next_button = safe_find_element(By.XPATH, "//button[@data-idom-class='Rj2Mlf OLiIxf PDpWxe P62QJc LQeN7 BqKGqe pIzcPc TrZEUc lw1w4b']")
next_button.click()

print("Login attempted successfully.")

time.sleep(5)

driver.quit()
