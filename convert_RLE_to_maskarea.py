import os
import numpy as np
import pycocotools.mask as mask_util
import json

json_file_path = "outputs/preds/"
json_out_file_path = "outputs/areas/"

newdict={}
json_list=[]
maskarea=[]

def add_masks(labels, mask):

    def find_indices(labels: list, value: int) -> list:
        """
        Get the index list of the specific elements
        :labels: The label list
        :value: The element that will get the indexs in labels list
        :Return: return the list of indexs

        example:
        labels = [1, 2, 2, 3, 2, 3]
        value = 2
        return: [1, 2, 4]

        """

        return [index for index, element in enumerate(labels) if element == value]

    label_element_index_list = [find_indices(labels, x) for x in set(labels)]

    new_mask = []
    for index in label_element_index_list:
        element_masks_sum = sum([mask[x] for x in index])
        new_mask.append(element_masks_sum)

    return list(set(labels)), new_mask

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
 
    
    newdict["labels"], newdict["maskarea"]=add_masks(data["labels"], maskarea)
    


        
    json_out_file = str(json_out_file_path + json_file)
    tf = open(json_out_file, "w")
    json.dump(newdict,tf)
    tf.close()
    print(f"Convert {json_file} successfully.")
    maskarea=[]

