all: install dist

install:
	sudo pip install -e .

dist:
	sudo python setup.py sdist

upload: dist
	twine upload dist/*

clean:
	sudo rm -rf dist cryptomkt.egg-info cryptomkt/__pycache__ cryptomkt/*.pyc cryptomkt/Payment/__pycache__ cryptomkt/Payment/*.pyc
