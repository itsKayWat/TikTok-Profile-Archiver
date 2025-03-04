TikTok Backup Tool
=================

Overview
--------
The TikTok Backup Tool is a powerful utility that creates comprehensive backups of TikTok profiles. It downloads and organizes profile information, videos, and associated metadata in a structured format.

Features
--------
* Profile Information Backup
  - Avatar image
  - Bio text
  - Statistics (followers, following, likes)

* Video Content Backup
  - Pinned videos
  - Regular videos
  - Video metadata (description, date, sound info)
  - Comments (when available)

* Organized Directory Structure
  - Timestamped backup folders
  - Clear categorization of content
  - Detailed metadata files

Requirements
-----------
- Python 3.8 or higher
- Google Chrome browser
- Internet connection
- Required Python packages (automatically installed):
  * selenium
  * yt-dlp
  * requests

Installation
-----------
1. Ensure Python 3.8+ is installed on your system
2. Download the tt-backup.py script
3. Run the script - it will automatically install required dependencies

Usage
-----
Run: python tt-backup.py

When prompted:
1. Enter TikTok usernames (comma-separated for multiple accounts)
2. Select backup options (reposts, favorites, liked videos)
3. Wait for the backup process to complete

Output Structure
--------------
@username_Month Day-Year/
├── 01_profile/
│   ├── 01_avatar/
│   ├── 02_bio/
│   └── 03_stats/
├── 02_pinned_videos/
├── 03_playlists/
├── 04_videos/
├── 05_reposts/
├── 06_favorites/
├── 07_liked/
└── 08_html_snapshot/

Common Use Cases
--------------
- Content creators backing up their own profiles
- Archiving TikTok content for preservation
- Creating local copies of favorite content
- Tracking profile changes over time

Support the Developer
-------------------
Developer: KayWat
Support Options:
- One Coffee ($6): https://www.paypal.com/donate/?hosted_button_id=J3ABMPG6MQF3L&custom=1coffee
- Two Coffees ($12): https://www.paypal.com/donate/?hosted_button_id=J3ABMPG6MQF3L&custom=2coffees
- Three Coffees ($24): https://www.paypal.com/donate/?hosted_button_id=J3ABMPG6MQF3L&custom=3coffees

Your support helps maintain and improve this tool! Thank you! 🙏 