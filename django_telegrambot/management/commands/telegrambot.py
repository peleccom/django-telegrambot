import logging

from django.core.management.base import BaseCommand
from django.conf import settings
from telegram.ext import Updater

from django_telegrambot.apps import DjangoTelegramBot


class Command(BaseCommand):
    help = "Run telegram bot in polling mode"

    def add_arguments(self, parser):
        parser.add_argument('--token_index', '-i', help="Bot token index in settings", default=None)
        parser.add_argument('--token', '-t', help="Bot token or bot name", default=None)
        pass

    def get_updater(self, token_index=None, token=None):
        updater = None
        if token_index is None and token is None:
            updater = DjangoTelegramBot.get_updater()
            if not updater:
                self.stderr.write("Cannot find default bot")
        elif token_index:
            updater = DjangoTelegramBot.get_updater(bot_index=token_index)
            if not updater:
                self.stderr.write("Cannot find bot with index {}".format(token_index))
        elif token:
            updater = DjangoTelegramBot.get_updater(token)
            if not updater:
                self.stderr.write("Cannot find bot with token/username {}".format(token))
        return updater

    def handle(self, *args, **options):
        updater = self.get_updater(token_index=options.get('token_index'), token=options.get('token'))
        if not updater:
            return
        # Enable Logging
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO)
        logger = logging.getLogger("telegrambot")
        logger.setLevel(logging.INFO)
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        console.setFormatter(logging.Formatter('%(name)s - %(levelname)s - %(message)s'))
        logger.addHandler(console)

        self.stdout.write("starting bot")
        self.stdout.write("polling")
        updater.start_polling()
        updater.idle()
