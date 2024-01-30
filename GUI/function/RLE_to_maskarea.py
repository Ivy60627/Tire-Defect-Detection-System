import os
import numpy as np
import pycocotools.mask as mask_util
import json


class RLEtoMaskArea():
    def __init__(self):  
        self.json_file_path = "outputs/preds/"
        self.json_out_file_path = "outputs/areas/"
        self.newdict={}
        self.json_list=[]
        self.maskarea=[]
        
    def read_json(self):
        for root,dirs,files in os.walk(self.json_file_path):
        	for file in files:
        		self.json_list.append(file)          
        return self.json_list
        

    def RLE_to_maskarea(self, json_list):
        for json_file in json_list:        
            f = open(self.json_file_path + json_file) 
            data = json.load(f)
             
            # check the masks is exists
            if "masks" not in data:
                print(f"The file {json_file} doesn't have masks.")
                continue
                
            # decode the RLE code and calculate the mask's area
            for i, _ in enumerate(data["labels"]):
                mask_decode = mask_util.decode(data["masks"][i])
                self.maskarea.append(np.count_nonzero(mask_decode))
            
            # TODO json改成名字:總area大小
            
                        
            self.newdict["labels"]=data['labels']
            self.newdict["maskarea"]=self.maskarea
            
            tf = open(self.json_out_file_path + json_file, "w")
            json.dump(self.newdict,tf)
            tf.close()
            print(f"Convert {json_file} successfully.")
            self.maskarea=[]
