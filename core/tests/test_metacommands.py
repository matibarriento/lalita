# -*- coding: utf8 -*-

import unittest
import re

from twisted.trial.unittest import TestCase as TwistedTestCase
from twisted.internet import defer, reactor

from core import events
from core import dispatcher
import ircbot

ircbot_factory = ircbot.IRCBotFactory(dict(log_config="error"))
ircbot.logger.setLevel("error")
bot = ircbot.IrcBot()
bot.factory = ircbot_factory
bot.msg = lambda *a:None

# FIXME: all these messages should be internationalized per server (not locale)
PREFIX_LIST = u"Las órdenes son: ".encode("utf8")
GENERIC_HELP = u'"list" para ver las órdenes; "help cmd" para cada uno'.encode("utf8")
NODOCSTRING = u"No tiene documentación, y yo no soy adivina...".encode("utf8")
SEVERALDOCS = u"Hay varios métodos para esa órden:".encode("utf8")


class TestList(unittest.TestCase):
    def setUp(self):
        self.disp = dispatcher.Dispatcher(bot)
        self.disp.init({})

        self.said = []
        bot.msg = lambda *a: self.said.append(a)

        class Helper(object):
            def f(self, *a): pass
            def g(self, *a): pass
        self.helper = Helper()
        self.disp.new_plugin(self.helper, "channel")

    def test_1met_1cmd(self):
        self.disp.register(events.COMMAND, self.helper.f, ("t1",))
        self.disp.push(events.COMMAND, "user", "channel", "list")
        self.assertEqual(self.said[0][1], PREFIX_LIST + "['t1']")

    def test_1met_2cmd(self):
        self.disp.register(events.COMMAND, self.helper.f, ("t1", "t2"))
        self.disp.push(events.COMMAND, "user", "channel", "list")
        self.assertEqual(self.said[0][1], PREFIX_LIST + "['t1', 't2']")

    def test_2met_1cmd(self):
        self.disp.register(events.COMMAND, self.helper.f, ("t1",))
        self.disp.register(events.COMMAND, self.helper.g, ("t2",))
        self.disp.push(events.COMMAND, "user", "channel", "list")
        self.assertEqual(self.said[0][1], PREFIX_LIST + "['t1', 't2']")

    def test_2met_2cmd(self):
        self.disp.register(events.COMMAND, self.helper.f, ("t1", "t2"))
        self.disp.register(events.COMMAND, self.helper.g, ("t3", "t4"))
        self.disp.push(events.COMMAND, "user", "channel", "list")
        self.assertEqual(self.said[0][1],
                         PREFIX_LIST + "['t1', 't2', 't3', 't4']")


class TestHelp(unittest.TestCase):
    def setUp(self):
        self.disp = dispatcher.Dispatcher(bot)
        self.disp.init({})

        self.said = []
        bot.msg = lambda *a: self.said.append(a)

        class Helper(object):
            def f(self, *a):
                pass
            def g(self, *a):
                "foo"
            def h(self, *a):
                "bar"
            def i(self, *a):
                pass
        self.helper = Helper()
        self.disp.new_plugin(self.helper, "channel")

    def test_generic_help(self):
        self.disp.push(events.COMMAND, "user", "channel", "help")
        self.assertEqual(self.said[0][1], GENERIC_HELP)

    def test_no_doc(self):
        self.disp.register(events.COMMAND, self.helper.f, ("cmd",))
        self.disp.push(events.COMMAND, "user", "channel", "help", "cmd")
        self.assertEqual(self.said[0][1], NODOCSTRING)

    def test_simple_doc(self):
        self.disp.register(events.COMMAND, self.helper.g, ("cmd",))
        self.disp.push(events.COMMAND, "user", "channel", "help", "cmd")
        self.assertEqual(self.said[0][1], "foo")

    def test_repeated_doc(self):
        self.disp.register(events.COMMAND, self.helper.g, ("cmd",))
        self.disp.register(events.COMMAND, self.helper.h, ("cmd",))
        self.disp.push(events.COMMAND, "user", "channel", "help", "cmd")
        self.assertEqual(self.said[0][1], SEVERALDOCS)
        self.assertEqual(self.said[1][1], " - foo")
        self.assertEqual(self.said[2][1], " - bar")

    def test_repeated_no_doc(self):
        self.disp.register(events.COMMAND, self.helper.f, ("cmd",))
        self.disp.register(events.COMMAND, self.helper.i, ("cmd",))
        self.disp.push(events.COMMAND, "user", "channel", "help", "cmd")
        self.assertEqual(self.said[0][1], SEVERALDOCS)
        self.assertEqual(self.said[1][1], " - " + NODOCSTRING)
        self.assertEqual(self.said[2][1], " - " + NODOCSTRING)

    def test_mixed_no_doc(self):
        self.disp.register(events.COMMAND, self.helper.g, ("cmd",))
        self.disp.register(events.COMMAND, self.helper.i, ("cmd",))
        self.disp.push(events.COMMAND, "user", "channel", "help", "cmd")
        self.assertEqual(self.said[0][1], SEVERALDOCS)
        self.assertEqual(self.said[1][1], " - foo")
        self.assertEqual(self.said[2][1], " - " + NODOCSTRING)


