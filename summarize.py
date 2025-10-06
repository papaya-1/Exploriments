# Use of AI
    # Used ChatGPT to generate code using specific prompts defining necessary features for summarize and for faster debugging
    # Adjusted the code given based on it (ex: choosing Ai models, debugging, etc)

#Code starts here

#data handling
import pandas as pd
#text pattern matching
import re
#running pretrained AI models
from transformers import pipeline, AutoTokenizer


# loading extracted data, quote char for any commas in text so it isn't interpreted as a column, on_bad_lines to skip any lines causing issues
df = pd.read_csv("data/extracted_papers.csv", engine = "python", quotechar = '"', on_bad_lines = 'skip', skipinitialspace = True)


# loads summarizer model
model_name = "google/pegasus-xsum"
summarizer = pipeline("summarization", model = model_name)
summarizer.model.config.max_length = 512
summarizer.model.config.min_length = 30
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
       return match.group(2).strip()
   else:
        return " ".join(text.split()[:300])


#Old code - doesn't work because hugging face can't process over a certain token limit so abstract gets cut off and the whole thing isn't processed properlu
#def summarize(text):
       #running summary model
       #summary = summarizer(text, max_length=300, min_length = 50, do_sample = False)
       #return summary[0]["summary_text"]


#splits abstract into chunks that hugging face model can process
def section_text(text, max_tokens = 512):
   #tokenizing
   inputs = tokenizer(text, return_tensors="pt", truncation = False)
   tokens = inputs["input_ids"][0]
   #list of chunks
   chunks = []
   #chunk tokens, convert back to text and add to list
   for i in range(0, len(tokens), max_tokens):
       chunk = tokenizer.decode(tokens[i:i+ max_tokens], skip_special_tokens = True)
       chunks.append(chunk)
   return chunks


def summarize(text):
   #split abstract into chunks
   chunks = section_text(text)
   #list of partial summaries
   partial_summaries = []
   #summarize each chunk
   for chunk in chunks:
       summary = summarizer(chunk, max_length = 200, min_length = 50, do_sample = False)[0]["summary_text"]
       partial_summaries.append(summary)
   #combine partial summaries
   combined_summary = "".join(partial_summaries)
   #summarize partial summaires
   if len(chunks) > 1:
       final_summary = summarizer(combined_summary, max_length = 200, min_length = 50, do_sample = False)[0]["summary_text"]
       return final_summary
   else:
       return partial_summaries[0]


#extract abstract for every paper
for i, row in df.iterrows():
   title = str(row["title"]);


   #checking to make sure it is a string
   entire_text = str(row["entire_text"]).strip()


   #extracting abstract and saving it to a var
   result = extract_abstract(entire_text)


   #if result isn't found
   if len (result) < 10:
       print(f" No result for '{title}'. Summary will be denoted as 'No summary available'")
       summary = "No summary available";
  
   #if result is found -> summarize
   else:
       print(f"{title} summarized")
       summary = summarize(result)


   #save summaries to list
   summaries.append({
       "title": title,
       "summary": summary
   })


#save summaries to CSV
csv = "summaries.csv";
pd.DataFrame(summaries).to_csv(csv, index = False)


print("Summaries finished")



