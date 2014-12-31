import zmq
context = zmq.Context()

from tornado.gen import coroutine, Task
from zmq.eventloop import ioloop
ioloop.install()
IOLoop = ioloop.IOLoop

from actor import Actor, channels

import cv2
cv = cv2.cv

import logging
from sys import stdout
logging.basicConfig(stream=stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)

@coroutine
def take_pic(message, actor):
	'''
	Takes a pic using the first camera opencv finds, then saves it
	and sends a message to command and control (which is nonexistant in this demo)
	letting it know that the task is completed
	'''

	camera = cv.CaptureFromCAM(0)

	img = cv.QueryFrame(camera)

	filepath = 'shot.jpg'

	cv.SaveImage(filepath, img)

	actor.send_message({
		'meta': {
			'to': ['candc'],
			'route': 'pic'
		},
	    'content': [filepath]
	})


actor = Actor(
	context,
    logger,

	[
		#bind to the channel you want to get messages from
		{ 'name':'brain', 'type': 'zmq', 'port':channels['brain'], 'bind_or_connect':'bind',
          'socket_type': zmq.PAIR, 'subscribe':False }
	],

	{ 'take_pic': take_pic }
)

#start the IOLoop
IOLoop.current().start()

