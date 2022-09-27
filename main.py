import os
from PIL import Image
from config import GeneratorConfig
from random_gen import get_random_index
import random
import time
import json
from metadata_example import metadata_template
import shutil


def create_filename_map(group_trait_prob_keys, trait_nums_indices, trait_directories):
    """
    :param group_trait_prob_keys: list of form ["bg", "co", "ey", "hr", "fa", "ha", "gr"]
    :param trait_nums_indices: dict of form {"trait_index": "trait_index", "trait_key": "trait_key"}
    :param trait_directories: dict of trait abbreviations to full directory names
    :return: dict of form {"trait" : trait_directory_name/trait_key.png""}
    """
    trait_to_filenames = {}
    suffixes = []

    for trait in group_trait_prob_keys:
        trait_to_filenames[trait] = f"{trait_directories[trait]}/{trait_nums_indices[trait]['trait_key']}.png"
        suffixes.append(trait_nums_indices[trait]['trait_key'])

    # compile variant nums and add as suffix
    trait_to_filenames['suffix'] = "_".join(suffixes)

    return trait_to_filenames


def create_image_composite(trait_to_filenames, class_type, nft_index):
    """
    xxx
    :param trait_to_filenames:
    :param x:
    :return:
    """
    base_path = os.path.join(os.path.abspath(os.getcwd()), "raw-images")

    gr_doubles = [
        "gears/gr_11_sub_1.png",
        "gears/gr_11_sub_2.png",
        "gears/gr_11_sub_3.png",
        "gears/gr_12_sub_1.png",
        "gears/gr_12_sub_2.png",
        "gears/gr_12_sub_3.png",
        "gears/gr_13_sub_1.png",
        "gears/gr_13_sub_2.png",
        "gears/gr_13_sub_3.png",
        "gears/gr_14_sub_1.png",
        "gears/gr_14_sub_2.png",
        "gears/gr_14_sub_3.png",
        "gears/gr_15_sub_1.png",
        "gears/gr_15_sub_2.png",
        "gears/gr_15_sub_3.png",
        "gears/gr_16_sub_1.png",
        "gears/gr_16_sub_2.png",
        "gears/gr_16_sub_3.png",
        "gears/gr_17_sub_1.png",
        "gears/gr_17_sub_2.png",
        "gears/gr_17_sub_3.png",
        "gears/gr_18_sub_1.png",
        "gears/gr_18_sub_2.png",
        "gears/gr_18_sub_3.png",
        "gears/gr_19_sub_1.png",
        "gears/gr_19_sub_2.png",
        "gears/gr_19_sub_3.png",
        "gears/gr_20_sub_1.png",
        "gears/gr_20_sub_2.png",
        "gears/gr_20_sub_3.png",
        "gears/gr_28.png"
    ]

    hr_doubles = {
        "hair/hr_13_sub_2.png": ["front", "top"],
        "hair/hr_22_sub_1.png": ["back", "front"],
        "hair/hr_22_sub_2.png": ["back", "front"],
        "hair/hr_28_sub_1.png": ["back", "front", "top"],
        "hair/hr_28_sub_2.png": ["back", "front", "top"],
        "hair/hr_29_sub_1.png": ["back", "front", "top"],
        "hair/hr_29_sub_2.png": ["back", "front", "top"],
        "hair/hr_30_sub_1.png": ["back", "front"],
        "hair/hr_30_sub_2.png": ["back", "front"],
        "hair/hr_32_sub_1.png": ["back", "front"],
        "hair/hr_32_sub_2.png": ["back", "front"],
        "hair/hr_37_sub_1.png": ["front", "top"],
        "hair/hr_37_sub_2.png": ["front", "top"],
        "hair/hr_39_sub_1.png": ["front", "top"],
        "hair/hr_39_sub_2.png": ["front", "top"]
    }

    mo_droids = [
        "mouth/mo_4.png",
        "mouth/mo_6.png",
        "mouth/mo_8.png",
        "mouth/mo_10.png",
        "mouth/mo_11.png",
        "mouth/mo_12.png",
        "mouth/mo_14.png",
        "mouth/mo_15.png",
        "mouth/mo_16.png",
        "mouth/mo_18.png",
        "mouth/mo_20.png",
        "mouth/mo_21.png",
        "mouth/mo_22.png"
    ]

    try:
        # open background image as boilerplate for composite (background always present)
        bg_full_path = os.path.join(base_path, trait_to_filenames["bg"])
        bg = Image.open(bg_full_path).convert('RGBA')
        composite = Image.new("RGBA", bg.size)
        composite = Image.alpha_composite(composite, bg)

        # create dictionary of traits to image layer objects
        trait_to_layer = {}
        for trait, filename in trait_to_filenames.items():
            if trait == "suffix":
                continue
            print(filename)

            # double gear situation
            if filename in gr_doubles:

                print('--- Double gear situation ---')

                # back layer for gears
                back_filename = filename.replace('.png', '_back.png')
                print(back_filename)
                back_layer = Image.open(os.path.join(base_path, back_filename))
                trait_to_layer[f"{trait}_back"] = back_layer

                # front layer for gears
                front_filename = filename.replace('.png', '_front.png')
                print(front_filename)
                front_layer = Image.open(os.path.join(base_path, front_filename))
                trait_to_layer[f"{trait}_front"] = front_layer

            # double hair situation
            elif filename in hr_doubles.keys():

                print('--- Double hair situation KINOKO ---')

                # loop through suffix array and add update trait_to_layer
                for suffix in hr_doubles[filename]:
                    suffix_filename = filename.replace('.png', f"_{suffix}.png")
                    print(f"Suffix filename: {suffix_filename}")
                    suffix_layer = Image.open(os.path.join(base_path, suffix_filename))
                    trait_to_layer[f"{trait}_{suffix}"] = suffix_layer

            # droid mouth situation
            elif filename in mo_droids and class_type in ['droid', 'ultra_droid']:

                # back layer for gears
                mo_droid_filename = filename.replace('.png', '_droid.png')
                print(mo_droid_filename)
                mo_droid_layer = Image.open(os.path.join(base_path, mo_droid_filename))
                trait_to_layer['mo'] = mo_droid_layer

            else:
                layer = Image.open(os.path.join(base_path, trait_to_filenames[trait]))
                trait_to_layer[trait] = layer

        # print(trait_to_layer)

        trait_ordering_default = ['cl', 'hr_back', 'co', 'hr_front', 'hr', 'ha', 'hr_top', 'gr', 'ey', 'mo', 'fa']
        trait_ordering_doubles = ['cl', 'hr_back', 'gr_back', 'co', 'hr_front', 'hr', 'ha', 'gr_front', 'hr_top', 'ey', 'mo', 'fa']

        # override default and doubles ordering for certain ha ordering cases
        ha_z_order_override = ['head-accessories/ha_3.png', 'head-accessories/ha_4.png', 'head-accessories/ha_5.png', 'head-accessories/ha_7.png']
        if 'ha' in trait_to_filenames.keys() and trait_to_filenames['ha'] in ha_z_order_override:

            # pop ha trait and move to end of list (make front most layer)
            trait_ordering_default.append(trait_ordering_default.pop(trait_ordering_default.index('ha')))
            trait_ordering_doubles.append(trait_ordering_doubles.pop(trait_ordering_doubles.index('ha')))
            print(f"KINOKO TEST FOR HA Z ORDERING OVERRIDE FOR trait_ordering_default: {trait_ordering_default}")
            print(f"KINOKO TEST FOR HA Z ORDERING OVERRIDE FOR trait_ordering_doubles: {trait_ordering_doubles}")

        # override default and doubles ordering for certain fa ordering cases
        fa_z_order_override = ['face-accessories/fa_22.png', 'face-accessories/fa_23.png']
        if 'fa' in trait_to_filenames.keys() and trait_to_filenames['fa'] in fa_z_order_override:

            # pop fa trait and move before hr layer
            trait_ordering_default.pop(trait_ordering_default.index('fa'))
            trait_ordering_default.insert(4, 'fa')
            trait_ordering_doubles.pop(trait_ordering_doubles.index('fa'))
            trait_ordering_doubles.insert(4, 'fa')
            print(f"KINOKO TEST FOR FA Z ORDERING OVERRIDE FOR trait_ordering_default: {trait_ordering_default}")
            print(f"KINOKO TEST FOR FA Z ORDERING OVERRIDE FOR trait_ordering_doubles: {trait_ordering_doubles}")

        # check if we are in a doubles or a default situation
        if ('gr_back' in trait_to_layer.keys()) or ('gr_front' in trait_to_layer.keys()):

            # print('--- Double gear situation ---')
            for trait in trait_ordering_doubles:
                if trait in trait_to_layer:
                    composite = Image.alpha_composite(composite, trait_to_layer[trait])

        else:
            for trait in trait_ordering_default:
                if trait in trait_to_layer:
                    composite = Image.alpha_composite(composite, trait_to_layer[trait])

        # Save the image
        composite = composite.save(f"output-images/{class_type}_{nft_index}_{trait_to_filenames['suffix']}.png")

    except:
        print("Failed to create image")


