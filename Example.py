import BaleCrawler
"""
This script initializes and runs a BaleCrawler instance to scrape data from a specified Bale chat channel.
Classes:
    BaleCrawler: A class from the BaleCrawler module used to interact with Bale chat channels.
Usage:
    The script sets up a BaleCrawler instance with the following parameters:
    - channel_url: The URL of the Bale chat channel to scrape.
    - browser: The browser to use for scraping ("chrome" or "edge").
    - user_data_dir: The directory where the browser's user data is stored.
    - profile_directory: The specific profile directory within the user data directory.
    After setting up the instance, the script calls the `run` method to start the scraping process.
Example:
        browser="edge",
"""

crawler = BaleCrawler.BaleCrawler(
    channel_url="",
    browser="",  # Can be "chrome" or "edge"
    user_data_dir=r"",
    profile_directory="Default"
)

crawler.run()
