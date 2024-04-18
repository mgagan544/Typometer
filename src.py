import curses
from curses import wrapper
import time
import sys
import random

def start(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome To WPM test:\n")
    stdscr.addstr("\nPress anyting to start")
    stdscr.refresh()
    stdscr.getkey()

def display(stdscr, target, current , wpm=0):
    stdscr.erase()  # Use erase instead of clear
    stdscr.addstr(0, 0, target)  # Position at line 0, column 0
    stdscr.addstr(1, 0, f"WPM : {wpm}")
    for i,char in enumerate(current):
        current_char=target[i]
        color=curses.color_pair(1)
        if current_char!=char:
            color=curses.color_pair(2)
        stdscr.addstr(0,i,char, color)

def load():
    with open("text.txt","r") as f:
        l=f.readlines()
        return random.choice(l).strip()
        
def wpm(stdscr):
    target_text = load()
    current_text = []
    wpm=0
    start_time=time.time()
    stdscr.nodelay(True)
    curses.noecho()  # Hide user input
    
    try:
        curses.curs_set(0)  # Hide cursor
    except curses.error:
        # Handle error if curs_set() is not supported
        pass
    
    while True:
        time_elapsed=max(time.time()-start_time,1)
        wpm=round((len(current_text)/(time_elapsed/60))/5)
        display(stdscr, target_text, current_text, wpm)  # Display the content
        stdscr.refresh()
        
        if "".join(current_text)==target_text:
            stdscr.nodelay(False)
            stdscr.addstr(2,0,"You Completed The test! Press any key to continue")
            stdscr.getch()  # Wait for a key press
            break
        
        try:
            key = stdscr.getch()  
        except:
            continue
        
        if key == 27:  
            sys.exit()  # Exit the program when ESC is pressed
        
        elif key == curses.KEY_BACKSPACE or key == 127:  
            if len(current_text) > 0:
                current_text.pop()
        elif 0 <= key <= 255 and len(current_text) < len(target_text):
            current_text.append(chr(key))  # Check if key is within ASCII range

def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
    start(stdscr)
    while True:
        wpm(stdscr)

wrapper(main)
