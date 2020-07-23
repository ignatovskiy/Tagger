import hashlib

import requests

import config


def get_group_id(group_name: str):
    request_body = "https://api.vk.com/method/groups.getById?group_ids={}&access_token={}&v=5.120"\
        .format(group_name, config.vk_key)

    groupd_id_dict = requests.get(request_body).json()

    if groupd_id_dict.get("response") is not None:
        group_id = int(-groupd_id_dict["response"][0]["id"])
        return group_id
    else:
        return False


def get_wall_pics_by_id(group_id: int, count_posts: int):
    request_body = "https://api.vk.com/method/wall.get?owner_id={}&count={}&access_token={}&v=5.120"\
        .format(group_id, count_posts, config.vk_key)

    walls_dict = requests.get(request_body).json()

    pics_list = []
    for post in walls_dict["response"]["items"]:
        try:
            temp_pic = (post["attachments"][0]["photo"]["sizes"][0]["url"],
                        post["attachments"][0]["photo"]["sizes"][-1]["url"])
            pics_list.append(temp_pic)
        except (IndexError, KeyError):
            pass

    return pics_list


def save_pic(pic_url: str):
    with open("test1.jpg", 'wb') as handle:
        response = requests.get(pic_url, stream=True)

        if not response.ok:
            print(response)

        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)



