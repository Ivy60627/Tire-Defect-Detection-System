label = [1, 2, 4, 3, 2, 3]
mask = [3, 4, 5, 5, 1, 6]


def add_masks(labels, mask):

    def find_indices(labels, value):
        return [index for index, element in enumerate(labels) if element == value]
        
    values = []

    for i in [find_indices(labels, x) for x in set(labels)]:
        values.append(sum([mask[x] for x in i]))

    return list(set(labels)), values

new_labels, new_masks = add_masks(label, mask)
print(new_labels, new_masks, sep='\n')


label= [0, 3, 3, 5, 3, 4, 4, 2]
maskarea= [2, 5, 5, 10, 8, 1, 3, 5]

for i, _ in enumerate(label):
    for j, _ in enumerate(label):
        if i==j:
            break
        if label[i] == label[j]:
            maskarea[i]=maskarea[i]+maskarea[j]
            label.pop(j)
            maskarea.pop(j)
            

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
