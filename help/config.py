from mautrix.util.config import BaseProxyConfig, ConfigUpdateHelper


class Config(BaseProxyConfig):
    def do_update(self, helper: ConfigUpdateHelper) -> None:
        helper.copy("devs")
        helper.copy("command_index")
        helper.copy("category_index")
        helper.copy("standard_category")
