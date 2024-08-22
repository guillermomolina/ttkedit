.PHONY: .venv deploy deployTest

.venv:
	python3 -m venv .venv
	. .venv/bin/activate ; \
	pip install -r requirements.txt
	#  Regen requirements;
	#    pip freeze > requirements.txt

deployTest: .venv
	. .venv/bin/activate ; \
	python3 -m twine upload --repository testpypi tmp/dist/* --verbose

deploy: .venv
	. .venv/bin/activate ; \
	python3 -m twine upload tmp/dist/* --repository ttkeditor --verbose

