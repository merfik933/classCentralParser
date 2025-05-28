# ClassCentralParser

**ClassCentralParser** is a course scraper for the [Class Central](vscode-file://vscode-app/d:/Programs/VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html) website, developed by Merfik. This tool automates the process of collecting detailed information about free online courses from various categories available on Class Central.

## Features

* **Category-Based Scraping:** Gathers courses from multiple predefined categories, including Computer Science, Business, Humanities, Data Science, Personal Development, Art and Design, Programming, Engineering, Health, Mathematics, Science, Social Sciences, Education, InfoSec, Conference Talks, Test Prep, and Certifications.
* **Proxy Support:** Utilizes a rotating list of proxies to avoid rate limiting and ensure stable scraping.
* **Asynchronous Requests:** Employs asynchronous HTTP requests for efficient and fast data collection.
* **Duplicate Avoidance:** Skips courses that are already present in the dataset to prevent duplicate entries.
* **Detailed Course Data:** Extracts comprehensive information for each course, such as title, description, provider, price, language, duration, image URL, rating, and review count.
* **Progress Tracking:** Allows the user to specify the starting page for scraping, making it easy to resume interrupted sessions.
* **Automatic Data Saving:** Appends new course data to an existing CSV file after each category is processed.

## How It Works

1. **Configuration:** The parser reads a list of proxies from [proxies.json](vscode-file://vscode-app/d:/Programs/VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html) and a list of categories from [categories.json](vscode-file://vscode-app/d:/Programs/VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html).
2. **Startup:** The user is prompted to enter the page number to start scraping from.
3. **Scraping:** For each category, the parser fetches all course listings, processes each course page, and extracts relevant details.
4. **Data Storage:** All collected data is saved to `data.csv`, ensuring that previously scraped courses are not duplicated.

## Requirements

* Python 3.8 or higher
* Required libraries: [requests](vscode-file://vscode-app/d:/Programs/VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html), [aiohttp](vscode-file://vscode-app/d:/Programs/VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html), [asyncio](vscode-file://vscode-app/d:/Programs/VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html), `beautifulsoup4`, [pandas](vscode-file://vscode-app/d:/Programs/VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html)

## Usage

1. Place your proxies in [proxies.json](vscode-file://vscode-app/d:/Programs/VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html) and categories in [categories.json](vscode-file://vscode-app/d:/Programs/VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html).
2. Ensure `data.csv` exists or will be created in the working directory.
3. Run the script and follow the prompt to enter the starting page number.
4. The script will scrape all courses from the specified categories and save the results to `data.csv`.

## Author

Developed by  **Merfik** .
