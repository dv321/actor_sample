import zmq
context = zmq.Context()

from tornado.gen import coroutine, Task
from zmq.eventloop import ioloop
ioloop.install()
IOLoop = ioloop.IOLoop

from actor import Actor, channels

import logging
from sys import stdout
logging.basicConfig(stream=stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)

def I_want_a_pic(actor):
	'''
	Tell brain that we want it to take a picture
	'''

	msg = {
		'meta': {
			'to': ['brain'],
            'route': 'take_pic'
        },
        'content': []
    }

	actor.send_message(msg)

actor = Actor(
	context,
    logger,

	#connect to brain so we can send messages
	[ { 'name':'brain', 'type':'zmq', 'port':channels['brain'], 'bind_or_connect':'connect',
	    'socket_type': zmq.PAIR, 'subscribe':False}
	]
)

#call 'I_want_a_pic' in 2 seconds, pass 'actor' as an argument
IOLoop.current().call_later( 2, I_want_a_pic, actor )

#start the IOLoop
IOLoop.current().start()
