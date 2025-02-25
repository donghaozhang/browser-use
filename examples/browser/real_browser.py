import os
import sys
from pathlib import Path
import logging
import tempfile

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

from browser_use.agent.views import ActionResult

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import asyncio

from langchain_openai import ChatOpenAI

from browser_use import Agent, Controller
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContext

from dotenv import load_dotenv
load_dotenv(dotenv_path="D:/AI_play/AI_Code/browser-use/.env")

# Print API key (with partial masking for security)
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    masked_key = api_key[:4] + "..." + api_key[-4:]
    logger.debug(f"API key loaded: {masked_key}")
else:
    logger.error("No API key found!")

# Create a temporary directory for the Chrome profile
temp_profile_dir = tempfile.mkdtemp()
logger.debug(f"Using temporary profile directory: {temp_profile_dir}")

# Configure the browser with minimal settings
logger.debug("Creating browser instance...")
browser = Browser(
    config=BrowserConfig(
        # Only use parameters we know are supported
        headless=False,
    )
)

async def main():
	logger.debug("Initializing agent...")
	agent = Agent(
		task='Go to notepad.online and write my Papa a quick letter',  # Use a service that doesn't require login
		llm=ChatOpenAI(model='gpt-4o'),
		browser=browser,
	)

	logger.debug("Running agent...")
	await agent.run()
	
	logger.debug("Closing browser...")
	await browser.close()

	input('Press Enter to close...')


if __name__ == '__main__':
	logger.debug("Starting main function...")
	asyncio.run(main())
	logger.debug("Main function completed.")
