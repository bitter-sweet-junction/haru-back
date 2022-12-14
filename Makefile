.PHONY: style quality test test-cov

check_dirs := haru/ haru-back-generate-image/ scripts/ tests/
test_dirs := haru/

style:
	black $(check_dirs)
	isort $(check_dirs)
	flake8 $(check_dirs)

quality:
	black --check $(check_dirs)
	isort --check-only $(check_dirs)
	flake8 $(check_dirs)

test:
	pytest

test-cov:
	pytest --cov-branch --cov $(test_dirs)
