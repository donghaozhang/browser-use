import os
import sys
import logging
import asyncio
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Add the parent directory to the path to import browser_use
sys.path.append(str(Path(__file__).parent.parent.parent))

from browser_use import Agent, Browser, BrowserConfig
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def main():
    """LinkedIn automation using browser-use with your existing Chrome profile"""
    
    # Check for API key
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        logger.error("Please set GOOGLE_API_KEY or GEMINI_API_KEY in your .env file")
        return
    
    logger.info("Starting LinkedIn automation...")
    
    try:
        # Configure the browser to use your existing Chrome profile
        # This approach connects to Chrome that you manually start with debugging enabled
        browser_config = BrowserConfig(
            headless=False,
            # Connect to Chrome running with --remote-debugging-port=9222
            cdp_url="http://localhost:9222"
        )
        
        # Create browser instance
        browser = Browser(config=browser_config)
        
        # Configure the LLM
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            temperature=0.1,
            google_api_key=api_key
        )
        
        # Define the LinkedIn automation task
        task = """
        Go to linkedin.com and perform the following steps:
        1. Navigate to the My Network tab
        2. Look for people with 5+ mutual connections
        3. Send connection requests to 5 such people
        4. For each request, add a personalized note mentioning the mutual connections
        """
        
        # Create the agent
        agent = Agent(
            task=task,
            llm=llm,
            browser=browser
        )
        
        logger.info("Task: LinkedIn networking automation")
        logger.info("Make sure Chrome is running with: chrome.exe --remote-debugging-port=9222")
        logger.info("And that you're logged into LinkedIn in that Chrome instance")
        
        # Run the automation
        result = await agent.run(max_steps=25)
        
        logger.info("LinkedIn automation completed!")
        logger.info(f"Result: {result}")
        
    except Exception as e:
        logger.error(f"Error during automation: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Clean up
        try:
            await browser.close()
            logger.info("Browser connection closed")
        except:
            pass

def print_instructions():
    """Print instructions for running the script"""
    print("""
LinkedIn Automation Setup Instructions:
=====================================

1. First, start Chrome with debugging enabled:
   Open Command Prompt or PowerShell and run:
   
   "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\\Users\\zdhpe\\AppData\\Local\\Google\\Chrome\\User Data" --profile-directory="Default"
   
2. In that Chrome window:
   - Go to linkedin.com
   - Make sure you're logged in with your account
   - Leave this Chrome window open
   
3. Then run this script:
   python linkedin_automation.py
   
4. The script will connect to your Chrome instance and perform the automation

Note: Make sure your .env file contains your Google API key:
GOOGLE_API_KEY=your_api_key_here
""")

if __name__ == "__main__":
    print_instructions()
    
    # Ask user if they want to proceed
    response = input("\nHave you started Chrome with debugging and logged into LinkedIn? (y/n): ")
    
    if response.lower() in ['y', 'yes']:
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            logger.info("Automation stopped by user")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
    else:
        print("Please follow the setup instructions above and try again.") 