class TestMoreHelp(unittest.TestCase):
    '''With the plugin in more channels.'''
    def setUp(self):
        self.disp = dispatcher.Dispatcher(bot)
        self.disp.init({})

        self.said = []
        bot.msg = lambda *a: self.said.append(a)

        class Helper(object):
            def f(self, *a):
                pass
            def g(self, *a):
                "foo"
            def h(self, *a):
                "bar"
            def i(self, *a):
                pass
        self.help1 = Helper()
        self.help2 = Helper()
        self.disp.new_plugin(self.help1, "channel")
        self.disp.new_plugin(self.help2, "chann2")

    def test_generic_help(self):
        self.disp.push(events.COMMAND, "user", "channel", "help")
        self.assertEqual(self.said[0][1], GENERIC_HELP)

    def test_no_doc(self):
        self.disp.register(events.COMMAND, self.help1.f, ("cmd",))
        self.disp.register(events.COMMAND, self.help2.f, ("cmd",))
        self.disp.push(events.COMMAND, "user", "channel", "help", "cmd")
        self.assertEqual(self.said[0][1], NODOCSTRING)

    def test_simple_doc(self):
        self.disp.register(events.COMMAND, self.help1.g, ("cmd",))
        self.disp.register(events.COMMAND, self.help2.g, ("cmd",))
        self.disp.push(events.COMMAND, "user", "channel", "help", "cmd")
        self.assertEqual(self.said[0][1], "foo")

    def test_repeated_doc(self):
        self.disp.register(events.COMMAND, self.help1.g, ("cmd",))
        self.disp.register(events.COMMAND, self.help1.h, ("cmd",))
        self.disp.register(events.COMMAND, self.help2.g, ("cmd",))
        self.disp.register(events.COMMAND, self.help2.h, ("cmd",))
        self.disp.push(events.COMMAND, "user", "channel", "help", "cmd")
        self.assertEqual(self.said[0][1], SEVERALDOCS)
        self.assertEqual(self.said[1][1], " - foo")
        self.assertEqual(self.said[2][1], " - bar")

    def test_repeated_no_doc(self):
        self.disp.register(events.COMMAND, self.help1.f, ("cmd",))
        self.disp.register(events.COMMAND, self.help1.i, ("cmd",))
        self.disp.register(events.COMMAND, self.help2.f, ("cmd",))
        self.disp.register(events.COMMAND, self.help2.i, ("cmd",))
        self.disp.push(events.COMMAND, "user", "channel", "help", "cmd")
        self.assertEqual(self.said[0][1], SEVERALDOCS)
        self.assertEqual(self.said[1][1], " - " + NODOCSTRING)
        self.assertEqual(self.said[2][1], " - " + NODOCSTRING)

    def test_mixed_no_doc(self):
        self.disp.register(events.COMMAND, self.help1.g, ("cmd",))
        self.disp.register(events.COMMAND, self.help1.i, ("cmd",))
        self.disp.register(events.COMMAND, self.help2.g, ("cmd",))
        self.disp.register(events.COMMAND, self.help2.i, ("cmd",))
        self.disp.push(events.COMMAND, "user", "channel", "help", "cmd")
        self.assertEqual(self.said[0][1], SEVERALDOCS)
        self.assertEqual(self.said[1][1], " - foo")
        self.assertEqual(self.said[2][1], " - " + NODOCSTRING)