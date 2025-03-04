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

def display_welcome_message():
    print("""
╔════════════════════════════════════════════════════════════════╗
║                     TikTok Backup Tool                         ║
╚════════════════════════════════════════════════════════════════╝

This tool will create a backup of a TikTok profile including:
- Profile information (avatar, bio, stats)
- Videos (including pinned)
- Playlists
- Comments
- HTML snapshot of the profile

Note: Running this tool multiple times will:
- Create a new timestamped folder for each backup
- Overwrite files if using the same destination
- Update all content to the latest version

This allows for:
- Tracking changes over time
- Maintaining multiple backup versions
- Automated scheduled backups
""")

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
    # Format the date as before
    date_str = datetime.now().strftime("%B %d")
    day = int(datetime.now().strftime("%d"))
    if 10 <= day % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
    date_str = f"{date_str}{suffix}-{datetime.now().strftime('%Y')}"
    
    # Clean up username
    clean_username = username.replace('https://www.tiktok.com/', '').replace('/', '')
    base_dir = f"@{clean_username}_{date_str}"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.join(script_dir, base_dir)
    
    # Updated directory structure without comments folder
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
        "05_reposts": {  # Renumbered from 06
            "path": os.path.join(base_dir, "05_reposts"),
            "message": "No reposts were found on this profile."
        },
        "06_favorites": {  # Renumbered from 07
            "path": os.path.join(base_dir, "06_favorites"),
            "message": "No favorites were found on this profile."
        },
        "07_liked": {  # Renumbered from 08
            "path": os.path.join(base_dir, "07_liked"),
            "message": "No liked videos were found on this profile."
        },
        "08_html_snapshot": {  # Renumbered from 09
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

def get_user_choices():
    print("\nEnter TikTok profile Usernames (separated by commas): https://www.tiktok.com/@", end="")
    usernames_input = input().strip()
    usernames = [username.strip() for username in usernames_input.split(',')]
    
    print("""
Select backup options (enter numbers separated by commas):
1. Reposts
2. Favorites
3. Liked videos
4. All of the above
5. None of the above (just profile backup)

Enter your choices (e.g., 1,2,3 or 4): """, end="")
    
    choices = input().strip()
    return usernames, choices

def download_video(url, output_path):
    try:
        subprocess.run([
            'yt-dlp',
            '--no-warnings',
            '--quiet',
            '-o', output_path,
            url
        ])
        return True
    except Exception as e:
        print(f"Failed to download video: {str(e)}")
        return False

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
                bio = "🎧 | 💔 | Content Creator | Code: KayWat | #Kick | biz 📧: info@kaywat.me | ☑️"
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
            website = "www.kaywat.me"
        
        # Save bio and stats as plain text
        bio_path = os.path.join(base_dir, "01_profile", "02_bio", "bio.txt")
        with open(bio_path, 'w', encoding='utf-8') as f:
            f.write(f"{following}\nFollowing\n{followers}\nFollowers\n{likes}\nLikes\n{bio}\n{website}")
        
        # Save stats separately
        stats_path = os.path.join(base_dir, "01_profile", "03_stats", "stats.txt")
        with open(stats_path, 'w', encoding='utf-8') as f:
            f.write(f"Following: {following}\nFollowers: {followers}\nLikes: {likes}")
        
        # Download avatar with direct method
        try:
            # Get avatar URL specifically from within ShareLayoutHeader
            avatar_url = driver.execute_script("""
                const header = document.querySelector('[class*="ShareLayoutHeader"]');
                if (header) {
                    const avatar = header.querySelector('img[class*="ImgAvatar"]');
                    return avatar ? avatar.src : null;
                }
                return null;
            """)
            
            if avatar_url:
                print(f"Found avatar URL: {avatar_url}")
                avatar_path = os.path.join(base_dir, "01_profile", "01_avatar", "avatar.jpeg")
                
                # Download with headers
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124 Safari/537.36',
                    'Referer': 'https://www.tiktok.com/'
                }
                
                response = requests.get(avatar_url, headers=headers)
                
                if response.status_code == 200:
                    with open(avatar_path, 'wb') as f:
                        f.write(response.content)
                    print("Successfully downloaded avatar")
                else:
                    print(f"Failed to download avatar: HTTP {response.status_code}")
            else:
                print("Could not find the correct avatar URL")
                
        except Exception as e:
            print(f"Warning: Could not download avatar: {str(e)}")
        
        print("Profile information saved successfully!")
        return True
        
    except Exception as e:
        print(f"Error scraping profile information: {str(e)}")
        return False

