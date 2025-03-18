import os
import sys
from pathlib import Path
import logging
import subprocess
import time
import json
import random
from langchain_openai import ChatOpenAI

# Set up logging with INFO level instead of DEBUG to reduce output
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Reduce logging from other modules
logging.getLogger('urllib3').setLevel(logging.WARNING)
logging.getLogger('browser_use').setLevel(logging.INFO)

# Try to import the required modules, install if missing
try:
    from langchain_openai import ChatOpenAI
except ImportError:
    logger.info("Installing missing langchain-openai package...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "langchain-openai"])
    from langchain_openai import ChatOpenAI

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
from browser_use.browser.context import BrowserContext, BrowserContextConfig

from dotenv import load_dotenv
load_dotenv(dotenv_path="D:/AI_play/AI_Code/browser-use/.env")



# Print API key (with partial masking for security)
gemini_api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
if gemini_api_key:
    masked_key = gemini_api_key[:4] + "..." + gemini_api_key[-4:]
    logger.info(f"Gemini API key loaded: {masked_key}")
    # Ensure it's available as GOOGLE_API_KEY for the library
    os.environ["GOOGLE_API_KEY"] = gemini_api_key
else:
    logger.error("No Gemini API key found in environment variables!")
    logger.info("Please add GOOGLE_API_KEY or GEMINI_API_KEY to your .env file")
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
    # "--disable-blink-features=AutomationControlled",  # Try to avoid automation detection
    "--window-size=1280,1100",  # Set explicit window size
    "--start-maximized"  # Ensure window is maximized
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
        # Set explicit window size in the browser config
        new_context_config=BrowserContextConfig(
            browser_window_size={'width': 1280, 'height': 1100},
            no_viewport=False
        )
    )
)

# Add a delay to ensure the browser is fully initialized
logger.info("Waiting for browser to fully initialize...")
time.sleep(3)

async def run_task_with_retry(browser, task_description, max_retries=3, initial_wait=60, max_page_load_retries=5):
    """Run a task with retry logic for rate limits and page load failures"""
    retry_count = 0
    page_load_retries = 0
    
    while retry_count <= max_retries:
        try:
            # Configure the LLM with Gemini Flash 2.0
            # llm = ChatOpenAI(model='gpt-4o')
            
            llm = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash-exp",  # This is Gemini Flash 2.0
                temperature=0.2,
                convert_system_message_to_human=True,
                google_api_key=os.getenv("GEMINI_API_KEY")  # Get from environment
            )

            agent = Agent(
                task=task_description,
                llm=llm,
                browser=browser,
                use_vision=True,
            )
            
            logger.info(f"Running task: {task_description}")
            
            # Set a timeout for the task
            try:
                await asyncio.wait_for(agent.run(max_steps=10), timeout=120)  # 2-minute timeout
                logger.info(f"Task completed successfully: {task_description}")
                return True
            except asyncio.TimeoutError:
                logger.error(f"Task timed out after 120 seconds: {task_description}")
                # If we're seeing page load failures, try refreshing the page
                if page_load_retries < max_page_load_retries:
                    page_load_retries += 1
                    logger.info(f"Attempting to refresh the page (attempt {page_load_retries}/{max_page_load_retries})...")
                    try:
                        # Try to navigate directly to the target site again
                        await browser.goto("https://tongyi.aliyun.com/read/")
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
                    # Try to navigate directly to the target site again
                    await browser.goto("https://tongyi.aliyun.com/read/")
                    logger.info("Page refreshed successfully")
                    time.sleep(3)  # Wait for page to load
                    continue
                except Exception as refresh_error:
                    logger.error(f"Error refreshing page: {refresh_error}")
            elif "Cannot take screenshot with 0 width" in str(e) and page_load_retries < max_page_load_retries:
                page_load_retries += 1
                logger.info(f"Screenshot error. Attempting to resize browser window (attempt {page_load_retries}/{max_page_load_retries})...")
                try:
                    # Try to resize the browser window
                    page = await browser.get_current_page()
                    await page.set_viewport_size({"width": 1280, "height": 1100})
                    # Try to navigate directly to the target site again
                    await browser.goto("https://tongyi.aliyun.com/read/")
                    logger.info("Browser window resized and page refreshed successfully")
                    time.sleep(3)  # Wait for page to load
                    continue
                except Exception as resize_error:
                    logger.error(f"Error resizing browser window: {resize_error}")
            else:
                logger.error(f"Failed to complete task after {retry_count} retries: {task_description}")
                return False

async def main():
    try:
        # Combined task approach - simpler and might avoid some of the page load issues
        task = "1 Go to https://tongyi.aliyun.com/read/ 2 分别点击前三个文章 3 点击 右上角 导出 3 勾选导读的 取消原文的勾选 4 文档格式然后选md格式 5进行导出 5确认他在下载文件夹"
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
