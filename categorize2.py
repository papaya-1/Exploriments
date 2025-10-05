import pandas as pd
import re
import tqdm

df = pd.read_csv("SB_Publication_PMC.csv")

categories = {
    "Altered Gravity": ["gravity", "flight", "weightless", "suspension", "hypergravity"],
    "Radiation": ["radiation", "ionizing", "hze", "gamma", "proton"],
    "ISS": ["space station", "ISS"],
    "Mars": ["mars", "martian"],
    "Moon": ["lunar", "moon"],
    "Musculoskeletal": ['muscle', 'bone', 'osteoclastic', 'osteolysis', 'skeletal', 'atrophy', 'cartilage', 'tendon', 'spine'],
    "Cardiovascular & Vascular": ['cardiovascular', 'cardiac', 'vascular', 'blood', 'artery', 'progenitor'],
    "Neuroscience & Sensory": ['brain', 'neurogenesis', 'retina', 'ocular', 'optic', 'vestibular', 'oligodendrocyte', 'progenitors', 'neuro-inflammation', 'olfactory'],
    "Immune Response & Infection": ['immune', 'microbe', 'antimicrobial', 'host', 'pathogen', 'viral', 't-cell', 'macrophage', 'neutrophil', 'lymphocyte'],
    "Metabolism & Cellular Stress": ['oxidative', 'stress', 'redox', 'dysregulation', 'mitochondria', 'leptin signaling', 'aging', 'frailty', 'insulin', 'telomere'],
    "Reproduction & Sex Differences": ['reproduce', 'reproduct', 'estrous', 'gonadectomy', 'sex', 'gender', 'infants'],
    "Humans": ['human', 'astronauts', 'crew', 'person', 'people'],
    "Rodents": ['mice', 'mouse', 'murine', 'rat'],
    "Invertebrates": ['invertebrate', 'drosophila', 'nematodes', 'tardigrades', 'toadfish', 'snail', 'squid'],
    "Plants": ['plant', 'stem', 'root', 'seed', 'arabidopsis', 'populus', 'lettuce', 'mustard', 'veg'],
    "Microorganism and Viruses": ['microbe', 'microbial', 'bacteria', 'fungi', 'yeast', 'microbiome', 'virus', 'viral', 'biofilm', 'amr', 'microorganism']
}

def categorize_title(titlebad, cats):
    title = titlebad.lower()
    matched = []
    for cate, keywords in cats.item():
        for key in keywords:
            if re.search(rf"\b{re.escape(key)}\b", title_lower):
                matched.append(category)
                break
    return matched

tqdm.pandas(dec="Categorizing")
df["Categories"] = df["Title"].fillna("").progress_apply(lambda x: categorize_title(x, categories))
print(df.head())