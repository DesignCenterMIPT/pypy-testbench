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

def print_on_file_p(string):
    file = open("p.log", "a")
    file.write(string)
    file.close()
    return 0

#@purefunction
def get_matching_bracket(bracket_map, pc):
    try:
        check_pc(pc)
    except ValueError:
        print_on_file_p("get_matching_bracket: p > 100\n")
    return bracket_map[pc]

def make_throw_100():
    m = 0;
    for i in range(1000000):
        m += i;
    
    raise ValueError

def lvl1_fake_function():
    lvl2_fake_function()

def lvl2_fake_function():
    lvl3_fake_function()

def lvl3_fake_function():
    lvl4_fake_function()

def lvl4_fake_function():
    lvl5_fake_function()

def lvl5_fake_function():
    make_throw_100()

def check_pc(pc):
    try:
        if pc > 100:
            lvl1_fake_function()
    except ValueError as ve:
        print_on_file_p("check_pc: p > 100\n")
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
                print_on_file_p("## count ==" + str(count) + "##\n")

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
    # init empty outout file
    file = open("p.log", "w")
    file.close()
    while True:
        read = os.read(fp, 4096)
        if len(read) == 0:
            break
        program_contents += read
    os.close(fp)
    program, bm = parse(program_contents)
    try:
        for i in range(170):
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
