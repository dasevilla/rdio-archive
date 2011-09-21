.PHONEY: archive site clean lint py-lint js-lint

archive:
	python rdio-downloader.py

site:
	python archive-music.py
	cp -r template/static _generated/

clean:
	- rm -r _generated/*

lint: py-lint js-lint

py-lint:
	find . -name '*.py' | xargs pyflakes
	find . -name '*.py' | xargs pep8

js-lint:
	jshint template/static/js/main.js
