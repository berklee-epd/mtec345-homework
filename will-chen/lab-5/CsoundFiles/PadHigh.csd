<CsoundSynthesizer>
<CsOptions>
</CsOptions>
<CsInstruments>
sr      =       96000
kr      =       96000
ksmps   =       1
nchnls  =       2

instr 1 

imaxfreq       =         5000                                    
imaxsweep      =         sr/2                                   
iratio         =         20                                     

itranspose     =         p15                                    
iseqfn         =         p16
iaccfn         =         p17
idurfn         =         p18
imaxamp        =         p19                                     
ibpm           =         p14                                    
inotedur       =         15/ibpm   
icount         init      0                                       
icount2        init      0                                     
ipcount2       init      0
idecaydur      =         inotedur
imindecay      =         (idecaydur<.2 ? .2 : idecaydur)         
ipitch         table     0,iseqfn                                
ipitch         =         cpspch(itranspose + 6 + ipitch/100)
kaccurve       init      0

kfco           line      p4, p3, p5
kres           line      p6, p3, p7
kenvmod        line      p8, p3, p9
kdecay         line      p10, p3, p11
kaccent        line      p12, p3, p13

start:
ippitch        =         ipitch
ipitch         table     ftlen(iseqfn)*frac(icount/ftlen(iseqfn)),iseqfn
ipitch         =         cpspch(itranspose + 6 + ipitch/100)

if ipcount2 !=         icount2 goto noslide
kpitch         linseg    ippitch, .06, ipitch, inotedur-.06, ipitch
goto next

noslide:
     kpitch    =         ipitch

next:
ipcount2       =         icount2
               timout    0,inotedur,contin
icount         =         icount + 1
               reinit    start
rireturn

contin:
iacc           table     ftlen(iaccfn)*frac((icount-1)/ftlen(iaccfn)), iaccfn
if iacc        ==        0 goto noaccent

ienvdecay      =         0                                                 
iremacc        =         i(kaccurve)
kaccurve       oscil1i   0, 1, .4, 3
kaccurve       =         kaccurve+iremacc                                  

goto sequencer

noaccent:
kaccurve       =         0                                                 
ienvdecay      =         i(kdecay)

sequencer:
aremovedc      init      0                                                 
imult          table     ftlen(idurfn)*frac(icount2/ftlen(idurfn)),idurfn
if imult       !=        0 goto noproblemo                                 

icount2        =         icount2 + 1
goto sequencer

noproblemo:
ieventdur      =         inotedur*imult

kmeg           expseg    1, imindecay+(3.4*ienvdecay), ienvdecay+.000001   
kmeg           expseg    1, imindecay+((ieventdur-imindecay)*ienvdecay), ienvdecay+.000001
kveg           linen     1, .004, ieventdur, .016

kamp           =         kveg*((1-i(kenvmod)) + kmeg*i(kenvmod)*(.5+.5*iacc*kaccent))

kfco           =         50 + imaxfreq*kfco*(1-kenvmod)+imaxsweep*kenvmod*(.7*kmeg +.3*kaccurve*kaccent)

kfco           =         (kfco > sr/2 ? sr/2 : kfco)                       

               timout    0, ieventdur, out
icount2        =         icount2 + 1
               reinit    contin

out:
abuzz          buzz      kamp, kpitch, sr/(4*kpitch), 1 ,0                
asawdc         filter2   abuzz, 1, 1, 1, -.99                              
asaw           =         asawdc                                            

ax             =         asaw
ay1            init      0
ay2            init      0
ay3            init      0
ay4            init      0

kfcon          =         kfco/(sr/2)                                       
kp             tablei    kfcon, 21, 1                                      
kscale         tablei    (kp+1)/2, 20, 1                                  
kk             =         kres*kscale

ax             =         ax - kk*ay4

ax1            delay1    ax
ay1            =         ax * (kp+1)/2 + ax1 * (kp+1)/2 - kp*ay1
ay11           delay1    ay1
ay2            =         ay1 * (kp+1)/2 + ay11 * (kp+1)/2 - kp*ay2
ay21           delay1    ay2
ay3            =         ay2 * (kp+1)/2 + ay21 * (kp+1)/2 - kp*ay3
ay31           delay1    ay3
ay4            =         ay3 * (kp+1)/2 + ay31 * (kp+1)/2 - kp*ay4
                         
ay4            =         tanh(ay4)     
                                   
ay5            =         (tanh(kres*ay4*iratio))/(tanh(kres*iratio))

               outall       imaxamp*kamp*ay5
               endin

</CsInstruments>
<CsScore>
f1 0 8192 10 1                                                                    \
f3  0 8193   8  0 512 1 1024 1 512 .5 2048 .2 4096  0                

f4  0  16  -2  12 24 12 14 15 12 0 12 12 24 12 14 15 6 13 16               
f5  0  32  -2   0  1  0  0  0  0 0  0  0  1  0  1  1 1  0  0 0 1 0 0 1 0 1 1 1 1 0 0 0 0 0 1
f6  0  16  -2   2     1  1  2    1  1  1  2     1  1 3       1 4 0 0 0     

f7  0  8  -2   10 0 12 0 7 10 12 7                                              
f8  0  16  -2   1 0  0 0 0  0  0 0 0 0 0 0 0 0 0 0                              
f9  0  2  -2   16 0                                                                  

f10  0  8  -2   0 12 0 0 12 0 0 12                                              
f11  0  8  -2   1  1 1 1  1 1 1  1                                              
f12  0  8  -2   1  1 1 1  1 1 1  1                                             

f20 0 8193 -25 0 4 8192 1

f21 0 8193 -27 0 -1 2048 -.22 4096 .4 6144 .83 7168 .92 8192 1

i1   0 20        .1     .3        .2  .2        .01  .1         .02 .1      0   0      120     2         7        8       9         7000
i1   0 20  0      .6        .5  .7        .01  .1         1   1       1   1      120     0         4        5       6         6000
i1  20 40  .2     1         .5  .9        .1   .1         .5  1       .5  1      120     2         7        8       9         4000
i1  40 20       .5     1         .8  .95       1    .9         1   .1      .5  1      120     0         4        5       6         3000
i1  30 30       .8     1         .5  .5        .7   .7         .6  .9      0   0      120     0        10       11      12        20000

e

i1   0 20        .1     .3        .2  .2        .1   .4         .05 .8      0   0      120     2         7        8       9         5000
i1   0 20  0      .6        .5  .98       .1   .4         1   1       1   1      120     0         4        5       6        10000
i1  20 40  .2     1         .5  .98       .1   .1         .5  1       .5  1      120     2         7        8       9         4000
i1  40 20       .5     1         .8  .99       1    .9         1   .1      .5  1      120     0         4        5       6         3000
i1  30 30       .8     1         .5  .5        .7   .7         .6  .9      0   0      120     0        10       11      12        20000

e
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
