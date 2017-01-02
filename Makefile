.PHONY: clean

clean:
	rm -rf build dist *.egg-info

publish:
	python setup.py sdist bdist_wheel upload
