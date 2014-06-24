from program import *
from random import random, choice

# no-operations
def nop0(ind): ind.ip += 1
def nop1(ind): ind.ip += 1
# flip bit
def or1(ind): ind.cx ^= 1; ind.ip += 1; regcheck(ind)
# shift left
def sh1(ind): ind.cx <<= 1; ind.ip += 1; regcheck(ind)
# reset register
def zero(ind): ind.cx ^= ind.cx; ind.ip += 1; regcheck(ind)
# do next if 0 else skip
def if_cz(ind): ind.ip += 2 if ind.cx != 0 else 1
# register subtraction instructions
def sub_ab(ind): ind.cx = ind.ax - ind.bx; ind.ip += 1; regcheck(ind)
def sub_ac(ind): ind.ax -= ind.cx; ind.ip += 1; regcheck(ind)
# register increment instructions
def inc_a(ind): ind.ax += 1; ind.ip += 1; regcheck(ind)
def inc_b(ind): ind.bx += 1; ind.ip += 1; regcheck(ind)
# register decrement instructions
def dec_c(ind): ind.cx -= 1; ind.ip += 1; regcheck(ind)
def inc_c(ind): ind.cx += 1; ind.ip += 1; regcheck(ind)
# stack push instructions
def push_ax(ind): ind.stack.append(ind.ax); ind.ip += 1; regcheck(ind)
def push_bx(ind): ind.stack.append(ind.bx); ind.ip += 1; regcheck(ind)
def push_cx(ind): ind.stack.append(ind.cx); ind.ip += 1; regcheck(ind)
def push_dx(ind): ind.stack.append(ind.dx); ind.ip += 1; regcheck(ind)
# stack pop instructions
def pop_ax(ind):
    if ind.stack: ind.ax = ind.stack.pop()
    else: ind.fail += 1
    ind.ip += 1; regcheck(ind)
def pop_bx(ind):
    if ind.stack: ind.bx = ind.stack.pop()
    else: ind.fail += 1
    ind.ip += 1; regcheck(ind)
def pop_cx(ind):
    if ind.stack: ind.cx = ind.stack.pop()
    else: ind.fail += 1
    ind.ip += 1; regcheck(ind)
def pop_dx(ind):
    if ind.stack: ind.dx = ind.stack.pop()
    else: ind.fail += 1
    ind.ip += 1; regcheck(ind)
# jump to template
def jmp(ind):
    sp = template(ind, (-1024,0), ind.sim.memory, -1)
    if not sp: sp = template(ind, (0,1024), ind.sim.memory)
    (ind.fail, ind.ip) = (ind.fail, sp[0]) if sp else (ind.fail + 1, ind.ip + 1)
def jmpb(ind):
    sp = template(ind, (-1024, 0), ind.sim.memory, -1)
    (ind.fail, ind.ip) = (ind.fail, sp[0]) if sp else (ind.fail + 1, ind.ip + 1)
# temporary jump to template
def call(ind):
    sp = template(ind, (-1024, 1024), ind.sim.memory)
    if sp: ind.stack.append(ind.ip + 1)
    (ind.fail, ind.ip) = (ind.fail, sp[0]) if sp else (ind.fail + 1, ind.ip + 1)
# return from call
def ret(ind): ind.ip = ind.stack.pop()
# move registers
def mov_cd(ind): ind.dx = ind.cx; ind.ip += 1; regcheck(ind)
def mov_ab(ind): ind.bx = ind.ax; ind.ip += 1; regcheck(ind)
# copy instruction 
def mov_iab(ind):
    if permission(ind, ind.sim.memory): write(ind, ind.sim.memory,ind.sim.copy_error_rate)
    else: ind.fail += 1
    ind.ip += 1
# find template
def adr(ind):
    sp = template(ind, (0,1024), ind.sim.memory)
    if not sp:  sp = template(ind, (-1024,0), ind.sim.memory, -1)
    if sp: ind.ax, ind.cx = sp
    else: ind.fail += 1
    ind.ip += 1; regcheck(ind)
def adrb(ind):
    sp = template(ind, (-1024, 0), ind.sim.memory, -1)
    if sp: ind.ax, ind.cx = sp
    else: ind.fail += 1
    ind.ip += 1; regcheck(ind)
def adrf(ind):
    sp = template(ind, (0, 1024), ind.sim.memory)
    if sp: ind.ax, ind.cx = sp
    else: ind.fail += 1
    ind.ip += 1; regcheck(ind)
# allocate daughter memory
def mal(ind):
    if permission(ind, ind.sim.memory) and not ind.offspring:
        ind.offspring = (ind.ax, ind.cx)
    else: ind.fail += 1
    ind.ip += 1
# divide into two
def div(ind):
    if not ind.offspring: ind.fail += 1
    elif not integrity(ind.sim.memory,ind.offspring): ind.fail += 1
    else: Program(ind.sim, ind.offspring, ind.id); ind.offspring = False
    ind.ip += 1

# aux fuctions
def template(ind, span, memory, direction = 1):
    temp = []
    i = ind.ip + 1
        # retrieving the template
    while True:
        if memory[i] == 0x01: temp.append(0x00); i += 1
        elif memory[i] == 0x00: temp.append(0x01); i += 1
        else: break
    if len(temp) == 0: return None

        # complement search
    if direction == -1:
        for k in range(i , i + span[0], -1):
            if memory[k - len(temp): k] == temp: return k, len(temp)
        else: return None
    else:
        for k in range(i, i + span[1]):
            if memory[k: k + len(temp)] == temp: return k + len(temp), len(temp)
        else: return None

def permission(ind, memory):
    return False if [True for i in memory[ind.ax: ind.ax+ind.dx] if i != -1]\
           else True 

def integrity(memory, offspring):
    begin, end = offspring[0], offspring[0] + offspring[1]
    return False if -1 in memory[begin:end] else True

def write(ind, memory, copy):
    memory[ind.ax] = choice(instructions.keys()) if random() <= copy else memory[ind.bx]
    
def wrapcheck(memory,pointer):
    return pointer if pointer < len(memory) else pointer - len(memory)

def regcheck(ind):
    regs = []
    for i in [ind.ax,ind.bx,ind.cx,ind.dx]:
        if i >= len(ind.sim.memory): i -= len(ind.sim.memory)
        if i < 0: i += len(ind.sim.memory)
        regs.append(i)
    ind.ax, ind.bx, ind.cx, ind.dx = regs[0],regs[1],regs[2],regs[3]

def none(ind): pass

instructions = {-0x01: none,
    0x00: nop0, 0x01: nop1, 0x02: or1, 0x03: sh1,
    0x04: zero, 0x05: if_cz, 0x06: sub_ab, 0x07: sub_ac,
    0x08: inc_a, 0x09: inc_b, 0x0a: dec_c, 0x0b: inc_c,
    0x0c: push_ax, 0x0d: push_bx, 0x0e: push_cx, 0x0f: push_dx,
    0x10: pop_ax, 0x11: pop_bx, 0x12: pop_cx, 0x13: pop_dx,
    0x14: jmp, 0x15: jmpb, 0x16: call, 0x17: ret,
    0x18: mov_cd, 0x19: mov_ab, 0x1a: mov_iab, 0x1b: adr,
    0x1c: adrb, 0x1d: adrf, 0x1e: mal, 0x1f: div}

