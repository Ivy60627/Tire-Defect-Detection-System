import os
import json


class ShowDefect():
    def __init__(self):  
        self.json_defect_file_path = "outputs/areas/"
        self.defect={}
        self.json_list=[]
        for num in range(7):
            self.defect[num]=[]
        
    def read_json(self):
        for root,dirs,files in os.walk(self.json_defect_file_path):
        	for file in files:
        		self.json_list.append(file)          
        return self.json_list    
    
    def get_key(self, dict, value):
        return [k for k, v in dict.items() if v in dict.value()]
    
    def show_defect(self, json_list):
        for json_file in json_list:        
            f = open(self.json_defect_file_path + json_file) 
            data = json.load(f)
                  
            # check the masks is exists
            if "maskarea" not in data:
                print(f"The file {json_file} doesn't have maskarea.")
                continue
            
            label = list(set(data["labels"]))            
            for defect_num in label:
                self.defect[defect_num].append(json_file[6:7])
                
        return self.defect   
