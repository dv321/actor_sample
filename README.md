actor_sample
============

A short and sweet example of an actor interface based on ZMQ and Tornado. Takes a pic with a camera via OpenCV

To run, create a virtualenv:
	http://docs.python-guide.org/en/latest/dev/virtualenvs/

Activate:
	. env/bin/activate

Install pip requirements:
	pip install -r requirements.txt

Install opencv:
	http://foxrow.com/installing-opencv-in-a-virtualenv/

In one tty run:
	python server.py

In another run:
	python client.py

