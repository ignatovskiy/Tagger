def tagging(labels_dict):
    dict_labels = dict()
    for img in labels_dict:
        temp_tags = []
        temp_labels = labels_dict[img]
        if "devices" in temp_labels:
            temp_tags.append("Technologies")
        if {"sport equipment", "winter sports"}.issubset(temp_labels):
            temp_tags.append("Sport")
        if ({"food", "kitchen tools"}.issubset(temp_labels)) \
                or ({"people", "kitchen tools"}.issubset(temp_labels)) \
                or ("kitchen tools" in temp_labels):
            temp_tags.append("Cooking")
        if "pets" in temp_labels:
            temp_tags.append("Pets")
        if (("food" in temp_labels) and ("interior" in temp_labels) and ("people" in temp_labels)) \
                or (("food" in temp_labels) and ("kitchen tools" in temp_labels) and ("people" in temp_labels)):
            temp_tags.append("Party")
        if "farm animals" in temp_labels and temp_labels["vegetation"] > 1:
            temp_tags.append("Village")
        if {"tie", "people"}.issubset(temp_labels):
            temp_tags.append("Business")
        if ("interior" in temp_labels) \
                or ({"interior", "potted plant"}.issubset(temp_labels)) \
                or ({"interior", "appliances"}.issubset(temp_labels)):
            temp_tags.append("Design")
        if ("people" in temp_labels and temp_labels["vegetation"] > 1) \
                or (temp_labels["water/road"] > 1 and temp_labels["vegetation"] > 1) \
                or (temp_labels["sky"] > 1 and temp_labels["vegetation"] > 1) \
                or ("wild animals" in temp_labels and temp_labels["vegetation"] > 1) \
                or "wild animals" in temp_labels and (temp_labels["sky"] > 1) \
                or ("wild animals" in temp_labels):
            temp_tags.append("Nature")
        if ("street" in temp_labels) \
                or (("public transport" in temp_labels or "transport" in temp_labels) and temp_labels["buildings"] > 1)\
                or (("public transport" in temp_labels or "transport" in temp_labels) and temp_labels["sky"] > 1)\
                or ("street" in temp_labels and (temp_labels["buildings"] > 1)) \
                or ({"people", "umbrella"}.issubset(temp_labels)) \
                or ("street items" in temp_labels and (temp_labels["buildings"] > 1)) \
                or ({"people", "street items"}.issubset(temp_labels)):
            temp_tags.append("Urban")
        dict_labels[img] = temp_tags
    return dict_labels

