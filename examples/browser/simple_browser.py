import asyncio
import logging
from browser_use.browser.browser import Browser
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv(dotenv_path="D:/AI_play/AI_Code/browser-use/.env")

async def main():
    logger.debug("Creating browser instance...")
    browser = Browser()
    
    # Let's try to directly create a page without using context
    logger.debug("Creating new page...")
    page = await browser.page()  # Try this method instead
    
    logger.debug("Navigating to Google...")
    await page.goto("https://www.google.com")
    
    logger.debug("Waiting for 5 seconds...")
    await asyncio.sleep(5)
    
    logger.debug("Closing browser...")
    await browser.close()
    
    logger.debug("Done!")

if __name__ == "__main__":
    asyncio.run(main()) 