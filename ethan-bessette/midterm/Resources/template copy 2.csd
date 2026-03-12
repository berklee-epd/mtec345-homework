<CsoundSynthesizer>
<CsOptions>
//-odac
</CsOptions>
<CsInstruments>

sr = 48000
ksmps = 1
nchnls = 1
0dbfs = 1

indx = 0
while (indx < 12) do
	schedule("fmNote",0,5,(indx+57))
	indx+=1
od

gisine		ftgen	0, 0, 8192, 10, 1						;FUNCTION TABLE THAT STORES A SINGLE CYCLE OF A SINE WAVE
//gifmmap 	ftgen 0, 0, -100, -7, 0, 0.01, 2.2, 10, 8.68, 10, 21, 10, 40, 10, 68, 10, 110, 10, 175, 10, 292, 10, 555, 0.01, 617, 0.01, 675, 0.01, 751, 0.01, 842, 0.01, 958, 0.01, 1117, 0.01, 1348, 0.01, 1731, 0.01, 2537, 0.01, 3627.5

// init fm map table with all zeros
//gifmmap ftgen 0, 0, -100, -2, 0
//instr fmgen
	//indx = 1
	//while indx <= 100 do
		//ipow pow indx,2
		//tablew (0.00005*ipow - 0.0008*indx + 0.00005), (indx-1), gifmmap
		//indx+=1
	//od
//endin
//schedule("fmgen",0,1)

//iarray[] init 100
//iarray fillarray 0,.00005,.00020,.00045,.00080,.00125,.00180,.00245,.00320,.00405,.00500,0.00605,


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


instr fmNote
seed 0
iseed unirand 1
rndseed iseed

ibaseFrequency cpsmidinn p4
ibasefreq = p4
i1ratio = 1
i2ratio = 1

//k1index1 init 0
//k1index1 chnget "scroll0"
//k1index2 init 0
//k1index2 chnget "scroll1"
//k2index2 chnget "scroll2"
//k2index2 init 0
//k2index1 chnget "scroll3"


i1index1 = int(rnd(551))/100
print i1index1

i1index2 = int(rnd(145))/10
print i1index2

i2index2 = int(rnd(551))/100
print i2index2

i2index1 = int(rnd(145))/10
print i2index1


i1out = int(rnd(100))/100
print i1out

i2out = int(rnd(100))/100
print i2out

iattack1 = int(rnd(5000))/1000
print iattack1
idecay1 = int(rnd(5000-(iattack1*1000)))/1000
print idecay1
irelease1 = int(rnd(5000-(iattack1*1000)-(idecay1*1000)))/1000
print irelease1
isustain1 = int(rnd(100))/100
print isustain1


iattack2 = int(rnd(5000))/1000
print iattack2
idecay2 = int(rnd(5000-(iattack2*1000)))/1000
print idecay2
irelease2 = int(rnd(5000-(iattack2*1000)-(idecay2*1000)))/1000
print irelease2
isustain2 = int(rnd(100))/100
print isustain2




kadsr1 adsr iattack1,idecay1,isustain1,irelease1
kadsr2 adsr iattack2,idecay2,isustain2,irelease2

klfo lfo 1,10

//koffset2 chnget "scroll6"
//koffset2 init 8.68
//koffset2 tablei (100*k2index2*kadsr2),gifmmap
//koffset2 = (((k2index2+0.01)*100)*((k2index2+0.01)*100) * 0.00005 - (k2index2+0.01*100) * 0.0001 + 0.00005) * kadsr2, gifmmap
//kx = (k2index2+0.01)*100
//koffset2 = (0.00005*(kx-1)+0.00011*((kx-1)*(kx-2)/2)-0.000001*((kx-1)*kx*(kx-5)/6)+0.000000003*((kx+1)*(kx-1)*kx*(kx-2))/12 - 0.000000000000149*kx*kx*kx*kx*kx) * kadsr2
//printk 1, koffset2
//kx1 = (k1index1+0.01)*100
//koffset1 = (0.00005*(kx1-1)+0.00011*((kx1-1)*(kx1-2)/2)-0.000001*((kx1-1)*kx1*(kx1-5)/6)+0.000000003*((kx1+1)*(kx1-1)*kx1*(kx1-2))/12 - 0.000000000000149*kx1*kx1*kx1*kx1*kx1) * kadsr1


