PYTHON=python3
PYPY=pypy
SOURCE=source
CODE=brainfuck
RPYTHON_DIR=$(PWD)/../pypy/rpython
RPYTHON=$(RPYTHON_DIR)/bin/rpython

python_only:
	$(PYTHON) $(SOURCE)/python_only.py $(CODE)/first_brainfuck.b

install_pypy_rpython:
	git submodule init
	git submodule update

simple_pypy:
	mkdir -p build
	$(PYPY) $(RPYTHON) --opt=2 $(SOURCE)/simple_pypy.py
	mv -f simple_pypy-c build 	

jit_pypy:
	mkdir -p build
	$(PYPY) $(RPYTHON) --opt=jit $(SOURCE)/jit_pypy.py
	mv -f jit_pypy-c build 	

opt_jit_pypy:	
	mkdir -p build
	$(PYPY) $(RPYTHON) --opt=jit $(SOURCE)/opt_jit_pypy.py
	mv -f opt_jit_pypy-c build 	

log_jit_pypy:	
	mkdir -p build
	$(PYPY) $(RPYTHON) --opt=jit $(SOURCE)/log_jit_pypy.py
	mv -f log_jit_pypy-c build

#use export PYPY_USESSION_DIR=`pwd`/tmp
rpython_help:
	$(PYPY) $(RPYTHON) --help

__jit_pypy_with: export PYPY_USESSION_DIR=$(PWD)/tmp/withjit
__jit_pypy_with:
	mkdir -p tmp/withjit
	$(PYPY) $(RPYTHON) -c --opt=jit $(SOURCE)/log_jit_pypy.py

__jit_pypy_without: export PYPY_USESSION_DIR=$(PWD)/tmp/withoutjit
__jit_pypy_without:
	mkdir -p tmp/withoutjit
	$(PYPY) $(RPYTHON) -c --opt=jit --no-pyjitpl $(SOURCE)/log_jit_pypy.py

diff: __jit_pypy_with __jit_pypy_without

diff_dir:
	diff -r $(PWD)/tmp/withjit/usession-8276b505180f-1/ $(PWD)/tmp/withoutjit/usession-8276b505180f-1/ # > d.diff

clear_diff: 
	rm -rfd $(PWD)/tmp/withoutjit/ $(PWD)/tmp/withjit

play_log: export PYPYLOG=jit-backend-dump:l.log
play_log: log_jit_pypy 
	cd build && ./log_jit_pypy-c ../brainfuck/mandel.b

viewcode: export PYTHONPATH=$(PWD)/../pypy
viewcode: play_log
	pypy $(RPYTHON_DIR)/jit/backend/tool/viewcode.py ./build/l.log

clean_viewcode:
	rm -f log build/log

funcall: export PYTHONPATH=$(PWD)/../pypy
funcall: export LIBPATH=$(PWD)/source/csource/hlib.so	
funcall:
	pypy ./source/csource/funcall.py

viewcode_withfun: export PYTHONPATH=$(PWD)/../pypy
viewcode_withfun: play_hellofun
	pypy $(RPYTHON_DIR)/jit/backend/tool/viewcode.py ./build/l.log	

play_hellofun: export PYPYLOG=jit-backend-dump:l.log
play_hellofun: export PYTHONPATH=$(PWD)/../pypy
play_hellofun: fun_jit_pypy
	cd build && ./fun_jit_pypy-c ../brainfuck/mandel.b

fun_jit_pypy: 
fun_jit_pypy:
	mkdir -p build
	$(PYPY) $(RPYTHON) --opt=jit $(SOURCE)/fun_jit_pypy.py
	mv -f fun_jit_pypy-c build

