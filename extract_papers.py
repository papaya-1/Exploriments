#logic for extracting texts. doesn't work because most pages aren't full text and PMC only returns metadata
import os
import re
import requests
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import pdfplumber

#creates folders
os.makedirs("data", exist_ok=True)
os.makedirs("pdfs", exist_ok=True)
os.makedirs("texts", exist_ok=True)

#loads the csv from github
csv_url = "https://raw.githubusercontent.com/jgalazka/SB_publications/main/SB_publication_PMC.csv"
print("Downloading CSV from GitHub...")
df = pd.read_csv(csv_url)
print(f"Loaded {len(df)} papers from the dataset.")

#actual
the_df = df
#for testing
#the_df = df.head(10);

#helper functions
def is_pdf(url):
    return urlparse(url).path.lower().endswith(".pdf")

def download_file(url, filename):
    """Download any file (pdf/html) to local folder"""
    headers = {"User-Agent": "Mozilla/5.0 (compatible; AcademicBot/1.0)"}
    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()
    with open(filename, "wb") as f:
        f.write(r.content)
    return filename

#find PMC (PubMed Central) link for PubMed entries
def get_pmc_url(pmid):
    """Try to find a PubMed Central (PMC) full-text link for a given PubMed ID"""
    base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi"
    params = {
        "dbfrom": "pubmed",
        "linkname": "pubmed_pmc",
        "id": pmid,
        "retmode": "json"
    }
    r = requests.get(base, params=params, timeout=15)
    if r.ok:
        m = re.search(r'PMC(\d+)', r.text)
        if m:
            pmc_id = m.group(1)
            return f"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC{pmc_id}/"
    return None

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
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "header", "footer", "nav", "aside"]):
        tag.decompose()
    paragraphs = soup.find_all("p")
    return "\n".join(p.get_text(strip=True) for p in paragraphs)

def find_pdf_link_in_html(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    for a in soup.find_all("a", href=True):
        href = a["href"].lower()
        if ".pdf" in href:  # match any href containing '.pdf'
            return urljoin(base_url, a["href"])
    return None

# def download_images_from_html(html, base_url, title):
#     """Download first few images from a paper"""
#     soup = BeautifulSoup(html, "html.parser")
#     imgs = soup.find_all("img")
#     image_paths = []
#     for i, img in enumerate(imgs[:3]):  # download up to 3 per paper
#         src = img.get("src")
#         if not src:
#             continue
#         full_url = urljoin(base_url, src)
#         ext = os.path.splitext(full_url)[1] or ".jpg"
#         safe_title = re.sub(r'[^a-zA-Z0-9]', '_', title)[:50]
#         filename = f"images/{safe_title}_{i}{ext}"
#         try:
#             with open(filename, "wb") as f:
#                 f.write(requests.get(full_url, timeout=20).content)
#             image_paths.append(filename)
#         except Exception as e:
#             print(f"Could not download image: {e}")
#     return image_paths

#extracts papers
extracted_papers = []

for i, row in tqdm(the_df.iterrows(), total=len(the_df), desc="Processing papers"):
    title = row.get("title") or row.get("Title") or f"Paper_{i}"
    link = row.get("link") or row.get("Link")

    print(f"\n Processing: {title}")
    full_text = ""
    # image_list = []

    try:
        #check for PubMed ID → find PMC full text link
        pmid_match = re.search(r'pubmed\.ncbi\.nlm\.nih\.gov/(\d+)', link)
        if pmid_match:
            pmid = pmid_match.group(1)
            pmc_url = get_pmc_url(pmid)
            if pmc_url:
                print(f" → Found PMC full text: {pmc_url}")
                try:
                    r = requests.get(pmc_url, timeout=30)
                    html = r.text
                    full_text = extract_text_from_html(html)
                except Exception as e:
                    print(f"PMC fetch failed: {e}")
        #direct pdf
        if is_pdf(link):
            pdf_path = f"pdfs/{i}.pdf"
            download_file(link, pdf_path)
            full_text = extract_text_from_pdf(pdf_path)

        #html page
        else:
            if not full_text.strip():  # fallback if PMC version fails
                r = requests.get(link, timeout=30)
                html = r.text
                full_text = extract_text_from_html(html)

    except Exception as e:
        print(f"Error downloading {title}: {e}")
        continue

    if not full_text.strip():
        full_text = "[No text extracted — possibly behind paywall or missing full text]"
    else:
        print(f" → Extracted {len(full_text)} characters for '{title}'")

    #save text file too
    safe_name = re.sub(r'[^a-zA-Z0-9]', '_', title)[:60]
    text_path = f"texts/{safe_name}.txt"
    with open(text_path, "w", encoding="utf-8") as f:
        f.write(full_text)

    #add to summary data
    extracted_papers.append({
        "title": title,
        "entire_text": full_text
    })

#save everything to csv
out_df = pd.DataFrame(extracted_papers)
out_df.to_csv("data/extracted_papers.csv", index=False)
print("\n Saved results to data/extracted_papers.csv")
print(f"Extracted {len(extracted_papers)} papers successfully.")