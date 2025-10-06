# 🌍 Exploriments by Planet Ptown  
### *NASA Space Apps Challenge 2025 Submission* 
#### *Exploring Life Science Discoveries Beyond Earth*

![NASA Badge](https://img.shields.io/badge/NASA%20Space%20Apps-2025-blue?style=for-the-badge&logo=nasa)
![Python](https://img.shields.io/badge/Python-3.10%2B-yellow?style=for-the-badge&logo=python)
![Hugging%20Face](https://img.shields.io/badge/AI%20Powered%20by-Hugging%20Face-orange?style=for-the-badge&logo=huggingface)
![GitHub Codespaces](https://img.shields.io/badge/Built%20in-GitHub%20Codespaces-purple?style=for-the-badge&logo=github)
![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

---

## 🌌 Overview

**Exploriments** is our official submission for the **NASA Space Apps Challenge 2025** —  
an AI-powered research navigator designed to make NASA’s *Space Biology* research more accessible and understandable.  

Our project automatically collects, categorizes, and summarizes scientific papers focused on **environmental factors**, **biological systems**, **living systems**, etc studied in space, into categories such as **microgravity**, **neuroscience**, **immune response**, **metabolism**, and **microrganisms**.  

It has the logic for extracting full-text papers, uses **Hugging Face AI models** for summarization, and categorizes articles. 

This repo contains the backend logic for our program with the front-end developed on Figma to show how it will eventually be trasferred over as a website. 

---

## 🚀 Features

- 🛰️ **Automatic Paper Extraction**  
  Downloads and extracts text from NASA open-access biology publications (WIP, see file for more info)

- 🧠 **AI Summarization & Categorization**  
  - Classifies research papers 
  - Uses Hugging Face Transformers to summarize research

- 💻 **Interactive Web Interface**  
  - Displays categorized summaries with search and filter controls (on Figma)

---

## 🧩 Tech Stack

| Layer | Technology | Purpose |
|--------|-------------|----------|
| **Backend** | Python (Requests, BeautifulSoup, PDFPlumber, Pandas) | Extracts text and images |
| **AI Models** | Hugging Face Transformers, Notebook LM | Summarization, Keyword Identification |
| **Frontend** | Figma | Displays summaries and adds interactivity |
| **Design** | Figma | UI/UX layout and visual design |
| **Environment** | GitHub Codespaces | Development & collaboration |
| **Hosting** | GitHub Pages | Public web access |

