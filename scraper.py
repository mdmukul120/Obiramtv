import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def scrape_m3u8_data():
    # Chrome Options setup (Headless mode for running on GitHub Actions)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Enable Network Performance Logging to capture dynamic m3u8 requests
    chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

    driver = webdriver.Chrome(options=chrome_options)
    
    url = "https://obiramtvlive.pages.dev/"
    print(f"Loading {url}...")
    driver.get(url)
    
    # Wait for dynamic content to load
    time.sleep(10)

    # 1. Fetching Network Logs for m3u8 URLs
    logs = driver.get_log('performance')
    m3u8_links = set()
    
    for entry in logs:
        message = entry['message']
        # Find urls ending with .m3u8 or containing m3u8 in network requests
        urls = re.findall(r'https?://[^\s"\'<>]+\.m3u8[^\s"\'<>]*', message)
        for u in urls:
            m3u8_links.add(u)

    # 2. Scrape Logos and Channel Names from DOM
    # (Note: CSS Selectors need to match the target webpage structure)
    channels_data = []
    
    # Example: Finding elements (Adjust selectors based on actual HTML structure)
    images = driver.find_elements("tag name", "img")
    
    print("\n--- Scraped Logos & Images ---")
    for img in images:
        src = img.get_attribute("src")
        alt = img.get_attribute("alt") or "Unknown Channel"
        if src:
            channels_data.append({"name": alt, "logo": src})

    driver.quit()

    # 3. Create M3U Playlist File
    print("\n--- Generating playlist.m3u ---")
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        
        # Writing m3u8 links found
        for idx, link in enumerate(m3u8_links):
            f.write(f'#EXTINF:-1 tvg-id="channel{idx+1}" tvg-name="Channel {idx+1}", Channel {idx+1}\n')
            f.write(f'{link}\n')

    print("Scraping completed! 'playlist.m3u' generated successfully.")

if __name__ == "__main__":
    scrape_m3u8_data()
