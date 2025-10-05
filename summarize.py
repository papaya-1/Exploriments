#data handling
import pandas as pd
#text pattern matching
import re
#running pretrained AI models
from transformers import pipeline

# loading extracted data, quote char for any commas in text so it isn't interpreted as a column, on_bad_lines to skip any lines causing issues
df = pd.read_csv("data/extracted_papers.csv", engine = "python", quotechar = '"', on_bad_lines = 'skip')

# loads summarizer model 
summarizer = pipeline("summarization", model = "facebook/bart-large-cnn")
summaries = []

#extracting only from abstract section 
def extract_abstract(entire_text):

    #remove spacing and cap sensitivity 
    text = str(entire_text).replace("\n", "").strip()

    #find text after abstract but before intro 
    match = re.search(r"(?i)abstract[:\s]*(.*?)(?=(introduction)[:\s])", text)

    if match: 
        #returns solely the abstract
        return match.group(1).strip 
    else:
        #if the section can't be found, takes the first 300 words since that is the typical length of an abstract
        return text[:300]; 

def summarize(text):

    #reduces text if it is too long so hugging face can process 
    text = text[:1000];

    #running summary model 
    summary = summarizer(text, max_length=150, min_length = 50, do_sample = False)

    return summary

#extract abstract for every paper 
for i, row in df.iterrows():
    title = str(row["title"]);

    #checking to make sure it is a string
    entire_text = str(row["entire_text"]).strip()

    #extracting abstract and saving it to a var
    abstract = extract_abstract(entire_text)

    #if abstract isn't found
    if len (abstract) < 10:
        print(f" No abstract for '{title}'. Summary will be denoted as 'No summary available'")
        summary = "No summary available";
    
    #if abstract is found -> summarize
    else:
        print(f"{title} summarized")
        summary = summarize(abstract)

    #save summaries to list
    summaries.append({
        "title": title,
        "summary": summary
    })

#save summaries to CSV
csv = "summaries.csv";
pd.DataFrame(summaries).to_csv(csv, index = False)

print("Summaries finished")

