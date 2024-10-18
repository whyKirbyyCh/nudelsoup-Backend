import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time

print("Start")

# Define the Chrome binary location explicitly
chrome_binary_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

options = uc.ChromeOptions()
options.binary_location = chrome_binary_path

# Add arguments to suppress pop-ups and notifications
options.add_argument("--disable-notifications")  # Disable notifications
options.add_argument("--disable-geolocation")     # Disable location prompts
options.add_argument("--disable-popup-blocking")  # Disable popup blocking (optional)

# Set experimental options to manage permissions
prefs = {
    "profile.default_content_setting_values.notifications": 2,  # Block notifications
    "profile.default_content_setting_values.geolocation": 2    # Block geolocation requests
}
options.add_experimental_option("prefs", prefs)

# Start the undetected Chrome browser with the specified options
driver = uc.Chrome(options=options)

# URL and credentials
url = "https://www.producthunt.com/"
email = "tim.schmid.student@gmail.com"
password = "Singapur2020"
method = "google"
headline = "Founder and Story teller"
company_name = "Company Name"
link_name = "example"
link = "example.com"



def headline_is_valid(headline):
    """Check that headline is less than 40 characters"""
    return len(headline) < 40

if not headline_is_valid(headline):
    print("Headline must be less than 40 characters")
    driver.quit()
    exit()

# Visit the website
driver.get(url)


def safe_find_element(by, value, timeout=10):
    """Helper function to safely find an element with retry on stale reference."""
    wait = WebDriverWait(driver, timeout)
    while True:
        try:
            return wait.until(EC.visibility_of_element_located((by, value)))
        except StaleElementReferenceException:
            print("Element went stale, retrying...")
        except NoSuchElementException as e:
            print(f"Element not found: {e}")
            break


try:
    # Locate and click the login button
    login_button = safe_find_element(By.XPATH,
                                     "//li[contains(@class, 'styles_submit__58ZM_') and .//button[contains(text(), 'Sign in')]]//button")
    print("Login button found")
    login_button.click()

    # Locate and click the Google login button
    login_method_button = safe_find_element(By.XPATH, "//button[@data-test='login-with-google']")
    print("Google login button found")
    login_method_button.click()

    # Enter the email
    email_input = safe_find_element(By.XPATH, "//input[@type='email' and @class='whsOnd zHQkBf']")
    print("Email input found")
    email_input.send_keys(email)

    # Click the "Next" button
    next_button = safe_find_element(By.XPATH,
                                    "//button[@data-idom-class='nCP5yc AjY5Oe DuMIQc LQeN7 BqKGqe Jskylb TrZEUc lw1w4b']")
    print("Next button found")
    next_button.click()

    time.sleep(2)

    # Enter the password
    password_input = safe_find_element(By.XPATH, "//input[@type='password' and @class='whsOnd zHQkBf']")
    print("Password input found")
    password_input.send_keys(password)

    next_button = safe_find_element(By.XPATH, "//button[@data-idom-class='nCP5yc AjY5Oe DuMIQc LQeN7 BqKGqe Jskylb TrZEUc lw1w4b']")
    if next_button:
        print("Next button found for password")
        next_button.click()
        time.sleep(2)
    else:
        print("Next button for password not found.")

    print("Login attempted successfully.")

    time.sleep(5)

    driver.get("https://www.producthunt.com/?bc=1")

    complete_onboarding_button = safe_find_element(By.XPATH, "//a[@data-test='complete-onboarding-btn' and contains(text(), 'Complete onboarding')]")
    print("Complete onboarding button found")
    complete_onboarding_button.click()

    try:
        headline_input = safe_find_element(By.XPATH,
                                           "//textarea[@name='headline' and contains(@placeholder, 'Example: Co-founder and storyteller. Building a social app.')]")
        if headline_input:
            print("Headline input found")
            headline_input.send_keys(headline)
        else:
            print("Headline input not found")

        time.sleep(2)

    except Exception as e:
        print(f"An error occurred in header finding: {e}")

    time.sleep(2)

    try:
        switch_entry_mode_button = safe_find_element(By.XPATH,
                                                     "//button[@type='button' and @class='text-left text-14 font-normal text-blue mt-5 sm:mt-0 styles_modeEntrySwitchButton__uJzdz' and @data-test='switch-company-name-entry-mode']")

        if switch_entry_mode_button:
            print("Switch entry mode button found")
            switch_entry_mode_button.click()

        else:
            print("Switch entry mode button not found")

    except Exception as e:
        print(f"An error occurred in mode switch button: {e}")

    time.sleep(2)

    try:
        company_name_input = safe_find_element(By.XPATH,
                                               "//input[@type='text' and @name='companyName' and @placeholder='Enter the name of your company' and @class='styles_input__mZc0X px-3 py-2 text-14 text-light-gray']")
        if company_name_input:
            print("Company name input found")
            company_name_input.click()
            company_name_input.send_keys(Keys.COMMAND + "A")
            company_name_input.send_keys(Keys.BACKSPACE)
            company_name_input.send_keys(company_name)

        else:
            print("Company name input not found")

    except Exception as e:
        print(f"An error occurred in company name input: {e}")


    try:
        newsletter_checkbox = safe_find_element(By.XPATH,
                                                "//li[contains(., 'Weekly Digest')]//input[@type='checkbox' and @name='weeklyNewsletterSubscription']")
        if newsletter_checkbox:
            print("Newsletter checkbox found")
            newsletter_checkbox.click()
        else:
            print("Newsletter checkbox not found")

    except Exception as e:
        print(f"An error occurred in newsletter checkbox: {e}")

    try:
        deeper_learning_checkbox = safe_find_element(By.XPATH,
                                                    "//input[@type='checkbox' and @name='deeperLearningSubscription' and @hidden and @checked]")
        if deeper_learning_checkbox:
            print("Deeper learning checkbox found")
            deeper_learning_checkbox.click()
        else:
            print("Deeper learning checkbox not found")

    except Exception as e:
        print(f"An error occurred in deeper learning checkbox: {e}")



    try:
        age_checkbox = safe_find_element(By.XPATH,
                                         "//label[contains(@class, 'flex') and contains(@class, 'gap-2') and .//div[contains(@class, 'styles_checkbox__HxLrG')] and .//input[@type='checkbox' and @name='confirmedAge' and @hidden] and .//div[contains(text(), 'I am aged 16 years of age or older')]")
        if age_checkbox:
            print("Age checkbox found")
            age_checkbox.click()
        else:
            print("Age checkbox not found")

    except Exception as e:
        print(f"An error occurred in age checkbox: {e}")


    try:
        captcha_checkbox = safe_find_element(By.XPATH,
                                             "//span[contains(@class, 'recaptcha-checkbox') and contains(@class, 'goog-inline-block') and contains(@class, 'recaptcha-checkbox-unchecked') and contains(@class, 'rc-anchor-checkbox')]")
        if captcha_checkbox:
            print("Captcha checkbox found")
            captcha_checkbox.click()
        else:
            print("Captcha checkbox not found")

    except Exception as e:
        print(f"An error occurred in captcha checkbox: {e}")

    try:
        save_button = safe_find_element(By.XPATH,
                                        "//button[contains(@class, 'styles_reset__0clCw') and contains(@class, 'styles_button__BmLM4') and contains(@class, 'styles_primary__o9u3f') and contains(text(), 'Save')]")
        if save_button:
            print("Save button found")
            save_button.click()
        else:
            print("Save button not found")

    except Exception as e:
        print(f"An error occurred in save button: {e}")

    time.sleep(2)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()
    print("Driver quit successfully.")
