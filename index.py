from selenium import webdriver
from selenium.webdriver.common.by import By
import pickle
import os
import time

# Step 1: Setup Chrome driver
driver = webdriver.Chrome()

# Check if cookies file exists
cookies_file = "youlikehits_cookies.pkl"

# Try to load cookies if available
if os.path.exists(cookies_file):
    driver.get("https://www.youlikehits.com")
    with open(cookies_file, "rb") as cookiesfile:
        cookies = pickle.load(cookiesfile)
        for cookie in cookies:
            driver.add_cookie(cookie)
    driver.refresh()
    time.sleep(3)  # Give time for page to load after applying cookies

    # Check if login was successful by trying to access a page only visible to logged-in users
    try:
        driver.get("https://www.youlikehits.com/addyoutube.php")
        if "YouLikeHits" in driver.title:  # Assuming title shows this if logged in
            print("Logged in using saved cookies.")
        else:
            raise Exception("Cookies expired or invalid.")
    except Exception as e:
        print(e)
        print("Cookies invalid or expired. Proceeding with manual login...")
        manual_login = True
else:
    manual_login = True

# If cookies failed or don't exist, ask for login credentials
if 'manual_login' in locals() and manual_login:
    username = input("Enter your YouLikeHits username: ")
    password = input("Enter your YouLikeHits password: ")

    driver.get("https://www.youlikehits.com/login.php")
    time.sleep(2)

    # Find and fill the login fields
    username_input = driver.find_element(By.ID, "username")
    password_input = driver.find_element(By.ID, "password")

    username_input.send_keys(username)
    password_input.send_keys(password)
    
    # Wait for user to manually solve CAPTCHA
    input("Please solve the CAPTCHA manually, then press Enter to continue...")
    password_input.send_keys('\n')  # Press Enter to login

    time.sleep(5)  # Wait for login to complete

    # Save cookies for future use
    with open(cookies_file, "wb") as cookiesfile:
        pickle.dump(driver.get_cookies(), cookiesfile)
    print("Cookies saved for future logins.")

# Step 2: Navigate to the YouTube video submission page
driver.get("https://www.youlikehits.com/addyoutube.php")
time.sleep(3)

# Step 3: Add the YouTube video URL and submit
youtube_video_url = input("Enter YouTube video URL to add: ")
video_input = driver.find_element(By.NAME, "id")
video_input.send_keys(youtube_video_url)

# Submit the video
submit_button = driver.find_element(By.XPATH, "//input[@value='Add Video']")
submit_button.click()

time.sleep(5)  # Wait for the page to load after submission

# Step 4: Handle confirmation (Yes, Add Video)
confirm_button = driver.find_element(By.LINK_TEXT, "Yes, Add Video")
confirm_button.click()

time.sleep(5)  # Wait for video submission to process

# Step 5: Navigate to "Manage YouTube" page and set the payout
manage_youtube_link = driver.find_element(By.LINK_TEXT, "Manage YouTube")
manage_youtube_link.click()

time.sleep(3)  # Wait for the Manage YouTube page to load

# Step 6: Set payout value
payout_value = input("Enter payout value (e.g., 10, 15, 20): ")
payout_dropdown = driver.find_element(By.XPATH, "//select[starts-with(@id, 'payoutlikes')]") # Locate the dropdown
payout_dropdown.click()

# Select the payout value
payout_option = driver.find_element(By.XPATH, f"//option[text()='{payout_value} Points']")
payout_option.click()

time.sleep(3)  # Wait for the selection to take effect

print(f"YouTube video successfully added and payout set to {payout_value} Points!")

input("Script complete. Press Enter to close the browser...")

