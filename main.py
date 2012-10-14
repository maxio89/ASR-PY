#!/usr/bin/python
# Voice control of industrial robot Kawasaki via Raspberry Pi
# author: Piotr Kozlowski
# created: September 2012


import subprocess
import pexpect
import time
import re
import string
import pxssh
import random
import sys
import telnetlib
from threading import Timer

#global
stage = 0
begin = 0
pause = 0
in_text = "sad"
checkersList = []
s = pxssh.pxssh()
color_human = "blabla"
color_robot = "blabla"
host = "192.168.1.202"
tn = 0
index = 10
timer_elapsed = 0
timer_fun = 0
timer_on = False
timer_end = 0
game = "blabla"
position = "position startpos moves"

class Checker(object):
    #def addChecker(name, x, y):
    def __init__(self, name=None, x=None, y=None):
    	self.name = name
        self.x = x
        self.y = y

def set_board(color):
	if checkersList:
		del checkersList[:]
	if color == "sheep":
		checkersList.append(Checker("sheep", 1, 1))
		checkersList.append(Checker("wolf", 2, 4))
		checkersList.append(Checker("sheep", 3, 1))
		checkersList.append(Checker("sheep", 5, 1))
		checkersList.append(Checker("sheep", 7, 1))
	elif color == "wolf":
		checkersList.append(Checker("sheep", 1, 7))
		checkersList.append(Checker("wolf", 1, 5))
		checkersList.append(Checker("sheep", 3, 7))
		checkersList.append(Checker("sheep", 6, 8))
		checkersList.append(Checker("sheep", 8, 8))
	elif color == "light" or color == "dark":
		#rnbqkbnr
		checkersList.append(Checker("R", 1, 1))
		checkersList.append(Checker("N", 2, 1))
		checkersList.append(Checker("B", 3, 1))
		checkersList.append(Checker("Q", 4, 1))
		checkersList.append(Checker("K", 5, 1))
		checkersList.append(Checker("B", 6, 1))
		checkersList.append(Checker("N", 7, 1))
		checkersList.append(Checker("R", 8, 1))
		checkersList.append(Checker("P", 1, 2))
		checkersList.append(Checker("P", 2, 2))
		checkersList.append(Checker("P", 3, 2))
		checkersList.append(Checker("P", 4, 2))
		checkersList.append(Checker("P", 5, 2))
		checkersList.append(Checker("P", 6, 2))
		checkersList.append(Checker("P", 7, 2))
		checkersList.append(Checker("P", 8, 2))
		
		checkersList.append(Checker("r", 1, 8))
		checkersList.append(Checker("n", 2, 8))
		checkersList.append(Checker("b", 3, 8))
		checkersList.append(Checker("q", 4, 8))
		checkersList.append(Checker("k", 5, 8))
		checkersList.append(Checker("b", 6, 8))
		checkersList.append(Checker("n", 7, 8))
		checkersList.append(Checker("r", 8, 8))
		checkersList.append(Checker("p", 1, 7))
		checkersList.append(Checker("p", 2, 7))
		checkersList.append(Checker("p", 3, 7))
		checkersList.append(Checker("p", 4, 7))
		checkersList.append(Checker("p", 5, 7))
		checkersList.append(Checker("p", 6, 7))
		checkersList.append(Checker("p", 7, 7))
		checkersList.append(Checker("p", 8, 7))
	
		
def telnet_send(source, target):
	global tn
	
	#if ssh_connect():
		#print "connected via ssh"
	#else:
		#print "ssh error!"
	
	#s.sendline("ls -l")
	#s.prompt()
	#print s.before
	#s.sendline("touch sshfile")
	#s.prompt()
	#s.sendline("touch sshfile2")
	#s.prompt()
	
	#s.sendline("SPEED 10")
	#s.prompt()
	#s.sendline("POINT #source=#" + )
	#s.prompt()
	#s.sendline("")
	#s.prompt()
	#s.sendline("POINT #target=#")
	#s.prompt()
	#s.sendline("")
	#s.prompt()
	#s.sendline("EX pg753")
	#s.prompt()
	
	tn.sendline('SPEED 10')
	tn.expect(">")
	print tn.before
	tn.sendline('POINT #source=#p_' + source)
	#tn.expect(">")
	print tn.before
	tn.sendline('')
	tn.expect(">")
	print tn.before
	tn.sendline('POINT #target=#p_' + target)
	#tn.expect(">")
	print tn.before	
	tn.sendline('')
	tn.expect(">")
	print tn.before
	tn.sendline('ex pg753')
	tn.expect("completed")
	print tn.before
	
	#time.sleep(1)
	
