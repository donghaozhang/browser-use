# LinkedIn Automation with Browser-Use

This directory contains scripts for automating LinkedIn networking tasks using the browser-use library.

## Files

- `linkedin_automation.py` - Main automation script that performs LinkedIn networking tasks
- `start_chrome_debug.py` - Helper script to start Chrome with debugging enabled
- `README_linkedin.md` - This documentation file

## Prerequisites

1. **Python Dependencies**: Make sure you have the required packages installed:
   ```bash
   pip install browser-use langchain-google-genai python-dotenv psutil
   ```

2. **Google API Key**: You need a Google Gemini API key. Add it to your `.env` file:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

3. **Chrome Browser**: Google Chrome must be installed at the default location:
   ```
   C:\Program Files\Google\Chrome\Application\chrome.exe
   ```

## Quick Start

### Method 1: Automated Setup (Recommended)

1. **Start Chrome with debugging**:
   ```bash
   cd examples/browser
   python start_chrome_debug.py
   ```
   
2. **In the Chrome window that opens**:
   - Navigate to linkedin.com
   - Log in with your LinkedIn account
   - Leave this Chrome window open

3. **Run the automation**:
   ```bash
   python linkedin_automation.py
   ```

### Method 2: Manual Setup

1. **Manually start Chrome with debugging**:
   ```bash
   "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\Users\zdhpe\AppData\Local\Google\Chrome\User Data" --profile-directory="Default"
   ```

2. **Log into LinkedIn** in that Chrome window

3. **Run the automation**:
   ```bash
   python linkedin_automation.py
   ```

## What the Automation Does

The LinkedIn automation script will:

1. Connect to your Chrome browser instance
2. Navigate to LinkedIn.com
3. Go to the "My Network" tab
4. Look for people with 5+ mutual connections
5. Send personalized connection requests to 5 such people
6. Add personalized notes mentioning mutual connections

## Configuration

### Customizing the Task

You can modify the automation task by editing the `task` variable in `linkedin_automation.py`:

```python
task = """
Your custom LinkedIn automation task here...
"""
```

### Adjusting Chrome Settings

If you need to modify Chrome startup parameters, edit the `chrome_args` list in `start_chrome_debug.py`.

### Changing the LLM Model

You can change the AI model used for automation:

```python
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-exp",  # Change this to other models
    temperature=0.1,
    google_api_key=api_key
)
```

## Troubleshooting

### Chrome Won't Start
- Make sure Chrome is installed at the default location
- Check that no other Chrome instances are running
- Try running the `start_chrome_debug.py` script as administrator

### Connection Failed
- Ensure Chrome is running with `--remote-debugging-port=9222`
- Check that port 9222 is not blocked by firewall
- Verify Chrome debug interface at: http://localhost:9222

### API Key Issues
- Make sure your `.env` file is in the project root
- Verify your Google API key is valid and has Gemini access
- Check that the environment variable name matches: `GOOGLE_API_KEY`

### LinkedIn Login Issues
- Make sure you're logged into LinkedIn in the Chrome debug instance
- Check that your LinkedIn account is not restricted
- Ensure you're using your regular Chrome profile with saved login

## Safety and Ethics

⚠️ **Important Considerations**:

- **Rate Limiting**: The script includes reasonable delays to avoid overwhelming LinkedIn's servers
- **LinkedIn Terms**: Make sure your automation complies with LinkedIn's Terms of Service
- **Personal Use**: This is intended for personal networking, not spam or bulk operations
- **Monitoring**: Always monitor the automation to ensure it behaves as expected

## Advanced Usage

### Running with Different Profiles

To use a different Chrome profile, modify the `profile_directory` in `start_chrome_debug.py`:

```python
profile_directory = "Profile 1"  # or "Profile 2", etc.
```

### Extending the Automation

You can extend the automation by:

1. Adding more complex LinkedIn tasks
2. Implementing data collection features
3. Adding integration with CRM systems
4. Creating reporting and analytics

### Debugging

To debug the automation:

1. Set logging level to DEBUG in the scripts
2. Use Chrome DevTools (F12) to inspect the page
3. Check the browser-use logs for detailed execution steps
4. Monitor the Chrome debug interface at http://localhost:9222

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review the browser-use documentation
3. Ensure all dependencies are correctly installed
4. Verify your Chrome and profile setup

## License

This automation script is provided as-is for educational and personal use. Please ensure compliance with LinkedIn's Terms of Service and applicable laws. 