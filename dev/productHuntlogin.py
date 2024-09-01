from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# replace with the site you want to visit
url = "https://www.producthunt.com/"

email = "tim.schmid.student@gmail.com"

password = "Singapur2020"

method = "google"

# Start the browser
driver = webdriver.Firefox()

driver.get(url)

# Get the button with the class name
login_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//li[contains(@class, 'styles_submit__58ZM_') and .//button[contains(text(), 'Sign in')]]//button"))
)

# Click the button
login_button.click()

# Wait for the page to load
time.sleep(5)