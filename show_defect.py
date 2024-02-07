import os
import json

json_file_path = "outputs/areas/"
defect={}
json_list=[]

for num in range(7):
    defect[num]=[]
    
def get_key(dict, value):
    return [k for k, v in dict.items() if v in dict.value()]

for root,dirs,files in os.walk(json_file_path):
	for file in files:
		json_list.append(file)          
 

for json_file in json_list:        
    f = open(json_file_path + json_file) 
    data = json.load(f)
     
    # check the masks is exists
    if "maskarea" not in data:
        print(f"The file {json_file} doesn't have maskarea.")
        continue
    
    label = list(set(data["labels"]))
    
    for defect_num in label:
        defect[defect_num].append(json_file[6:8]) #[0:7]
        
for i in defect:
    print(defect[i])
        
