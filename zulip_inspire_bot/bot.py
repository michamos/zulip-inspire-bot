# -*- coding: utf-8 -*-
#
# This file is part of INSPIRE.
# Copyright (C) 2018 CERN.
#
# INSPIRE is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# INSPIRE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with INSPIRE. If not, see <http://www.gnu.org/licenses/>.
#
# In applying this license, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization
# or submit itself to any jurisdiction.

"""Zulip chatbot for Inspire"""

from __future__ import absolute_import, division, print_function

from io import RawIOBase

from six import iteritems
from zulip import Client

class ZulipBot(object):
    def __init__(self, name, stream):
        self._client = Client()
        self._name = name
        self._self_short_name = u'{name}-bot'.format(name=self._name)
        self._self_mention = self._format_mention(self._name)
        self._stream = stream
        self._topic_router = {}
        self._command_handlers = {
            'hello': self._hello_command_handler,
            'help': self._help_command_handler,
        }

    def run(self):
        self._client.call_on_each_message(self._message_handler)

    def send_public_message(self, content, topic, stream=None):
        message = {
            'type': 'stream',
            'to': stream or self._stream,
            'content': content,
            'topic': topic,
        }
        self._client.send_message(message)

    def send_private_message(self, content, address):
        message = {
            'type': 'private',
            'to': address,
            'content': content
        }
        self._client.send_message(message)

    def send_reply(self, content, message):
        """Send content as reply to message."""
        if self._is_private_message(message):
            self.send_private_message(content, message.get('sender_email'))
        else:
            self.send_public_message(content, message.get('subject'), message.get('stream'))

    @staticmethod
    def _format_mention(name):
        return u'@**{name}**'.format(name=name)

    def _is_self_sent(self, message):
        return message.get('sender_short_name') == self._self_short_name

    def _is_self_mention(self, message):
        return message.get('content').find(self._self_mention) != -1

    def _strip_self_mention(self, content):
        return content.replace(self._self_mention, '')

    @staticmethod
    def _is_private_message(message):
        return message.get('type') == 'private'

    def _message_handler(self, message):
        is_relevant_message = not self._is_self_sent(message) and (
                self._is_self_mention(message) or self._is_private_message(message)
        )
        if is_relevant_message:
            topic = message.get('subject')
            self._topic_router.get(topic, self._default_router)(message)

    def _default_router(self, message):
        commands = [cmd for cmd in self._strip_self_mention(message.get('content')).split(' ') if cmd]
        self._command_handlers.get(commands[0], self._default_command_handler)(commands[1:], message)

    def _default_command_handler(self, subcommands, message):
        reply = (
            u'I did not understand the message:\n'
            u'```quote\n'
            u'{content}\n'
            u'```\n'
            u'For a list of recognized commands, send `help`.'
        ).format(content=message.get('content'))
        self.send_reply(reply, message)

    def _help_command_handler(self, subcommands, message):
        """Get help about recognized commands."""
        if subcommands and subcommands[0] in self._command_handlers:
            command = subcommands[0]
            reply = u'*{command}*: {desc}'.format(command=command, desc=self._command_handlers[command].__doc__)
        else:
            reply = [(
                u'**Supported commands**\n'
                u'\n'
                u'Command|Description\n'
                u'-------|-----------'
            )]
            reply.extend(u'{cmd}|{desc}'.format(cmd=k, desc=v.__doc__.split('\n')[0])
                         for (k, v) in iteritems(self._command_handlers))
            reply.append(u'\nSend `help {command}` for more information.')
            reply = '\n'.join(reply)

        self.send_reply(reply, message)

    def _hello_command_handler(self, subcommands, message):
        """Say hello."""
        sender = message.get('sender_short_name')
        reply = u'Hi {mention} :wave:'.format(mention=self._format_mention(sender))
        self.send_reply(reply, message)


class ZulipWriter(RawIOBase):
    def __init__(self, client, stream, topic):
        self._client = client
        self._stream = stream
        self._topic = topic

    def write(self, content):
        message = {
            'type': 'private',
            'to': ['michamos@gmail.com'],
            'content': content,
            'subject': self._topic,
        }
        print(self._client.send_message(message))
