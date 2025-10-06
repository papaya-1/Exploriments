# Use of AI
   # Used ChatGPT for basic structure and notebook LM to generate keywords

#Code starts here

import pandas as pd
import re
import tqdm

df = pd.read_csv("data/SB_publication_PMC.csv")

categories = {
   "Altered Gravity": ["gravity", "flight", "weightless", "suspension", "hypergravity"],
   "Radiation": ["radiation", "ionizing", "hze", "gamma", "proton"],
   "ISS": ["space station", "ISS"],
   "Mars": ["mars", "martian"],
   "Moon": ["lunar", "moon"],
   "Musculoskeletal": ['muscle', 'bone', 'osteoclastic', 'osteolysis', 'skeletal', 'atrophy', 'cartilage', 'tendon', 'spine'],
   "Cardiovascular & Vascular": ['heart', 'vein', 'cardiovascular', 'cardiac', 'vascular', 'blood', 'artery', 'progenitor'],
   "Neuroscience & Sensory": ['brain', 'neurogenesis', 'retina', 'ocular', 'optic', 'vestibular', 'oligodendrocyte', 'progenitors', 'neuro-inflammation', 'olfactory'],
   "Immune Response & Infection": ['inflammation', 'killer', 'stem cell', 'immune', 'immunity', 'microbe', 'antimicrobial', 'host', 'pathogen', 'viral', 't-cell', 'macrophage', 'neutrophil', 'lymphocyte'],
   "Metabolism & Cellular Stress": ['oxidative', 'stress', 'redox', 'dysregulation', 'mitochondria', 'leptin signaling', 'aging', 'frailty', 'insulin', 'telomere'],
   "Reproduction & Sex Differences": ['in vitro', 'reproduce', 'reproduct', 'estrous', 'gonadectomy', 'sex', 'gender', 'infants'],
   "Humans": ['human', 'astronauts', 'crew', 'person', 'people'],
   "Rodents": ['mice', 'mouse', 'murine', 'rat'],
   "Invertebrates": ['invertebrate', 'drosophila', 'nematodes', 'tardigrades', 'toadfish', 'snail', 'squid'],
   "Plants": ['pollen', 'plant', 'root', 'seed', 'arabidopsis', 'populus', 'lettuce', 'mustard', 'veg'],
   "Microorganisms and Viruses": ['microbe', 'microbial', 'bacteria', 'fungi', 'yeast', 'microbiome', 'virus', 'viral', 'biofilm', 'amr', 'microorganism'],
   "Genetics": ['dna', "rna", "chromo", "genetic", "gene", "transcript", "genotype", "genom", "methyl", "telomere"],
   "Macromolecular Interactions": ["lipid", "protein", "membrane", "binding"]
}


def categorize_title(titlebad, categories):
   title = titlebad.lower()
   matched = []
   for cate, keywords in categories.items():
       for key in keywords:
           if key in title:
               matched.append(cate)
               break
   return matched if matched else []

df["Categories"] = df["Title"].apply(lambda x: categorize_title(x, categories))
df.to_csv("SB_publication_categorized.csv", index=False)