def create_cumulative_prob_map(trait_probs):
    cumulatives = [sum(trait_probs[0:x:1]) for x in range(0, len(trait_probs) + 1)]
    return cumulatives[1:]


def _pretty_print(target):
    # _pretty_print(trait_nums_indices)
    print(json.dumps(target, indent=4))


def clear_output_dir():

    output_dirs = ['output-images', 'output-jsons']

    for output_dir in output_dirs:
        output_json_dir_path = os.path.join(os.getcwd(), output_dir)
        try:
            shutil.rmtree(output_json_dir_path)
            print(f"Successfully deleted directory and contents at: {output_json_dir_path}")
            os.mkdir(output_json_dir_path)
            print(f"Successfully created empty directory at: {output_json_dir_path}")
        except OSError as e:
            print("Error: %s : %s" % (output_json_dir_path, e.strerror))


def generate_metadata(trait_to_filenames, class_type, nft_index):
    """
    generate metadata and write to JSON
    :param trait_to_filenames:
    :return:
    """
    trait_to_filenames_for_metadata = trait_to_filenames
    suffix_value = trait_to_filenames_for_metadata.pop('suffix')

    for key, value in trait_to_filenames_for_metadata.items():
        trait_to_filenames_for_metadata[key] = value.rsplit('/', 1)[-1].replace(".png", "")
    print(f"Metadata dictionary: {trait_to_filenames_for_metadata}")

    metadata_json = {
        "attributes": [],
        "description": "",
        "image": "",
        "name": ""
    }

    for key, value in trait_to_filenames_for_metadata.items():
        attribute_category = {
            'cl': 'Class',
            'bg': 'Background',
            'co': 'Clothing',
            'ey': 'Eyes',
            'mo': 'Mouth',
            'hr': 'Hair',
            'fa': 'Face Accessory',
            'ha': 'Head Accessory',
            'gr': 'Gears',
        }

        attribute_dict = {
            "trait_type": attribute_category[key],
            "value": config.metadata_labels[value][0]
        }

        metadata_json['attributes'].append(attribute_dict)

    # Write file to json folder
    metadata_json_path = os.path.join('output-jsons', f"{class_type}_{nft_index}_{suffix_value}")

    with open(metadata_json_path, 'w') as f:
        # json.dump(metadata_json, f)
        json.dump(metadata_json, f, indent=4)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # clear and recreate output image and metadata JSON directories
    clear_output_dir()

    # instantiate config and counter
    config = GeneratorConfig()
    nft_count = 0
    t0 = time.time()

    # generate random NFTs
    for class_type, volume in config.class_types.items():

        for nft_index in range(volume):

            print(f"----- 💫 STARTING CREATION OF NFT #{nft_count} 💫 ----- \n")

            # get class probability map
            class_type_probs = config.class_type_probs[class_type]                  # {'cl_6': 3333, 'cl_7': 3333, 'cl_8': 3333}
            class_type_prob_list = list(class_type_probs.values())                  # [3333, 3333, 3333] for human
            cl_prob_map = create_cumulative_prob_map(class_type_prob_list)          # [3333, 6666, 9999] for human
            cl_index = get_random_index(cl_prob_map)                                # ex: 0, 1, 2 for human
            cl_key = list(class_type_probs.keys())[cl_index]                        # ex: cl_6 for index 0 for human

            # roll for relevant rarity group (group 1, 2 or 3)
            group_prob_list = list(config.group_probs.values())                     # [3333, 3333, 3333]
            group_cum_prob = create_cumulative_prob_map(group_prob_list)            # [3333, 6666, 9999]
            group_index = get_random_index(group_cum_prob)                          # ex: 0, 1, 2
            group_key = list(config.group_probs.keys())[group_index]                # ex: group_1 for index 0
            # print(f"group_index: {group_index} with group_key: {group_key}")

            # given rarity group, get trait probabilities
            group_trait_probs = config.trait_probs_by_group[group_key]
            class_trait_probs = config.trait_probs_by_class[class_type]

            # build list of relevant traits for this NFT using random rolls (1.0 vs. 0.75 vs. 0.5)
            group_trait_prob_keys = []
            for trait, group_prob in group_trait_probs.items():
                if random.uniform(0, 1) <= group_prob:
                    group_trait_prob_keys.append(trait)
            print(f"Relevant traits for {group_key}: {group_trait_prob_keys}")

            # build dictionary of relevant trait indices and trait names using random rolls
            trait_nums_indices = {}
            for trait in group_trait_prob_keys:
                trait_cum_prob = config.trait_cum_probs_by_class[class_type][trait]
                trait_index = get_random_index(trait_cum_prob)
                trait_key = list(class_trait_probs[trait].keys())[trait_index]
                trait_nums_indices[trait] = {"trait_index": trait_index, "trait_key": trait_key}
                print(f"Trait: {trait} with trait_index: {trait_index} and trait_key: {trait_key}")

            # apply exclusion criteria check for hair trait and head accessory trait pair
            if 'ha' in trait_nums_indices.keys():                                               # enter if statement if ha exists (relevant for group 3 only)
                hr_trait_raw = trait_nums_indices['hr']['trait_key']                            # get initially rolled hr trait
                hr_trait = "_".join(hr_trait_raw.split("_", 2)[:2])                             # hr_1_sub_1 -> hr_1
                ha_trait = trait_nums_indices['ha']['trait_key']                                # get initially rolled ha trait

                if hr_trait in config.exclusion_criteria_hr_ha.keys():                          # only enter reroll loop if initial hr trait exists in exclusion criteria dictionary
                    while ha_trait in config.exclusion_criteria_hr_ha[hr_trait]:
                        ha_cum_prob = config.trait_cum_probs_by_class[class_type]['ha']
                        ha_index = get_random_index(ha_cum_prob)
                        ha_key = list(class_trait_probs['ha'].keys())[ha_index]
                        trait_nums_indices['ha'] = {"trait_index": ha_index, "trait_key": ha_key}
                        print(f"Given hr trait: {hr_trait}, rerolled ha trait from old value: {ha_trait} to new value: {ha_key}")
                        ha_trait = ha_key

            # apply exclusion criteria check for head accessory trait and face accessory trait pair
            if 'ha' in trait_nums_indices.keys() and 'fa' in trait_nums_indices.keys():         # enter if statement if ha exists (relevant for group 3 only)
                fa_trait = trait_nums_indices['fa']['trait_key']                                # get initially rolled ha trait
                ha_trait = trait_nums_indices['ha']['trait_key']                                # get initially rolled ha trait

                if ha_trait in config.exclusion_criteria_ha_fa.keys():                          # only enter reroll loop if initial ha trait exists in exclusion criteria dictionary
                    while fa_trait in config.exclusion_criteria_ha_fa[ha_trait]:
                        fa_cum_prob = config.trait_cum_probs_by_class[class_type]['fa']
                        fa_index = get_random_index(fa_cum_prob)
                        fa_key = list(class_trait_probs['fa'].keys())[fa_index]
                        trait_nums_indices['fa'] = {"trait_index": fa_index, "trait_key": fa_key}
                        print(f"Given ha trait: {ha_trait}, rerolled fa trait from old value: {fa_trait} to new value: {fa_key}")
                        fa_trait = fa_key

            # apply exclusion criteria check for hair trait and clothing trait pair
            hr_trait_raw = trait_nums_indices['hr']['trait_key']  # get initially rolled hr trait
            hr_trait = "_".join(hr_trait_raw.split("_", 2)[:2])  # hr_1_sub_1 -> hr_1
            co_trait = trait_nums_indices['co']['trait_key']                                # get initially rolled ha trait

            if hr_trait in config.exclusion_criteria_hr_co.keys():                          # only enter reroll loop if initial ha trait exists in exclusion criteria dictionary
                while co_trait in config.exclusion_criteria_hr_co[hr_trait]:
                    co_cum_prob = config.trait_cum_probs_by_class[class_type]['co']
                    co_index = get_random_index(co_cum_prob)
                    co_key = list(class_trait_probs['co'].keys())[co_index]
                    trait_nums_indices['co'] = {"trait_index": co_index, "trait_key": co_key}
                    print(f"Given hr trait: {hr_trait}, rerolled co trait from old value: {co_trait} to new value: {co_key}")
                    co_trait = co_key

            # apply exclusion criteria check for face accessory trait and mouth trait pair
            if 'fa' in trait_nums_indices.keys():                                               # enter if statement if fa exists (relevant for all groups)
                fa_trait = trait_nums_indices['fa']['trait_key']                                # get initially rolled fa trait
                mo_trait = trait_nums_indices['mo']['trait_key']                                # get initially rolled mo trait

                if fa_trait in config.exclusion_criteria_fa_mo.keys():                          # only enter reroll loop if initial fa trait exists in exclusion criteria dictionary
                    while mo_trait in config.exclusion_criteria_fa_mo[fa_trait]:
                        mo_cum_prob = config.trait_cum_probs_by_class[class_type]['mo']
                        mo_index = get_random_index(mo_cum_prob)
                        mo_key = list(class_trait_probs['mo'].keys())[mo_index]
                        trait_nums_indices['mo'] = {"trait_index": mo_index, "trait_key": mo_key}
                        print(f"Given fa trait: {fa_trait}, rerolled mo trait from old value: {mo_trait} to new value: {mo_key}")
                        mo_trait = mo_key

            # --- COLOR BALANCE MAPPING ---
            # If the rolled eye has an associated color, then set target_color to eye color
            # Otherwise, if rolled hair has an associated color, then set target_color to hair color
            # Otherwise set target_color to null
            # If the rolled gear is a gear type that has color variations (gr_7 and gr_10) force gear color to align with target_color
            if 'gr' in trait_nums_indices.keys():

                ey_trait = trait_nums_indices['ey']['trait_key']
                hr_trait = trait_nums_indices['hr']['trait_key']
                gr_trait = trait_nums_indices['gr']['trait_key']

                if config.color_balance[ey_trait] != 'null':
                    target_color = config.color_balance[ey_trait]
                elif config.color_balance[hr_trait] != 'null':
                    target_color = config.color_balance[hr_trait]
                else:
                    target_color = 'null'

                if (gr_trait in ['gr_7', 'gr_10']) and (target_color != 'null'):
                    trait_nums_indices['gr']['trait_key'] = f"{gr_trait}_{target_color}"
                    print(f"SUCCESS: Gear {gr_trait} and set to target color: {gr_trait}_{target_color}.")
                elif (gr_trait in ['gr_7', 'gr_10']) and (target_color == 'null'):
                    print(f"ERROR: Gear {gr_trait} found but no target color: {target_color}.")
                else:
                    print(f"SUCCESS: Gear {gr_trait} found but with no target color as expected.")
            else:
                print('SUCCESS: No gear trait was rolled for this NFT')

            # if there are 2 or more golden traits, replace background with golden background
            golden_traits = ["gr_27", "gr_28", "hr_45_sub_1", "hr_45_sub_2", "ey_43", "co_60"]
            flattened_traits = [trait_nums_indices[trait]['trait_key'] for trait in trait_nums_indices.keys()]
            golden_trait_count = {golden_trait: flattened_traits.count(golden_trait) for golden_trait in golden_traits}
            golden_trait_sum = sum(golden_trait_count.values())
            if golden_trait_sum >= 2:
                trait_nums_indices['bg']['trait_index'] = 21
                trait_nums_indices['bg']['trait_key'] = 'bg_22'
                print(f"{golden_trait_sum} golden traits found, setting golden background with output: {trait_nums_indices}")

            # nulling step for specific fa traits and trait categories
            flattened_traits = [trait_nums_indices[trait]['trait_key'] for trait in trait_nums_indices.keys()]
            if 'fa' in trait_nums_indices.keys() and trait_nums_indices['fa']['trait_key'] in config.unrender_fa.keys():
                fa_trait = trait_nums_indices['fa']['trait_key']
                pop_trait = config.unrender_fa[fa_trait][0]
                group_trait_prob_keys.remove(pop_trait)
                trait_nums_indices.pop(pop_trait)
                print(f"Given fa trait: {fa_trait}, popped {pop_trait} from group_trait_prob_keys: {group_trait_prob_keys} and trait_nums_indices: {trait_nums_indices}")

            # nulling step for co_60 and fa_8 and fa_21 (killing collars with golden clothing)
            if 'fa' in trait_nums_indices.keys() and trait_nums_indices['co']['trait_key'] in ['co_50', 'co_60', 'co_57', 'co_38', 'co_25', 'co_24', 'co_47', 'co_45'] and trait_nums_indices['fa']['trait_key'] in ['fa_8', 'fa_21']:
                fa_trait = trait_nums_indices['fa']['trait_key']
                group_trait_prob_keys.remove('fa')
                trait_nums_indices.pop('fa')
                print(f"Given {trait_nums_indices['co']['trait_key']} and fa trait: {fa_trait}, popped fa from group_trait_prob_keys: {group_trait_prob_keys} and trait_nums_indices: {trait_nums_indices}")

            # nulling step for hr and fa traits
            hr_fa_nulling = {
                'hr_38': ['fa_7', 'fa_8', 'fa_21'],
                'hr_35': ['fa_7'],
                'hr_21': ['fa_7'],
                'hr_7': ['fa_21'],
                'hr_1': ['fa_7', 'fa_18'],
            }

            hr_trait_raw = trait_nums_indices['hr']['trait_key']  # get initially rolled hr trait
            hr_trait = "_".join(hr_trait_raw.split("_", 2)[:2])  # hr_1_sub_1 -> hr_1
            if 'fa' in trait_nums_indices.keys() and hr_trait in hr_fa_nulling.keys() and trait_nums_indices['fa']['trait_key'] in hr_fa_nulling[hr_trait]:
                print(f"NULLED OUT A FACE ACCESSORY GIVEN A HAIR ACCESSORY!")
                fa_trait = trait_nums_indices['fa']['trait_key']
                group_trait_prob_keys.remove('fa')
                trait_nums_indices.pop('fa')
                print(f"Given hr trait: {hr_trait}, popped fa from group_trait_prob_keys: {group_trait_prob_keys} and trait_nums_indices: {trait_nums_indices}")

            # create dictionary of traits to image filenames
            trait_to_filenames = create_filename_map(group_trait_prob_keys, trait_nums_indices, config.trait_directories)
            trait_to_filenames['cl'] = f"classes/{cl_key}.png"
            print(trait_to_filenames, '\n', trait_to_filenames['suffix'])

            # create final NFT image, generate metadata, and write to JSON
            create_image_composite(trait_to_filenames, class_type, nft_index)
            generate_metadata(trait_to_filenames, class_type, nft_index)

            print(f" \n ----- 🚀 SUCCESSFULLY CREATED NFT #{nft_count} 🚀 ----- \n \n")
            nft_count = nft_count + 1

    # generate handcrafted NFTs
    handcrafted_config = config.handcrafted_config
    for nft_index, handcrafted in enumerate(handcrafted_config):

        trait_to_filenames = create_filename_map(handcrafted["group_trait_prob_keys"], handcrafted["trait_nums_indices"], config.trait_directories)
        trait_to_filenames['cl'] = f"classes/{handcrafted['cl_key']}.png"

        # create final NFT image, generate metadata, and write to JSON
        create_image_composite(trait_to_filenames, handcrafted['class_type'], nft_index)
        generate_metadata(trait_to_filenames, handcrafted['class_type'], nft_index)

    # generate legendary NFTs
    legendary_image_filelist = os.listdir('legendary-images')
    if '.DS_Store' in legendary_image_filelist:
        legendary_image_filelist.remove('.DS_Store')

    for image_name in legendary_image_filelist:

        src_image_file = os.path.join('legendary-images', image_name)
        dst_image_file = os.path.join("output-images", image_name)
        if os.path.isfile(src_image_file):
            shutil.copy(src_image_file, dst_image_file)
            print(f"Successfully copied legendary image: {image_name}")

        json_name = image_name.replace(".png", "")
        src_json_file = os.path.join('legendary-jsons', json_name)
        dst_json_file = os.path.join("output-jsons", json_name)
        if os.path.isfile(src_json_file):
            shutil.copy(src_json_file, dst_json_file)
            print(f"Successfully copied legendary JSON: {json_name}")

    print(time.time() - t0)
