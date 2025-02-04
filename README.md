# bidding-monitor
# Tender Data Scraper

## Overview
This Python script automates the process of scraping tender information from the China Bidding website, filtering for semiconductor polishing equipment, and pushing updates to a DingTalk group.

## Features
- **Web Scraping**: Uses Playwright to scrape tender data from China Bidding.
- **Data Cleaning**: Filters and removes duplicate tender entries.
- **DingTalk Integration**: Pushes the filtered tender information to a DingTalk group via webhook.

## Prerequisites
Ensure you have Python installed along with the required libraries:

```bash
pip install playwright pandas requests
python -m playwright install
```

## Usage
1. **Edit the script**:
   - Replace `'your_dingtalk_webhook_url'` with your actual DingTalk webhook URL.
   - Adjust the CSS selectors in the script to match the structure of the China Bidding website if needed.

2. **Run the script**:

```bash
python bidding-monitor.py
```

3. **Output**:
   - The script will scrape tender data based on the keyword "半导体研磨设备".
   - Cleaned data will be pushed to the specified DingTalk group.

## Notes
- Make sure the Playwright browser drivers are correctly installed.
- Ensure that the DingTalk webhook permissions are properly configured to allow incoming messages.

## License
本工具为XX厂时机案例脱敏版本

