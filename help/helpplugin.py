from typing import Type

import requests
from maubot import Plugin
from maubot.handlers import command
from mautrix.types import MessageEvent

from help.config import Config


class HelpPlugin(Plugin):
    commands: object
    categories: object
    standard_category: str

    async def start(self) -> None:
        self.config.load_and_update()
        self.standard_category = self.config["standard_category"]
        await self.fetch_help()

    async def fetch_help(self):
        self.log.info("Loading help data..")
        commands = requests.request("GET", self.config['command_index'], headers={}, data="")
        self.commands = commands.json()
        self.log.info(f"Command infos loaded. The command index contains {len(self.commands.keys())} commands.")

        categories = requests.request("GET", self.config['category_index'], headers={}, data="")
        self.categories = categories.json()
        self.log.info(f"Category infos loaded. The category index contains {len(self.categories.keys())} categories.")

    @command.new("help", aliases=["hilfe"])
    @command.argument("name", pass_raw=True, required=False)
    async def help_command(self, evt: MessageEvent, name: str):
        if name == "" or name == " ":
            command_index: dict = {}
            used_commands: list = []
            for cat in sorted(self.categories):
                command_index[cat] = self.categories[cat]
                for cmd in self.categories[cat]:
                    used_commands.append(cmd)
            if self.standard_category not in command_index:
                command_index[self.standard_category] = []
            for key in sorted(self.commands):
                if key not in used_commands:
                    command_index[self.standard_category].append(key)
            msg: str = "<p><strong>Liste der Befehle:</strong></p>\n<ol>\n"

            for key in sorted(command_index):
                if key == self.standard_category or len(command_index[key]) == 0:
                    continue
                msg = msg + f"<li><b>{key}</b>\n<ul>"
                for cmd in sorted(command_index[key]):
                    msg = msg + f"<li>{cmd}</li>\n"
                msg = msg + "</ul></li>\n"
            if len(command_index[self.standard_category]) != 0:
                msg = msg + f"<li><b>{self.standard_category}</b>\n<ul>\n"
                for cmd in sorted(command_index[self.standard_category]):
                    msg = msg + f"<li>{cmd}</li>"
                msg = msg + "</ul></li>\n"
            msg = msg + "</ol><p><em>Nähere Informationen über einen Befehl erhälst du mit <code>!help " \
                        "&ltBefehl&gt</code>.</em></p> "
            await evt.respond(msg, markdown=False, allow_html=True)

        elif name == "reload":
            if evt.sender in self.config['devs']:
                await self.fetch_help()
                await evt.respond("Die Hilfenachrichten wurden neu geladen.")
            else:
                await evt.respond("Nur Developer können die Hilfenachrichten neu laden, um Spam vorzubeugen.")
        else:
            if self.commands[name] is None:
                await evt.respond(
                    f"Für den Befehl `{name}` gibt es keine Informationen. Entweder exsistiert dieser Befehl nicht, "
                    f"oder die Developer haben vergessem, diesen zu registrieren.")
            else:
                await evt.respond(f"**Hilfe:** `!{name}`\n\n*{self.commands[name]}*")

    @classmethod
    def get_config_class(cls) -> Type['BaseProxyConfig']:
        return Config
