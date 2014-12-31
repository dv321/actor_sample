import zmq
from zmq.eventloop import zmqstream
import zmq.utils.jsonapi as json

channels = {
	'world': 45670,
	'brain': 45671,
	'candc': 45672
}

class Actor(object):

	def __init__(self, context, logger, channels, routes=None):

		self.context = context
		self.logger = logger
		self.channels = channels
		self.routes = routes

		#go through each channel and add it to our internal channel list
		for channel in self.channels:

			port = channel['port']
			socket_type = channel['socket_type']
			subscribe = channel['subscribe']
			bind_or_connect = channel['bind_or_connect']

			socket = self.context.socket(socket_type)

			if subscribe:
				socket.setsockopt_string(zmq.SUBSCRIBE, u"")

			if bind_or_connect == "bind":
				socket.bind( "tcp://127.0.0.1:"+str(port) )
			else:
				socket.connect( "tcp://127.0.0.1:"+str(port) )

			stream = zmqstream.ZMQStream(socket)

			if self.routes:
				self.logger.debug("listening")
				stream.on_recv_stream(self.on_receive_message)

			channel['socket'] = socket
			channel['stream'] = stream


	#when we get a message, route it to the appropriate callback
	def on_receive_message(self, stream, message):

		self.route(message)

	def send_message(self, message):

		if "to" not in message['meta'] or len( message['meta']['to'] ) == 0:
			self.logger.debug("'TO' NOT IN OBJECT META")
			raise AttributeError

		send_to = []

		#go through the list of recipients
		for recipient in message['meta']['to']:

			#go through the channels and find ones that we want to send to
			#and that we can write to
			for channel in self.channels:
				if channel['name'] == recipient:
					send_to.append( channel )

		for channel in send_to:

			self.logger.debug("sending to "+channel['name'])
			self.logger.debug(message)

			channel['socket'].send_json(message)

	def route(self, message):

		message = json.loads( message[0].decode("utf-8") )

		self.logger.debug("received message")
		self.logger.debug(message)

		#call the function associated with the route
		#pass it the message and the actor instance
		self.routes[ message['meta']['route'] ] (message, self)

