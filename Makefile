PYTHON=python3
PYPY2=pypy2.7
PYPY3=pypy3.9
SOURCE=$(PWD)/source
CODE=$(PWD)/brainfuck
#PYPY_DIR=$(PWD)/../pypy-native
PYPY_DIR=$(PWD)/../pypy
RPYTHON_DIR=$(PYPY_DIR)/rpython
RPYTHON=$(RPYTHON_DIR)/bin/rpython

python_only:
	$(PYTHON) $(SOURCE)/python_only.py $(CODE)/first_brainfuck.b

simple_pypy:
	mkdir -p build 
	cd build; $(PYPY2) $(RPYTHON) --opt=2 $(SOURCE)/simple_pypy.py

jit_pypy:
	mkdir -p build
	cd build; $(PYPY2) $(RPYTHON) --opt=jit $(SOURCE)/jit_pypy.py

opt_jit_pypy:	
	mkdir -p build; 
	cd build; $(PYPY2) $(RPYTHON) --opt=jit $(SOURCE)/opt_jit_pypy.py

log_jit_pypy:	
	mkdir -p build 
	cd build; $(PYPY2) $(RPYTHON) --opt=jit $(SOURCE)/log_jit_pypy.py

rpython_help:
	$(PYPY2) $(RPYTHON) --help

__jit_pypy_with: export PYPY_USESSION_DIR=$(PWD)/tmp/withjit
__jit_pypy_with: export PYPY_USESSION_BASENAME=testbench
__jit_pypy_with:
	mkdir -p tmp/withjit
	mkdir -p build
	cd build; $(PYPY2) $(RPYTHON) -c --opt=jit $(SOURCE)/log_jit_pypy.py
	cd -

__jit_pypy_without: export PYPY_USESSION_DIR=$(PWD)/tmp/withoutjit
__jit_pypy_without: export PYPY_USESSION_BASENAME=testbench
__jit_pypy_without:
	mkdir -p tmp/withoutjit
	mkdir -p build
	cd build; $(PYPY2) $(RPYTHON) -c --opt=jit --no-pyjitpl $(SOURCE)/log_jit_pypy.py

diff: __jit_pypy_with __jit_pypy_without

diff_dir:
	diff -r $(PWD)/tmp/withjit/usession-testbench-`whoami`/ $(PWD)/tmp/withoutjit/usession-testbench-`whoami`/ > d.diff

clear_diff: 
	rm -rfd $(PWD)/tmp/withoutjit/ $(PWD)/tmp/withjit

play_log: export PYPYLOG=jit-backend-dump:jit-backend.dump
play_log: log_jit_pypy 
	mkdir -p build
	cd build; ./log_jit_pypy-c $(CODE)/mandel.b

viewcode: export PYTHONPATH=$(PWD)/../pypy
viewcode: play_log
	$(PYPY2) $(RPYTHON_DIR)/jit/backend/tool/viewcode.py ./build/jit-backend.dump

clean_viewcode:
	rm -f log build/log

funcall: export PYTHONPATH=$(PYPY_DIR)
funcall: export LIBPATH=$(SOURCE)/csource/hlib.so	
funcall:
	$(PYPY2) $(SOURCE)/csource/call_c_fun.py

viewcode_withfun: export PYTHONPATH=$(PYPY_DIR)
viewcode_withfun: play_hellofun
	$(PYPY2) $(RPYTHON_DIR)/jit/backend/tool/viewcode.py ./build/jit-backend.dump

play_hellofun: export PYTHONPATH=$(PYPY_DIR)
play_hellofun: fun_jit_pypy
	mkdir -p build
	cd build; ./fun_jit_pypy-c $(CODE)/hello.b

play_hellofun_alone: export PYPYLOG=jit-backend-dump:jit-backend.dump
play_hellofun_alone:
	mkdir -p build
	cd build ./fun_jit_pypy-c $(CODE)/hello.b

fun_jit_pypy:
	mkdir -p build
	cd build; $(PYPY2) $(RPYTHON) --opt=2 $(SOURCE)/fun_jit_pypy.py

try_except: export PYPY_USESSION_DIR=$(PWD)/tmp/try_except
try_except: 
	mkdir -p tmp/try_except
	mkdir -p build
	cd build; $(PYPY2) $(RPYTHON) -c --opt=2 --gc=incminimark $(SOURCE)/try_except.py
	cd build; ./try_except-c $(CODE)/first_brainfuck.b > $(SOURCE)/../out.log

try_except_mod: export PYPY_USESSION_DIR=$(PWD)/tmp/try_except_mod
try_except_mod: 
	mkdir -p tmp/try_except_mod
	mkdir -p build
	cd build; $(PYPY2) $(RPYTHON) -c --opt=2 --gc=incminimark $(SOURCE)/try_except_mod.py
	cd build; ./try_except_mod-c $(CODE)/first_brainfuck.b > $(SOURCE)/../out.log

