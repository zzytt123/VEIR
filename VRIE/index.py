import time
import numpy as np
labels=[]
img_num=1000
total_labels=80
labels = np.array([])  # Initializes an empty array
with open('C:/Users/zyt/Desktop/labels.txt', 'r') as f:  # Open fileIt ,can be understood as a bitmap after transposition, each representing the value of all feature vectors of an image
    for i, line in enumerate(f):
        if i == img_num:
            break
        split_data = line.strip().split('. ')  # Remove the newline and press. Separate each element
        row = [float(x) for x in split_data]  # Convert each element to a floating point number
        labels = np.append(labels, row)  # Add the line to the array
# Converts a one-dimensional array to a two-dimensional array
labels = labels.reshape((img_num, len(split_data)))
labels_t=labels.T





query = ['0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '1', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0']
#tag records the position of the label in the query vector
tag = [i for i, q in enumerate(query) if q == '1']
result_set=[]
if not tag:
    print('no result!')
else:
    start = time.perf_counter()
    #index_set stores the bitmap, the label vector is 24 dimensional, the image number is 4000, and the bitmap size is 24*4000
    #Initialize result to the tag[0] row of index_set, that is, make result equal to the row in the bitmap corresponding to the first tag of the query vector
    result = labels_t[tag[0]]
    for i in tag[1:]:
        #Let the rows in the bitmap corresponding to the labels of the result and query vectors operate with and, if both are 1, the result is 1, otherwise it is 0
        result += labels_t[i]
    #In the final result, the position of element 1 is the queried image

    for i in range(len(result)):
        if result[i]>1:
            result_set.append(str(i+1))
    end = time.perf_counter()
    print(result_set[0:49])
print('检索时间',(end-start)*1000,'ms')

