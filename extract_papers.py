import os
import re
import requests
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import pdfplumber

#creates folders
os.makedirs("images", exist_ok=True)
os.makedirs("pdfs", exist_ok=True)
os.makedirs("texts", exist_ok=True)

#loads the csv from github
csv_url = "https://raw.githubusercontent.com/jgalazka/SB_publications/main/SB_publication_PMC.csv"
print("Downloading CSV from GitHub...")
df = pd.read_csv(csv_url)
print(f"Loaded {len(df)} papers from the dataset.")

#picks only first 10 for testing
sample_df = df.head(10)

#helper functions
def is_pdf(url):
    return urlparse(url).path.lower().endswith(".pdf")

def download_file(url, filename):
    """Download any file (pdf/html) to local folder"""
    headers = {"User-Agent": "blah/5.0"}
    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()
    with open(filename, "wb") as f:
        f.write(r.content)
    return filename

def extract_text_from_pdf(path):
    """Extract readable text from PDF"""
    text = ""
    try:
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"PDF extraction failed for {path}: {e}")
    return text.strip()

def extract_text_from_html(html):
    """Pull paragraph text out of HTML"""
    soup = BeautifulSoup(html, "html.parser")
    paragraphs = soup.find_all("p")
    text = "\n".join(p.get_text().strip() for p in paragraphs if p.get_text())
    return text

def find_pdf_link_in_html(html, base_url):
    """Find PDF link inside an HTML page"""
    soup = BeautifulSoup(html, "html.parser")
    for a in soup.find_all("a", href=True):
        href = a["href"].lower()
        if href.endswith(".pdf"):
            return urljoin(base_url, a["href"])
    return None

def download_images_from_html(html, base_url, title):
    """Download first few images from a paper"""
    soup = BeautifulSoup(html, "html.parser")
    imgs = soup.find_all("img")
    image_paths = []
    for i, img in enumerate(imgs[:3]):  # download up to 3 per paper
        src = img.get("src")
        if not src:
            continue
        full_url = urljoin(base_url, src)
        ext = os.path.splitext(full_url)[1] or ".jpg"
        safe_title = re.sub(r'[^a-zA-Z0-9]', '_', title)[:50]
        filename = f"images/{safe_title}_{i}{ext}"
        try:
            with open(filename, "wb") as f:
                f.write(requests.get(full_url, timeout=20).content)
            image_paths.append(filename)
        except Exception as e:
            print(f"Could not download image: {e}")
    return image_paths

#extracts papers
papers_data = []

for i, row in tqdm(sample_df.iterrows(), total=len(sample_df), desc="Processing papers"):
    title = row.get("title") or row.get("Title") or f"Paper_{i}"
    link = row.get("link") or row.get("Link")

    if not link:
        continue

    print(f"\n Processing: {title}")
    full_text = ""
    image_list = []

    try:
        #direct pdf
        if is_pdf(link):
            pdf_path = f"pdfs/{i}.pdf"
            download_file(link, pdf_path)
            full_text = extract_text_from_pdf(pdf_path)

        #html page
        else:
            r = requests.get(link, timeout=30)
            html = r.text
            pdf_link = find_pdf_link_in_html(html, link)

            if pdf_link:
                pdf_path = f"pdfs/{i}.pdf"
                download_file(pdf_link, pdf_path)
                full_text = extract_text_from_pdf(pdf_path)
            else:
                full_text = extract_text_from_html(html)
                image_list = download_images_from_html(html, link, title)

    except Exception as e:
        print(f"Error downloading {title}: {e}")
        continue

    #save text file too
    safe_name = re.sub(r'[^a-zA-Z0-9]', '_', title)[:60]
    text_path = f"texts/{safe_name}.txt"
    with open(text_path, "w", encoding="utf-8") as f:
        f.write(full_text)

    #add to summary data
    papers_data.append({
        "Title": title,
        "URL": link,
        "TextFile": text_path,
        "ImageFiles": "; ".join(image_list),
        "TextPreview": full_text[:300].replace("\n", " ")  # just preview
    })

#save everything to csv
out_df = pd.DataFrame(papers_data)
out_df.to_csv("paper_texts.csv", index=False)
print("\nDone, saved results to paper_texts.csv")
print(f"Extracted {len(out_df)} papers successfully.")