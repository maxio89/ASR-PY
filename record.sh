rec -c 1 -p | sox -p -b 16 -r 16000 -t wavpcm /home/pi/HTK-ASR-WILKiOWCE-ICAO/test/test1.wav silence -l 1 0.1 0.5% 1 1.2 0.5%

sox /home/pi/HTK-ASR-WILKiOWCE-ICAO/test/test1.wav /home/pi/HTK-ASR-WILKiOWCE-ICAO/test/test2.wav reverse trim 0 0.5 reverse

sox /home/pi/HTK-ASR-WILKiOWCE-ICAO/test/test2.wav /home/pi/HTK-ASR-WILKiOWCE-ICAO/test/test1.wav /home/pi/HTK-ASR-WILKiOWCE-ICAO/test/test.wav
