import sys
import py
import os
from os.path import exists

import rpython.rtyper
from rpython.rlib.objectmodel import specialize
from rpython.rlib import rdynload
from rpython.rtyper.lltypesystem import rffi, lltype
from rpython.rtyper.lltypesystem.lltype import FuncType, Ptr

try:
	from rpython.rlib.jit import JitDriver, purefunction
except ImportError:
	class JitDriver(object):
		def __init__(self,**kw): pass
		def jit_merge_point(self,**kw): pass
		def can_enter_jit(self,**kw): pass

def get_location(pc, program, bracket_map):
	return "%s|%s|%s" % (
		program[:pc], program[pc], program[pc+1:]
	)

jitdriver = JitDriver(greens=['pc', 'program', 'bracket_map'], reds=['tape'], 
		get_printable_location=get_location)

@purefunction
def get_matching_bracket(bracket_map, pc):
	return bracket_map[pc]

def mainloop(program, bracket_map):
	pc = 0
	tape = Tape()
	while pc < len(program):
		jitdriver.jit_merge_point(pc=pc, 
				tape=tape, program=program,
				bracket_map=bracket_map,)

		code = program[pc]

		if code == ">":
			tape.advance()

		elif code == "<":
			tape.devance()

		elif code == "+":
			tape.inc()

		elif code == "-":
			tape.dec()
  
		elif code == ".":
			os.write(1, chr(tape.get()))

		elif code == ",":
			tape.set(ord(os.read(0, 1)[0]))

		elif code == "[" and tape.get() == 0:
			pc = get_matching_bracket(bracket_map, pc)

		elif code == "]" and tape.get() != 0:
			pc = get_matching_bracket(bracket_map, pc)

		elif code == "h":
			tape.hello()	

		elif code == "p":
			tape.printPos()

		elif code == "w":
			tape.printVal()

		elif code == "c":
			tape.cfun()

		pc += 1

@specialize.memo()
def return_caller(func):
	source = py.code.Source("""
		def cpy_call_external(funcptr):
			funcptr()
		""")
	miniglobals = {'__name__': __name__}

	exec(source.compile()) in miniglobals
	call_external_function = miniglobals['cpy_call_external']
	call_external_function._dont_inline_ = True
	call_external_function._annspecialcase_ = 'specialize:ll'
	call_external_function._gctransformer_hint_close_stack_ = True

	@specialize.ll()
	def func_exec():
		return call_external_function(func)
	return func_exec

func_void_to_void = lltype.Ptr(lltype.FuncType([], lltype.Void))

func_void_to_int = lltype.Ptr(lltype.FuncType([], lltype.Signed))

######
#subStuct = lltype.GcStruct('uint', ('value', lltype.Unsigned))
exaptionStruct = lltype.GcStruct('exception_t', ('size', lltype.Unsigned), ('array', lltype.Unsigned))

func_exaption_to_void = lltype.Ptr(lltype.FuncType([lltype.Ptr(exaptionStruct)], lltype.Void))
func_exaption_to_int = lltype.Ptr(lltype.FuncType([lltype.Ptr(exaptionStruct)], lltype.Signed))
func_void_to_exaption = lltype.Ptr(lltype.FuncType([lltype.Void], lltype.Ptr(exaptionStruct)))
func_jmp_buf_to_int = lltype.Ptr(lltype.FuncType([lltype.Unsigned], lltype.Signed))
#exp = ['size':0, 'array':, ]	
######

IntStruct = lltype.Struct('MyInt', ('Int', lltype.Signed))
func_void_MyInt = lltype.Ptr(lltype.FuncType([lltype.Ptr(IntStruct)], lltype.Void))

# Add C-func that
from rpython.rtyper.lltypesystem import rffi # lltype 
from rpython.translator.tool.cbuild import ExternalCompilationInfo

info = ExternalCompilationInfo(
	includes=['/home/molotkov/workspace/projects/pyhuawei/pypy-testbench/c-fun/fun.h'],
	include_dirs=['/home/molotkov/workspace/projects/pyhuawei/pypy-testbench/c-fun'],
	separate_module_files=['/home/molotkov/workspace/projects/pyhuawei/pypy-testbench/c-fun/fun.c']
    #libraries=[], 
)
        
# void fun(void)
cHello = rffi.llexternal(
    "hello", [rffi.lltype.Void], rffi.lltype.Void, compilation_info=info
)
# void fun(int)
cPrintInt = rffi.llexternal(
    "printInt", [rffi.lltype.Signed], rffi.lltype.Void, compilation_info=info
)
# int fun(int)
cReturnInt  = rffi.llexternal(
    "printInt", [rffi.lltype.Signed], rffi.lltype.Signed, compilation_info=info
)
# int fun(int, int, int)
cReturnSum = rffi.llexternal(
    "returnSum", [rffi.lltype.Signed, rffi.lltype.Signed], rffi.lltype.Signed, compilation_info=info
)

