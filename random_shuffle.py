import os
import random
import json


if __name__ == '__main__':

    # append `tmp_` to all files
    raw_image_filelist = os.listdir('output-images')
    if '.DS_Store' in raw_image_filelist:
        raw_image_filelist.remove('.DS_Store')
    unique_list = list(set(raw_image_filelist))
    print(f"Before running distinct: {len(raw_image_filelist)}. After running distinct: {len(unique_list)}")

    for raw_image in raw_image_filelist:

        old_image_file = os.path.join("output-images", raw_image)
        new_image_file = os.path.join("output-images", f"tmp_{raw_image}")
        os.rename(old_image_file, new_image_file)

        raw_json = raw_image.replace(".png", "")
        old_json_file = os.path.join("output-jsons", raw_json)
        new_json_file = os.path.join("output-jsons", f"tmp_{raw_json}")
        os.rename(old_json_file, new_json_file)

    # randomly shuffle and rename files based on index
    raw_image_filelist = os.listdir('output-images')
    if '.DS_Store' in raw_image_filelist:
        raw_image_filelist.remove('.DS_Store')
    print(f"Pre-shuffled file list of length {len(raw_image_filelist)} is: {raw_image_filelist}")

    shuffled_image_filelist = random.sample(raw_image_filelist, len(raw_image_filelist))
    print(f"Shuffled file list of length {len(shuffled_image_filelist)} is: {shuffled_image_filelist}")

    for index, filename in enumerate(shuffled_image_filelist):

        old_image_file = os.path.join("output-images", filename)
        new_image_file = os.path.join("output-images", f"{index}.png")
        os.rename(old_image_file, new_image_file)

        raw_json = filename.replace(".png", "")
        old_json_file = os.path.join("output-jsons", raw_json)
        new_json_file = os.path.join("output-jsons", str(index))
        os.rename(old_json_file, new_json_file)

        with open(new_json_file) as f:
            metadata_data = json.load(f)
            metadata_data['description'] = "Aiko Virtual is a collection of 8,888 generative portrait artworks."
            metadata_data['name'] = f"Aiko #{index}"

        with open(new_json_file, 'w') as f:
            # json.dump(metadata_data, f)
            json.dump(metadata_data, f, indent=4)