def telnet_connect():
	global tn
	
	try: 
		tn = pexpect.spawn ('telnet 192.168.1.202')
		tn.expect("login: ")
		print tn.before
		tn.sendline('as')
		
		tn.expect(">")
		print tn.before
		
	except pexpect.EOF:
		tn.close()

def play_wav(name):
	try: 
		child = pexpect.spawn ('aplay wav/' + name)
		child.expect("play")
	except pexpect.EOF:
		child.close

def letter_to_number(letter):
	x = 1
	try:
		return {
	    		'ALFA': 1,
	    		'BRAVO': 2,
	    		'CHARLIE': 3,
	    		'DELTA': 4,
	    		'ECHO': 5,
	    		'FOXTROT': 6,
	    		'GOLF': 7,
	    		'HOTEL': 8
	    		}[letter]
  	except KeyError:
  		pass
  		
def number_to_number(number):
	x = 1
	try:
		return {
	    		'JEDYNKA': 1,
	    		'DWA': 2,
	    		'TRZY': 3,
	    		'CZTERY': 4,
	    		'PIATKA': 5,
	    		'SZESC': 6,
	    		'SIEDEM': 7,
	    		'OSIEM': 8
	    		}[number]
  	except KeyError:
  		pass
 
def number_to_letter(number):
	x = 1
	try:
		return {
	    		1: 'a',
	    		2: 'b',
	    		3: 'c',
	    		4: 'd',
	    		5: 'e',
	    		6: 'f',
	    		7: 'g',
	    		8: 'h'
	    		}[number]
  	except KeyError:
  		pass
 
def letter_to_number2(letter):
	x = 1
	try:
		return {
	    		'a': 1,
	    		'b': 2,
	    		'c': 3,
	    		'd': 4,
	    		'e': 5,
	    		'f': 6,
	    		'g': 7,
	    		'h': 8
	    		}[letter]
  	except KeyError:
  		pass

def check_field(x, y):
	global checkersList
	l = []
	i = 0
	for item in checkersList:
		if item.x == x and item.y == y:
			l.append(item.name)
			l.append(i)
			return l
		i += 1
	return l
			
def is_odd(num):
        return num & 1 and True or False

def print_checker_list():
	global checkersList
	for item in checkersList:
		print item.name, " [", item.x, "][", item.y, "]" 

def check_winner(color, target):
	global color_robot
	global color_human
	
	l = []
	if color == color_robot: 
		if color == "wolf":
			if target[1] == 1:
				#wolf won
				print "ROBOT WILK WYGRAL!!!!"
				win("robot")
		elif color == "sheep":
			l = where_wolf()
			cnt = check_sheep(l)
			if cnt == 4:
				#sheep won
				print "ROBOT OWCE WYGRAL!!!!"
				win("robot")			
		
	if color == color_human: 
		if color == "wolf":
			if target[1] == 8:
				#wolf won
				print "CZLOWIEK WILK WYGRAL!!!!"
				win("human")
				
		elif color == "sheep":
			l = where_wolf()
			cnt = check_sheep(l)
			if cnt == 4:
				#sheep won
				print "CZLOWIEK OWCE WYGRAL!!!!"
				win("human")

def where_wolf():
	l = 0
	for item in checkersList:
		if item.name == "wolf":
			l = item
			break
	return l

def check_sheep(l):
	x = l.x
	y = l.y
	cnt = 0
	foo = 0
	if (x == 1 and y == 1):
		foo = 1
	elif (x == 1):
		foo = 2
	elif (x == 8):
		foo = 3
	elif (y == 1):
		foo = 4
	for item in checkersList:
		if foo == 1:
			if item.name == "sheep" and item.x == (x + 1) and item.y == (y + 1):
				cnt += 4
		elif foo == 2:
			if item.name == "sheep" and (item.x == (x + 1) and item.y == (y + 1)):
				cnt += 2
			elif item.name == "sheep" and (item.x == (x + 1) and item.y == (y - 1)):
				cnt += 2
		elif foo == 3:
			if item.name == "sheep" and (item.x == (x - 1) and item.y == (y + 1)):
				cnt += 2
			elif item.name == "sheep" and (item.x == (x - 1) and item.y == (y - 1)):
				cnt += 2
		elif foo == 4:
			if item.name == "sheep" and (item.x == (x - 1) and item.y == (y + 1)):
				cnt += 2
			elif item.name == "sheep" and (item.x == (x + 1) and item.y == (y + 1)):
				cnt += 2
		elif foo == 0 and item.name == "sheep" and (item.x == (x + 1) and item.y == (y + 1)):
			cnt += 1
		elif foo == 0 and item.name == "sheep" and (item.x == (x + 1) and item.y == (y - 1)):
			cnt += 1
		elif foo == 0 and item.name == "sheep" and (item.x == (x - 1) and item.y == (y + 1)):
			cnt += 1
		elif foo == 0 and item.name == "sheep" and (item.x == (x - 1) and item.y == (y - 1)):
			cnt += 1
	return cnt