class Tape(object):
	def func_caller(self):
		self.helloFunc()

	def printer(self, val):
		pIntStruct = lltype.malloc(IntStruct, flavor='raw', immortal=True)
		pIntStruct.Int = val
		self.printMyInt(pIntStruct) 

	def __init__(self):
		self.thetape = [0]
		self.position = 0
		ll_libname = rffi.str2charp('../source/csource/hlib.so')
		self.dll = rdynload.dlopen(ll_libname, rdynload._dlopen_default_mode())
		lltype.free(ll_libname, flavor='raw')

		initptr = rdynload.dlsym(self.dll, 'hello')
		self.helloFunc = rffi.cast(func_void_to_void, initptr)

		printptr = rdynload.dlsym(self.dll, 'printMyInt')
		self.printMyInt = rffi.cast(func_void_MyInt, printptr)

		rptr = rdynload.dlsym(self.dll, 'return42')
		self.return42Func = rffi.cast(func_void_to_int, rptr)
		
		########
		ll_libname = rffi.str2charp('/home/molotkov/workspace/projects/pyhuawei/pypy-testbench/c-fun/hlib.so')
		self.dll2 = rdynload.dlopen(ll_libname, rdynload._dlopen_default_mode())
		lltype.free(ll_libname, flavor='raw')

		#exception_new = rdynload.dlsym(self.dll2, 'exception_new')
		#self.exception_new = rffi.cast(func_void_to_exaption, exception_new)

		exception_init = rdynload.dlsym(self.dll2, 'exception_init')
		self.exception_init = rffi.cast(func_exaption_to_void, exception_init)

		exception_new_point = rdynload.dlsym(self.dll2, 'exception_new_point')
		self.exception_new_point = rffi.cast(func_exaption_to_void, exception_new_point)

		exception_delete = rdynload.dlsym(self.dll2, 'exception_delete')
		self.exception_delete = rffi.cast(func_exaption_to_void, exception_delete)

		try_catch = rdynload.dlsym(self.dll2, 'try_catch')
		self.try_catch = rffi.cast(func_exaption_to_int, try_catch)

		try_catch_end = rdynload.dlsym(self.dll2, 'try_catch_end')
		self.try_catch_end = rffi.cast(func_exaption_to_void, try_catch_end)

		throw = rdynload.dlsym(self.dll2, 'throw')
		self.throw = rffi.cast(func_exaption_to_int, throw)

		setjmp = rdynload.dlsym(self.dll2, 'setjmp')
		self.setjmp = rffi.cast(func_jmp_buf_to_int, setjmp)

		########
	def get(self):
		return self.thetape[self.position]
	def set(self, val):
		self.thetape[self.position] = val
	def inc(self):
		self.thetape[self.position] += 1
	def dec(self):
		self.thetape[self.position] -= 1
	def advance(self):
		self.position += 1
		if len(self.thetape) <= self.position:
			self.thetape.append(0)
	def devance(self):
		self.position -= 1
	def hello(self):
		self.func_caller()
	def printPos(self):
		self.printer(self.position)
	def printVal(self):
		self.printer(self.return42Func())
	def cfun(self):
		#cHello()
		#cPrintInt(5)
		#cPrintInt(cReturnInt(10))
		#cPrintInt(cReturnSum(10, 20))
		exp = lltype.malloc(exaptionStruct)
		#print(exp.array)
		#exp = self.exception_new()
		self.exception_init(exp)
		#print(exp.array)
		self.exception_new_point(exp)
		print("1:try_catch start")

		a = self.try_catch(exp)
		if a != 0:
			print("3:catch section")
		else:
			print("2:Throw")
			self.throw(exp)
			print("ERROR:Baaaaaaaaaad")
		self.try_catch_end(exp)

def parse(program):
	parsed = []
	bracket_map = {}
	leftstack = []
	pc = 0
	for char in program:
		if char in ('[', ']', '<', '>', '+', '-', ',', '.', 'h', 'p', 'w', 'c'):
			parsed.append(char)

			if char == '[':
				leftstack.append(pc)
			elif char == ']':
				left = leftstack.pop()
				right = pc
				bracket_map[left] = right
				bracket_map[right] = left
			pc += 1

	return "".join(parsed), bracket_map

def run(fp):
	program_contents = ""
	while True:	
		read = os.read(fp, 4096)
		if len(read) == 0:
			break
		program_contents += read
	os.close(fp)
	program, bm = parse(program_contents)
	mainloop(program, bm)

def entry_point(argv):
	try:
		filename = argv[1]
	except IndexError:
		print("You must supply a filename")
		return 1
    
	run(os.open(filename, os.O_RDONLY, 0777))
	return 0

def jitpolicy(driver):
	from rpython.jit.codewriter.policy import JitPolicy
	return JitPolicy()

def target(*args):
	return entry_point, None
    
if __name__ == "__main__":
	entry_point(sys.argv)
