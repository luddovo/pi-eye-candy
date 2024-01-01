#!/usr/bin/env python3

import decimal,curses, itertools, signal

# Chudnovsky algorithm for calculating pi from Wikipedia

def binary_split(a, b):
    if b == a + 1:
        Pab = -(6*a - 5)*(2*a - 1)*(6*a - 1)
        Qab = 10939058860032000 * a**3
        Rab = Pab * (545140134*a + 13591409)
    else:
        m = (a + b) // 2
        Pam, Qam, Ram = binary_split(a, m)
        Pmb, Qmb, Rmb = binary_split(m, b)
        
        Pab = Pam * Pmb
        Qab = Qam * Qmb
        Rab = Qmb * Ram + Pam * Rmb
    return Pab, Qab, Rab


def chudnovsky(n):
    P1n, Q1n, R1n = binary_split(1, n)
    return (426880 * decimal.Decimal(10005).sqrt() * Q1n) / (13591409*Q1n + R1n)

term_resized = False

# Signal handler gets called when terminal is resized

def resize_term(signum, frame):
    global term_resized
    term_resized = True

# Set up the signal handler

signal.signal(signal.SIGWINCH, resize_term)

# Main iteration and display code

def main(stdscr):

    stdscr.clear()

    height,width = stdscr.getmaxyx()

    prev = str(decimal.Decimal(0))

    decimal.getcontext().prec = height * width - 2 
    
    for n in itertools.count(3):

        v = chudnovsky(n)

        vs = str(v)

        stdscr.move(0,0)

        done = True

        for i in range(min(len(prev), len(vs))):

            if term_resized: return

            if prev[i] == vs[i]:
                stdscr.addch(vs[i], curses.A_BOLD)
            else:
                stdscr.addch(vs[i])
                done = False

        stdscr.refresh()

        if done: break

        prev = str(v)

    stdscr.getch()

    return 

# Call the main code, if terminal is resized, restart

while True:
    curses.wrapper(main)
    if term_resized:
        term_resized = False
    else:
        break
        
