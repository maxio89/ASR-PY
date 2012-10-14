#!/usr/bin/python
# Voice control of industrial robot Kawasaki via Raspberry Pi
# author: Piotr Kozlowski
# created: September 2012


import pexpect
import time
import re
from time import sleep

#global
stage = 0
begin = 0
pause = 0


def get_confidence(out_text):
    linearray = out_text.split("\n")
    for line in linearray:
        if line.find('sentence1') != -1:
            sentence1 = line
        elif line.find('cmscore1') != -1:
            cmscore1 = line
        elif line.find('score1') != -1:
            score1 = line
    cmscore_array = cmscore1.split()
    err_flag = False
    for score in cmscore_array:
        try:
            ns = float(score)
        except ValueError:
            continue
        if (ns < 0.999):
            err_flag = True
            print "Confidence error:", ns, ":", sentence1
    score1_val = float(score1.split()[1])      
    if score1_val < -13000:
        err_flag = True
        print "Score1 error:", score1_val, sentence1
    if (not err_flag):
        print "Recognized:"
        print sentence1
        print score1
        print cmscore1
        #pass sentence1 to controller functions
        process_sentence(sentence1)
    else:
    	print "Recognized with errors:"
    	process_sentence(sentence1)
        #pass

def play_wav(name):
	try: 
		child = pexpect.spawn ('aplay wav/' + name)
		child.expect("play")
	except pexpect.EOF:
	      	pass
	child.close
	
def process_sentence(sentence1):
	global stage
	global pause
	global begin
	
	print "-------- PROCESS -----------"
	
	match_se = re.search("ZATRZYMAJ", sentence1)
	if match_se:
		pause = 1
		print "ZATRZYMANO"
		play_wav("pause.wav")
		
	match_se = re.search("START", sentence1)
	if match_se:
		if pause != 1:
			if begin == 0:
				stage = 1
				print "process stage 1 - ", stage
				play_wav("start.wav")
		else:
			pause = 0
			play_wav("pause.wav")
	
	if pause == 0:
		
		match_se = re.search("WITAJ JESTEM", sentence1)
	    	if match_se:
			stage = 2
			print "process stage ", stage
			play_wav("witaj.wav")
			
		match_se = re.search("ZAGRAJMY", sentence1)
		if match_se:
			stage = 3
			print "process stage ", stage
			
		match_se = re.search("ROZPOCZNIJ", sentence1)
	    	if match_se:
			stage = 4
			begin = 1
			
	    	match_se = re.search("JAROZPOCZYNAM", sentence1)
	    	if match_se:
			stage = 4
			begin = 1
		
		match_se = re.search(" NA ", sentence1)
	    	if match_se:
			stage = 5
			begin = 1
			
		match_se = re.search("TWOJRUCH", sentence1)
	    	if match_se:
			stage = 4
			begin = 1
			
		match_se = re.search("COFNIJ", sentence1)
	    	if match_se:
			back = 1
			stage = 4
			print "COFNIJ"
			play_wav("przykromi.wav")
			
		match_se = re.search("KONIEC", sentence1)
	    	if match_se:
	    		print "KONIEC"
			if begin == 1:
				begin = 0
				play_wav("tobyldopieropoczatek.wav")
				play_wav("end.wav")
		
		
	

if __name__ == "__main__":

	
	while True:	
		try:
			if stage == 1:
				child = pexpect.spawn ('julius -input mic -C ../HTK-ASR-WILKiOWCE-ICAO/HTK-ASR-WILKiOWCE-witaj/julius/julius.jconf')
			elif stage == 2:
				child = pexpect.spawn ('julius -input mic -C ../HTK-ASR-WILKiOWCE-ICAO/HTK-ASR-WILKiOWCE-zagrajmy/julius/julius.jconf')
			elif stage == 3:
				child = pexpect.spawn ('julius -input mic -C ../HTK-ASR-WILKiOWCE-ICAO/HTK-ASR-WILKiOWCE-rozpocznij/julius/julius.jconf')
			elif stage == 5:
				child = pexpect.spawn ('julius -input mic -C ../HTK-ASR-WILKiOWCE-ICAO/HTK-ASR-WILKiOWCE-cofnij/julius/julius.jconf')
			else:
				child = pexpect.spawn ('julius -input mic -C ../HTK-ASR-WILKiOWCE-ICAO/julius/julius.jconf')
				print "else"
		except:
			print "error"
			
		while True:
			try:
				child.expect('please speak', timeout=30)
				print "Please speak - stage ", stage
				in_text = child.before
				match_res = re.match(r'(.*)sentence1(\.*)', in_text, re.S)
				if match_res:
        				get_confidence(in_text)
        				print "Break!"
        				child.close(force=True)
        				break
    				else:
					print "I didn't recognize!"
				
				
			except pexpect.TIMEOUT:
				child.close(force=True)
				print "EXCEPTION: Timeout!"
			except KeyboardInterrupt:
				child.close(force=True)
				print "EXCEPTION: Ctr + c"
		
