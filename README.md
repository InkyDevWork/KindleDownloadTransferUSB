# Kindle Book Downloader

This is a script I quickly put together using ChatGPT that automates the downloading of Kindle books via Amazon's 'Download & Transfer via USB' Feature before it goes away.
Summary: You need to be already logged in befopre starting. The URL & number of pages are hard coded and need to be updated before running. 
There are pauses in the script to mimic human like browser & avoid being blocked (A page of 25 books takes aroung 5 min).

## Prerequisites

### 1. Install Playwright
Ensure you have Python installed, then install Playwright:
```sh
pip install playwright
```

### 2. Install Chrome Driver (Remote Debugging Mode)
Launch Chrome with remote debugging enabled:
```sh
chrome --remote-debugging-port=9222 --user-data-dir="C:\chrome-remote"
```
**For Mac/Linux:**
```sh
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir="~/chrome-remote"
```
Ensure **Google Chrome** is installed and accessible from the command line.

### 3. Verify Remote Debugging
Check if Chrome is running in debug mode:
```sh
curl http://localhost:9222/json/version
```
If this returns a JSON response, Chrome is correctly configured.

## Usage

### 1. Run the Script
Once Chrome is running in debugging mode, execute the script:
```sh
python AmazonUSBDownload.py
```

### 2. Download Location
All downloaded Kindle books will be saved in the `KindleDownloads` folder within the script directory.

### 🚀 **3. Pagination Handling (Important!)** 🚀

**The script assumes Amazon UK (`amazon.co.uk`) and the number of pages is hardcoded - !!UPDATE MANUALLY BEFORE RUNNING!!**

### 4. Login Requirement
The script assumes you are **already logged into your Amazon account** in the Chrome instance running with remote debugging mode. Ensure you log in before starting the script.

## License
This script is for personal use only. Ensure compliance with Amazon's terms of service before using.

---
For any questions or improvements, feel free to contribute or report issues!

