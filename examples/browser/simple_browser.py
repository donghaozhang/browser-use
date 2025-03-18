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
    
    # Create a browser context first
    logger.debug("Creating browser context...")
    context = await browser.new_context()
    
    try:
        # Create a new tab using the context.create_new_tab() method
        logger.debug("Creating new tab...")
        await context.create_new_tab()
        
        # Get the current page/tab
        session = await context.get_session()
        page = await context.get_current_page()
        
        logger.debug("Navigating to Google...")
        await page.goto("https://www.google.com")
        
        logger.debug("Waiting for 5 seconds...")
        await asyncio.sleep(5)
    finally:
        # Close the context first
        logger.debug("Closing context...")
        await context.close()
        
        # Then close the browser
        logger.debug("Closing browser...")
        await browser.close()
    
    logger.debug("Done!")

if __name__ == "__main__":
    asyncio.run(main()) 