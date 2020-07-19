from telegram.ext.dispatcher import run_async
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters
import telegram

import config
import utils


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
    users[user_id] = message
    utils.write_users(users)

    # parsing from vk part

    tags = ", ".join(utils.read_instance_groups().keys())
    text = "Сообщество {} зарегистрировано, теперь выберите интересующий вас тег " \
           "или отправьте ссылку на другое сообщество. \n\nТеги:\n\n".format(message)

    bot.send_message(chat_id=user_id, text=text + tags)


def tag_handling(message, user_id):
    message = message[1:]
    bot = updater.bot
    # parsing from vk part

    bot.send_message(chat_id=user_id, text="Посты по заданному тегу " + message)


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


def tag_photo(update: telegram.Update, context: CallbackContext):
    bot = context.bot
    message = update.message
    user_id = message.chat.id

    file = bot.get_file(message.photo[-1].file_id)
    file.download('test1.jpg')

    instance_labels, semantic_labels = utils.get_image_labels()
    instance_groups_labels = utils.read_instance_groups()
    instance_groups = utils.find_instance_groups(instance_labels, instance_groups_labels)

    bot.send_message(chat_id=user_id, text="Instance groups: " + str(instance_groups) + "\n\n" +
                                           "Instance labels: " + str(instance_labels) + "\n\n" +
                                           "Segmentation labels: " + str(semantic_labels))


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
