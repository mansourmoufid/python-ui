all: README.rst

README.rst: README.md
	pandoc README.md -o README.rst

.PHONY: check
check:
	pyflakes ui/*.py
	pycodestyle ui/*.py
	mypy ui/*.py

.PHONY: test
test:
	py.test

.PHONY: cleanup
cleanup:
	rm -f ui/*.pyc ui/*.pyd ui/*.pyo
	rm -rf ui/__pycache__

.PHONY: clean
clean: cleanup
	rm -f README.rst