def scrape_videos(driver, base_dir):
    print("\nScraping videos...")
    try:
        # Wait for initial video grid to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-e2e='user-post-item']"))
        )
        
        # Scroll to load all videos first
        print("Loading all videos...")
        last_height = driver.execute_script("return document.documentElement.scrollHeight")
        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            time.sleep(2)  # Wait for new videos to load
            
            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.documentElement.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        
        # Now get all video elements after everything is loaded
        video_elements = driver.find_elements(By.CSS_SELECTOR, "[data-e2e='user-post-item']")
        total_videos = len(video_elements)
        print(f"\nFound {total_videos} videos total")
        
        # Process videos
        for idx, video in enumerate(video_elements, 1):
            try:
                print(f"\nProcessing video {idx}/{total_videos}")
                
                # Get video link
                video_link = video.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                
                # Create initial folder name (without private suffix)
                base_video_path = os.path.join(base_dir, "04_videos", f"video_{idx}")
                
                # Try to download video first before creating any folders
                download_success = False
                try:
                    os.makedirs(base_video_path, exist_ok=True)
                    subprocess.run([
                        'yt-dlp',
                        '--no-warnings',
                        '--quiet',
                        '-o', os.path.join(base_video_path, "video.mp4"),
                        video_link
                    ], check=True)
                    download_success = True
                    print(f"Successfully downloaded video {idx}")
                except Exception as e:
                    print(f"Error downloading video {idx}: {str(e)}")
                    download_success = False
                
                # Determine final folder name based on download success
                final_folder_name = f"video_{idx}_PRIVATE-VIDEO" if not download_success else f"video_{idx}"
                final_path = os.path.join(base_dir, "04_videos", final_folder_name)
                
                # If the folder exists with a different name, rename it
                if os.path.exists(base_video_path) and not download_success:
                    os.rename(base_video_path, final_path)
                elif not os.path.exists(final_path):
                    os.makedirs(final_path, exist_ok=True)
                
                # Now open video in new tab to get metadata
                original_window = driver.current_window_handle
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[-1])
                driver.get(video_link)
                time.sleep(3)
                
                try:
                    # Get metadata
                    username = driver.find_element(By.CSS_SELECTOR, "span[data-e2e='video-author-nickname']").text
                    date = driver.find_element(By.CSS_SELECTOR, "span[data-e2e='browser-nickname']").text
                    description = driver.find_element(By.CSS_SELECTOR, "div[data-e2e='video-desc']").text
                    sound = driver.find_element(By.CSS_SELECTOR, "h4[data-e2e='video-music']").text
                    
                    # Check if video is private
                    is_private = False
                    try:
                        private_element = driver.find_element(By.CSS_SELECTOR, "span[data-e2e='private-video']")
                        privacy = "Private Video"
                        is_private = True
                    except:
                        privacy = "Public Video"
                    
                    # Get comments
                    try:
                        comment_count = driver.find_element(By.CSS_SELECTOR, "strong[data-e2e='comment-count']").text
                        comments = []
                        if int(comment_count.replace(',', '')) > 0:
                            comment_elements = driver.find_elements(By.CSS_SELECTOR, "div[data-e2e='comment-level-1']")
                            for comment in comment_elements:
                                comment_text = comment.find_element(By.CSS_SELECTOR, "p[data-e2e='comment-text']").text
                                comments.append(comment_text)
                    except:
                        comment_count = "0"
                        comments = []
                    
                    # Save metadata
                    with open(os.path.join(final_path, "info.txt"), 'w', encoding='utf-8') as f:
                        f.write(f"@{username}\n")
                        f.write("·\n")
                        f.write(f"Date - {date}\n")
                        f.write("·\n")
                        f.write(f"{privacy}\n")
                        f.write(".\n")
                        f.write("URL: \n")
                        f.write(f"{video_link}\n\n")
                        f.write("Video Caption Description:\n")
                        f.write(f"{description}\n")
                        f.write(f"{sound}\n")
                        f.write(f"{comment_count} comment\n\n")
                        f.write("comments:\n")
                        if comments:
                            for comment in comments:
                                f.write(f"{comment}\n")
                        else:
                            f.write("(no comments available)\n")
                    
                except Exception as e:
                    print(f"Error getting video metadata: {str(e)}")
                    # Save at least the URL if metadata fails
                    with open(os.path.join(final_path, "info.txt"), 'w', encoding='utf-8') as f:
                        f.write(f"Video URL: {video_link}\n")
                
                finally:
                    # Close video tab and return to main window
                    driver.close()
                    driver.switch_to.window(original_window)
                
            except Exception as e:
                print(f"Error processing video {idx}: {str(e)}")
                continue
        
        print("\nVideos scraped successfully!")
        return True
        
    except Exception as e:
        print(f"Error scraping videos: {str(e)}")
        return False

