<CsoundSynthesizer>
<CsOptions>
-odac
</CsOptions>
<CsInstruments>

sr = 48000
ksmps = 128
nchnls = 1
0dbfs = 1

indx = 0
//while (indx < 12) do
	//schedule("note",0,4,(indx+61))
	//indx+=1
//od

gisine		ftgen	0, 0, 8192, 10, 1						;FUNCTION TABLE THAT STORES A SINGLE CYCLE OF A SINE WAVE
//gifmmap 	ftgen 0, 0,
//ga1 init 0
//ga2 init 0

//instr note
//inote cpsmidinn p4
//inot = p4
//kadsr adsr 0.05,0.05,0.8,0.2
//aout vco2 0.2*kadsr,inote
//Sname sprintf "0000_%02d.wav", inot
//fout Sname,15,aout
//endin

opcode factorial,i,i
inum xin
	if inum == 0 then
		iout = 1
	elseif inum == 1 then
		iout = 1
	else
		iresult = 1
		indx = 2
		while (indx <= inum) do
			iresult *= indx
			indx += 1
		od
		iout = iresult
	endif
xout iout
endop

opcode bessel_j0,k,k
kx xin
	ksum init 0
	indx = 0
	while (indx < 3) do
		in1 pow (-1), indx
		kn2 pow (kx/2), (2*indx)
		id1 factorial indx
		
		ksum += (in1 * kn2) / (id1*id1)
	od
xout ksum
endop

opcode bessel_j1,k,k
kx xin
	ksum init 0
	indx = 0
	while (indx < 3) do
		in1 pow (-1), indx
		kn2 pow (kx/2), (2*indx + 1)
		id1 factorial indx
		id2 factorial (indx + 1)
		
		ksum += (in1 * kn2) / (id1 * id2)
	od
xout ksum
endop

opcode bessel_jn,k,ik
iN, kx xin
	if iN < 0 then
		iout1 pow (-1), iN
		iN = (-1)*iN
		kout2 bessel_jn iN,kx
		kout = iout1 * kout2
	elseif iN == 0 then
		kout bessel_j0 kx
	elseif iN == 1 then
		kout bessel_j1 kx
	else
		kJ_nm1 bessel_j0 kx
		kJ_nm2 bessel_j1 kx
		indx = 1
		while indx < iN do
			kJ_nk = (2 * indx / kx) * kJ_nm1 - kJ_nm2
			kJ_nm2 = kJ_nm1
			kJ_nm1 = kJ_nk
		od
		kout = kJ_nm1
	endif
xout kout
endop
	
opcode fmCorrect,k,k
kbeta xin
	knum init 0
	kden init 0
	indx = -1
	while indx <= 1 do
		kJn bessel_jn indx,kbeta
		kJn = abs(kJn)
		in1 = abs(1 + indx)
		
		knum += kJn * in1
		
		kden += kJn
	od
	if kden == 0 then
		kout = 1
	else
		kout = knum / kden
	endif
xout kout
endop


instr fmNote
ibaseFrequency cpsmidinn p4
ibasefreq = p4
i1ratio = 1.0
i2ratio = 1.0

i1index1 = 0.
i1index2 = 0.
k2index2 chnget "slider2"
i2index1 = 0.

i1out = 0
i2out = 1

kadsr1 adsr 0.05,0.05,1,0.2
kadsr2 adsr 0.05,0.05,1,0.2

klfo lfo 1,10

//kfmCorrect2 fmCorrect kadsr2 * i2index2
a1 init 0
a2 init 0
a1 oscili kadsr1, (ibaseFrequency * i1ratio)*(1 + (a1 * i1index1) + (a2 * i2index1))
a2 oscili kadsr2, (ibaseFrequency * i2ratio)*(1 + (a2 * k2index2) + (a1 * i1index2))

aout = 0.5 * ((i1out/(i1out+i2out))*a1 + (i2out/(i1out+i2out))*a2)
out aout
dispfft aout, 0.05, 2048, 1
endin
schedule("fmNote",0,90,61)

