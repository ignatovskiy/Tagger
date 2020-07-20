import json

from instance_segmentation import main as instance
from semantic_segmentation import main as semantic


def get_image_labels(image_name="test1.jpg") -> (dict, dict):
    instance_labels = instance(input_pic=image_name)
    semantic_labels = semantic(image_name=image_name)

    return instance_labels, semantic_labels


def read_instance_groups() -> dict:
    with open("instance_groups.json", "r", encoding="UTF-8") as f:
        groups_json = json.load(f)
    return groups_json


def read_users() -> dict:
    with open("users.json", "r", encoding="UTF-8") as f:
        users = json.load(f)
    return users


def write_users(users_dict):
    with open("users.json", "w", encoding="UTF-8") as f:
        json.dump(users_dict, f)


def find_instance_groups(instance_labels, groups_json) -> dict:
    instance_groups = dict()

    for label in instance_labels:
        temp_groups = []

        for group in groups_json:
            if label in groups_json[group]:
                temp_groups.append(group)
                if group not in instance_groups:
                    instance_groups[group] = instance_labels[label]
                else:
                    instance_groups[group] += instance_labels[label]

        if len(temp_groups) == 0:
            instance_groups[label] = instance_labels[label]

    return instance_groups


def main(image_name="test1.jpg") -> (dict, dict):
    instance_labels, semantic_labels = get_image_labels(image_name)
    instance_groups = find_instance_groups(instance_labels, read_instance_groups())
    return instance_groups, semantic_labels
