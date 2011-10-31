.PHONEY: download resources site clean lint py-lint js-lint

GIT_PATH=$(shell python rdioconfig.py get_downloader_path)
GEN_PATH=$(shell python rdioconfig.py get_archiver_path)
WEB_PATH=$(shell python rdioconfig.py get_web_path)

download:
	python rdio-downloader.py

site: resources
	python archive-music.py
	cp -r template/static _generated/

resources:
	cp -r template/static _generated/

deploy:
	cp -r $(GEN_PATH)/*  $(WEB_PATH)

commit:
	cd $(GIT_PATH) && git add .
	cd $(GIT_PATH) && git commit -m "`date \"+%D %R\"` import"
	cd $(GIT_PATH) && git push

clean:
	- rm -r _generated/*

lint: py-lint js-lint

py-lint:
	find . -name '*.py' | xargs pyflakes
	find . -name '*.py' | xargs pep8

js-lint:
	jshint template/static/js/main.js
