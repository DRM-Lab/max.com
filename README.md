# 🎬 Max.com Movie Scraper (by Mike | DRMLab.io)

An interactive, intelligent, and emoji-enhanced scraper for [https://play.max.com](https://play.max.com), designed to extract movie URLs using multiple modes: browse, genre, or smart search.

---

## 🚀 Features

### 🎛️ Menu Options
- `1️⃣` Extract movies from the `/movies` page (supports scroll)
- `2️⃣` Perform random searches with smart keywords
- `3️⃣` Extract movies by genre (action, comedy, sci-fi, etc.)
- `4️⃣` Exit (with session persistence option)

---

### 🧠 Built-in Intelligence
- ✅ Duplicate filtering using `seen_links.txt`
- 💾 Saves movie links to `output_movies/`, 10 per file
- 📜 Supports lazy-loaded content with auto-scroll
- 🔁 Persistent session between operations — no need to restart
- 🎲 Random search words like “love”, “war”, “moon” return diverse results

---

## 📦 Requirements
- Python 3.8+
- Google Chrome
- Selenium
- WebDriver Manager

```bash
pip install selenium webdriver-manager


## 🧑‍🤝‍🧑 Join Our Community

👉 [Join the official DRMLab.io Discord server](https://discord.gg/7bdh7ad6ex)
