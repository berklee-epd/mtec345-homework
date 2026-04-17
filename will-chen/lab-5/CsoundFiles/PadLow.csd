<CsoundSynthesizer>
<CsInstruments>
sr      =       96000
kr      =       96000
ksmps   =       1
nchnls  =       2

          instr 1
          
itranspose init     0                        
imaxfreq  =         1000                     
imaxsweep =         10000                    
imaxamp   =         20000                    
ireson    =         1                       

ibpm      =         p14                      
inotedur  =         15/ibpm
icount    init      0                        
icount2   init      0                        
ipcount2  init      0
idecaydur =         inotedur
imindecay =         (idecaydur<.2 ? .2 : idecaydur) 
ipitch    table     0,4                     
ipitch    =         cpspch(itranspose + 6 + ipitch/100)
kaccurve  init      0

kfco      line      p4, p3, p5
kres      line      p6, p3, p7
kenvmod   line      p8, p3, p9
kdecay    line      p10, p3, p11
kaccent   line      p12, p3, p13

start:
ippitch   =         ipitch
ipitch    table     ftlen(4)*frac(icount/ftlen(4)),4
ipitch    =         cpspch(itranspose + 6 + ipitch/100)

          if        ipcount2 != icount2 goto noslide
kpitch    linseg    ippitch, .06, ipitch, inotedur-.06, ipitch
          goto      next

noslide:
kpitch    =         ipitch

next:
ipcount2  =         icount2
          timout    0,inotedur,contin
icount    =         icount + 1
          reinit    start
rireturn

contin:
iacc      table     ftlen(5)*frac((icount-1)/ftlen(5)), 5
          if        iacc == 0 goto noaccent
ienvdecay =         0               
iremacc   =         i(kaccurve)
kaccurve  oscil1i   0, 1, .4, 3
kaccurve  =         kaccurve+iremacc         

          goto      sequencer

noaccent:
kaccurve  =         0                       
ienvdecay =         i(kdecay)

sequencer:
aremovedc init      0                       
imult     table     ftlen(6)*frac(icount2/ftlen(6)),6
          if        imult != 0 goto noproblemo 
icount2   =         icount2 + 1
          goto      sequencer

noproblemo:
ieventdur =         inotedur*imult

kmeg      expseg    1, imindecay+((ieventdur-imindecay)*ienvdecay),ienvdecay+.000001
kveg      linen     1, .01, ieventdur, .016 

kamp      =         kveg*((1-i(kenvmod)) + kmeg*i(kenvmod)*(.5+.5*iacc*kaccent))

ksweep    =         kveg * (imaxfreq + (.75*kmeg+.25*kaccurve*kaccent)*kenvmod*(imaxsweep-imaxfreq))
kfco      =         20 + kfco * ksweep    
kfco      =         (kfco > sr/2 ? sr/2 : kfco) 
                                             
          timout    0, ieventdur, out
icount2   =         icount2 + 1
          reinit    contin

out:
abuzz     buzz      kamp, kpitch, sr/(2*kpitch), 1 ,0 
asaw      integ     abuzz,0
asawdc    atone     asaw,1

ainpt     =         asawdc - aremovedc*kres*ireson
alpf      tone      ainpt,kfco
alpf      tone      alpf,kfco
alpf      tone      alpf,kfco
alpf      tone      alpf,kfco

aout      balance   alpf,asawdc

aremovedc atone     aout,10
          outall       imaxamp*aremovedc
          endin

</CsInstruments>
<CsScore>
f 1 0 8192 10 1 
f 3  0 8193   8  0 512 1 1024 1 512 .5 2048 .2 4096  0 
f 4  0  16  -2  12 24 12 14 15 12 0 12 12 24 12 14 15 6 13 16 
f 5  0  32  -2   0  1  0  0  0  0 0  0  0  1  0  1  1 1  0  0 0 1 0 0 1 0 1 1 1 1 0 0 0 0 0 1 
f 6  0  16  -2   2     1  1  2    1  1  1  2     1  1 3       1 4 0 0 0 
f 7 0 1024   8 -.8 42 -.78  200 -.74 200 -.7 140 .7  200 .74 200 .78 42 .8 

i 1   0 10    .1     .3 .2  .2   .1   .4    .05 .8    0   0      120 
i 1  11 10    .95    1  .1  1    .8   1     .1  .01   0   1      120 
i 1  22 10    0      1  .5  1    .1   .4   1    1     1   1      120 
i 1  33 10   .5      1  .95 1     1   .9   .1   0     1   1      120 
i 1  44 10   .05     1  .5  1    .1   .1   .5   1     .5  1      120 
 </CsScore>
</CsoundSynthesizer>






<bsbPanel>
 <label>Widgets</label>
 <objectName/>
 <x>0</x>
 <y>0</y>
 <width>0</width>
 <height>0</height>
 <visible>true</visible>
 <uuid/>
 <bgcolor mode="nobackground">
  <r>255</r>
  <g>255</g>
  <b>255</b>
 </bgcolor>
</bsbPanel>
<bsbPresets>
</bsbPresets>
