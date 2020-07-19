from telegram.ext.dispatcher import run_async
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters
import telegram

import config
import utils


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
    # dispatcher.add_handler(CommandHandler("start", register_user))
    dispatcher.add_handler(MessageHandler(Filters.photo, tag_photo))

    updater.start_polling()
