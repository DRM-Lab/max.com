import os
import time
import random
import string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

SEEN_LINKS_FILE = "seen_links.txt"

GENRE_URLS = [
    "https://play.max.com/genre/action",
    "https://play.max.com/genre/comedy",
    "https://play.max.com/genre/drama",
    "https://play.max.com/genre/horror",
    "https://play.max.com/genre/sci-fi",
    "https://play.max.com/genre/documentary"
]

def setup_browser():
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def scroll_to_bottom(driver, max_wait=60):
    print("\U0001f4dc Scrolling to load all movies...")
    last_height = driver.execute_script("return document.body.scrollHeight")
    start_time = time.time()

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2.5)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            print("\u2705 Reached bottom of page.")
            break
        last_height = new_height
        if time.time() - start_time > max_wait:
            print("\u23f1\ufe0f Scroll timed out.")
            break

def extract_movie_links(driver):
    anchors = driver.find_elements(By.XPATH, '//a[contains(@href, "/movie/")]')
    links = list(set([a.get_attribute("href") for a in anchors if "/movie/" in a.get_attribute("href")]))
    return links

def generate_random_query():
    letters = string.ascii_lowercase
    return ''.join(random.choices(letters, k=random.choice([1, 2])))

def load_seen_links():
    if not os.path.exists(SEEN_LINKS_FILE):
        return set()
    with open(SEEN_LINKS_FILE, "r") as f:
        return set([line.strip() for line in f if line.strip()])

def save_seen_links(new_links):
    with open(SEEN_LINKS_FILE, "a") as f:
        for link in new_links:
            f.write(link + "\n")

def save_links(links, batch_id, prefix):
    output_dir = "output_movies"
    os.makedirs(output_dir, exist_ok=True)
    for i in range(0, len(links), 10):
        chunk = links[i:i+10]
        file_path = os.path.join(output_dir, f"{prefix}_{batch_id}_{(i // 10) + 1}.txt")
        with open(file_path, "w") as f:
            for link in chunk:
                f.write(link + "\n")
        print(f"\U0001f4be Saved {len(chunk)} links to {file_path}")

def run_movies_mode(driver, seen_links, batch_counter):
    driver.get("https://play.max.com/movies")
    time.sleep(4)
    scroll_to_bottom(driver)
    all_links = extract_movie_links(driver)
    print(f"\u2705 Loaded {len(all_links)} movie links.")

    while True:
        try:
            count = int(input("\U0001f522 How many random movies do you want to extract? "))
            break
        except ValueError:
            print("\u274c Invalid number.")

    sample = random.sample(all_links, min(count, len(all_links)))
    unique_links = [link for link in sample if link not in seen_links]
    duplicates = len(sample) - len(unique_links)

    if unique_links:
        save_links(unique_links, batch_counter, "movies")
        save_seen_links(unique_links)
        print(f"\u2705 Saved {len(unique_links)} new links. \u267b Skipped {duplicates} duplicates.")
    else:
        print("\u26a0\ufe0f All selected links were duplicates.")

def run_search_mode(driver, seen_links, search_counter):
    search_terms = [
        "the", "man", "love", "dark", "moon", "fire", "red", "blue", "night",
        "girl", "life", "death", "dream", "war", "blood", "star", "light", "king", "queen"
    ]
    max_attempts = 10
    found_total = 0

    for attempt in range(max_attempts):
        query = random.choice(search_terms)
        url = f"https://play.max.com/search?q={query}"
        print(f"\n\U0001f50d Searching for query: '{query}'")
        driver.get(url)
        time.sleep(4)

        links = extract_movie_links(driver)
        unique_links = [link for link in links if link not in seen_links]
        duplicates = len(links) - len(unique_links)

        if unique_links:
            save_links(unique_links, search_counter, "search")
            save_seen_links(unique_links)
            print(f"\u2705 Found {len(unique_links)} new links. \u267b Skipped {duplicates} duplicates.")
            search_counter += 1
            found_total += len(unique_links)
        else:
            print(f"\u26a0\ufe0f No new links found for query '{query}'.")

        print("\u23f3 Waiting 10 seconds before next search...")
        time.sleep(10)

    print(f"\n\ud83d\udcca Search complete. Found total {found_total} new movie links in {max_attempts} searches.")

def run_genre_mode(driver, seen_links, genre_batch):
    found_total = 0
    for genre_url in GENRE_URLS:
        print(f"\n\U0001f3ac Loading genre: {genre_url}")
        driver.get(genre_url)
        time.sleep(4)
        scroll_to_bottom(driver)
        links = extract_movie_links(driver)
        unique_links = [link for link in links if link not in seen_links]
        duplicates = len(links) - len(unique_links)

        if unique_links:
            save_links(unique_links, genre_batch, "genre")
            save_seen_links(unique_links)
            print(f"\u2705 Found {len(unique_links)} new links. \u267b Skipped {duplicates} duplicates.")
            genre_batch += 1
            found_total += len(unique_links)
        else:
            print("\u26a0\ufe0f No new unique links in this genre.")
        time.sleep(5)

    print("📊 Genre scan complete. Found total", found_total, "new movie links.")

def main():
    print("🛠️ Max.com Movie Scraper — Created by Mike | DRMLab.io Project")
    driver = setup_browser()

    try:
        print("\U0001f310 Opening Max.com homepage...")
        driver.get("https://play.max.com")
        time.sleep(3)

        print("\n\U0001f511 Please log in manually in the browser.")
        input("\u23f3 After you're logged in, press ENTER here to continue...")

        seen_links = load_seen_links()
        movie_batch = 1
        search_batch = 1
        genre_batch = 1

        while True:
            print("📋 === MAIN MENU ===")
            print("1️⃣  Extract movies from /movies page")
            print("2️⃣  Extract random movies via search")
            print("3️⃣  Extract movies by genre")
            print("4️⃣  Exit")
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                run_movies_mode(driver, seen_links, movie_batch)
                movie_batch += 1
            elif choice == "2":
                run_search_mode(driver, seen_links, search_batch)
                search_batch += 1
            elif choice == "3":
                run_genre_mode(driver, seen_links, genre_batch)
                genre_batch += 1
            elif choice == "4":
                break
            else:
                print("\u274c Invalid choice.")

    finally:
        again = input("⏹ Do you want to close the browser? (yes/no): ").strip().lower()
        if again != "yes":
            main()
        else:
            input("✅ Press ENTER to exit.")
        driver.quit()

if __name__ == "__main__":
    main()

