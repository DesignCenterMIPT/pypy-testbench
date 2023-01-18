import os
import sys

s = ""

try:
    from rpython.rlib.jit import JitDriver, purefunction
except ImportError:
    class JitDriver(object):
        def __init__(self,**kw): pass
        def jit_merge_point(self,**kw): pass
        def can_enter_jit(self,**kw): pass

jitdriver = JitDriver(greens=['pc', 'program', 'bracket_map'], reds=['tape'])

#@purefunction
def get_matching_bracket(bracket_map, pc):

    try:
        check_pc(pc)
    except ValueError:
        print "get_matching_bracket: p > 100 \n"
        s = "get_matching_bracket: p > 100 \n"
    return bracket_map[pc]

def make_throw_100():
    raise ValueError

def check_pc(pc):

    try:
        if pc > 100:
            make_throw_100()
    except ValueError as ve:
        print "check_pc: p > 100 \n"
        s = "check_pc: p > 100 \n"
        raise ve

def mainloop(program, bracket_map):
    pc = 0
    tape = Tape()
    count = 1
    while pc < len(program):
        jitdriver.jit_merge_point(pc=pc, 
				tape=tape, program=program,
        		bracket_map=bracket_map)

        code = program[pc]
        if code == "[" and tape.get() == 0:
            try:
                pc = get_matching_bracket(bracket_map, pc)                
                if pc == 10000000:
                    raise RuntimeError("pc == 10000000")
                try:
                    if count % 100 == 0:
                        raise RuntimeError("count")
                except TypeError:
                    print "TypeError raised"
            except RuntimeError as er:
                print "## count ==", count, "##" 

        elif code == "]" and tape.get() != 0:
            pc = get_matching_bracket(bracket_map, pc)
        pc += 1
        count += 1

class Tape(object):
    def __init__(self):
        self.thetape = [0]
        self.position = 0
    
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

def parse(program):
    parsed = []
    bracket_map = {}
    leftstack = []

    pc = 0
    for char in program:
        if char in ('[', ']', '<', '>', '+', '-', ',', '.'):
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
    try:
        mainloop(program, bm)
    except ValueError:
        print "value error in run"

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
