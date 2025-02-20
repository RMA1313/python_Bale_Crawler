import json
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

class BaleCrawler:
    def __init__(self, channel_url, browser="edge", user_data_dir=None, profile_directory=None):
        self.channel_url = channel_url
        self.browser = browser.lower()
        self.user_data_dir = user_data_dir
        self.profile_directory = profile_directory
        self.driver = None
        self.scroll_pause_time = 2
        self.max_scrolls = 300
        self.output_file_json = "bale_channel_messages.json"
        self.output_file_csv = "bale_channel_messages.csv"

    def _setup_browser(self):
        """Initializes the WebDriver based on the selected browser."""
        if self.browser == "edge":
            options = EdgeOptions()
            service = EdgeService(EdgeChromiumDriverManager().install())
        elif self.browser == "chrome":
            options = ChromeOptions()
            service = ChromeService(ChromeDriverManager().install())
        else:
            raise ValueError("Unsupported browser. Use 'edge' or 'chrome'.")

        options.add_argument("--start-maximized")
        options.add_argument("--disable-gpu")
        options.add_argument("--log-level=3")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        # ✅ Set user profile if provided
        if self.user_data_dir:
            options.add_argument(f"user-data-dir={self.user_data_dir}")
        if self.profile_directory:
            options.add_argument(f"--profile-directory={self.profile_directory}")

        self.driver = webdriver.Chrome(service=service, options=options) if self.browser == "chrome" else webdriver.Edge(service=service, options=options)

    def _scroll_to_load_messages(self):
        """Scrolls up until all messages are loaded or 'کانال ایجاد شد' is found."""
        try:
            scroller_container = self.driver.find_element(By.XPATH, "//div[starts-with(@class, 'Scroller_scroller')]")
            print("[SUCCESS] Found chat scroller container.")
        except Exception as e:
            print(f"[ERROR] Could not locate chat scroller container: {e}")
            self.driver.quit()
            return

        last_scroll_position = self.driver.execute_script("return arguments[0].scrollTop;", scroller_container)
        scroll_count = 0

        while scroll_count < self.max_scrolls:
            # ✅ Check if "کانال ایجاد شد" message exists
            service_messages = self.driver.find_elements(By.XPATH, "//p[contains(@class, 'ServiceMessage_Content')]")
            for msg in service_messages:
                if "کانال ایجاد شد" in msg.text:
                    print("[INFO] Found 'کانال ایجاد شد' - No more scrolling needed.")
                return

            # ✅ Scroll up
            self.driver.execute_script("arguments[0].scrollTop -= 9000;", scroller_container)
            time.sleep(self.scroll_pause_time)

            # ✅ Check if scrolling has stopped
            new_scroll_position = self.driver.execute_script("return arguments[0].scrollTop;", scroller_container)
            if new_scroll_position == last_scroll_position:
                print("[INFO] No more messages to load (scroll position unchanged).")
                break

            last_scroll_position = new_scroll_position
            scroll_count += 1

        print(f"[INFO] Finished scrolling after {scroll_count} scrolls.")

    def _extract_messages(self):
        """Extracts only the messages from the chat (no timestamps)."""
        messages = []
        message_elements = self.driver.find_elements(By.XPATH, "//div[starts-with(@class, 'Text_text')]")

        print(f"[DEBUG] Found {len(message_elements)} messages.")

        for msg in message_elements:
            try:
                spans = msg.find_elements(By.TAG_NAME, "span")
                full_text = " ".join([span.text.strip() for span in spans if span.text.strip()])

                if full_text and full_text not in messages:
                    messages.append({"text": full_text})

            except Exception as e:
                print(f"[ERROR] Failed to extract message: {e}")

        return messages

    def _save_messages(self, messages):
        """Saves extracted messages to JSON and CSV."""
        with open(self.output_file_json, "w", encoding="utf-8") as f:
            json.dump(messages, f, ensure_ascii=False, indent=4)

        df = pd.DataFrame(messages)
        df.to_csv(self.output_file_csv, index=False, encoding="utf-8")

        print(f"[INFO] Messages saved to:\n- {self.output_file_json}\n- {self.output_file_csv}")

    def run(self):
        """Runs the full crawling process."""
        self._setup_browser()

        print("[INFO] Opening channel page...")
        self.driver.get(self.channel_url)
        time.sleep(20)

        if "login" in self.driver.current_url:
            print("[ERROR] You are not logged into Bale. Please log in manually and re-run the script.")
            self.driver.quit()
            return

        print(f"[SUCCESS] Channel page loaded: {self.driver.current_url}")

        self._scroll_to_load_messages()
        messages = self._extract_messages()
        self._save_messages(messages)

        self.driver.quit()
        print(f"[SUCCESS] Total messages extracted: {len(messages)}")

