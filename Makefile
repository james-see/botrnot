PY=python3 -m py_compile
.PHONY:
	all
	test
	install
	dist
	clean
all:
	@+make test
	@make install
test:
	nosetest
install:
	python3 setup.py\
	install
dist:
	@python3 setup.py sdist bdist_wheel;
	@echo "ready for twine upload dist/*";
compile:
	$(PY) test.py
clean:
	@rm -rf dist build;
	@rm -rf botrnot.egg-info;
	@echo "directories cleaned"
empty:
	# this is a comment
