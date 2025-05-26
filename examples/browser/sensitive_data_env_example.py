"""
@file purpose: Demonstrates secure handling of sensitive data using environment variables
This example shows the recommended approach of using environment variables for credentials
instead of hardcoding them in the script.
"""

import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from dotenv import load_dotenv

load_dotenv()

from langchain_openai import ChatOpenAI
from browser_use import Agent
from browser_use.browser import BrowserProfile, BrowserSession


# Find Chrome executable on Windows
def find_chrome_path():
	"""Find Chrome executable path on Windows"""
	common_paths = [
		r'C:\Program Files\Google\Chrome\Application\chrome.exe',
		r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
		os.path.expanduser(r'~\AppData\Local\Google\Chrome\Application\chrome.exe'),
	]
	
	for path in common_paths:
		if os.path.exists(path):
			return path
	
	# If not found, return None to use default browser
	return None


async def main():
	# Check for required environment variables
	google_email = os.getenv('GOOGLE_EMAIL')
	google_password = os.getenv('GOOGLE_PASSWORD')
	
	if not google_email or not google_password:
		print("❌ Missing required environment variables!")
		print("Please set the following in your .env file:")
		print("GOOGLE_EMAIL=your-email@gmail.com")
		print("GOOGLE_PASSWORD=your-password")
		print()
		print("Or set them as environment variables:")
		print("export GOOGLE_EMAIL=your-email@gmail.com")
		print("export GOOGLE_PASSWORD=your-password")
		return

	# Initialize the model
	llm = ChatOpenAI(
		model='gpt-4o',
		temperature=0.0,
	)

	# Domain-specific sensitive data using environment variables
	# The model will only see the placeholder keys (x_email, x_password) but never the actual values
	sensitive_data = {
		'https://*.google.com': {
			'x_email': google_email,
			'x_password': google_password
		}
	}

	# Find Chrome path
	chrome_path = find_chrome_path()

	# Configure browser profile
	browser_profile = BrowserProfile(
		browser_binary_path=chrome_path,
		user_data_dir='~/.config/browseruse/profiles/env_demo',  # Separate profile for this demo
	)

	# Configure browser session with restricted domains for security
	browser_session = BrowserSession(
		browser_profile=browser_profile,
		allowed_domains=[
			'https://*.google.com',  # Only allow Google domains
			'https://accounts.google.com',  # Explicitly include Google accounts
		]
	)

	# Task that references the sensitive data using placeholder names
	# task = '''
	# 1. Go to docs.google.com and log in using x_email and x_password if needed.
	# 2. create a doc named test".
	# '''

    # no successful task
	# task = '''
	# 1. Go to x.com and log in using x_email and x_password if needed.
	# 2. post a message test".
	# '''

    # no successful task
	task = '''
	1. Go to linkedin.com and 
	2. check notification.
	'''

	# Create agent with sensitive data
	agent = Agent(
		task=task,
		llm=llm,
		sensitive_data=sensitive_data,
		browser_session=browser_session,
	)

	print("🔐 Starting agent with environment-based sensitive data protection...")
	print(f"📧 Using email: {google_email[:3]}***@{google_email.split('@')[1] if '@' in google_email else 'hidden'}")
	print("🔒 Password is completely hidden from the AI model")
	print("🌐 Browser restricted to Google domains only")
	print()

	try:
		await agent.run()
		print("✅ Task completed successfully!")
	except Exception as e:
		print(f"❌ Error occurred: {e}")
	finally:
		await browser_session.close()

	input('Press Enter to close...')


if __name__ == '__main__':
	print("🔐 SECURE SENSITIVE DATA EXAMPLE")
	print("=" * 40)
	print("This example demonstrates the recommended approach:")
	print("✅ Using environment variables for credentials")
	print("✅ Domain restriction for security")
	print("✅ Separate browser profile")
	print("✅ Credential validation before execution")
	print()
	
	asyncio.run(main()) 