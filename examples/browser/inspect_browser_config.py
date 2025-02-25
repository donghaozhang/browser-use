from browser_use.browser.browser import BrowserConfig
import inspect

def main():
    # Print the signature of BrowserConfig.__init__
    print(f"BrowserConfig.__init__ signature: {inspect.signature(BrowserConfig.__init__)}")
    
    # Print the docstring
    print(f"\nBrowserConfig.__init__ docstring: {BrowserConfig.__init__.__doc__}")
    
    # Try to create a BrowserConfig with different parameters
    try:
        config = BrowserConfig(
            headless=False,
            chrome_instance_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        )
        print("\nSuccessfully created BrowserConfig with headless and chrome_instance_path")
    except Exception as e:
        print(f"\nError creating BrowserConfig: {e}")
    
    # Print all attributes of BrowserConfig
    config = BrowserConfig()
    print("\nBrowserConfig attributes:")
    for attr in dir(config):
        if not attr.startswith('_'):
            print(f"  - {attr}: {getattr(config, attr)}")

if __name__ == "__main__":
    main() 