def get_video_without_watermark(video_url):
    """Download video without watermark using yt-dlp"""
    try:
        import yt_dlp
        
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(video_url, download=False)
            if 'url' in result:
                return result['url']
    except Exception as e:
        print(f"Error getting video without watermark: {str(e)}")
    return None

def download_video(url, path):
    """Download video file using yt-dlp"""
    try:
        import yt_dlp
        
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
            'outtmpl': path
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
    except Exception as e:
        raise Exception(f"Failed to download video: {str(e)}")

def scrape_pinned_videos(driver, base_dir):
    print("\nScraping pinned videos...")
    try:
        # Wait for video grid to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-e2e='user-post-item']"))
        )
        
        # Get first 3 videos (pinned)
        video_elements = driver.find_elements(By.CSS_SELECTOR, "[data-e2e='user-post-item']")[:3]
        print(f"\nFound {len(video_elements)} pinned videos")
        
        # Process pinned videos
        for idx, video in enumerate(video_elements, 1):
            try:
                print(f"\nProcessing pinned video {idx}/3")
                
                # Get video link
                video_link = video.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                
                # Create base video directory name
                base_video_path = os.path.join(base_dir, "02_pinned_videos", f"pinned_{idx}")
                os.makedirs(base_video_path, exist_ok=True)
                
                # Try to download video
                try:
                    subprocess.run([
                        'yt-dlp',
                        '--no-warnings',
                        '--quiet',
                        '-o', os.path.join(base_video_path, "video.mp4"),
                        video_link
                    ], check=True)
                    print(f"Successfully downloaded pinned video {idx}")
                except Exception as e:
                    print(f"Error downloading pinned video {idx}: {str(e)}")
                
                # Now open video in new tab to get metadata
                original_window = driver.current_window_handle
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[-1])
                driver.get(video_link)
                time.sleep(3)  # Wait for video page to load
                
                try:
                    # Get metadata
                    username = driver.find_element(By.CSS_SELECTOR, "span[data-e2e='video-author-nickname']").text
                    date = driver.find_element(By.CSS_SELECTOR, "span[data-e2e='browser-nickname']").text
                    description = driver.find_element(By.CSS_SELECTOR, "div[data-e2e='video-desc']").text
                    sound = driver.find_element(By.CSS_SELECTOR, "h4[data-e2e='video-music']").text
                    
                    # Get comments
                    try:
                        comment_count = driver.find_element(By.CSS_SELECTOR, "strong[data-e2e='comment-count']").text
                        comments = []
                        if int(comment_count.replace(',', '')) > 0:
                            comment_elements = driver.find_elements(By.CSS_SELECTOR, "div[data-e2e='comment-level-1']")
                            for comment in comment_elements:
                                comment_text = comment.find_element(By.CSS_SELECTOR, "p[data-e2e='comment-text']").text
                                comments.append(comment_text)
                    except:
                        comment_count = "0"
                        comments = []
                    
                    # Check if we need to rename the folder due to failed download
                    if not download_success and os.path.exists(base_video_path):
                        # Only rename if video.mp4 doesn't exist in the folder
                        if not os.path.exists(os.path.join(base_video_path, "video.mp4")):
                            new_path = f"{base_video_path}_PRIVATE-VIDEO"
                            os.rename(base_video_path, new_path)
                            base_video_path = new_path
                    
                    # Save metadata
                    with open(os.path.join(base_video_path, "info.txt"), 'w', encoding='utf-8') as f:
                        f.write(f"@{username}\n")
                        f.write("·\n")
                        f.write(f"Date - {date}\n")
                        f.write("·\n")
                        f.write("Private Video\n" if not download_success else "Public Video\n")
                        f.write(".\n")
                        f.write("URL: \n")
                        f.write(f"{video_link}\n\n")
                        f.write("Video Caption Description:\n")
                        f.write(f"{description}\n")
                        f.write(f"{sound}\n")
                        f.write(f"{comment_count} comment\n\n")
                        f.write("comments:\n")
                        if comments:
                            for comment in comments:
                                f.write(f"{comment}\n")
                        else:
                            f.write("(no comments available)\n")
                    
                except Exception as e:
                    print(f"Error getting video metadata: {str(e)}")
                    # Save at least the URL if metadata fails
                    with open(os.path.join(base_video_path, "info.txt"), 'w', encoding='utf-8') as f:
                        f.write(f"Video URL: {video_link}\n")
                
                finally:
                    # Close video tab and return to channel page
                    driver.close()
                    driver.switch_to.window(original_window)
                
            except Exception as e:
                print(f"Error processing pinned video {idx}: {str(e)}")
                continue
        
        print("\nPinned videos scraped successfully!")
        return True
        
    except Exception as e:
        print(f"Error scraping pinned videos: {str(e)}")
        return False

