from ast import keyword
import json
import os 
import pandas as pd 

ent = 'ent_dataset.json'
ics = 'ics_dataset.json'

# reading json: 
with open(ent) as ent_file:
    open_ent = json.load(ent_file)

# convert json to dataframe:
ent_df = pd.DataFrame.from_dict(open_ent, orient = 'index')
ent_df.reset_index(level=0, inplace=True)

#ent_df.info()

ent_df.groupby(ent_df[3])
ent_df.aggregate(ent_df[0])



#def _concate_json(path_json1, path_json2):
#    dataset1 = json.loads(open(path_json1))
#    dataset2 = json.loads(open(path_json2))

#    merged_dict = {key: value for (key, value) in (dataset1.items() + dataset2.items())}

    # string dump of the merged dict
#    jsonString_merged = json.dumps(merged_dict)