def move_checker(color, i, source, target):
	global checkersList
	global color_robot
	global game
	global position
	
	checkersList.pop(i)
	source1 = number_to_letter(source[0])
	source1 = source1 + str(source[1])
	
	if target[0] == "O" and target[1] == "S":
		print source1, " outside"
		target1 = "os"
		telnet_send(source1, target1)
	else:
		checkersList.append(Checker(color, target[0], target[1]))
		target1 = number_to_letter(target[0])
		target1 = target1 + str(target[1])
		print source1, " ", target1
		position = position + " " + source1 + target1
		print position
		telnet_send(source1, target1)
	if game == "chess":
		if color.isupper():
			color = "light"
		else:
			color = "dark"
	if color == color_robot:
		time.sleep(2)
		play_wav("twojruch.wav")
		#timer = Timer(10.0, time_elapse())
		#timer.start() 
		
	if game == "wolfandsheep":
		check_winner(color, target)
			
	
def check_rules(color, source, target, player):
	
	
	if player  == "human":
		if color == "wolf":
			if (target[0] == (source[0] + 1)) or (target[0] == (source[0] - 1)):
				if  (target[1] == (source[1] + 1)) or (target[1] == (source[1] - 1)):
					print "move!"	
					return True			
				else:
					print "wrong move!"
					play_wav("zlyruchwilkiowce.wav")
					return False
			else:
				print "wrong move!"
				play_wav("zlyruchwilkiowce.wav")
				return False
		if color == "sheep":
			if (target[0] == (source[0] + 1)) or (target[0] == (source[0] - 1)):
				if  target[1] == (source[1] + 1):
					print "move!"	
					return True			
				else:
					print "wrong move!"
					play_wav("zlyruchwilkiowce.wav")
					return False
			else:
				print "wrong move!"
				play_wav("zlyruchwilkiowce.wav")
				return False
				
	elif player  == "robot":
		if color == "wolf":
			if (target[0] == (source[0] + 1)) or (target[0] == (source[0] - 1)):
				if  (target[1] == (source[1] + 1)) or (target[1] == (source[1] - 1)):
					print "move!"	
					return True			
				else:
					print "wrong move!"
					play_wav("zlyruchwilkiowce.wav")
					return False
			else:
				print "wrong move!"
				play_wav("zlyruchwilkiowce.wav")
				return False
		if color == "sheep":
			if (target[0] == (source[0] + 1)) or (target[0] == (source[0] - 1)):
				if  target[1] == (source[1] - 1):
					print "move!"	
					return True			
				else:
					print "wrong move!"
					play_wav("zlyruchwilkiowce.wav")
					return False
			else:
				print "wrong move!"
				play_wav("zlyruchwilkiowce.wav")
				return False

	    
