import unittest

import ircbot

class PluginTest(unittest.TestCase):

    test_server = dict(
        encoding = 'utf8',
        host='0.0.0.0', port=6667,
        nickname='test',
        channels={},
        plugins_dir="plugins",
    )

    def init(self, plugin_name, config={}):
        self.test_server["plugins"] = { plugin_name: config }
        self.test_server["log_config"] = { plugin_name: "error" }
        ircbot.logger.setLevel("error")
        ircbot_factory = ircbot.IRCBotFactory(self.test_server)
        self.bot = ircbot.IrcBot()
        self.bot.factory = ircbot_factory
        self.bot.config = self.test_server
        self.bot.nickname = "TestBot"
        self.bot.encoding_server = "utf-8"
        self.bot.encoding_channels = {}
        self.bot.load_server_plugins()
        # configure the dispatcher
        self.bot.dispatcher.init(self.bot.config)

        self.answer = []
        def g(towhere, msg, _):
            self.answer.append((towhere, msg.decode("utf8")))
        self.bot.msg = g

        self.disp = self.bot.dispatcher
        for plugin in self.bot.dispatcher._plugins.keys():
            fullname = "%s.%s" % (plugin.__module__, plugin.__class__.__name__)
            if fullname == plugin_name:
                self.plugin = plugin
                break
        else:
            raise ValueError("The searched plugin does not exist!")