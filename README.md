# 🚀 python_Bale_Crawler

**`python_Bale_Crawler`** is a Python script that uses **Selenium** to scrape messages from **Bale Messenger channels**.  
This tool allows you to **extract all messages from a Bale channel** and save them in **JSON and CSV formats**.

---

## 📌 **Features**
✅ **Extracts all messages from a Bale channel**  
✅ **Supports `Chrome` and `Edge` browsers**  
✅ **Uses browser profile for automatic login**  
✅ **Stops scrolling automatically when "Channel Created" message is found**  
✅ **Saves messages in `JSON` and `CSV` formats**  
✅ **No manual intervention required for scrolling**  

---

## 🔧 **Requirements**
Before running this project, make sure you have the following installed:

- **Python 3.x**
- **Google Chrome or Microsoft Edge**
- **Chromedriver / Edgedriver (Automatically managed by WebDriver Manager)**
- **Selenium** library

You can install the required dependencies using:

```sh
pip install selenium webdriver-manager pandas

📥 Installation

    Clone this repository:

git clone https://github.com/YOUR_USERNAME/python_Bale_Crawler.git
cd python_Bale_Crawler

Set up your Python environment:

pip install -r requirements.txt

Run the script:

    python main.py

🚀 How to Use
1️⃣ Run the Crawler

To run the crawler, use the following example:

from bale_crawler import BaleCrawler

crawler = BaleCrawler(
    channel_url="https://web.bale.ai/chat?uid=",
    browser="edge",  # Options: "edge" or "chrome"
    user_data_dir=r"",  # Optional
    profile_directory="Default"  # Optional
)

crawler.run()

2️⃣ Output Files

After execution, the extracted messages will be saved in:

    bale_channel_messages.json
    bale_channel_messages.csv

⚙️ Customization
Change Browser

Set browser="chrome" or browser="edge" when initializing BaleCrawler.
Use Browser Profile (for Auto Login)

To keep your login session:

    Set user_data_dir to the path of your browser’s profile.
    Set profile_directory to the correct profile name.

Example for Edge:

user_data_dir=r""
profile_directory="Default"

Example for Chrome:

user_data_dir=r""
profile_directory="Default"

🛠 Troubleshooting
1️⃣ WebDriver Issues

If WebDriver is not found, update it using:

pip install --upgrade webdriver-manager

2️⃣ Bale Login Issues

If the script says "You are not logged in", make sure you:

    Open Bale Web (https://web.bale.ai/) in your browser.
    Login manually.
    Use the correct browser profile.

3️⃣ No Messages Extracted

    Ensure that the CSS selectors for messages (Text_text) and scrolling container (Scroller_scroller) haven't changed.
    Increase SCROLL_PAUSE_TIME in the script if messages take time to load.

📜 License

This project is licensed under the MIT License.
🤝 Contributing

If you’d like to contribute:

    Fork the repository
    Create a new branch
    Submit a pull request (PR)
