# 🌍 Planet Ptown  
### *NASA Space Apps Challenge 2025 Submission* (THIS IS A SAMPLE README)  
#### *Exploring Life Science Discoveries Beyond Earth*

![NASA Badge](https://img.shields.io/badge/NASA%20Space%20Apps-2025-blue?style=for-the-badge&logo=nasa)
![Python](https://img.shields.io/badge/Python-3.10%2B-yellow?style=for-the-badge&logo=python)
![Hugging%20Face](https://img.shields.io/badge/AI%20Powered%20by-Hugging%20Face-orange?style=for-the-badge&logo=huggingface)
![GitHub Codespaces](https://img.shields.io/badge/Built%20in-GitHub%20Codespaces-purple?style=for-the-badge&logo=github)
![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

---

## 🌌 Overview

**Planet Ptown** is our official submission for the **NASA Space Apps Challenge 2025** —  
an AI-powered research explorer designed to make NASA’s *Space Biology* research more accessible and understandable.  

Our project automatically collects, categorizes, and summarizes scientific papers focused on **environmental factors**, **analogs**, and **platforms** studied in space — including **microgravity**, **radiation**, **ISS**, **Mars**, and **the Moon**.  

It extracts full-text papers, retrieves key images and graphs, uses **Hugging Face AI models** for summarization, and displays everything on a clean, interactive web interface.

---

## 🚀 Features

- 🛰️ **Automatic Paper Extraction**  
  Downloads and extracts text + images from NASA open-access biology publications.

- 🧠 **AI Summarization & Categorization**  
  Uses Hugging Face Transformers to summarize and classify research into:
  - Altered Gravity  
  - Radiation  
  - ISS  
  - Mars  
  - Moon  

- 📊 **Graph & Image Retrieval**  
  Pulls up to 3 figures or graphs from each paper.

- 💻 **Interactive Web Interface**  
  Displays categorized summaries with search and filter controls.

- 🌐 **Built in GitHub Codespaces**  
  Fully cloud-based — no setup required on your computer.

---

## 🧩 Tech Stack

| Layer | Technology | Purpose |
|--------|-------------|----------|
| **Backend** | Python (Requests, BeautifulSoup, PDFPlumber, Pandas) | Extracts text and images |
| **AI Models** | Hugging Face Transformers + KeyBERT | Summarization & Keyword Extraction |
| **Frontend** | HTML, CSS, JavaScript | Displays summaries and adds interactivity |
| **Design** | Figma | UI/UX layout and visual design |
| **Environment** | GitHub Codespaces | Development & collaboration |
| **Hosting** | GitHub Pages | Public web access |

---

## 🧠 How It Works

### 1️⃣ Extract Papers  
Pulls the list of scientific papers and gathers text + images.

```bash
python extract_papers.py