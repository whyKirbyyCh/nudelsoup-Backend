import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
import time

surname = "test"
name = "test"
month = "January"
day = "1"
year = "2000"
username = "wbrtliwebrilwebr34"
password = "Thisisastrongpassword3"

def safe_find_element(by, value, timeout=10):
    """Helper function to safely find an element with retry on stale reference."""
    wait = WebDriverWait(driver, timeout)
    while True:
        try:
            return wait.until(EC.presence_of_element_located((by, value)))
        except StaleElementReferenceException:
            print("Element went stale, retrying...")

# Open the browser
driver = uc.Chrome()

# Check if the username is available

def check_username_format():
    if len(username) < 6 or len(username) > 30:
        print("Username is not the correct length.")
        exit()

    if "&=_'-+,.<>[".find(username[0]) != -1 or "&=_'-+,.<>[".find(username[-1]) != -1 or '..' in username:
        print("Username contains invalid characters.")
        exit()

def check_username_availability():
    try:
        username_check_url = "https://accounts.google.com/v3/signin/identifier?flowEntry=ServiceLogin&flowName=GlifWebSignIn&hl=en-GB&ifkv=Ab5oB3p7lHqzPUgm_rQ7zfZpq0-HiqSuByg5xTF-82qgLW3aBgQl1YpGJrXjd5CI4RqVrD7itkoCDA&dsh=S-1241345780%3A1725777663657897&ddm=0"
        driver.get(username_check_url)
        username_input = safe_find_element(By.XPATH, "//input[@class='whsOnd zHQkBf' and @aria-label='Email or phone']")
        username_input.send_keys(username)
        print(f"Username {username} entered.")

        next_button = safe_find_element(By.XPATH,
                                        "//button[@class='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 BqKGqe Jskylb TrZEUc lw1w4b']")
        next_button.click()
        print("Next button clicked.")

        time.sleep(2)

        error_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), \"Couldn't find your Google Account\")]"))
        )

        print(error_message.text)

        if error_message:
            print("Username is already taken.")
        else:
            exit()
    except NoSuchElementException:
        print("Username not available.")
        exit()

def check_password_format():
    if len(password) < 8:
        print("Password is not long enough.")
        exit()

    if not any(char.isdigit() for char in password):
        print("Password must contain at least one number.")
        exit()

    if not any(char.isalpha() for char in password):
        print("Password must contain at least one letter.")
        exit()

    if any(char in password for char in username.split() + [name, surname]):
        print("Password cannot contain personal information.")
        exit()

    if " " in password:
        print("Password cannot contain spaces.")
        exit()

check_username_format()
check_username_availability()


# Visit the Gmail account creation page
driver.get("https://gmail.com")

time.sleep(2)

# Find and click the "Create account" button
create_account_button = safe_find_element(By.XPATH, "//button[contains(@class, 'VfPpkd-LgbsSe') and .//span[contains(text(), 'Create account')]]")
create_account_button.click()

print("Create account button clicked.")

time.sleep(2)

# Find and select the "For work or my business" option
for_work_button = safe_find_element(By.XPATH, "//li[contains(@class, 'gNVsKb G3hhxb VfPpkd-StrnGf-rymPhb-ibnC6b') and .//span[contains(text(), 'For work or my business')]]")
for_work_button.click()

print("For work or my business button clicked.")

time.sleep(2)

# Find and click the "Get a Gmail address" button
get_gmail_address_button = safe_find_element(By.XPATH, "//button[contains(@class, 'UywwFc-LgbsSe') and .//span[contains(text(), 'Get a Gmail address')]]")
get_gmail_address_button.click()

print("Get a Gmail address button clicked.")

time.sleep(2)

# Enter the surname
surname_input = safe_find_element(By.XPATH, "//input[@class='whsOnd zHQkBf' and @aria-label='First name']")
surname_input.send_keys(surname)

print("Surname entered.")

if name != "":
    name_input = safe_find_element(By.XPATH, "//input[@id='lastName']")
    name_input.send_keys(name)
    print("Name entered.")

time.sleep(2)

next_button = safe_find_element(By.XPATH, "//button[@class='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 BqKGqe Jskylb TrZEUc lw1w4b']")
next_button.click()

print("Next button clicked.")

month_option = safe_find_element(By.XPATH, f"//select[@id='month']//option[contains(text(), '{month}')]")
month_option.click()
print(f"Month {month} selected.")

time.sleep(1)

day_input = safe_find_element(By.XPATH, "//input[@id='day']")
day_input.send_keys(day)
print(f"Day {day} entered.")

time.sleep(1)

year_input = safe_find_element(By.XPATH, "//input[@id='year']")
year_input.send_keys(year)
print(f"Year {year} entered.")

time.sleep(1)

gender_option = safe_find_element(By.XPATH, "//select[@id='gender']//option[contains(text(), 'Rather not say')]")
gender_option.click()
print("Gender selected.")

time.sleep(1)

next_button = safe_find_element(By.XPATH, "//button[@class='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 BqKGqe Jskylb TrZEUc lw1w4b']")
next_button.click()
print("Next button clicked.")

time.sleep(2)
username_input = safe_find_element(By.XPATH, "//input[@class='whsOnd zHQkBf' and @aria-label='Username']")
username_input.send_keys(username)
print(f"Username {username} entered.")

next_button = safe_find_element(By.XPATH, "//button[@class='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 BqKGqe Jskylb TrZEUc lw1w4b']")
next_button.click()
print("Next button clicked.")

time.sleep(2)

password_input = safe_find_element(By.XPATH, "//input[@type='password' and @class='whsOnd zHQkBf']")
password_input.send_keys(password)
print(f"Password {password} entered.")

password_confirm_input = safe_find_element(By.XPATH, "//input[@type='password' and @class='whsOnd zHQkBf' and @aria-label='Confirm']")
password_confirm_input.send_keys(password)
print(f"Password {password} confirmed.")

next_button = safe_find_element(By.XPATH, "//button[@class='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 BqKGqe Jskylb TrZEUc lw1w4b']")
next_button.click()
print("Next button clicked.")

time.sleep(10)

driver.quit()
