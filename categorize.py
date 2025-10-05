import numpy as np
import pandas as pd
from transformers import pipeline
from tqdm import tqdm
import requests
from bs4 import BeautifulSoup

df = pd.read_csv("data/SB_publication_PMC.csv", header=None)
df.columns = ["Title", "Link"]

categories = {
    "Altered Gravity": "",
    "Radiation": "",
    "ISS": "",
    "Mars": "",
    "Moon": "",
    "Musculoskeletal": "",
    "Cardiovascular & Vascular": "",
    "Neuroscience & Sensory": "",
    "Immune Response & Infection": "",
    "Metabolism & Cellular Stress": "",
    "Reproduction & Sex Differences": "",
    "Humans": "",
    "Rodents": "",
    "Invertebrates": "",
    "Plants": "",
    "Microorganism and Viruses": ""
}



labels = list(categories.keys())

#device = 0 if torch.cuda.is_available() else -1  
# Load zero-shot classification pipeline
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli", device=-1)


def categorize(text):
    result = classifier(text[:1000], labels)
    return result["labels"][0]

print("check")
# Add results to dataset
print(df['Title'].apply(categorize))
# Save new dataset
df.to_csv("data/papers_categorized.csv", index=False)

print("\n✅ Categorization complete!")
print(f"Results saved to 'SB_publication_PMC_categorized.csv'")