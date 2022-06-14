import json
import os 

def _concate_json(path_json1, path_json2):
    dataset1 = json.loads(open(path_json1))
    dataset2 = json.loads(open(path_json2))

    merged_dict = {key: value for (key, value) in (dataset1.items() + dataset2.items())}

    # string dump of the merged dict
    jsonString_merged = json.dumps(merged_dict)