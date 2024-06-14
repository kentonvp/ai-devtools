.PHONY: tests docs

tests:
	poetry run pytest . -v

docs:
	poetry run pdoc3 . -o ./docs
