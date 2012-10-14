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

#global
stage = 0
begin = 0
pause = 0
in_text = "sad"
checkersList = []
s = pxssh.pxssh()
color_human = "blabla"
color_robot = "blabla"

class Checker(object):
    #def addChecker(name, x, y):
    def __init__(self, name=None, x=None, y=None):
    	self.name = name
        self.x = x
        self.y = y


checkersList.append(Checker("sheep", 1, 1))
checkersList.append(Checker("wolf", 3, 5))
checkersList.append(Checker("sheep", 3, 1))
checkersList.append(Checker("sheep", 5, 1))
checkersList.append(Checker("sheep", 7, 1))

def play_wav(name):
	try: 
		child = pexpect.spawn ('aplay wav/' + name)
		child.expect("play")
	except pexpect.EOF:
	      	pass
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
  
def move_checker(color, i, source, target):
	global checkersList

	checkersList.pop(i)
	checkersList.append(Checker(color, target[0], target[1]))
	source1 = number_to_letter(source[0])
	target1 = number_to_letter(target[0])
	source1 = source1 + str(source[1])
	target1 = target1 + str(target[1])
	print source1, " ", target1
	#ssh_send(source1, target1)
	

def ssh_send(source, target):
	global s
	
	#if ssh_connect():
		#print "connected via ssh"
	#else:
		#print "ssh error!"
	
	s.sendline("ls -l")
	s.prompt()
	print s.before
	s.sendline("touch sshfile")
	s.prompt()
	s.sendline("touch sshfile2")
	s.prompt()
	
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
	
	time.sleep(1)
	
def ssh_connect():
	global s
	
	try:
		s.login("192.168.1.10", "piotrek", "hasl0")
		return True
	except pxssh.ExceptionPxssh, e:
        	print "pxssh failed on login"
        	print str(e)
		return False
	
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
						
						move_checker(color_human, source_checker[1], source, target)
						stage = 6
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
	else:
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
	
	raw_input("Press Enter")
	
	
	l_max = []
	last = 0
	i = 0
	for item in l:	
		if checkersList[item].y >= last:
			l_max.append(checkersList[i])
			
		last = checkersList[i].y
		i += 1
	
	print l_max[0].y, len(l_max)
	
	raw_input("Press Enter")
	#random.shuffle(l_max)
	
	i = 0
	last = 0
	current = 0
	for item in l_max:
		for item2 in l_enemies:
			if abs(checkersList[item2].y - item.y) > abs(checkersList[item2].y - last):
				current = item
		i += 1
		last = item.y
		
	#print current.y
	raw_input("Press Enter")	
	
	while True:
		source = []
		target = []
		if not l_max:
			break
		else:
			source.append(l_max[0].x)
			source.append(l_max[0].y)
			l_max.pop(0)
		
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
								pass
		
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
					print "wrong checker!"
		else:
			print "target isn't empty!"
				
	
def process_text(in_text):
	global stage
	global pause
	global begin
	global color_human
	
	play_wav("recognize.wav")
	print "-------- PROCESS ----------- (stage ", stage, ")"
	
	match_se = re.search("ZATRZYMAJ", in_text)
	if match_se and begin == 1 and pause == 0:
		pause = 1
		print "ZATRZYMANO"
		play_wav("pause.wav")
		
	match_se = re.search(" START ", in_text)
	if match_se:
		if pause != 1:
			if begin == 0:
				stage = 1
				print "START"
				
		else:
			pause = 0
			play_wav("pause.wav")
	
	if pause == 0:
		
		match_se = re.search("WITAJ", in_text)
		match_se = re.search("JESTEM", in_text)
	    	if match_se:
			stage = 2
			print "WITAJ"
			play_wav("witaj.wav")
			
		match_se = re.search("ZAGRAJMY", in_text)
		if match_se:
			stage = 3
			print "ZAGRAJMY"
			play_wav("kimgrasz.wav")
		
		match_se = re.search("WILKIEM", in_text)
		match_se2 = re.search("OWCAMI", in_text)
		
		if match_se:
			color_human = "wolf"
		if match_se2:
			color_human = "sheep"
		if match_se or match_se2:
			stage = 4
			print "WYBOR KOLORU"
			play_wav("ktorozpoczyna.wav")
			
		match_se = re.search("ROZPOCZNIJ", in_text)
	    	if match_se:
			stage = 5
			begin = 1
			print "ROZPOCZNIJ"
			play_wav("start.wav")
			
	    	match_se = re.search("JAROZPOCZYNAM", in_text)
	    	if match_se:
			stage = 5
			begin = 1
			print "JAROZPOCZYNAM"
			play_wav("start.wav")
		
		match_se = re.search(" NA ", in_text)
	    	if match_se and begin == 1:
			#stage = 6
			#begin = 1
			print "NA"
			play_game1_human(in_text)
			print_checker_list()
			
		match_se = re.search("TWOJRUCH", in_text)
	    	if match_se:
			stage = 5
			#begin = 1
			print "TWOJRUCH"
			play_game1_robot()
			print_checker_list()
			
			
		match_se = re.search("COFNIJ", in_text)
	    	if match_se:
			back = 1
			stage = 5
			print "COFNIJ"
			play_wav("przykromi.wav")
			
		match_se = re.search("KONIEC", in_text)
	    	if match_se:
	    		print "KONIEC"
			#if begin == 1:
				#begin = 0
				#play_wav("tobyldopieropoczatek.wav")
				#play_wav("end.wav")
		
		
def shutdown():
	global s
	s.logout()

if __name__ == "__main__":
	
	#ssh_connect()
	play_wav("bootup2.wav")
	print_checker_list()
	stage = 5
	while True:	
		try:
			
			#soxi -D aa.wav
			begin = 1
			color_human = "sheep"
			if stage == 5:
				min_length = '0.2'
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
			
			while True:
				try:
					print in_text
					process_text(in_text)
					raw_input("Press Enter")
					break
	    				
				

				except KeyboardInterrupt:
					print "EXCEPTION: Ctr + c"
					break
					break
				
		except KeyboardInterrupt:
			print "MAIN EXCEPTION: Ctr + c"
			break
		
