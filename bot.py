import json

from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters
import telegram

import config
import utils
import vk_bot
from tags import tagging


def text_handling(update: telegram.Update, context: CallbackContext):
    bot = context.bot
    message = update.message
    user_id: int = message.from_user.id
    text: str = message.text

    if text.startswith("https://vk.com/"):
        community_handling(text, user_id)
    elif text.startswith("+"):
        tag_handling(text, user_id)
    else:
        information_print(update, context)


def community_handling(message, user_id):
    bot = updater.bot

    users = utils.read_users()

    message = message.replace("https://vk.com/", "")
    photo_name = 'test1.jpg'

    group_id = vk_bot.get_group_id(message)

    users[user_id] = str(group_id)
    utils.write_users(users)

    if group_id is not False:
        bot.send_message(chat_id=user_id, text="Идет обработка постов сообщества. Пожалуйста, подождите (~50 секунд)")
        pics = vk_bot.get_wall_pics_by_id(group_id, 10)

        all_tags = []
        pics_dict = dict()

        for pic in pics:
            vk_bot.save_pic(pic[0])
            tags = get_tags(photo_name)

            all_tags.extend(tags)
            pics_dict[pic[1]] = tags

        with open(str(group_id), "w", encoding="UTF-8") as f:
            json.dump(pics_dict, f)

        tags = ", ".join(set(all_tags))
        text = "Сообщество {} зарегистрировано, теперь выберите интересующий вас тег " \
               "или отправьте ссылку на другое сообщество. \n\nТеги:\n\n".format(message)

        bot.send_message(chat_id=user_id, text=text + tags)

    else:
        bot.send_message(chat_id=user_id, text="Ошибка, данного сообщества не существует или оно закрытое.")


def tag_handling(message, user_id):
    message = message[1:]
    bot = updater.bot

    with open("users.json", "r", encoding="UTF-8") as f:
        users_dict = json.load(f)

    group_id = users_dict.get(str(user_id))

    if group_id is not None:

        with open(str(group_id), "r", encoding="UTF-8") as f:
            posts_dict = json.load(f)

        posts = []
        for post in posts_dict:
            if message in posts_dict[post]:
                posts.append(post)

        if len(posts) > 0:
            bot.send_message(chat_id=user_id, text="Посты по заданному тегу " + message)

            for post in posts:
                bot.send_photo(chat_id=user_id, photo=post)

        else:
            bot.send_message(chat_id=user_id, text="За последнее время в этом сообществе не было постов с этим тегом.")

    else:
        bot.send_message(chat_id=user_id, text="Ошибка, отправьте правильную ссылку на любой открытый паблик в ВК с фото.")


def information_print(update: telegram.Update, context: CallbackContext):
    bot = context.bot
    message = update.message
    user_id = message.chat.id

    message_text = "<b> Добро пожаловать в Tagger-бота! </b> \n\n" \
                   "Функционал бота:\n\n" \
                   "- Отправьте любую фотографию и получите теги к ней.\n\nили\n\n" \
                   "- Введите ссылку на паблик в ВК \n(например: https://vk.com/ru2ch)\n" \
                   "- Введите интересующий вас тег \n(например: +travel)."

    bot.send_message(chat_id=user_id, text=message_text, parse_mode="HTML")


def get_tags(photo_name):
    instance_labels, semantic_labels = utils.get_image_labels()
    instance_groups_labels = utils.read_instance_groups()
    instance_groups = utils.find_instance_groups(instance_labels, instance_groups_labels)

    instance_groups.update(semantic_labels)

    tags = tagging({photo_name: instance_groups})[photo_name]
    return tags


def tag_photo(update: telegram.Update, context: CallbackContext):
    bot = context.bot
    message = update.message
    user_id = message.chat.id

    photo_name = 'test1.jpg'

    file = bot.get_file(message.photo[-1].file_id)
    file.download(photo_name)

    tags = get_tags(photo_name)

    bot.send_message(chat_id=user_id, text="Tags: " + ", ".join(tags), reply_to_message_id=message.message_id)


if __name__ == '__main__':
    updater = Updater(
        workers=32,
        use_context=True,
        token=config.bot_key)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", information_print))
    dispatcher.add_handler(MessageHandler(Filters.text, text_handling))
    dispatcher.add_handler(MessageHandler(Filters.photo, tag_photo))

    updater.start_polling()
