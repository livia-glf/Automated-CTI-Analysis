import os
import json
from collections import defaultdict # generates default key if missing 

dataset = defaultdict(list)

# loop through enterprise attack-pattern:
folder_name = '/homes/lgf21/AutomatedCTI/CTI Analysis/Automated-CTI-Analysis/data/ics-attack-pattern' 
for filename in os.listdir(folder_name): 
    if filename.endswith('.json'):
        with open(os.path.join(folder_name, filename)) as file:
            file_json = json.load(file)["objects"][0] 

            # retrieve information:
            urls = []
            tactic_name = []
            for tactic in file_json['kill_chain_phases']: # tactic name 
                tactic_name.append(tactic['phase_name']) 
            tech_name = file_json['name'] # technique name
            tech_id = file_json['external_references'][0]['external_id'] # retrieve technique id
            #description = file_json['description']
            #mitre_domain = file_json['x_mitre_domains']
        
            for ref in file_json['external_references'][1:]:
                if 'url' in ref: # check if source has url 
                    url = ref['url'] # retrieve url 
                    
                    # data cleaning: 
                    filtering = ['youtube', 'mitre']
                    if filtering not in url:
                        urls.append(url)
                        dataset[url].append((tactic_name, tech_name, tech_id))    

keys = len(list(dataset.keys())) 
print(keys) 
            
with open('ics_dataset.json', 'w') as file:
   json.dump(dataset, file)