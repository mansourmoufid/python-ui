.PHONY: check
check:
	pyflakes ui/*.py
	pycodestyle ui/*.py

.PHONY: cleanup
cleanup:
	rm -f ui/*.pyc ui/*.pyd ui/*.pyo
	rm -rf ui/__pycache__

.PHONY: clean
clean: cleanup
