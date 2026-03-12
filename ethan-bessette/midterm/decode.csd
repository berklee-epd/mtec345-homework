<CsoundSynthesizer>
<CsOptions>
-odac -W
</CsOptions>
<CsInstruments>

sr = 48000
ksmps = 1
nchnls = 1
0dbfs = 1


ginotelength = 5
ginumberofnotes = 1
gisine		ftgen	0, 0, 8192, 10, 1
gifilenumber = 0

indx = 0
while (indx < 1) do
	schedule(1,indx,ginotelength*ginumberofnotes)
	indx+=1
od

instr 1
	ktrig metro (1 / (ginotelength))
	printk 1,ktrig
	
	schedkwhen ktrig,0,0, 2,0,5
	
endin
	

instr 2
gifilenumber += 1

Sparamfile sprintf "Generated/%04d.txt",gifilenumber

ioutparams ftgen 0, 0, -17, -2,0

ftload Sparamfile,1,ioutparams

// Read parameters from table //

 i1ratio tab_i 0,ioutparams
 i1index1 tab_i 1,ioutparams
 i1index2 tab_i 2,ioutparams
 i2index2 tab_i 3,ioutparams
 i2index1 tab_i 4,ioutparams
 i1out tab_i 5,ioutparams
 i2out tab_i 6,ioutparams
 iattack1 tab_i 7,ioutparams
 idecay1 tab_i 8,ioutparams
 isustaintime1 tab_i 9,ioutparams
 isustain1 tab_i 10,ioutparams
 irelease1 tab_i 11,ioutparams
 iattack2 tab_i 12,ioutparams
 idecay2 tab_i 13,ioutparams
 isustaintime2 tab_i 14,ioutparams
 isustain2 tab_i 15,ioutparams
 irelease2 tab_i 16,ioutparams

	
indx = 0
while (indx < 12) do
	schedule(3,0,ginotelength,(indx+57),i1ratio,i1index1,i1index2,i2index2,i2index1,i1out,i2out,iattack1,idecay1,isustaintime1,isustain1,irelease1,iattack2,idecay2,isustaintime2,isustain2,irelease2)
	indx+=1
od


endin
						

instr 3

//seed 0
//iseed unirand 1
//rndseed iseed

ibaseFrequency cpsmidinn p4
ibasefreq = p4


// Parameters //

i1ratio = p5
i1index1 = p6
i1index2 = p7
i2index2 = p8
i2index1  = p9
i1out = p10
i2out = p11
iattack1 = p12
idecay1 = p13
isustaintime1 = p14
isustain1 = p15
irelease1 = p16
iattack2 = p17
idecay2 = p18
isustaintime2 = p19
isustain2 = p20
irelease2 = p21

// Ratios
i1ratio = i1ratio * 16
i2ratio = 1

//print i1ratio
//print i2ratio

// Indexes
i1index1 = int(i1index1*551) /100
i1index2 = int(i1index2*145)/10
i2index2 = int(i2index2*551)/100
i2index1 = int(i2index1*145)/10

//print i1index1
//print i1index2
//print i2index2
//print i2index1

// Output levels
i1out = int(i1out*100)/100
i2out = int(i2out*100)/100

//print i1out
//print i2out

// ADSR1 //

iadsrtime1 = iattack1 + idecay1 + isustaintime1 + irelease1

iattack1 = iattack1 / iadsrtime1 * ginotelength
idecay1 = idecay1 / iadsrtime1 * ginotelength
isustaintime1 = isustaintime1 / iadsrtime1 * ginotelength
irelease1 = irelease1 / iadsrtime1 * ginotelength

//print iattack1
//print idecay1
//print isustain1
//print isustaintime1
//print irelease1


// ADSR2 //

iadsrtime2 = iattack2 + idecay2 + isustaintime2 + irelease1

iattack2 = iattack2 / iadsrtime2 * ginotelength
idecay2 = idecay2 / iadsrtime2 * ginotelength
isustaintime2 = isustaintime2 / iadsrtime2 * ginotelength
irelease2 = irelease2 / iadsrtime2 * ginotelength

//print iattack2
//print idecay2
//print isustain2
//print isustaintime2
//print irelease2


// ADSR Envelopes //

kadsr1 adsr iattack1,idecay1,isustain1,irelease1
kadsr2 adsr iattack2,idecay2,isustain2,irelease2


// Self modulation adjustment curves //
ix1 = (i1index1+0.01)*100
koffset1 = (0.00005*(ix1-1)+0.00011*((ix1-1)*(ix1-2)/2)-0.000001*((ix1-1)*ix1*(ix1-5)/6)+0.000000003*((ix1+1)*(ix1-1)*ix1*(ix1-2))/12 - 0.000000000000149*ix1*ix1*ix1*ix1*ix1) * kadsr1

ix2 = (i2index2+0.01)*100
koffset2 = (0.00005*(ix2-1)+0.00011*((ix2-1)*(ix2-2)/2)-0.000001*((ix2-1)*ix2*(ix2-5)/6)+0.000000003*((ix2+1)*(ix2-1)*ix2*(ix2-2))/12 - 0.000000000000149*ix2*ix2*ix2*ix2*ix2) * kadsr2


a1correction oscili 0.05*koffset1,((ibaseFrequency * i1ratio)),gisine
a2correction oscili 0.05*koffset2,((ibaseFrequency * i2ratio)),gisine



// Audio generation
a1 init 0
a2 init 0

a1 oscili kadsr1, koffset1*ibaseFrequency + (ibaseFrequency * i1ratio)*(1 + (a1 * i1index1) + (a2 * i2index1) + a1correction), gisine
a2 oscili kadsr2, koffset2*ibaseFrequency + (ibaseFrequency * i2ratio)*(1 + (a2 * i2index2) + (a1 * i1index2) + a2correction), gisine

aout = ((i1out/(i1out+i2out))*a1 + (i2out/(i1out+i2out))*a2)


// File operations //

Saudio sprintf "Generated/%04d_%02d.wav", gifilenumber, ibasefreq

fout Saudio,16,aout

//out aout
//dispfft aout, 0.05, 2048, 1
endin

//schedule("fmNote",0,ginotelength,57)

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
 <width>370</width>
 <height>417</height>
 <visible>true</visible>
 <uuid/>
 <bgcolor mode="background">
  <r>240</r>
  <g>240</g>
  <b>240</b>
 </bgcolor>
 <bsbObject version="2" type="BSBScope">
  <objectName/>
  <x>20</x>
  <y>85</y>
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
 <bsbObject version="2" type="BSBGraph">
  <objectName/>
  <x>17</x>
  <y>267</y>
  <width>350</width>
  <height>150</height>
  <uuid>{a747b28d-e9e3-4abe-b364-cccd32a41482}</uuid>
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
</bsbPanel>
<bsbPresets>
</bsbPresets>
