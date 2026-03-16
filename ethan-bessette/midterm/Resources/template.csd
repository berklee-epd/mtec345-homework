<CsoundSynthesizer>
<CsOptions>
</CsOptions>
<CsInstruments>

sr = 48000
ksmps = 1
nchnls = 1
0dbfs = 1

indx = 0
while (indx < 12) do
	schedule("note",0,4,(indx+61))
	indx+=1
od


instr note
inote cpsmidinn p4
inot = p4
kadsr adsr 0.05,0.05,0.8,0.2
aout vco2 0.2*kadsr,inote
Sname sprintf "0000_%02d.wav", inot
fout Sname,15,aout
endin

</CsInstruments>
<CsScore>
e 4
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