</CsInstruments>
<CsScore>
e 99999

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
 <bsbObject type="BSBVSlider" version="2">
  <objectName>slider0</objectName>
  <x>62</x>
  <y>270</y>
  <width>20</width>
  <height>100</height>
  <uuid>{187c948c-0c07-4f26-b222-0433a14ecda0}</uuid>
  <visible>true</visible>
  <midichan>0</midichan>
  <midicc>0</midicc>
  <description/>
  <minimum>0.00000000</minimum>
  <maximum>1.00000000</maximum>
  <value>0.00000000</value>
  <mode>lin</mode>
  <mouseControl act="jump">continuous</mouseControl>
  <resolution>-1.00000000</resolution>
  <randomizable group="0">false</randomizable>
 </bsbObject>
 <bsbObject type="BSBVSlider" version="2">
  <objectName>slider2</objectName>
  <x>121</x>
  <y>271</y>
  <width>20</width>
  <height>100</height>
  <uuid>{99f082ac-d78f-48db-9b28-a1014894551d}</uuid>
  <visible>true</visible>
  <midichan>0</midichan>
  <midicc>0</midicc>
  <description/>
  <minimum>0.00000000</minimum>
  <maximum>10.00000000</maximum>
  <value>0.00000000</value>
  <mode>lin</mode>
  <mouseControl act="jump">continuous</mouseControl>
  <resolution>-1.00000000</resolution>
  <randomizable group="0">false</randomizable>
 </bsbObject>
 <bsbObject type="BSBVSlider" version="2">
  <objectName>slider1</objectName>
  <x>92</x>
  <y>271</y>
  <width>20</width>
  <height>100</height>
  <uuid>{e60d5f12-d5d1-4ea7-b514-147d86b1000e}</uuid>
  <visible>true</visible>
  <midichan>0</midichan>
  <midicc>0</midicc>
  <description/>
  <minimum>0.00000000</minimum>
  <maximum>1.00000000</maximum>
  <value>0.00000000</value>
  <mode>lin</mode>
  <mouseControl act="jump">continuous</mouseControl>
  <resolution>-1.00000000</resolution>
  <randomizable group="0">false</randomizable>
 </bsbObject>
 <bsbObject type="BSBVSlider" version="2">
  <objectName>slider3</objectName>
  <x>150</x>
  <y>270</y>
  <width>20</width>
  <height>100</height>
  <uuid>{42254ac1-0b0d-4d08-8168-73285a986502}</uuid>
  <visible>true</visible>
  <midichan>0</midichan>
  <midicc>0</midicc>
  <description/>
  <minimum>0.00000000</minimum>
  <maximum>1.00000000</maximum>
  <value>0.00000000</value>
  <mode>lin</mode>
  <mouseControl act="jump">continuous</mouseControl>
  <resolution>-1.00000000</resolution>
  <randomizable group="0">false</randomizable>
 </bsbObject>
 <bsbObject type="BSBGraph" version="2">
  <objectName/>
  <x>128</x>
  <y>495</y>
  <width>350</width>
  <height>150</height>
  <uuid>{d7b51f03-d13a-4f4e-91d3-7158907bbb5c}</uuid>
  <visible>true</visible>
  <midichan>0</midichan>
  <midicc>-3</midicc>
  <description/>
  <value>0</value>
  <objectName2/>
  <zoomx>1.00000000</zoomx>
  <zoomy>1.00000000</zoomy>
  <dispx>1.00000000</dispx>
  <dispy>1.00000000</dispy>
  <modex>lin</modex>
  <modey>lin</modey>
  <showSelector>true</showSelector>
  <showGrid>true</showGrid>
  <showTableInfo>true</showTableInfo>
  <showScrollbars>true</showScrollbars>
  <enableTables>true</enableTables>
  <enableDisplays>true</enableDisplays>
  <all>true</all>
 </bsbObject>
 <bsbObject type="BSBScope" version="2">
  <objectName/>
  <x>261</x>
  <y>343</y>
  <width>350</width>
  <height>150</height>
  <uuid>{113ac297-6ef2-40b7-a564-14bb7974f0fa}</uuid>
  <visible>true</visible>
  <midichan>0</midichan>
  <midicc>-3</midicc>
  <description/>
  <value>-255.00000000</value>
  <type>scope</type>
  <zoomx>2.00000000</zoomx>
  <zoomy>1.00000000</zoomy>
  <dispx>1.00000000</dispx>
  <dispy>1.00000000</dispy>
  <mode>0.00000000</mode>
  <triggermode>NoTrigger</triggermode>
 </bsbObject>
</bsbPanel>
<bsbPresets>
</bsbPresets>
