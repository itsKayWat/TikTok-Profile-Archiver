import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import json
from datetime import datetime
import subprocess
import re
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

def install_dependencies():
    """Install required dependencies"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "selenium"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    except Exception as e:
        print(f"Error installing dependencies: {str(e)}")

def setup_chrome_profile():
    chrome_options = webdriver.ChromeOptions()
    
    # Get the correct path for Windows
    user_data_dir = os.path.join(os.environ['LOCALAPPDATA'], 'Google', 'Chrome', 'User Data')
    
    # Add necessary options to prevent crashes and detection
    chrome_options.add_argument(f'--user-data-dir={user_data_dir}')
    chrome_options.add_argument('--profile-directory=Default')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--remote-debugging-port=9222')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Close any existing Chrome instances
    os.system("taskkill /f /im chrome.exe")
    time.sleep(2)
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        # Mask selenium's presence
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return driver
    except Exception as e:
        print(f"Error initializing Chrome with profile: {str(e)}")
        print("\nTrying alternative method without user profile...")
        
        try:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            driver = webdriver.Chrome(options=chrome_options)
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            return driver
        except Exception as e:
            print(f"Error with alternative method: {str(e)}")
            sys.exit("Could not initialize Chrome. Please make sure Chrome is installed.")

def handle_empty_directory(directory, message="No content was found to scrape for this section."):
    """Create an explanation file in empty directories"""
    if os.path.exists(directory) and not os.listdir(directory):
        with open(os.path.join(directory, "Nothing to Scrape.txt"), 'w', encoding='utf-8') as f:
            f.write(message)

def create_backup_structure(username):
    """Create the backup directory structure and handle empty folders"""
    # Format the date
    date_str = datetime.now().strftime("%B %d")
    day = int(datetime.now().strftime("%d"))
    if 10 <= day % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
    date_str = f"{date_str}{suffix}-{datetime.now().strftime('%Y')}"
    
    # Clean up username
    clean_username = username.replace('https://www.tiktok.com/', '').replace('/', '')
    
    # Create backups directory in script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    backups_dir = os.path.join(script_dir, "backups")
    os.makedirs(backups_dir, exist_ok=True)
    
    # Create user backup directory inside backups folder
    base_dir = os.path.join(backups_dir, f"@{clean_username}_{date_str}")
    
    # Create directory structure
    directories = {
        "01_profile": {
            "path": os.path.join(base_dir, "01_profile"),
            "subdirs": ["01_avatar", "02_bio", "03_stats"],
            "message": "No profile information was found to scrape."
        },
        "02_pinned_videos": {
            "path": os.path.join(base_dir, "02_pinned_videos"),
            "message": "No pinned videos were found on this profile."
        },
        "03_playlists": {
            "path": os.path.join(base_dir, "03_playlists"),
            "message": "No playlists were found on this profile."
        },
        "04_videos": {
            "path": os.path.join(base_dir, "04_videos"),
            "message": "No videos were found on this profile."
        },
        "05_reposts": {
            "path": os.path.join(base_dir, "05_reposts"),
            "message": "No reposts were found on this profile."
        },
        "06_favorites": {
            "path": os.path.join(base_dir, "06_favorites"),
            "message": "No favorites were found on this profile."
        },
        "07_liked": {
            "path": os.path.join(base_dir, "07_liked"),
            "message": "No liked videos were found on this profile."
        },
        "08_html_snapshot": {
            "path": os.path.join(base_dir, "08_html_snapshot"),
            "message": "No HTML snapshot was created for this profile."
        }
    }
    
    # Create directories
    for dir_info in directories.values():
        os.makedirs(dir_info["path"], exist_ok=True)
        if "subdirs" in dir_info:
            for subdir in dir_info["subdirs"]:
                os.makedirs(os.path.join(dir_info["path"], subdir), exist_ok=True)
        handle_empty_directory(dir_info["path"], dir_info["message"])
    
    return base_dir

def handle_tiktok_page_load(driver, url):
    try:
        # Initial page load
        driver.get(url)
        time.sleep(3)  # Wait for initial load
        
        # Refresh the page to bypass automation detection
        driver.refresh()
        time.sleep(3)  # Wait after refresh
        
        # Wait for body element to be present
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Additional wait for content to load
        time.sleep(2)
        
        return True
    except Exception as e:
        print(f"Error loading page: {str(e)}")
        return False

def scrape_profile_info(driver, base_dir):
    print("\nScraping profile information...")
    try:
        # Wait longer for the page to fully load
        time.sleep(5)
        
        # Get profile information using updated selectors
        try:
            # Get bio using JavaScript to get the full text content
            bio = driver.execute_script("""
                return document.querySelector('h2[data-e2e="user-bio"]').textContent
                || document.querySelector('h2[data-e2e="user-subtitle"]').textContent
            """)
            if not bio:
                bio = "No bio found"
        except:
            bio = "No bio found"
            
        try:
            following = driver.find_element(By.CSS_SELECTOR, "strong[data-e2e='following-count']").text
        except:
            following = "0"
            
        try:
            followers = driver.find_element(By.CSS_SELECTOR, "strong[data-e2e='followers-count']").text
        except:
            followers = "0"
            
        try:
            likes = driver.find_element(By.CSS_SELECTOR, "strong[data-e2e='likes-count']").text
        except:
            likes = "0"
            
        try:
            website = driver.find_element(By.CSS_SELECTOR, "a[data-e2e='user-link']").get_attribute('href')
        except:
            website = "No website found"
        
        # Save bio and stats
        bio_path = os.path.join(base_dir, "01_profile", "02_bio", "bio.txt")
        with open(bio_path, 'w', encoding='utf-8') as f:
            f.write(f"{following}\nFollowing\n{followers}\nFollowers\n{likes}\nLikes\n{bio}\n{website}")
        
        stats_path = os.path.join(base_dir, "01_profile", "03_stats", "stats.txt")
        with open(stats_path, 'w', encoding='utf-8') as f:
            f.write(f"Following: {following}\nFollowers: {followers}\nLikes: {likes}")
        
        # Download avatar
        try:
            avatar_url = driver.execute_script("""
                const header = document.querySelector('[class*="ShareLayoutHeader"]');
                if (header) {
                    const avatar = header.querySelector('img[class*="ImgAvatar"]');
                    return avatar ? avatar.src : null;
                }
                return null;
            """)
            
            if avatar_url:
                avatar_path = os.path.join(base_dir, "01_profile", "01_avatar", "avatar.jpeg")
                response = requests.get(avatar_url, headers={
                    'User-Agent': 'Mozilla/5.0',
                    'Referer': 'https://www.tiktok.com/'
                })
                if response.status_code == 200:
                    with open(avatar_path, 'wb') as f:
                        f.write(response.content)
                
        except Exception as e:
            print(f"Warning: Could not download avatar: {str(e)}")
        
        return True
        
    except Exception as e:
        print(f"Error scraping profile information: {str(e)}")
        return False

def scrape_pinned_videos(driver, base_dir):
    print("\nScraping pinned videos...")
    try:
        # Wait for video grid to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-e2e='user-post-item']"))
        )
        
        # Get first 3 videos (pinned)
        video_elements = driver.find_elements(By.CSS_SELECTOR, "[data-e2e='user-post-item']")[:3]
        
        for idx, video in enumerate(video_elements, 1):
            try:
                video_link = video.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                video_path = os.path.join(base_dir, "02_pinned_videos", f"pinned_{idx}")
                os.makedirs(video_path, exist_ok=True)
                
                try:
                    subprocess.run([
                        'yt-dlp',
                        '--no-warnings',
                        '--quiet',
                        '-o', os.path.join(video_path, "video.mp4"),
                        video_link
                    ], check=True)
                except Exception as e:
                    print(f"Error downloading pinned video {idx}: {str(e)}")
                    continue
                
            except Exception as e:
                print(f"Error processing pinned video {idx}: {str(e)}")
                continue
        
        return True
        
    except Exception as e:
        print(f"Error scraping pinned videos: {str(e)}")
        return False

def scrape_videos(driver, base_dir):
    print("\nScraping videos...")
    try:
        # Wait for video grid to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-e2e='user-post-item']"))
        )
        
        # Scroll to load all videos
        print("Loading all videos...")
        last_height = driver.execute_script("return document.documentElement.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.documentElement.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        
        # Get all video elements
        video_elements = driver.find_elements(By.CSS_SELECTOR, "[data-e2e='user-post-item']")
        
        for idx, video in enumerate(video_elements, 1):
            try:
                video_link = video.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                video_path = os.path.join(base_dir, "04_videos", f"video_{idx}")
                os.makedirs(video_path, exist_ok=True)
                
                try:
                    subprocess.run([
                        'yt-dlp',
                        '--no-warnings',
                        '--quiet',
                        '-o', os.path.join(video_path, "video.mp4"),
                        video_link
                    ], check=True)
                except Exception as e:
                    print(f"Error downloading video {idx}: {str(e)}")
                    continue
                
            except Exception as e:
                print(f"Error processing video {idx}: {str(e)}")
                continue
        
        return True
        
    except Exception as e:
        print(f"Error scraping videos: {str(e)}")
        return False

if __name__ == "__main__":
    print("This module is meant to be imported, not run directly.") 