def play_game1_human(in_text):
	#Wolf and sheep (also known as Fox and Hounds)
	global checkersList
	global color_human
	global stage
	
	lines = string.split(in_text, '\n')
	words = string.split(lines[3], ' ')
	source = []
	source.append(words[2])
	words = string.split(lines[4], ' ')
	source.append(words[2])
	words = string.split(lines[6], ' ')
	target = []
	target.append(words[2])
	words = string.split(lines[7], ' ')
	target.append(words[2])
	print source, " to ", target
	source[0] = letter_to_number(source[0])
	target[0] = letter_to_number(target[0])
	source[1] = number_to_number(source[1])
	target[1] = number_to_number(target[1])
	print source, " to ", target
	
	
	checker = []
	checker = check_field(source[0], source[1]);
	source_checker = []
	if checker:
		source_checker.append(checker[0])
		source_checker.append(checker[1])
	else:
		print "source empty!"
		play_wav("polezrodlowe.wav")
		
	checker = check_field(target[0], target[1]);
	target_checker = []
	if not checker:
		if source_checker:
			if source_checker[0] == color_human:
				if (is_odd(target[0]) and is_odd(target[1])) or (not is_odd(target[0]) and not is_odd(target[1])):	
					
					if check_rules(color_human, source, target, "human"):
						
						stage = 6
						move_checker(color_human, source_checker[1], source, target)
						
				else:
					print "wrong move!"
					play_wav("zlyruchwilkiowce.wav")
			else:
				print "wrong checker!"
				if color_human == "sheep":
					play_wav("graszowcaminiemozesz.wav")
				else:
					play_wav("graszwilkiemniemozesz.wav")
	else:
		print "target isn't empty!"
		play_wav("poledocelowe.wav")
		

def play_game1_robot():
	#Wolf and sheep (also known as Fox and Hounds)
	global checkersList
	global color_robot
	if color_human == "wolf":
		color_robot = "sheep"
	elif color_human == "sheep":
		color_robot = "wolf"
	l_enemies = []
	current = []
	l = []
	
	i = 0
	for item in checkersList:
		if item.name == color_robot:
			l.append(i)
		if item.name == color_human:
			l_enemies.append(i)
		i += 1
	print l
	print "___________________"
	print l_enemies
	
	#raw_input("Press Enter")
	
	
	l_max = []
	l_max.append(0)
	last = 0
	i = 0
	
	for item in l:	
		if checkersList[item].y > last:
			del l_max[:]
			l_max.append(checkersList[item])
			
		
		elif checkersList[item].y == l_max[0].y:
			l_max.append(checkersList[item])
				
		last = checkersList[item].y
		print "last: ", last
		i += 1
	i=0
	for item in l_max:
		i += 1
		print item.y, "[", i, "]"
	
	#raw_input("Press Enter")
	#random.shuffle(l_max)
	
	i = 0
	last = l_max[0].x
	current = 0
	for item in l_max:
		for item2 in l_enemies:
			print "1" , abs(checkersList[item2].y - item.y)
			print "2" , abs(checkersList[item2].y - last)
			print "3" , abs(checkersList[item2].x - item.x)
			print "3" , abs(checkersList[item2].x - last)
			if abs(checkersList[item2].x - item.x) >= abs(checkersList[item2].x - last):
				current = item
		i += 1
		last = item.x
		
	if current:
		print "current: ", current
	print "last: ",last
	#raw_input("Press Enter")	
	del l_max[:]
	l_max.append(current)
	while True:
		source = []
		target = []
		if not l_max:
			break
		else:
			source.append(l_max[0].x)
			source.append(l_max[0].y)
			l_max.pop(0)
		print source
		if color_robot == "sheep":
			if source[0] == 1:
				target.append(source[0] + 1)
				target.append(source[1] - 1)
			elif source[0] == 8:
				target.append(source[0] - 1)
				target.append(source[1] - 1)
			else:
				if is_odd(source[1]):
					target.append(source[0] + 1)
					target.append(source[1] - 1)
				else:
					target.append(source[0] - 1)
					target.append(source[1] - 1)
		elif color_robot == "wolf":
			if source[0] == 1:
				target.append(source[0] + 1)
				target.append(source[1] - 1)
				checker = check_field(target[0], target[1]);
				if checker:
					target[1] = source[1] + 1
				
			elif source[0] == 8:
				target.append(source[0] - 1)
				target.append(source[1] - 1)
				checker = check_field(target[0], target[1]);
				if checker:
					target[1] = source[1] + 1
			else:
				target.append(source[0] + 1)
				target.append(source[1] - 1)
				checker = check_field(target[0], target[1]);
				if checker:
					target[0] = source[0] - 1
					target[1] = source[1] - 1
					checker = check_field(target[0], target[1]);
					if checker:
						target[0] = source[0] + 1
						target[1] = source[1] + 1
						checker = check_field(target[0], target[1]);
						if checker:
							target[0] = source[0] - 1
							target[1] = source[1] + 1
							checker = check_field(target[0], target[1]);
							if checker:
								#sheep won!
								print "CZLOWIEK OWCE WYGRAL!!!!"
								win("human")
			
		
		checker = []
		checker = check_field(source[0], source[1]);
		source_checker = []
		if checker:
			source_checker.append(checker[0])
			source_checker.append(checker[1])
		else:
			print "source empty!"
			
		
		checker = check_field(target[0], target[1]);
		target_checker = []
		if not checker:
			if source_checker:
				if source_checker[0] == color_robot:
					if (is_odd(target[0]) and is_odd(target[1])) or (not is_odd(target[0]) and not is_odd(target[1])):	
					
						if check_rules(color_robot, source, target, "robot"):
							move_checker(color_robot, source_checker[1], source, target)
							
							break
					else:
						print "wrong move!"
							
				else:
					print "wrong checker!!"
		else:
			print "target isn't empty!"