ix1 = (i1index1+0.01)*100
koffset1 = (0.00005*(ix1-1)+0.00011*((ix1-1)*(ix1-2)/2)-0.000001*((ix1-1)*ix1*(ix1-5)/6)+0.000000003*((ix1+1)*(ix1-1)*ix1*(ix1-2))/12 - 0.000000000000149*ix1*ix1*ix1*ix1*ix1) * kadsr1

ix2 = (i2index2+0.01)*100
koffset2 = (0.00005*(ix2-1)+0.00011*((ix2-1)*(ix2-2)/2)-0.000001*((ix2-1)*ix2*(ix2-5)/6)+0.000000003*((ix2+1)*(ix2-1)*ix2*(ix2-2))/12 - 0.000000000000149*ix2*ix2*ix2*ix2*ix2) * kadsr2




a1 init 0
a2 init 0

a1correction oscili 0.05*koffset1,((ibaseFrequency * i1ratio)),gisine
a2correction oscili 0.05*koffset2,((ibaseFrequency * i2ratio)),gisine



//kfm2 tablei (kadsr2*k2index2*100),gifmmap
a1 oscili kadsr1, koffset1*ibaseFrequency + (ibaseFrequency * i1ratio)*(1 + (a1 * i1index1) + (a2 * i2index1) + a1correction), gisine
a2 oscili kadsr2, koffset2*ibaseFrequency + (ibaseFrequency * i2ratio)*(1 + (a2 * i2index2) + (a1 * i1index2) + a2correction), gisine

aout = ((i1out/(i1out+i2out))*a1 + (i2out/(i1out+i2out))*a2)


Sname sprintf "0001_%02d.wav", ibasefreq
fout Sname,15,aout
//out aout
dispfft aout, 0.05, 2048, 1
endin

</CsInstruments>
<CsScore>
e 5
</CsScore>
</CsoundSynthesizer>


























