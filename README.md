# 🧠 Wikipedia Summary Scraper

A Python script that scrapes the **title** and **introductory summary** from any public Wikipedia page, based on a **URL**, **exact page title**, or even a **general keyword**.

---

## ✨ Features

- ✅ Accepts Wikipedia page titles, full URLs, or keywords 
- 🔍 Suggests similar titles if the exact one is not found using Wikipedia's search API
- 📄 Extracts the official title and the first 100 words of the article
- 💾 Saves the title and summary to a `.txt` file automatically
- 🧼 Cleans the filename so it’s safe across operating systems

---

## 🛠️ Requirements

- Python 3.8+
- Install dependencies using:

```bash
pip install requests beautifulsoup4