def play_game2_human(in_text):
	#Chess
	global checkersList
	global color_human
	global stage
	global game
	
	lines = string.split(in_text, '\n')
	words = string.split(lines[3], ' ')
	source = []
	source.append(words[2])
	words = string.split(lines[4], ' ')
	source.append(words[2])
	words = string.split(lines[6], ' ')
	target = []
	target.append(words[2])
	words = string.split(lines[7], ' ')
	target.append(words[2])
	print source, " to ", target
	source[0] = letter_to_number(source[0])
	target[0] = letter_to_number(target[0])
	source[1] = number_to_number(source[1])
	target[1] = number_to_number(target[1])
	print source, " to ", target
	#raw_input("enter")
	checker = []
	checker = check_field(source[0], source[1]);
	source_checker = []
	if checker:
		source_checker.append(checker[0])
		source_checker.append(checker[1])
	else:
		print "source empty!"
		play_wav("polezrodlowe.wav")
		
	checker = check_field(target[0], target[1]);
	target_checker = []
	if source_checker:
		if checker:
			outside = []
			outside.append('O')
			outside.append('S')
			print "target isn't empty!"
			move_checker(color_human, source_checker[1], target, outside)
		color = source_checker[0]
		if game == "chess":
			if source_checker[0].isupper():
				color = "light"
			else:
				color = "dark"
			
		if color == color_human:		
			stage = 6
			move_checker(source_checker[0], source_checker[1], source, target)
					
		else:
			print "wrong checker!"
			if color_human == "sheep":
				play_wav("graszowcaminiemozesz.wav")
			elif color_human == "wolf":
				play_wav("graszwilkiemniemozesz.wav")
			elif color_human == "light":
				play_wav("graszowcaminiemozesz.wav")
			elif color_human == "dark":
				play_wav("graszwilkiemniemozesz.wav")
	
		#play_wav("poledocelowe.wav")

def play_game2_robot():
	#Chess
	global color_robot
	global color_human
	
	if color_human == "light":
		color_robot = "dark"
	elif color_human == "dark":
		color_robot = "light"
	
	try: 
		child = pexpect.spawn ('stockfish')
		print child.before
		child.sendline (position)
		child.sendline ('go depth 5')  
		child.expect("ponder")
		out_text = child.before
		print out_text
	except pexpect.EOF:
		child.close
	linearray = out_text.split("\n")
	bestmove = ""
    	for line in linearray:
        	if line.find('bestmove') != -1:
            		bestmove = line
        print bestmove
	
	
	linearray = bestmove.split(" ")
	print linearray[1]
	foo = linearray[1]
	foo1 = letter_to_number2(foo[0])
	foo2 = int(foo[1])
	foo3 = letter_to_number2(foo[2])
	foo4 = int(foo[3])
	print foo1, foo2, " to ", foo3, foo4
	#raw_input("Press Enter")
	source = []
	target = []
	source.append(foo1)
	source.append(foo2)
	target.append(foo3)
	target.append(foo4)
	print source, " to ", target
	#raw_input("Press Enter")
	checker = []
	checker = check_field(source[0], source[1]);
	source_checker = []
	if checker:
		source_checker.append(checker[0])
		source_checker.append(checker[1])
	else:
		print "source empty!"
		play_wav("polezrodlowe.wav")
		
	checker = check_field(target[0], target[1]);
	target_checker = []
	if source_checker:
		if checker:
			print "target isn't empty!"
			move_checker(color_human, source_checker[1], target, "OS")
		color = source_checker[0]
		if game == "chess":
			if source_checker[0].isupper():
				color = "light"
			else:
				color = "dark"
			
		if color == color_robot:		
			stage = 6
			move_checker(source_checker[0], source_checker[1], source, target)
		
			#raw_input("Press Enter")		
		else:
			print "wrong checker!"
			if color_robot == "light":
				play_wav("graszjasnymi.wav")
			elif color_robot == "dark":
				play_wav("graszciemnymi.wav")
		print source_checker[0]
		print color_robot
		print color
		#play_wav("poledocelowe.wav")
				
