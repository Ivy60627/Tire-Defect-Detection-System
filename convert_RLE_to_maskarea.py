import os
import numpy as np
import pycocotools.mask as mask_util
import json

json_file_path = "outputs/preds/"
json_out_file_path = "outputs/areas/"

newdict={}
json_list=[]
maskarea=[]

for root,dirs,files in os.walk(json_file_path):
	for file in files:
		json_list.append(file)

for json_file in json_list:        
    # returns JSON object as a dictionary
    f = open(json_file_path + json_file) 
    data = json.load(f)
     
    # check the masks is exists
    if "masks" not in data:
        print(f"The file {json_file} doesn't have masks.")
        continue
        
    # decode the RLE code and calculate the mask's area
    for i, _ in enumerate(data["labels"]):
        mask_decode = mask_util.decode(data["masks"][i])
        maskarea.append(np.count_nonzero(mask_decode))
        
    newdict["labels"]=data['labels']
    newdict["maskarea"]=maskarea
    
    json_out_file = str(json_out_file_path + json_file)
    tf = open(json_out_file, "w")
    json.dump(newdict,tf)
    tf.close()
    print(f"Convert {json_file} successfully.")

