sox $1test/test1.wav $1test/test2.wav reverse trim 0 0.5 reverse

sox $1test/test2.wav $1test/test1.wav $1test/test.wav

HVite -C $1config3  -H $1hmm15/macros -H $1hmm15/hmmdefs -S $1testQT.scp -l '*' -i $1recoutQT.mlf -w $1wdnet -p 0.0 -s 5.0 $1dict $1tiedlist 

cat $1recoutQT.mlf