def fun():
	global index
	global timer_fun
	
	
	#l = []
	#l.append("sneeze")
	#l.append("whistle")
	#l.append("snore")
	#play_wav(l[index] + ".wav")
	index += 4
	#if index > 2:
	#	index = 0
	play_wav("sneeze.wav")
	play_wav('przepraszam.wav')
	try:
		timer_fun.cancel()
		timer_fun = Timer(index, fun)
		timer_fun.start()
	except KeyboardInterrupt:
		print "FUN EXCEPTION: Ctr + c"


def time_elapse():
	global timer_elapsed
	
	play_wav("pospieszsie.wav")
	
def timer_1():
	global timer_elapsed
	global timer_on
	global timer_end
	
	
	if timer_on == True:
		timer_on = False
		print "timer false!!!!!!"
		#raw_input("Press Enter")
		try:
			
			#timer_elapsed.cancel()
			#timer_end.cancel()
			pass
		except KeyboardInterrupt:
			print "FUN EXCEPTION: Ctr + c"
			
	elif timer_on == False:
		timer_on = True
		print "timer true!!!!!!"
		
		#raw_input("Press Enter")
		try:
			#timer_elapsed = Timer(20, time_elapse)
			#timer_elapsed.start()
			#timer_2()
			pass
		except KeyboardInterrupt:
			print "FUN EXCEPTION: Ctr + c"
		#timer_elapsed.cancel()
	#raw_input("Press Enter")		
def timer_2():
	global timer_end
	try:
		timer_end = Timer(30, time_elapsed)
		timer_end.start()
	except KeyboardInterrupt:
		print "FUN EXCEPTION: Ctr + c"
		
def time_elapsed():
	play_wav("widzezeomniezapomniales.wav")
	play_wav("niegramztobajuzdluzej.wav")	
			
