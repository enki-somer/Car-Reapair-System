.PHONY: test clean-test coverage

test:
	python -m unittest discover tests -v

clean-test:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "test_*.db" -delete
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type d -name "htmlcov" -exec rm -r {} +
	find . -type f -name ".coverage" -delete

coverage:
	coverage run -m unittest discover tests
	coverage report
	coverage html 