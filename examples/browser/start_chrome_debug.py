import os
import sys
import subprocess
import time
import psutil
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def kill_chrome_processes():
    """Kill all Chrome processes to ensure clean start"""
    killed_count = 0
    try:
        for proc in psutil.process_iter(['pid', 'name']):
            if 'chrome' in proc.info['name'].lower():
                try:
                    proc.kill()
                    killed_count += 1
                    logger.info(f"Killed Chrome process {proc.info['pid']}")
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
    except Exception as e:
        logger.warning(f"Error killing Chrome processes: {e}")
    
    if killed_count > 0:
        logger.info(f"Killed {killed_count} Chrome processes")
        time.sleep(2)  # Wait for processes to fully terminate

def start_chrome_with_debugging():
    """Start Chrome with debugging enabled using your existing profile"""
    
    # Chrome executable path
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    
    # Your Chrome user data directory and profile
    user_data_dir = r"C:\Users\zdhpe\AppData\Local\Google\Chrome\User Data"
    profile_directory = "Default"  # Your profile with zdhpeter1991@gmail.com
    
    # Check if Chrome executable exists
    if not os.path.exists(chrome_path):
        logger.error(f"Chrome not found at: {chrome_path}")
        logger.info("Please update the chrome_path variable with your Chrome installation path")
        return None
    
    # Kill any existing Chrome processes
    logger.info("Closing any running Chrome instances...")
    kill_chrome_processes()
    
    # Chrome command line arguments
    chrome_args = [
        chrome_path,
        f"--user-data-dir={user_data_dir}",
        f"--profile-directory={profile_directory}",
        "--remote-debugging-port=9222",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-background-timer-throttling",
        "--disable-backgrounding-occluded-windows",
        "--disable-renderer-backgrounding",
        "--disable-features=TranslateUI",
        "--disable-web-security",  # Sometimes needed for automation
        "--disable-features=VizDisplayCompositor",  # Can help with stability
    ]
    
    logger.info(f"Starting Chrome with profile: {profile_directory}")
    logger.info(f"Debug port: 9222")
    
    try:
        # Start Chrome process
        process = subprocess.Popen(
            chrome_args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == "win32" else 0
        )
        
        logger.info(f"Chrome started with PID: {process.pid}")
        logger.info("Chrome is starting up...")
        
        # Wait a bit for Chrome to initialize
        time.sleep(3)
        
        # Check if process is still running
        if process.poll() is None:
            logger.info("✅ Chrome is running successfully!")
            logger.info("🌐 You can now navigate to LinkedIn and log in")
            logger.info("🤖 After logging in, run: python linkedin_automation.py")
            return process
        else:
            logger.error("❌ Chrome process terminated unexpectedly")
            stdout, stderr = process.communicate()
            if stderr:
                logger.error(f"Chrome error: {stderr.decode()}")
            return None
            
    except Exception as e:
        logger.error(f"Failed to start Chrome: {e}")
        return None

def main():
    """Main function to start Chrome with debugging"""
    print("""
Chrome Debug Launcher for LinkedIn Automation
============================================

This script will:
1. Close any running Chrome instances
2. Start Chrome with debugging enabled
3. Use your existing Chrome profile (with saved LinkedIn login)
4. Enable remote debugging on port 9222

After Chrome starts:
- Navigate to linkedin.com
- Make sure you're logged in
- Then run: python linkedin_automation.py
""")
    
    response = input("Start Chrome with debugging? (y/n): ")
    
    if response.lower() in ['y', 'yes']:
        process = start_chrome_with_debugging()
        
        if process:
            try:
                print("\n" + "="*50)
                print("Chrome is running with debugging enabled!")
                print("Debug URL: http://localhost:9222")
                print("="*50)
                print("\nNext steps:")
                print("1. Go to linkedin.com in the Chrome window")
                print("2. Make sure you're logged in")
                print("3. Run: python linkedin_automation.py")
                print("\nPress Ctrl+C to stop Chrome and exit")
                
                # Keep the script running so Chrome stays open
                while True:
                    time.sleep(1)
                    if process.poll() is not None:
                        logger.info("Chrome process ended")
                        break
                        
            except KeyboardInterrupt:
                logger.info("Stopping Chrome...")
                try:
                    process.terminate()
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    logger.warning("Force killing Chrome...")
                    process.kill()
                logger.info("Chrome stopped")
        else:
            logger.error("Failed to start Chrome")
    else:
        print("Chrome not started. Run this script again when ready.")

if __name__ == "__main__":
    main() 