def process_text(in_text):
	global timer
	global stage
	global pause
	global begin
	global color_human
	global timer_fun
	global game
	
	play_wav("recognize.wav")
	
	match_se = re.search("ZATRZYMAJ", in_text)
	if match_se and begin == 1 and pause == 0:
		timer_1()
		pause = 1
		print "ZATRZYMANO"
		play_wav("pause.wav")
		try:
			timer_fun = Timer(10.0, fun)
			timer_fun.start()
		except KeyboardInterrupt:
			print "PROCESS_TEXT EXCEPTION: Ctr + c"
		
		return True
		
	match_se = re.search(" START ", in_text)
	if match_se:
		if pause != 1:
			if begin == 0:
				stage = 1
				print "START"
				
		else:
			pause = 0
			play_wav("pause.wav")
			timer_fun.cancel()
		return True
	
	match_se = re.search("KONIEC", in_text)
    	if match_se:
    		timer_1()
    		print "KONIEC"
		if begin == 1:
			begin = 0
		play_wav("tobyldopieropoczatek.wav")
		play_wav("end.wav")
		shutdown()
		return True
				
	match_se = re.search("RESET", in_text)
	if match_se:
		stage = 0
		begin = 0
		play_wav("switch.wav")
		print "RESET"
		return True
	
	if pause == 0:
		
		match_se = re.search("WITAJ", in_text)
		match_se2 = re.search("JESTEM", in_text)
	    	if match_se and match_se2:
	    		match_se = re.search("PIOTR", in_text)
			stage = 2
			print "WITAJ"
			if match_se:
				play_wav("witaj.wav")
			else:
				play_wav("witajnieznajomy.wav")
			return True
			
		match_se = re.search("ZAGRAJMY", in_text)
		match_se2 = re.search("WWILKIOWCE", in_text)
		match_se3 = re.search("WSZACHY", in_text)
		if match_se and match_se2:
			stage = 3
			game = "wolfandsheep"
			print "ZAGRAJMY"
			play_wav("kimgrasz.wav")
			return True
		elif match_se and match_se3:
			stage = 3
			game = "chess"
			print "ZAGRAJMY"
			play_wav("jakikolor.wav")
			#play_wav("przykrominieumiemgracwszachy.wav")
			return True
		match_se = False
		if game == "wolfandsheep":
			match_se = re.search("WILKIEM", in_text)
			match_se2 = re.search("OWCAMI", in_text)
		elif game == "chess":
			match_se = re.search("JASNY", in_text)
			match_se2 = re.search("CIEMNY", in_text)
		#print match_se, match_se2
		#raw_input("Press Enter")
		if game == "wolfandsheep":
			if match_se:
				color_human = "wolf"
			if match_se2:
				color_human = "sheep"
		elif game == "chess":
			if match_se:
				color_human = "light"
			if match_se2:
				color_human = "dark"
		#print match_se, match_se2
		#print game
		#raw_input("Press Enter")
		if match_se or match_se2:
			set_board(color_human)
			print_checker_list()
			print "WYBOR KOLORU"
			if game == "wolfandsheep":
				stage = 4
				play_wav("ktorozpoczyna.wav")
			else:
				stage = 5
				play_wav("jasnezaczynaja.wav")
				begin = 1
				play_wav("start.wav")
				if color_human == "light":
					print "JAROZPOCZYNAM"
				elif color_human == "dark":
					print "ROZPOCZNIJ"
					play_game2_robot()
					print_checker_list()
			return True
			
		match_se = re.search("ROZPOCZNIJ", in_text)
	    	if match_se:
	    		
			stage = 5
			begin = 1
			print "ROZPOCZNIJ"
			play_wav("start.wav")
			if game == "wolfandsheep":
				play_game1_robot()
			elif game == "chess":
				play_game2_robot()
			print_checker_list()
			return True
				
	    	match_se = re.search("JAROZPOCZYNAM", in_text)
	    	if match_se:
			
			stage = 5
			begin = 1
			print "JAROZPOCZYNAM"
			play_wav("start.wav")
			print_checker_list()
			return True
		
		match_se = re.search(" NA ", in_text)
	    	if match_se and begin == 1:
			#stage = 6
			#begin = 1
			print "NA"
			#timer.cancel()
			if game == "wolfandsheep":
				play_game1_human(in_text)
			elif game == "chess":
				play_game2_human(in_text)
			
			print_checker_list()
			return True
			
		match_se = re.search("TWOJRUCH", in_text)
	    	if match_se:
			stage = 5
			#begin = 1
			print "TWOJRUCH"
			if game == "wolfandsheep":
				play_game1_robot()
			elif game == "chess":
				play_game2_robot()
			print_checker_list()
			return True
			
			
		match_se = re.search("COFNIJ", in_text)
	    	if match_se:
			#back = 1
			#stage = 5
			print "COFNIJ"
			play_wav("przykromi.wav")
			return True
	
	return False

	
def win(winner):
	global begin
	global stage
	
	if winner == "robot":
		play_wav("fail.wav")
		play_wav("wygralem.wav")
		play_wav("dziekuje.wav")
	elif winner == "human":
		play_wav("win.wav")
		play_wav("wygrales.wav")
		play_wav("dziekuje.wav")
		
	stage = 2
	begin = 0
	
def shutdown():
	global tn
	
	try: 	
		play_wav("end.wav")
		child = pexpect.spawn ('sudo shutdown -h now')
		child.expect("system")
	except pexpect.EOF:
		child.close
	sys.exit()
	#tn.close()
	