<bsbPanel>
 <label>Widgets</label>
 <objectName/>
 <x>0</x>
 <y>0</y>
 <width>611</width>
 <height>652</height>
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
  <x>156</x>
  <y>266</y>
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
 <bsbObject type="BSBGraph" version="2">
  <objectName/>
  <x>18</x>
  <y>502</y>
  <width>350</width>
  <height>150</height>
  <uuid>{a747b28d-e9e3-4abe-b364-cccd32a41482}</uuid>
  <visible>true</visible>
  <midichan>0</midichan>
  <midicc>-3</midicc>
  <description/>
  <value>2</value>
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
 <bsbObject type="BSBScrollNumber" version="2">
  <objectName>scroll6</objectName>
  <x>221</x>
  <y>193</y>
  <width>80</width>
  <height>25</height>
  <uuid>{cc3d59df-e8c7-4667-868c-8c1076ada064}</uuid>
  <visible>true</visible>
  <midichan>0</midichan>
  <midicc>0</midicc>
  <description/>
  <alignment>left</alignment>
  <font>Arial</font>
  <fontsize>10</fontsize>
  <color>
   <r>0</r>
   <g>0</g>
   <b>0</b>
  </color>
  <bgcolor mode="background">
   <r>255</r>
   <g>255</g>
   <b>255</b>
  </bgcolor>
  <value>0.00000000</value>
  <resolution>0.00001000</resolution>
  <minimum>-999999999999.00000000</minimum>
  <maximum>999999999999.00000000</maximum>
  <bordermode>true</bordermode>
  <borderradius>1</borderradius>
  <borderwidth>1</borderwidth>
  <randomizable group="0">false</randomizable>
  <mouseControl act=""/>
 </bsbObject>
 <bsbObject type="BSBScrollNumber" version="2">
  <objectName>scroll2</objectName>
  <x>102</x>
  <y>216</y>
  <width>80</width>
  <height>25</height>
  <uuid>{d92d540b-b4e9-4435-928c-8d9c53081132}</uuid>
  <visible>true</visible>
  <midichan>0</midichan>
  <midicc>0</midicc>
  <description/>
  <alignment>left</alignment>
  <font>Arial</font>
  <fontsize>10</fontsize>
  <color>
   <r>0</r>
   <g>0</g>
   <b>0</b>
  </color>
  <bgcolor mode="background">
   <r>255</r>
   <g>255</g>
   <b>255</b>
  </bgcolor>
  <value>5.51000000</value>
  <resolution>0.01000000</resolution>
  <minimum>-999999999999.00000000</minimum>
  <maximum>999999999999.00000000</maximum>
  <bordermode>true</bordermode>
  <borderradius>1</borderradius>
  <borderwidth>1</borderwidth>
  <randomizable group="0">false</randomizable>
  <mouseControl act=""/>
 </bsbObject>
 <bsbObject type="BSBScrollNumber" version="2">
  <objectName>scroll1</objectName>
  <x>102</x>
  <y>184</y>
  <width>80</width>
  <height>25</height>
  <uuid>{3ef8f5ce-9c0b-4b56-9527-a29145642fd8}</uuid>
  <visible>true</visible>
  <midichan>0</midichan>
  <midicc>0</midicc>
  <description/>
  <alignment>left</alignment>
  <font>Arial</font>
  <fontsize>10</fontsize>
  <color>
   <r>0</r>
   <g>0</g>
   <b>0</b>
  </color>
  <bgcolor mode="background">
   <r>255</r>
   <g>255</g>
   <b>255</b>
  </bgcolor>
  <value>14.50000000</value>
  <resolution>0.01000000</resolution>
  <minimum>-999999999999.00000000</minimum>
  <maximum>999999999999.00000000</maximum>
  <bordermode>true</bordermode>
  <borderradius>1</borderradius>
  <borderwidth>1</borderwidth>
  <randomizable group="0">false</randomizable>
  <mouseControl act=""/>
 </bsbObject>
 <bsbObject type="BSBScrollNumber" version="2">
  <objectName>scroll0</objectName>
  <x>7</x>
  <y>216</y>
  <width>80</width>
  <height>25</height>
  <uuid>{602b09f6-4c13-4c7c-819a-7cc77793b597}</uuid>
  <visible>true</visible>
  <midichan>0</midichan>
  <midicc>0</midicc>
  <description/>
  <alignment>left</alignment>
  <font>Arial</font>
  <fontsize>10</fontsize>
  <color>
   <r>0</r>
   <g>0</g>
   <b>0</b>
  </color>
  <bgcolor mode="background">
   <r>255</r>
   <g>255</g>
   <b>255</b>
  </bgcolor>
  <value>5.51000000</value>
  <resolution>0.01000000</resolution>
  <minimum>-999999999999.00000000</minimum>
  <maximum>999999999999.00000000</maximum>
  <bordermode>true</bordermode>
  <borderradius>1</borderradius>
  <borderwidth>1</borderwidth>
  <randomizable group="0">false</randomizable>
  <mouseControl act=""/>
 </bsbObject>
 <bsbObject type="BSBScrollNumber" version="2">
  <objectName>scroll3</objectName>
  <x>6</x>
  <y>183</y>
  <width>80</width>
  <height>25</height>
  <uuid>{f757b8f2-6fd5-4152-ad4c-4cfa6e645c3f}</uuid>
  <visible>true</visible>
  <midichan>0</midichan>
  <midicc>0</midicc>
  <description/>
  <alignment>left</alignment>
  <font>Arial</font>
  <fontsize>10</fontsize>
  <color>
   <r>0</r>
   <g>0</g>
   <b>0</b>
  </color>
  <bgcolor mode="background">
   <r>255</r>
   <g>255</g>
   <b>255</b>
  </bgcolor>
  <value>14.50000000</value>
  <resolution>0.01000000</resolution>
  <minimum>-999999999999.00000000</minimum>
  <maximum>999999999999.00000000</maximum>
  <bordermode>true</bordermode>
  <borderradius>1</borderradius>
  <borderwidth>1</borderwidth>
  <randomizable group="0">false</randomizable>
  <mouseControl act=""/>
 </bsbObject>
 <bsbObject type="BSBButton" version="2">
  <objectName>button10</objectName>
  <x>119</x>
  <y>105</y>
  <width>100</width>
  <height>30</height>
  <uuid>{e24c1015-317e-43d8-8d21-4b85cac4c06d}</uuid>
  <visible>true</visible>
  <midichan>0</midichan>
  <midicc>0</midicc>
  <description/>
  <type>event</type>
  <pressedValue>1.00000000</pressedValue>
  <stringvalue/>
  <text>button10</text>
  <image>/</image>
  <eventLine>schedule("fmNote",0,5,57)</eventLine>
  <latch>false</latch>
  <momentaryMidiButton>false</momentaryMidiButton>
  <latched>false</latched>
  <fontsize>10</fontsize>
 </bsbObject>
</bsbPanel>
<bsbPresets>
</bsbPresets>
