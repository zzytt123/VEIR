import cv2
import numpy as np
import time
import random
def process_image(image_path,vector_s):
    # Define the empty vector l
    l = []

    # Read image
    image = cv2.imread(image_path)

    # Dividing the image into r,g,b channel
    r, g, b = cv2.split(image)


    # Get the height and width of the image
    height, width = r.shape
    s_index = 0
    # Traverse each 2x1 block in the image
    for i in range(0, height, 2):
        for j in range(width):
            # Remove a block from the three grayscale images
            r_block = r[i:i+2, j]
            g_block = g[i:i+2, j]
            b_block = b[i:i+2, j]

            # Check that each of these three blocks is satisfied that the first 2 bits of all pixels in the block are the same
            r_check = np.all(r_block & 0b10000000 == r_block[0] & 0b10000000)
            g_check = np.all(g_block & 0b10000000 == g_block[0] & 0b10000000)
            b_check = np.all(b_block & 0b10000000 == b_block[0] & 0b10000000)

            # If the condition is met, add an element of value 1 to l, otherwise add 0
            if r_check and g_check and b_check:
                l.append(1)
                for block in [r_block, g_block, b_block]:
                    block[1] = (block[1] >> 1) | ((vector_s[s_index] & 0b1) << 7)
                    s_index = (s_index + 1) % len(vector_s)
            else:
                l.append(0)

            # Check whether the end condition is met
            if 128 + len(l) > 2 * np.sum(l):
                return l

    return l
vector_s = [random.randint(0, 1) for _ in range(128)]  # A secret message to embed
s=time.perf_counter()
#Select the image you want to embed
process_image('C:/Users/zyt/Desktop/enc/sailboat_encrypted_64.bmp',vector_s)
e=time.perf_counter()
print((e-s)*1000)