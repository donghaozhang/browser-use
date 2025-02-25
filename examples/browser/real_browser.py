import os
import sys
from pathlib import Path
import logging
import subprocess
import time
import json
import random

# Set up logging with INFO level instead of DEBUG to reduce output
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Reduce logging from other modules
logging.getLogger('urllib3').setLevel(logging.WARNING)
logging.getLogger('browser_use').setLevel(logging.INFO)

# Try to import the required modules, install if missing
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
except ImportError:
    logger.info("Installing missing langchain-google-genai package...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "langchain-google-genai"])
    from langchain_google_genai import ChatGoogleGenerativeAI

from browser_use.agent.views import ActionResult

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import asyncio

from browser_use import Agent, Controller
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContext

from dotenv import load_dotenv
load_dotenv(dotenv_path="D:/AI_play/AI_Code/browser-use/.env")

# After the load_dotenv line, add:
if not os.getenv("GOOGLE_API_KEY"):
    # Fallback to hardcoded key if not in .env
    os.environ["GOOGLE_API_KEY"] = "AIzaSyDubxzMx5lzQis9nORHnVCv1vWpL-EdrBE"
    logger.info("Using fallback API key")

# Print API key (with partial masking for security)
gemini_api_key = os.getenv("GOOGLE_API_KEY")
if gemini_api_key:
    masked_key = gemini_api_key[:4] + "..." + gemini_api_key[-4:]
    logger.info(f"Gemini API key loaded: {masked_key}")
else:
    logger.error("No Gemini API key found in environment variables!")
    logger.info("Please add GOOGLE_API_KEY to your .env file")
    logger.info("Example: GOOGLE_API_KEY=your_api_key_here")
    sys.exit(1)  # Exit if no API key is found

# Configure the browser with your profile
logger.info("Creating browser instance...")

# Define the path to your Chrome executable and profile
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
chrome_user_data_dir = r"C:\Users\zdhpe\AppData\Local\Google\Chrome\User Data"

# We want to use the Default profile, but we need to pass the User Data directory to Chrome
# and specify the profile name separately
user_data_dir = chrome_user_data_dir
profile_name = "Default"  # This is the profile with zdhpeter1991@gmail.com

logger.info(f"Using Chrome profile: {profile_name}")

# Close any running Chrome instances
logger.info("Closing any running Chrome instances...")
os.system("taskkill /f /im chrome.exe")

# Start Chrome with your profile and remote debugging
logger.info("Starting Chrome with your profile...")
chrome_process = subprocess.Popen([
    chrome_path,
    f"--user-data-dir={user_data_dir}",  # Point to the parent User Data directory
    f"--profile-directory={profile_name}",  # Specify which profile to use
    "--remote-debugging-port=9222",
    "--disable-blink-features=AutomationControlled"  # Try to avoid automation detection
])

# Wait for Chrome to start
logger.info("Waiting for Chrome to start...")
time.sleep(5)  # Increase wait time to ensure Chrome is fully loaded

# Connect to the running Chrome instance
logger.info("Connecting to running Chrome instance...")
browser = Browser(
    config=BrowserConfig(
        headless=False,
        # Connect to the running Chrome instance via CDP
        cdp_url="http://localhost:9222",
    )
)

async def run_task_with_retry(browser, task_description, max_retries=3, initial_wait=60, max_page_load_retries=5):
    """Run a task with retry logic for rate limits and page load failures"""
    retry_count = 0
    page_load_retries = 0
    
    while retry_count <= max_retries:
        try:
            # Configure the LLM with Gemini Flash 2.0
            llm = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash",  # This is Gemini Flash 2.0
                temperature=0.2,
                convert_system_message_to_human=True,
                google_api_key=os.getenv("GOOGLE_API_KEY")  # Get from environment
            )
            
            agent = Agent(
                task=task_description,
                llm=llm,
                browser=browser,
            )
            
            logger.info(f"Running task: {task_description}")
            
            # Set a timeout for the task
            try:
                await asyncio.wait_for(agent.run(), timeout=120)  # 2-minute timeout
                logger.info(f"Task completed successfully: {task_description}")
                return True
            except asyncio.TimeoutError:
                logger.error(f"Task timed out after 120 seconds: {task_description}")
                # If we're seeing page load failures, try refreshing the page
                if page_load_retries < max_page_load_retries:
                    page_load_retries += 1
                    logger.info(f"Attempting to refresh the page (attempt {page_load_retries}/{max_page_load_retries})...")
                    try:
                        # Try to navigate directly to LinkedIn again
                        await browser.goto("https://www.linkedin.com")
                        logger.info("Page refreshed successfully")
                        time.sleep(3)  # Wait for page to load
                        continue
                    except Exception as e:
                        logger.error(f"Error refreshing page: {e}")
                return False
            
        except Exception as e:
            logger.error(f"Error during task: {e}")
            if "429" in str(e) and retry_count < max_retries:
                retry_count += 1
                wait_time = initial_wait * (2 ** (retry_count - 1))  # Exponential backoff
                logger.info(f"Rate limit hit. Waiting {wait_time} seconds before retry {retry_count}/{max_retries}...")
                await asyncio.sleep(wait_time)
            elif "Page load failed" in str(e) and page_load_retries < max_page_load_retries:
                page_load_retries += 1
                logger.info(f"Page load failed. Attempting to refresh (attempt {page_load_retries}/{max_page_load_retries})...")
                try:
                    # Try to navigate directly to LinkedIn again
                    await browser.goto("https://www.linkedin.com")
                    logger.info("Page refreshed successfully")
                    time.sleep(3)  # Wait for page to load
                    continue
                except Exception as refresh_error:
                    logger.error(f"Error refreshing page: {refresh_error}")
            else:
                logger.error(f"Failed to complete task after {retry_count} retries: {task_description}")
                return False

async def main():
    try:
        # Combined task approach - simpler and might avoid some of the page load issues
        task = "Go to linkedin.com, then click on the My Network tab, find 5 people with more than 5 mutual connections, and send connection requests to them"
        await run_task_with_retry(browser, task, max_retries=3, initial_wait=60, max_page_load_retries=5)
        
        # Allow manual interaction before closing
        input("Press Enter to close the browser...")
    
    finally:
        # Clean up resources
        logger.info("Closing browser...")
        try:
            await browser.close()
        except Exception as e:
            logger.error(f"Error closing browser: {e}")
        
        # Also terminate the Chrome process we started
        logger.info("Terminating Chrome process...")
        try:
            chrome_process.terminate()
        except Exception as e:
            logger.error(f"Error terminating Chrome process: {e}")


if __name__ == '__main__':
    logger.info("Starting main function...")
    asyncio.run(main())
    logger.info("Main function completed.")