if __name__ == "__main__":
	
	#timer = Timer(10.0, time_elapse)
	#timer.start() 
	telnet_connect()
	recognize = False
	timer_1()
	try:
		#timer_elapsed.cancel()
		#timer_elapsed = Timer(4, time_elapse)
		#timer_elapsed.start()
		pass
	except KeyboardInterrupt:
		print "FUN EXCEPTION: Ctr + c"
		
	
	play_wav("bootup2.wav")
	print_checker_list()
	while True:	
		try:
			
			if stage == 1:
				min_length = '0.1'
				path = '/home/pi/HTK-ASR-WILKiOWCE-ICAO/HTK-ASR-WILKiOWCE-witaj/'
				p1 = subprocess.Popen (['rec', '-c', '1', '-p'], stdout=subprocess.PIPE)
				p2 = subprocess.Popen (['sh', 'sox.sh', path, min_length], stdin=p1.stdout)
				p2.wait()
				p1.kill()
				in_text = subprocess.check_output (['sh', 'recognize_live.sh', path])
			elif stage == 2:
				min_length = '0.1'
				path = '/home/pi/HTK-ASR-WILKiOWCE-ICAO/HTK-ASR-WILKiOWCE-zagrajmy/'
				p1 = subprocess.Popen (['rec', '-c', '1', '-p'], stdout=subprocess.PIPE)
				p2 = subprocess.Popen (['sh', 'sox.sh', path, min_length], stdin=p1.stdout)
				p2.wait()
				p1.kill()
				in_text = subprocess.check_output (['sh', 'recognize_live.sh', path])
			elif stage == 3:
				min_length = '0.1'
				path = '/home/pi/HTK-ASR-WILKiOWCE-ICAO/HTK-ASR-WILKiOWCE-kolor/'
				p1 = subprocess.Popen (['rec', '-c', '1', '-p'], stdout=subprocess.PIPE)
				p2 = subprocess.Popen (['sh', 'sox.sh', path, min_length], stdin=p1.stdout)
				p2.wait()
				p1.kill()
				in_text = subprocess.check_output (['sh', 'recognize_live.sh', path])
			elif stage == 4:
				min_length = '0.1'
				path = '/home/pi/HTK-ASR-WILKiOWCE-ICAO/HTK-ASR-WILKiOWCE-rozpocznij/'
				p1 = subprocess.Popen (['rec', '-c', '1', '-p'], stdout=subprocess.PIPE)
				p2 = subprocess.Popen (['sh', 'sox.sh', path, min_length], stdin=p1.stdout)
				p2.wait()
				p1.kill()
				in_text = subprocess.check_output (['sh', 'recognize_live.sh', path])
			elif stage == 5:
				min_length = '0.1'
				path = '/home/pi/HTK-ASR-WILKiOWCE-ICAO/'
				p1 = subprocess.Popen (['rec', '-c', '1', '-p'], stdout=subprocess.PIPE)
				p2 = subprocess.Popen (['sh', 'sox.sh', path, min_length], stdin=p1.stdout)
				p2.wait()
				p1.kill()
				in_text = subprocess.check_output (['sh', 'recognize_live.sh', path])
			elif stage == 6:
				min_length = '0.1'
				path = '/home/pi/HTK-ASR-WILKiOWCE-ICAO/HTK-ASR-WILKiOWCE-cofnij/'
				p1 = subprocess.Popen (['rec', '-c', '1', '-p'], stdout=subprocess.PIPE)
				p2 = subprocess.Popen (['sh', 'sox.sh', path, min_length], stdin=p1.stdout)
				p2.wait()
				p1.kill()
				in_text = subprocess.check_output (['sh', 'recognize_live.sh', path])
			else:
				min_length = '0.1'
				path = '/home/pi/HTK-ASR-WILKiOWCE-ICAO/'
				p1 = subprocess.Popen (['rec', '-c', '1', '-p'], stdout=subprocess.PIPE)
				p2 = subprocess.Popen (['sh', 'sox.sh', path, min_length], stdin=p1.stdout)
				p2.wait()
				p1.kill()
				in_text = subprocess.check_output (['sh', 'recognize_live.sh', path])
 				
 				
				print "else"
			#timer_1()
			timer_1()
			while True:
				try:
					
					#soxi -D /home/pi/HTK-ASR-WILKiOWCE-ICAO/test/test.wav
					#p = subprocess.Popen (['soxi', '-D', '/home/pi/HTK-ASR-WILKiOWCE-ICAO/test/test.wav'])
					#p.wait()
					#p.kill()
					text = subprocess.check_output (['soxi', '-D', '/home/pi/HTK-ASR-WILKiOWCE-ICAO/test/test.wav'])
					#print text
					#match_se = re.search("\n", text)
	    				#if match_se:
	    					#print "znalazlem"
	    				l = text.split('\n')
	    				print l[0]
	    				#l = l[0].split('.')
	    				length = float(l[0])
	    				print length
					#raw_input("Press Enter")
					print in_text
					
					if length > 2.1:
						recognize = process_text(in_text)
						print "-------- PROCESS ----------- (stage ", stage, ")"
					
					#if recognize:
						#timer_1()
						#timer_1()
					#raw_input("Press Enter")
					break
	    				
				

				except KeyboardInterrupt:
					print "EXCEPTION: Ctr + c"
					break
					break
				
		except KeyboardInterrupt:
			print "MAIN EXCEPTION: Ctr + c"
			break
		
