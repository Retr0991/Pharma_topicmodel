import openai, json, time
import pandas as pd
from bertopic import BERTopic
from bertopic.representation import OpenAI
import os

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Access the API key
api_key = os.getenv("API_KEY")


# returns topic_number, count, name
# -1 in topic_number repersents outlier
def get_tops(drug, df):
    df1 = df[df['drugName'] == drug]

    df1 = df1[df1['condition'] != 'Not Listed / Othe']
    df1.dropna(inplace=True)

    li = df1.review.to_list()
    li_new = []
    for ele in li:
        li_new.append(ele[1:-1])
    li = li_new

    # use your own key
    client = openai.OpenAI(api_key=api_key)
    representation_model = OpenAI(client, model="gpt-3.5-turbo", chat=True)
    topic_model = BERTopic(representation_model=representation_model)
    _, _ = topic_model.fit_transform(li)
    df = topic_model.get_topic_info()
    fin = []
    for i in range(len(df)):
        fin.append((df.iloc[i].Topic, df.iloc[i].Count, df.iloc[i].Name, df.iloc[i].Representative_Docs))
    
    return fin


data_path = r"C:\Users\Retr0991\ML stuf\Phama_topicmodel\pharma_shit\drugsComTrain_raw.csv"


df = pd.read_csv(data_path)
df.dropna(inplace=True)
df.drop(columns=['uniqueID'], inplace=True)
li = df['drugName'].to_list()

d = {}
for ele in li:
    if ele in d:
        d[ele] += 1
    else:
        d[ele] = 1
sorted_dict = dict(sorted(d.items(), key=lambda item: item[1]))

li = []
for i in range(40):
    last_key, last_value = sorted_dict.popitem()
    li.append(((last_key, last_value)))

drug_list = [x[0] for x in li]
# top 40 drugs only
drug_list = drug_list[0:40]
data = {}
i = 1
for drug in drug_list:
    print("Generating Topics...")
    li = get_tops(drug, df)
    data[drug.replace(" ", "_").split('/')[0].rstrip("_")] = {}
    for tup in li:
        data[drug.replace(" ", "_").split('/')[0].rstrip("_")].update({f"topic_number_{int(tup[0])}" : 
                                                                       {
                                                                           "count" : int(tup[1]), 
                                                                           "name" : tup[2],
                                                                           "tweet" : {f"tweet_{i}": tup[3][i] for i in range(len(tup[3]))}
                                                                        }
                                                                    })
    print(i, end = " ")
    time.sleep(21)
    print("wait done")
    i += 1
        
# Path to save the CSV file
# csv_file_path = 'data.csv'

# Write the data to a CSV file
with open("data.json", "w") as json_file:
    json.dump(data, json_file, indent=4)

print("DONE")

    
