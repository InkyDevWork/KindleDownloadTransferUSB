import os
import time
import requests
from playwright.sync_api import sync_playwright

BASE_URL = "https://www.amazon.co.uk/hz/mycd/digital-console/contentlist/booksAll/dateDsc/?pageNumber={}"  # UPDATE HERE
DOWNLOAD_FOLDER = os.path.join(os.getcwd(), "KindleDownloads")  # Save downloads in this folder

def download_books():
    with sync_playwright() as p:
        #browser = p.chromium.connect_over_cdp("http://localhost:9222", timeout=0)
        browser = p.chromium.connect_over_cdp("ws://localhost:9222/devtools/browser/0bfbe1ce-9fb0-4770-93c6-b3542fcc954a", timeout=0)
        context = browser.contexts[0]
        page = context.new_page()

        for page_number in range(1, 18):  # UPDATE HERE Loop through pages 1 to 17
            page.goto(BASE_URL.format(page_number))
            time.sleep(10)

            books = page.query_selector_all('td')
            if not books:
                print(f"No books found on page {page_number}!")
                continue

            for book in books:
                try:
                    title = book.inner_text().strip().split("\n")[0]  # Extract book title
                    print(f"Downloading: {title}")

                    # Locate the input checkbox element
                    input_element = book.query_selector('input[type="checkbox"]')

                    if input_element:
                        input_id = input_element.get_attribute("id")  # Get the full ID (e.g., "B0CWCRS5RN:KindleEBook")
                        asin = input_id.split(":")[0] if input_id else "UNKNOWN"  # Extract ASIN
                        print(f"ASIN: {asin}")

                    more_actions_btn = book.query_selector("[class^='Dropdown-module_container__']")
                    if more_actions_btn:
                        more_actions_btn.click()
                        time.sleep(2)  # Human-like delay

                        usb_option = book.query_selector("span:text('Download & transfer via USB')")
                        if usb_option:
                            usb_option.click()
                            time.sleep(2)

                            kindle_selector = f'ul[id="download_and_transfer_list_{asin}"] input[type="radio"]'
                            kindle_radio = page.query_selector(kindle_selector)
                            if kindle_radio:
                                kindle_radio.click()
                                time.sleep(1)

                            # Listen for the download event
                            with page.expect_download() as download_info:
                                parent_div_selector = f'div[id="DOWNLOAD_AND_TRANSFER_DIALOG_{asin}"]'
                                parent_div = page.query_selector(parent_div_selector)

                                if parent_div:
                                    download_btn = parent_div.query_selector('div[id$="_CONFIRM"]')
                                    if download_btn:
                                        download_btn.click()
                                        time.sleep(3)

                                    # Save the downloaded file
                                    download = download_info.value
                                    download_path = os.path.join(DOWNLOAD_FOLDER, download.suggested_filename)
                                    download.save_as(download_path)
                                    print(f"Downloaded: {download_path}")

                                    # Close the modal by clicking the notification-close span
                                    close_modal = page.query_selector('span#notification-close')
                                    if close_modal:
                                        close_modal.click()
                                        time.sleep(2)  # Short delay after closing
                except Exception as e:
                    print(f"Error processing book: {e}")

        browser.close()

download_books()
