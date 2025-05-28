import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import asyncio
import aiohttp

with open('proxies.json', 'r', encoding='utf-8') as f:
    proxies = json.load(f)

with open('categories.json', 'r', encoding='utf-8') as f:
    categories = json.load(f)

df = pd.read_csv('data.csv')

all_courses_data = []
counter = 0

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Accept-Language': 'en-US,en;q=0.5',
}

REQUESTS_PER_SECOND = 90
semaphore = asyncio.Semaphore(REQUESTS_PER_SECOND)
tasks = []
course_tasks = []

start_with_page = int(input('Enter the page to start with: '))

proxy_counter = 0
def get_next_proxy():
    global proxy_counter
    proxy = proxies[proxy_counter]
    proxy_counter += 1
    if proxy_counter >= len(proxies):
        proxy_counter = 0
    return f"http://{proxy}"

async def fetch(session, url, semaphore, handler, category, retries=3):
    async with semaphore:
        proxy = get_next_proxy()
        try:
            print(f"Fetching {url} with {proxy}...")
            async with session.get(url, proxy=proxy, timeout=10) as response:
                if response.status != 200:
                    print(f"Error {response.status} with {url}. Retrying...")
                    return await fetch(session, url, semaphore, handler, category)
                
                print(f"Got response from {url} with {proxy}")
                
                html = await response.text()
                soup = BeautifulSoup(html, "html.parser")
                await handler(soup, session, url, category)

        except Exception as e:
            if retries == 0:
                print(f"Failed to fetch {url} with {proxy}: {e}")
                return
            else:
                print(f"Proxy {proxy} not working: {e}")
                return await fetch(session, url, semaphore, handler, category, retries - 1)

async def get_course_info(soup, session, url, category):
    course_id = url.split("-")[-1]
    course_title = soup.select_one("h1").text.strip()

    try: course_description = soup.select_one(".padding-bottom-large .line-wide").text.strip()
    except: course_description = ""

    try: course_provider = soup.select_one("li:has(.icon-provider-charcoal) a").text.strip()
    except: course_provider = ""

    course_price = "Free"
    
    try: course_language = soup.select_one("li:has(.icon-language-charcoal) a.color-charcoal").text.strip()
    except: course_language = ""
    
    try: course_duration = soup.select_one("li:has(.icon-clock-charcoal) span.line-tight").text.strip()
    except: course_duration = ""
    
    try: course_picture_url = soup.select_one("source")["srcset"]
    except: course_picture_url = ""
    
    try: course_rating = soup.select_one("#reviews-contents .inline-block .weight-bold:first-child").text.strip()
    except: course_rating = "0"
    
    try: reviews_count = soup.select_one("#reviews-contents .inline-block .weight-bold:last-child").text.strip()
    except: reviews_count = "0"

    all_courses_data.append({
        "URL": url,
        "ID": course_id,
        "Title": course_title,
        "Description": course_description.strip(),
        "Category": category,
        "Provider": course_provider,
        "Price": course_price,
        "Language": course_language,
        "Duration": course_duration,
        "Picture URL": course_picture_url,
        "Rating": course_rating,
        "Reviews Count": reviews_count,
    })

    global counter
    counter += 1
    print(f"Course {counter} scraped: {course_title}. Category: {category}")

async def get_courses_from_page(soup, session, url, category):
    courses = soup.select("li.course-list-course")
    if not courses:
        print(f"Page {url} is empty. Skipping...")
        return
    
    for course in courses:
        course_url = "https://www.classcentral.com" + course.select_one("a.course-name")["href"]

        if "/classroom/" in course_url:
            print(f"Course {course_url} is a video. Skipping...")
            continue

        course_id = course_url.split("-")[-1]

        if int(course_id) in df["ID"].values:
            print(f"Course {course_url} already exists in the dataset. Skipping...")
            continue

        task = asyncio.create_task(fetch(session, course_url, semaphore, get_course_info, category))
        course_tasks.append(task)

    print(f"Page {url} scraped!")
                     
async def main():
    async with aiohttp.ClientSession() as session:
        for category in categories:
            global start_with_page
            page = start_with_page
            start_with_page = 1

            category_url = category['url']
            course_category = category['name']

            response = requests.get(category_url, headers=headers)
            if response.status_code != 200:
                print(f'Error {response.status_code} with {category_url}. Retrying...')
                await asyncio.sleep(1 / REQUESTS_PER_SECOND)
                continue
            soup = BeautifulSoup(response.text, 'html.parser')
            text_with_total_courses = soup.select_one('span.hidden.small-up-inline-block').text
            total_courses = int(text_with_total_courses.split('of')[-1].strip())
            total_pages = (total_courses // 15) + 1

            print(f'Scraping category: {course_category}...')

            while True:
                global tasks
                global course_tasks

                print(f'Scraping page {page} of {course_category}({category_url})...')

                page_url = f'{category_url}&page={page}'

                task = asyncio.create_task(fetch(session, page_url, semaphore, get_courses_from_page, course_category))
                tasks.append(task)

                page += 1
                if page > total_pages:
                    break

            await asyncio.gather(*tasks)
            await asyncio.gather(*course_tasks)

            course_tasks = []
            tasks = []

            print('All courses scraped!')
            global df
            global all_courses_data
            df = pd.concat([df, pd.DataFrame(all_courses_data)])
            all_courses_data = []
            df.to_csv('data.csv', index=False)
            print('Data saved to data.csv')
        
asyncio.run(main())