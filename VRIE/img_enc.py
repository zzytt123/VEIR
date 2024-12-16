import numpy as np
from PIL import Image
import random
import time
import os

def scramble_and_encrypt(channel_array, seed, block_size):
    num_blocks_per_row = channel_array.shape[1] // block_size[1]
    num_blocks_per_col = channel_array.shape[0] // block_size[0]

    # Block scrambling
    blocks = [channel_array[i:i + block_size[0], j:j + block_size[1]]
              for i in range(0, num_blocks_per_col * block_size[0], block_size[0])
              for j in range(0, num_blocks_per_row * block_size[1], block_size[1])]

    np.random.seed(seed)
    random_list = np.random.permutation(len(blocks))
    blocks = [blocks[i] for i in random_list]

    # XOR encryption
    random.seed(seed)
    encrypted_blocks = []
    for i, block in enumerate(blocks):
        block_height, block_width = block.shape
        block_flat = block.flatten()
        block_bin = np.array([list(format(val, '08b')) for val in block_flat]).flatten()
        random_string = np.random.randint(2, size=block_height * block_width * 8).astype(int)  #Stream password, using random numbers instead to test the effect
        xor = np.logical_xor(block_bin.astype(int), random_string).astype(int).astype(str)
        encrypted_block = np.packbits(np.array([int(x) for x in xor])).reshape(block_height, block_width)
        encrypted_blocks.append(encrypted_block)

    # Combining blocks back into a single array
    new_channel_array = np.concatenate(
        [np.concatenate(encrypted_blocks[i:i + num_blocks_per_row], axis=1)
         for i in range(0, len(encrypted_blocks), num_blocks_per_row)],
        axis=0
    )

    # Handle the remaining part on the right side
    if channel_array.shape[1] % block_size[1] != 0:
        right_remain = channel_array[:num_blocks_per_col * block_size[0], num_blocks_per_row * block_size[1]:]
        right_remain_encrypted = scramble_and_encrypt(right_remain, seed, (block_size[0], right_remain.shape[1]))
        new_channel_array = np.concatenate([new_channel_array, right_remain_encrypted], axis=1)

    # Handle the remaining part at the bottom
    if channel_array.shape[0] % block_size[0] != 0:
        bottom_remain = channel_array[num_blocks_per_col * block_size[0]:, :]
        bottom_remain_encrypted = scramble_and_encrypt(bottom_remain, seed, (bottom_remain.shape[0], block_size[1]))
        new_channel_array = np.concatenate([new_channel_array, bottom_remain_encrypted], axis=0)

    return new_channel_array

def encrypt_images_in_folder(folder_path, rand_num, block_size, output_folder=None):
    if output_folder is None:
        output_folder = folder_path

    # Iterate through all the files in the folder
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        # Check whether it is an image file
        if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            # Read image
            img = Image.open(file_path)
            r, g, b = img.split()
            r_array = np.array(r)
            g_array = np.array(g)
            b_array = np.array(b)

            # Encrypt each channel of the image
            new_r = scramble_and_encrypt(r_array, rand_num, block_size)
            new_g = scramble_and_encrypt(g_array, rand_num, block_size)
            new_b = scramble_and_encrypt(b_array, rand_num, block_size)

            # Splice the three channels into a new image
            new_image = Image.merge('RGB', [Image.fromarray(new_r), Image.fromarray(new_g), Image.fromarray(new_b)])

            # save new image
            encrypted_file_name = os.path.splitext(file_name)[0] + '_encrypted_64.bmp'
            encrypted_file_path = os.path.join(output_folder, encrypted_file_name)
            new_image.save(encrypted_file_path)


block_size = [64,64]  # Define block size
rand_num = (2023)
folder_path='C:/Users/zyt/Desktop/testt'   # Folder to store test images
output_folder='C:/Users/zyt/Desktop/enc'   # Folder to store encrypted images
start = time.perf_counter()
encrypt_images_in_folder(folder_path,rand_num,block_size,output_folder)
end = time.perf_counter()
print('加密时间',(end-start),'s')