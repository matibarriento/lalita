# -*- coding: utf-8 -*-

from core.events import TALKED_TO_ME, PUBLIC_MESSAGE, PRIVATE_MESSAGE
from randomer_utils.randomer import contestame
import random
import re


class Randomer(object):

    def __init__(self,config,params):
        self._internals = {}
        pattern = re.compile('.*%s.*' % params['nickname'])
        params['register'](TALKED_TO_ME,self.answer)
        params['register'](PUBLIC_MESSAGE,self.answer,pattern)
        params['register'](PRIVATE_MESSAGE,self.priv_answer)

    def priv_answer(self, user, *args):
        if not user or user.lower() in ['nickserv', 'chanserv']:
            return (user,'')
        else: print '+='*200,user
        return self.answer(user,None,*args)

    def answer(self, user, channel, *args):
        comment = u' '.join(args)
        whom = random.random() > 0.9 and '%s: ' % user or ''
        where = channel is not None and channel or user
        return (where,'%s%s' % (whom,contestame(comment)))
