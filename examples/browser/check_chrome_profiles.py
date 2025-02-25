import os
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def check_chrome_profiles():
    """Check all Chrome profiles and look for specific email addresses."""
    # Define the path to Chrome user data directory
    chrome_user_data_dir = r"C:\Users\zdhpe\AppData\Local\Google\Chrome\User Data"
    
    if not os.path.exists(chrome_user_data_dir):
        logger.error(f"Chrome user data directory not found: {chrome_user_data_dir}")
        return
    
    logger.info(f"Checking Chrome profiles in {chrome_user_data_dir}")
    
    # List to store profile information
    profiles = []
    
    # Check each profile directory
    for item in os.listdir(chrome_user_data_dir):
        if item.startswith("Profile ") or item == "Default":
            profile_dir = os.path.join(chrome_user_data_dir, item)
            preferences_file = os.path.join(profile_dir, "Preferences")
            
            if os.path.exists(preferences_file):
                try:
                    with open(preferences_file, 'r', encoding='utf-8') as f:
                        prefs = json.load(f)
                        
                        # Extract profile information
                        profile_name = prefs.get('profile', {}).get('name', 'Unknown')
                        
                        # Extract email (might be in different locations)
                        email = "Unknown"
                        account_info = prefs.get('account_info', [])
                        if account_info and len(account_info) > 0:
                            email = account_info[0].get('email', 'Unknown')
                        
                        # Check if this is the target profile
                        is_target = 'zdhpeter1991@gmail.com' in email
                        
                        # Add to profiles list
                        profiles.append({
                            'directory': item,
                            'path': profile_dir,
                            'name': profile_name,
                            'email': email,
                            'is_target': is_target
                        })
                        
                        # Log profile information
                        logger.info(f"Found profile: {item} - {profile_name} - {email}")
                        
                        if is_target:
                            logger.info(f"*** TARGET PROFILE FOUND: {item} - {profile_name} - {email} ***")
                
                except Exception as e:
                    logger.error(f"Error reading preferences for {item}: {e}")
    
    # Summary
    logger.info("\n--- Profile Summary ---")
    logger.info(f"Total profiles found: {len(profiles)}")
    
    target_profile = next((p for p in profiles if p['is_target']), None)
    if target_profile:
        logger.info(f"Target profile (zdhpeter1991@gmail.com) found:")
        logger.info(f"  Directory: {target_profile['directory']}")
        logger.info(f"  Path: {target_profile['path']}")
        logger.info(f"  Name: {target_profile['name']}")
    else:
        logger.info("Target profile (zdhpeter1991@gmail.com) NOT found.")
        logger.info("Available profiles:")
        for p in profiles:
            logger.info(f"  {p['directory']} - {p['name']} - {p['email']}")

if __name__ == "__main__":
    check_chrome_profiles() 