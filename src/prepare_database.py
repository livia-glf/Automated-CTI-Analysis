from ast import keyword
import json
import os 
import pandas as pd 

data = 'dataset_full.json'

# reading json: 
with open(data) as file:
    open_data = json.load(file)

# convert json to dataframe:
df = pd.DataFrame.from_dict(data, orient='index', columns = ['URL', 'MITRE domain', 'Tactic name', 'Technique name', 'Technique ID' ])

print(df)

#df.reset_index(level=0, inplace=True)

#ent_df.info()
#print(df.groupby(df[:,3]))
#ent_df.aggregate(ent_df[0])





#def _concate_json(path_json1, path_json2):
#    dataset1 = json.loads(open(path_json1))
#    dataset2 = json.loads(open(path_json2))

#    merged_dict = {key: value for (key, value) in (dataset1.items() + dataset2.items())}

    # string dump of the merged dict
#    jsonString_merged = json.dumps(merged_dict)

