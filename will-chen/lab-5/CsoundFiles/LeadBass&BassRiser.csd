<CsoundSynthesizer>
<CsOptions>
</CsOptions>
<CsInstruments>
sr      =       96000 
kr      =       96000 
ksmps   =       1 
nchnls  =       2 

instr    1

ilevl    = p4*32767   
ifreq    = cpspch(p5) 
ishape   = p6         

asaw     oscili  1, ifreq, 1 
asaw1    limit  asaw, 0, ishape 
asaw2    limit  asaw, ishape, 1

aramp    = asaw1*(.5/ishape) + (asaw2 - ishape)*(.5/(1 - ishape))

apulse   table  aramp, 2, 1

outall      apulse*ilevl

endin

</CsInstruments>
<CsScore>
f1 0 8193 -7 0 8192 1 
f2 0 4096 7 1 2048 1 0 -1 2048 -1

i1  0.00  1.00  1.00  06.00 0.25
i1  +     .     .     .     0.50
i1  +     .     .     .     0.75
i1  +     .     .     .     0.999
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
 <bgcolor mode="background">
  <r>240</r>
  <g>240</g>
  <b>240</b>
 </bgcolor>
</bsbPanel>
<bsbPresets>
</bsbPresets>
