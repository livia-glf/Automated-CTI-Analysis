from ast import keyword
import os
import json
from collections import defaultdict # generates default key if missing 

dataset1 = defaultdict(list)
dataset2 = defaultdict(list)
dataset3 = defaultdict(list)
dataset4 = defaultdict(list)
dataset5 = defaultdict(list)
rows = []

with open('malware.json') as malware_file:
    malwares = json.load(malware_file)

malware_urls = set()

for malware in malwares:
    for url in malware['urls']:
        malware_urls.add(url)
print("malware url count", len(malware_urls))
# loop through enterprise attack-pattern:
root_folder = '../data/'
folder_names = ['enterprise-attack-pattern', 'ics-attack-pattern']
for folder_name in folder_names: 
    folder = os.path.join(root_folder, folder_name)
    for filename in os.listdir(folder): 
        if filename.endswith('.json'):
            with open(os.path.join(folder, filename)) as file:
                file_json = json.load(file)["objects"][0] 

                # retrieve information:
                urls = []
                tactic_name = []
                for tactic in file_json['kill_chain_phases']: # tactic name 
                    tactic_name.append(tactic['phase_name']) 
                tech_name = file_json['name'] # technique name
                tech_id = file_json['external_references'][0]['external_id'] # retrieve technique id
                mitre_domain = file_json['x_mitre_domains']
                description = file_json['description']
                
                for ref in file_json['external_references'][1:]:
                    if 'url' in ref: # check if source has url 
                        url = ref['url'] # retrieve url 

                        # filtering out unecessary reports:
                        filtering = ['microsoft', 'apple', 'github', 'wikipedia', \
                            'support.office', 'amazon', 'gitlab', 'capec', 'docker', 'youtube', 'google', 'mitre', 'zip']
                        
                        #if filtering not in url:  
                        urls.append(url)
                        if url in malware_urls:
                            dataset = dataset1
                        elif all(keyword not in url.lower() for keyword in filtering):
                            dataset = dataset2
                        else:
                            dataset = dataset3
                        dataset[url].append((mitre_domain, tactic_name, tech_name, tech_id))
                rows.append({
                'name':tech_name,
                'id':tech_id, 
                'tactic': tactic_name,
                'filename' : filename,         
                #'description':description,
                'mitre_domain': mitre_domain,
                'urls':urls
            })    

dataset4 = dataset1.copy()
dataset4.update(dataset2)

for name, dataset in [('dataset_malware.json', dataset1), ('dataset_no_malware.json', dataset2), ('dataset_with_keywords.json', dataset3), \
    ('dataset_full.json', dataset4)]:
    print(name, len(dataset))
    with open(name, 'w') as file:
        json.dump(dataset, file)

with open('techniques.json', 'w') as file:
    json.dump(rows, file)