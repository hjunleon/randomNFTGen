import yaml
import csv
import json


def read_yaml(file_path):
    """
    read in yaml file
    :param file_path: path to yaml file
    :return: yaml object
    """
    with open(file_path, "r") as f:
        return yaml.safe_load(f)


class GeneratorConfig:

    def __init__(self):
        self.config_file = read_yaml('config.yml')

    @property
    def _config_file(self):
        return self.config_file

    @staticmethod
    def create_probability_map(trait_nums, trait_probs):
        if (len(trait_nums) == len(trait_probs)) and (sum(trait_probs) == 100):
            cumulatives = [sum(trait_probs[0:x:1]) for x in range(0, len(trait_probs) + 1)]
            return cumulatives[1:]
        else:
            print("Input array lengths not equal or probabilities are not equal to 100")

    @property
    def trait_directories(self):
        return self.config_file['trait_directories']

    @property
    def class_types(self):
        return self.config_file['class_types']

    @property
    def class_type_probs(self):
        return self.config_file['class_type_probs']

    @property
    def trait_probs_by_class(self):
        """
        Read in config CSV file and parse into dictionary.
        Prints out in pretty JSON format for error checking.
        :return: dictionary object
        """
        filename = f"{self.config_file['config_criteria_prefix']}/{self.config_file['config_filename']}"

        with open(filename, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            fields = csvreader.__next__()

            class_types = fields[2:]
            # print(class_types)

            trait_probs_by_class = {class_type: {} for class_type in class_types}
            trait_abbrevs = ['bg', 'co', 'ey', 'mo', 'hr', 'fa', 'ha', 'gr']

            for class_type in trait_probs_by_class.keys():
                trait_probs_by_class[class_type] = {trait_abbrev: {} for trait_abbrev in trait_abbrevs}

            for row in csvreader:
                for class_index, class_type in enumerate(class_types):
                    trait_probs_by_class[class_type][row[0]][row[1]] = int(row[class_index + 2])

        # print(json.dumps(trait_probs_by_class, indent=4))
        # return self.config_file['trait_probs_by_class']
        return trait_probs_by_class

    @property
    def exclusion_criteria_hr_ha(self):
        """
        Read in exclusion criteria CSV file for hr and ha pair and parse into dictionary.
        Prints out in pretty JSON format for error checking.
        :return: dictionary object
        """
        filename = f"{self.config_file['config_criteria_prefix']}/{self.config_file['exclusion_hr_ha_filename']}"

        with open(filename, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            fields = csvreader.__next__()

            exclusion_criteria = {}
            for row in csvreader:
                if row[0] in exclusion_criteria.keys():
                    exclusion_criteria[row[0]].append(row[1])
                else:
                    exclusion_criteria[row[0]] = [row[1]]

        # print(json.dumps(exclusion_criteria, indent=4))
        return exclusion_criteria

    @property
    def exclusion_criteria_ha_fa(self):
        """
        Read in exclusion criteria CSV file for ha and fa pair and parse into dictionary.
        Prints out in pretty JSON format for error checking.
        :return: dictionary object
        """
        filename = f"{self.config_file['config_criteria_prefix']}/{self.config_file['exclusion_ha_fa_filename']}"

        with open(filename, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            fields = csvreader.__next__()

            exclusion_criteria = {}
            for row in csvreader:
                if row[0] in exclusion_criteria.keys():
                    exclusion_criteria[row[0]].append(row[1])
                else:
                    exclusion_criteria[row[0]] = [row[1]]

        # print(json.dumps(exclusion_criteria, indent=4))
        return exclusion_criteria

    @property
    def exclusion_criteria_hr_co(self):
        """
        Read in exclusion criteria CSV file for hr and co pair and parse into dictionary.
        Prints out in pretty JSON format for error checking.
        :return: dictionary object
        """
        filename = f"{self.config_file['config_criteria_prefix']}/{self.config_file['exclusion_hr_co_filename']}"

        with open(filename, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            fields = csvreader.__next__()

            exclusion_criteria = {}
            for row in csvreader:
                if row[0] in exclusion_criteria.keys():
                    exclusion_criteria[row[0]].append(row[1])
                else:
                    exclusion_criteria[row[0]] = [row[1]]

        # print(json.dumps(exclusion_criteria, indent=4))
        return exclusion_criteria

    @property
    def exclusion_criteria_fa_mo(self):
        """
        Read in exclusion criteria CSV file for fa and mo pair and parse into dictionary.
        Prints out in pretty JSON format for error checking.
        :return: dictionary object
        """
        filename = f"{self.config_file['config_criteria_prefix']}/{self.config_file['exclusion_fa_mo_filename']}"

        with open(filename, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            fields = csvreader.__next__()

            exclusion_criteria = {}
            for row in csvreader:
                if row[0] in exclusion_criteria.keys():
                    exclusion_criteria[row[0]].append(row[1])
                else:
                    exclusion_criteria[row[0]] = [row[1]]

        # print(json.dumps(exclusion_criteria, indent=4))
        return exclusion_criteria

    # -------------------------------------------------------------------
    @property
    def nulling_criteria_hr_fa(self):
        """
        Read in nulling criteria CSV file for hr and fa pair and parse into dictionary.
        Prints out in pretty JSON format for error checking.
        :return: dictionary object
        """
        filename = f"{self.config_file['config_criteria_prefix']}/{self.config_file['nulling_criteria_hr_fa_filename']}"

        with open(filename, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            fields = csvreader.__next__()

            exclusion_criteria = {}
            for row in csvreader:
                if row[0] in exclusion_criteria.keys():
                    exclusion_criteria[row[0]].append(row[1])
                else:
                    exclusion_criteria[row[0]] = [row[1]]

        print(json.dumps(exclusion_criteria, indent=4))
        return exclusion_criteria
    # -------------------------------------------------------------------

    @property
    def color_balance(self):
        """
        Read in color balance CSV file and parse into dictionary.
        Prints out in pretty JSON format for error checking.
        :return: dictionary object
        """
        filename = f"{self.config_file['config_criteria_prefix']}/{self.config_file['color_balance_filename']}"

        with open(filename, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            fields = csvreader.__next__()

            color_balance = {}
            for row in csvreader:
                color_balance[row[0]] = row[1]

        # print(json.dumps(color_balance, indent=4))
        return color_balance

    @property
    def unrender_fa(self):
        """
        Read in unrender criteria CSV file and parse into dictionary.
        Prints out in pretty JSON format for error checking.
        :return: dictionary object
        """
        filename = f"{self.config_file['config_criteria_prefix']}/{self.config_file['unrender_fa']}"

        with open(filename, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            fields = csvreader.__next__()

            unrender_fa = {}
            for row in csvreader:
                if row[0] in unrender_fa.keys():
                    unrender_fa[row[0]].append(row[1])
                else:
                    unrender_fa[row[0]] = [row[1]]

        # print(json.dumps(exclusion_criteria, indent=4))
        return unrender_fa

    @property
    def metadata_labels(self):
        """
        Read in metadata labels CSV file for writing to JSON file.
        :return: dictionary object
        """
        filename = f"{self.config_file['config_criteria_prefix']}/{self.config_file['metadata_labels']}"

        with open(filename, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            fields = csvreader.__next__()

            metadata_labels = {}
            for row in csvreader:
                if row[0] in metadata_labels.keys():
                    metadata_labels[row[0]].append(row[1])
                else:
                    metadata_labels[row[0]] = [row[1]]

        # print(json.dumps(metadata_labels, indent=4))
        return metadata_labels

    @property
    def trait_cum_probs_by_class(self):
        """
        Conver trait_probs_by_class dictionary object into
        list of cumulative probabilities by class and by trait.
        :return: dictionary object
        """
        trait_cum_probs_by_class = {class_type: {} for class_type in self.trait_probs_by_class}

        for class_type in self.trait_probs_by_class:
            for trait_type in self.trait_probs_by_class[class_type]:
                trait_probs = list(self.trait_probs_by_class[class_type][trait_type].values())
                cumulatives = [sum(trait_probs[0:x:1]) for x in range(0, len(trait_probs) + 1)]
                trait_cum_probs_by_class[class_type][trait_type] = cumulatives[1:]

        # print(json.dumps(trait_cum_probs_by_class, indent=4))
        return trait_cum_probs_by_class

    @property
    def group_probs(self):
        return self.config_file['group_probs']

    @property
    def trait_probs_by_group(self):
        return self.config_file['trait_probs_by_group']

    @property
    def handcrafted_config(self):

        handcrafted_config = [
            {
                "group_trait_prob_keys": ['bg', 'co', 'ey', 'fa', 'gr', 'hr', 'ha', 'mo'],
                "trait_nums_indices": {
                    'bg': {'trait_key': 'bg_22'},
                    'co': {'trait_key': 'co_60'},
                    'ey': {'trait_key': 'ey_43'},
                    'fa': {'trait_key': 'fa_1'},
                    'gr': {'trait_key': 'gr_28'},
                    'hr': {'trait_key': 'hr_45_sub_2'},
                    'ha': {'trait_key': 'ha_5'},
                    'mo': {'trait_key': 'mo_2'}
                },
                "cl_key": 'cl_9',
                "class_type": 'master_ronin',
            },
            {
                "group_trait_prob_keys": ['bg', 'co', 'ey', 'fa', 'gr', 'hr', 'ha', 'mo'],
                "trait_nums_indices": {
                    'bg': {'trait_key': 'bg_22'},
                    'co': {'trait_key': 'co_60'},
                    'ey': {'trait_key': 'ey_20'},
                    'fa': {'trait_key': 'fa_3'},
                    'gr': {'trait_key': 'gr_28'},
                    'hr': {'trait_key': 'hr_45_sub_1'},
                    'ha': {'trait_key': 'ha_3'},
                    'mo': {'trait_key': 'mo_18'}
                },
                "cl_key": 'cl_8',
                "class_type": 'master_ronin',
            },
            {
                "group_trait_prob_keys": ['bg', 'co', 'ey', 'gr', 'hr', 'ha', 'mo'],
                "trait_nums_indices": {
                    'bg': {'trait_key': 'bg_22'},
                    'co': {'trait_key': 'co_60'},
                    'ey': {'trait_key': 'ey_26'},
                    'gr': {'trait_key': 'gr_28'},
                    'hr': {'trait_key': 'hr_45_sub_2'},
                    'ha': {'trait_key': 'ha_4'},
                    'mo': {'trait_key': 'mo_24'}
                },
                "cl_key": 'cl_7',
                "class_type": 'master_ronin',
            },
            {
                "group_trait_prob_keys": ['bg', 'co', 'ey', 'fa', 'gr', 'hr', 'ha', 'mo'],
                "trait_nums_indices": {
                    'bg': {'trait_key': 'bg_22'},
                    'co': {'trait_key': 'co_60'},
                    'ey': {'trait_key': 'ey_43'},
                    'fa': {'trait_key': 'fa_2'},
                    'gr': {'trait_key': 'gr_27'},
                    'hr': {'trait_key': 'hr_45_sub_1'},
                    'ha': {'trait_key': 'ha_7'},
                    'mo': {'trait_key': 'mo_12'}
                },
                "cl_key": 'cl_3',
                "class_type": 'ultra_droid',
            },
            {
                "group_trait_prob_keys": ['bg', 'co', 'ey', 'fa', 'gr', 'hr', 'ha', 'mo'],
                "trait_nums_indices": {
                    'bg': {'trait_key': 'bg_22'},
                    'co': {'trait_key': 'co_60'},
                    'ey': {'trait_key': 'ey_42'},
                    'fa': {'trait_key': 'fa_24'},
                    'gr': {'trait_key': 'gr_27'},
                    'hr': {'trait_key': 'hr_45_sub_2'},
                    'ha': {'trait_key': 'ha_3'},
                    'mo': {'trait_key': 'mo_2'}
                },
                "cl_key": 'cl_3',
                "class_type": 'ultra_droid',
            },
            {
                "group_trait_prob_keys": ['bg', 'co', 'ey', 'fa', 'gr', 'hr', 'ha', 'mo'],
                "trait_nums_indices": {
                    'bg': {'trait_key': 'bg_22'},
                    'co': {'trait_key': 'co_60'},
                    'ey': {'trait_key': 'ey_24'},
                    'fa': {'trait_key': 'fa_23'},
                    'gr': {'trait_key': 'gr_27'},
                    'hr': {'trait_key': 'hr_45_sub_1'},
                    'ha': {'trait_key': 'ha_5'},
                    'mo': {'trait_key': 'mo_11'}
                },
                "cl_key": 'cl_3',
                "class_type": 'ultra_droid',
            },
            {
                "group_trait_prob_keys": ['bg', 'co', 'ey', 'fa', 'gr', 'hr', 'ha', 'mo'],
                "trait_nums_indices": {
                    'bg': {'trait_key': 'bg_12'},
                    'co': {'trait_key': 'co_54'},
                    'ey': {'trait_key': 'ey_37'},
                    'fa': {'trait_key': 'fa_21'},
                    'gr': {'trait_key': 'gr_26'},
                    'hr': {'trait_key': 'hr_39_sub_1'},
                    'ha': {'trait_key': 'ha_3'},
                    'mo': {'trait_key': 'mo_8'}
                },
                "cl_key": 'cl_7',
                "class_type": 'master_ronin',
            },
            {
                "group_trait_prob_keys": ['bg', 'co', 'ey', 'fa', 'gr', 'hr', 'ha', 'mo'],
                "trait_nums_indices": {
                    'bg': {'trait_key': 'bg_9'},
                    'co': {'trait_key': 'co_52'},
                    'ey': {'trait_key': 'ey_34'},
                    'fa': {'trait_key': 'fa_8'},
                    'gr': {'trait_key': 'gr_24'},
                    'hr': {'trait_key': 'hr_37_sub_1'},
                    'ha': {'trait_key': 'ha_4'},
                    'mo': {'trait_key': 'mo_12'}
                },
                "cl_key": 'cl_9',
                "class_type": 'master_ronin',
            },
            {
                "group_trait_prob_keys": ['bg', 'co', 'ey', 'fa', 'gr', 'hr', 'ha', 'mo'],
                "trait_nums_indices": {
                    'bg': {'trait_key': 'bg_16'},
                    'co': {'trait_key': 'co_56'},
                    'ey': {'trait_key': 'ey_42'},
                    'fa': {'trait_key': 'fa_20'},
                    'gr': {'trait_key': 'gr_10_blue'},
                    'hr': {'trait_key': 'hr_41_sub_1'},
                    'ha': {'trait_key': 'ha_7'},
                    'mo': {'trait_key': 'mo_25'}
                },
                "cl_key": 'cl_3',
                "class_type": 'ultra_droid',
            },
            {
                "group_trait_prob_keys": ['bg', 'co', 'ey', 'fa', 'gr', 'hr', 'ha', 'mo'],
                "trait_nums_indices": {
                    'bg': {'trait_key': 'bg_19'},
                    'co': {'trait_key': 'co_58'},
                    'ey': {'trait_key': 'ey_41'},
                    'fa': {'trait_key': 'fa_23'},
                    'gr': {'trait_key': 'gr_10_purple'},
                    'hr': {'trait_key': 'hr_43_sub_2'},
                    'ha': {'trait_key': 'ha_5'},
                    'mo': {'trait_key': 'mo_12'}
                },
                "cl_key": 'cl_3',
                "class_type": 'ultra_droid',
            },
            {
                "group_trait_prob_keys": ['bg', 'co', 'ey', 'fa', 'gr', 'hr', 'ha', 'mo'],
                "trait_nums_indices": {
                    'bg': {'trait_key': 'bg_22'},
                    'co': {'trait_key': 'co_60'},
                    'ey': {'trait_key': 'ey_37'},
                    'fa': {'trait_key': 'fa_1'},
                    'gr': {'trait_key': 'gr_28'},
                    'hr': {'trait_key': 'hr_45_sub_2'},
                    'ha': {'trait_key': 'ha_5'},
                    'mo': {'trait_key': 'mo_19'}
                },
                "cl_key": 'cl_4',
                "class_type": 'ronin',
            },
            {
                "group_trait_prob_keys": ['bg', 'co', 'ey', 'fa', 'gr', 'hr', 'ha', 'mo'],
                "trait_nums_indices": {
                    'bg': {'trait_key': 'bg_22'},
                    'co': {'trait_key': 'co_60'},
                    'ey': {'trait_key': 'ey_42'},
                    'fa': {'trait_key': 'fa_23'},
                    'gr': {'trait_key': 'gr_27'},
                    'hr': {'trait_key': 'hr_45_sub_1'},
                    'ha': {'trait_key': 'ha_7'},
                    'mo': {'trait_key': 'mo_10'}
                },
                "cl_key": 'cl_1',
                "class_type": 'droid',
            },
            {
                "group_trait_prob_keys": ['bg', 'co', 'ey', 'gr', 'hr', 'ha', 'mo'],
                "trait_nums_indices": {
                    'bg': {'trait_key': 'bg_22'},
                    'co': {'trait_key': 'co_60'},
                    'ey': {'trait_key': 'ey_43'},
                    'gr': {'trait_key': 'gr_28'},
                    'hr': {'trait_key': 'hr_45_sub_2'},
                    'ha': {'trait_key': 'ha_7'},
                    'mo': {'trait_key': 'mo_8'}
                },
                "cl_key": 'cl_10',
                "class_type": 'human',
            },
            {
                "group_trait_prob_keys": ['bg', 'co', 'ey', 'gr', 'hr', 'ha', 'mo'],
                "trait_nums_indices": {
                    'bg': {'trait_key': 'bg_22'},
                    'co': {'trait_key': 'co_60'},
                    'ey': {'trait_key': 'ey_43'},
                    'gr': {'trait_key': 'gr_27'},
                    'hr': {'trait_key': 'hr_45_sub_1'},
                    'ha': {'trait_key': 'ha_5'},
                    'mo': {'trait_key': 'mo_2'}
                },
                "cl_key": 'cl_12',
                "class_type": 'human',
            },
            {
                "group_trait_prob_keys": ['bg', 'co', 'ey', 'gr', 'hr', 'ha', 'mo'],
                "trait_nums_indices": {
                    'bg': {'trait_key': 'bg_1'},
                    'co': {'trait_key': 'co_26'},
                    'ey': {'trait_key': 'ey_2'},
                    'gr': {'trait_key': 'gr_24'},
                    'hr': {'trait_key': 'hr_28_sub_1'},
                    'ha': {'trait_key': 'ha_9'},
                    'mo': {'trait_key': 'mo_17'}
                },
                "cl_key": 'cl_10',
                "class_type": 'human',
            },
        ]

        return handcrafted_config

    # @property
    # # ex: background_nums = [0, 1, 2, 3, 4, 5]
    # # ex: ex: background_probs = [5, 25, 10, 25, 25, 10]
    # def background_prob_map(self):
    #     background_nums = list(range(len(self.background_trait_map)))
    #     background_probs = [value[1] for key, value in self.background_trait_map.items()]
    #     return self.create_probability_map(background_nums, background_probs)
    #
    # @property
    # def body_trait_map(self):
    #     return self._traits['body']
    #
    # @property
    # def body_label_map(self):
    #     return [value[0] for key, value in self.body_trait_map.items()]
    #
    # @property
    # def body_prob_map(self):
    #     body_nums = list(range(len(self.body_trait_map)))
    #     body_probs = [value[1] for key, value in self.body_trait_map.items()]
    #     return self.create_probability_map(body_nums, body_probs)
    #
    # @property
    # def face_trait_map(self):
    #     return self._traits['face']
    #
    # @property
    # def face_label_map(self):
    #     return [value[0] for key, value in self.face_trait_map.items()]
    #
    # @property
    # def face_prob_map(self):
    #     face_nums = list(range(len(self.face_trait_map)))
    #     face_probs = [value[1] for key, value in self.face_trait_map.items()]
    #     return self.create_probability_map(face_nums, face_probs)
    #
    # @property
    # def eyes_trait_map(self):
    #     return self._traits['eyes']
    #
    # @property
    # def eyes_label_map(self):
    #     return [value[0] for key, value in self.eyes_trait_map.items()]
    #
    # @property
    # def eyes_prob_map(self):
    #     eyes_nums = list(range(len(self.eyes_trait_map)))
    #     eyes_probs = [value[1] for key, value in self.eyes_trait_map.items()]
    #     return self.create_probability_map(eyes_nums, eyes_probs)
    #
    # @property
    # def mouth_trait_map(self):
    #     return self._traits['mouth']
    #
    # @property
    # def mouth_label_map(self):
    #     return [value[0] for key, value in self.mouth_trait_map.items()]
    #
    # @property
    # def mouth_prob_map(self):
    #     mouth_nums = list(range(len(self.mouth_trait_map)))
    #     mouth_probs = [value[1] for key, value in self.mouth_trait_map.items()]
    #     return self.create_probability_map(mouth_nums, mouth_probs)
    #
    # @property
    # def shroom_trait_map(self):
    #     return self._traits['shroom']
    #
    # @property
    # def shroom_label_map(self):
    #     return [value[0] for key, value in self.shroom_trait_map.items()]
    #
    # @property
    # def shroom_prob_map(self):
    #     shroom_nums = list(range(len(self.shroom_trait_map)))
    #     shroom_probs = [value[1] for key, value in self.shroom_trait_map.items()]
    #     return self.create_probability_map(shroom_nums, shroom_probs)
    #
    # @property
    # def gen_trait_map(self):
    #     return self._traits['gen']
    #
    # @property
    # def gen_label_map(self):
    #     return [value[0] for key, value in self.gen_trait_map.items()]
    #
    # @property
    # def gen_prob_map(self):
    #     gen_nums = list(range(len(self.gen_trait_map)))
    #     gen_probs = [value[1] for key, value in self.gen_trait_map.items()]
    #     return self.create_probability_map(gen_nums, gen_probs)