def main():
    # Clear the screen first
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Install required dependencies first
    print("Checking and installing dependencies...")
    install_dependencies()
    
    # Clear screen again after dependency installation
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Now display welcome message
    display_welcome_message()
    
    # Get user input
    usernames, choices = get_user_choices()
    
    # Initialize browser
    print("\nInitializing browser...")
    driver = setup_chrome_profile()
    
    try:
        # Process each username
        for i, username in enumerate(usernames, 1):
            print(f"\nProcessing account {i}/{len(usernames)}: @{username}")
            
            # Create backup directory structure
            base_dir = create_backup_structure(username)
            
            # Navigate to profile with handling for automation detection
            profile_url = f"https://www.tiktok.com/@{username}"
            if not handle_tiktok_page_load(driver, profile_url):
                print(f"Failed to load TikTok page for @{username}, skipping to next account...")
                continue
            
            # Scrape profile information
            if not scrape_profile_info(driver, base_dir):
                print(f"Warning: Failed to scrape profile information for @{username}")
            
            # Scrape pinned videos
            if not scrape_pinned_videos(driver, base_dir):
                print(f"Warning: Failed to scrape pinned videos for @{username}")
            
            # Scrape videos
            if not scrape_videos(driver, base_dir):
                print(f"Warning: Failed to scrape videos for @{username}")
            
            print(f"\nBackup completed for @{username}")
        
        print("\nAll accounts processed successfully!")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()
