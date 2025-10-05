#data handling
import pandas as pd
#text pattern matching
import re
#running pretrained AI models
from transformers import pipeline, AutoTokenizer

# loading extracted data, quote char for any commas in text so it isn't interpreted as a column, on_bad_lines to skip any lines causing issues
df = pd.read_csv("data/extracted_papers.csv", engine = "python", quotechar = '"', on_bad_lines = 'skip', skipinitialspace = True)

# loads summarizer model 
model_name = "facebook/bart-large-cnn"
summarizer = pipeline("summarization", model = model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
summaries = []

#extracting only from abstract section 
def extract_abstract(entire_text):

    #remove spacing and cap sensitivity 
    text = str(entire_text).replace("\n", "").strip()
    #find text after abstract but before intro 
    match = re.search(r"(?i)abstract[:\s]*(.*?)(?=(introduction)[:\s])", text)
    if match: 
        #returns solely the abstract
        return match.group(1).strip()
    else:
        #if the section can't be found, takes the first 300 words since that is the typical length of an abstract
        return text[:300]; 

#Old code - doesn't work because hugging face can't process over a certain token limit so abstract gets cut off and the whole thing isn't processed properlu
#def summarize(text):
        #running summary model 
        #summary = summarizer(text, max_length=300, min_length = 50, do_sample = False)
        #return summary[0]["summary_text"]

#splits 
def section_text()

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
