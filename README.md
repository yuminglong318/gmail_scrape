## Open the Guest Browser using open_browser.cmd

! The chrome must be in environmental path

chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\selenium\ChromeProfile" --guest

## Connects the Guest Browser with the Selenium Webdriver

options = Options()

options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

driver = webdriver.Chrome(options=options)
