"""
A simple script to scrape the title and summary of a Wikipedia page.
"""
import sys
import re
import requests
from bs4 import BeautifulSoup

def sanitize_filename(filename: str) -> str:
    """Removes characters that are invalid in most file systems."""
    return re.sub(r'[<>:"/\\|?*]', '_', filename).strip()

def fetch_wikipedia_page(url: str) -> BeautifulSoup | None:
    """Fetches a Wikipedia page and returns a BeautifulSoup object."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}", file=sys.stderr)
        return None

def extract_summary(soup: BeautifulSoup, max_words: int = 100) -> str:
    """
    Extracts a summary of up to `max_words` from the Wikipedia page.
    It tries to get the first meaningful paragraphs from the content section.
    """
    # Try to select paragraphs from the main content
    paragraphs = soup.select('div.mw-parser-output > p')

    # Fallback if structure is different
    if not paragraphs:
        print("No paragraphs found with main selector. Trying fallback...", file=sys.stderr)
        paragraphs = soup.select('p')

    print(f"Found {len(paragraphs)} paragraph(s).")  # Debug info

    summary_parts = []
    word_count = 0

    for p in paragraphs:
        text = p.get_text(strip=True)
        if text and not p.find('span', id='coordinates'):
            summary_parts.append(text)
            word_count += len(text.split())
            if word_count >= max_words:
                break

    if not summary_parts:
        print("Still couldn't extract any usable summary.", file=sys.stderr)

    return "\n\n".join(summary_parts)

def main():
    """Main function to scrape title and summary from a Wikipedia page."""
    user_input = input("Enter the full Wikipedia URL or just the page title: ").strip()

    if user_input.startswith("http"):
        url = user_input
    else:
        page_title = user_input.replace(" ", "_")
        url = f"https://en.wikipedia.org/wiki/{page_title}"

    print(f"Fetching data from: {url}")
    soup = fetch_wikipedia_page(url)
    if not soup:
        sys.exit(1)

    # Extract the title
    title_element = soup.find('h1', id='firstHeading')
    if not title_element:
        print("Could not find the page title.", file=sys.stderr)
        sys.exit(1)

    page_title_text = title_element.get_text(strip=True)
    print(f"\nTitle: {page_title_text}\n")

    # Extract the summary
    summary = extract_summary(soup)
    if not summary:
        print("Could not extract a summary from the page.", file=sys.stderr)
        sys.exit(1)

    print(f"Summary:\n{summary}")

    # Save to file
    filename = sanitize_filename(page_title_text) + "_summary.txt"
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(f"Title: {page_title_text}\n\n")
            file.write(summary)
        print(f"\nSummary saved to {filename}")
    except IOError as e:
        print(f"Error writing to file {filename}: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
