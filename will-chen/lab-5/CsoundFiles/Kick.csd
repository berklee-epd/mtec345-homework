<CsoundSynthesizer>
<CsOptions>
</CsOptions>
<CsInstruments>
sr      =       96000
kr      =       96000
ksmps   =       1
nchnls  =       2

	seed 0

	instr 1

imkey	=  p4
imvel	=  p5

icps	=  440.0*exp(log(2.0)*(imkey-69.0)/12.0)
iamp	=  0.0039+imvel*imvel/16192

ivol	table	 0,	64
ibpm	table	 1,	64

ifrqs	table	 2,	64
ifrqe	table	 3,	64
ifrqd	table	 4,	64

iffr1s	table	 5,	64
iffr1d	table	 6,	64
iffr2s	table	 7,	64
iffr2d	table	 8,	64
iffr3s	table	 9,	64
iffr3d	table	10,	64
iffr4s	table	11,	64
iffr4d	table	12,	64

iEQ1fo	table	13,	64
iEQ1fn	table	14,	64
iEQ1fa	table	15,	64
iEQ1l	table	16,	64
iEQ1q	table	17,	64
iEQ1m	table	18,	64

iEQ2fo	table	19,	64
iEQ2fn	table	20,	64
iEQ2fa	table	21,	64
iEQ2l	table	22,	64
iEQ2q	table	23,	64
iEQ2m	table	24,	64

iEQ3fo	table	25,	64
iEQ3fn	table	26,	64
iEQ3fa	table	27,	64
iEQ3l	table	28,	64
iEQ3q	table	29,	64
iEQ3m	table	30,	64

iEQ4fo	table	31,	64
iEQ4fn	table	32,	64
iEQ4fa	table	33,	64
iEQ4l	table	34,	64
iEQ4q	table	35,	64
iEQ4m	table	36,	64

insmix	table	37,	64

iEQn1fo	table	38,	64
iEQn1fn	table	39,	64
iEQn1fa	table	40,	64
iEQn1l	table	41,	64
iEQn1q	table	42,	64
iEQn1m	table	43,	64

iEQn2fo	table	44,	64
iEQn2fn	table	45,	64
iEQn2fa	table	46,	64
iEQn2l	table	47,	64
iEQn2q	table	48,	64
iEQn2m	table	49,	64

p3	=  p3+0.15

ibtime	=  60/ibpm

kamp	linseg 1,p3-0.15,1,0.05,0,0.1,0
kamp	=  kamp*iamp*ivol

kcps	port ifrqe*icps,ibtime/ifrqd,ifrqs*icps
knumh	=  sr/(2*kcps)

a_	buzz sr/(3.14159265*10),kcps,knumh,1,0
a__	buzz sr/(3.14159265*10),kcps,knumh,1,0.5

a0	tone a_-a__,10

a_	unirand 2
a_	=  a_-1

a_	pareq a_,iEQn1fa+icps*iEQn1fn+kcps*iEQn1fo,iEQn1l,iEQn1q,iEQn1m
a_	pareq a_,iEQn2fa+icps*iEQn2fn+kcps*iEQn2fo,iEQn2l,iEQn2q,iEQn2m

a0	=  a0+insmix*a_

a0	pareq a0,iEQ1fa+icps*iEQ1fn+kcps*iEQ1fo,iEQ1l,iEQ1q,iEQ1m
a0	pareq a0,iEQ2fa+icps*iEQ2fn+kcps*iEQ2fo,iEQ2l,iEQ2q,iEQ2m
a0	pareq a0,iEQ3fa+icps*iEQ3fn+kcps*iEQ3fo,iEQ3l,iEQ3q,iEQ3m
a0	pareq a0,iEQ4fa+icps*iEQ4fn+kcps*iEQ4fo,iEQ4l,iEQ4q,iEQ4m

kffr1	port 0,ibtime/iffr1d,iffr1s
kffr2	port 0,ibtime/iffr2d,iffr2s
kffr3	port 0,ibtime/iffr3d,iffr3s*icps
kffr4	port 0,ibtime/iffr4d,iffr4s*icps

kffrq	=  kffr1+kffr2+kffr3+kffr4

a0	butterlp a0,kffrq

a_	=  a0*kamp

	outall a_

	endin



</CsInstruments>
<CsScore>

t 0 135.00

i 1	0.0000	0.4000	33	120
i 1	1.0100	0.4000	33	112
i 1	2.0100	0.4000	33	124
i 1	3.0050	0.4000	33	112
i 1	4.0000	0.4000	33	116
i 1	5.0100	0.4000	33	112
i 1	6.0100	0.4000	33	120
i 1	6.9900	0.3000	33	120
i 1	7.5000	0.3000	33	116

i 1	8.0000	0.4000	33	120
i 1	9.0100	0.4000	33	112
i 1	10.010	0.4000	33	124
i 1	11.005	0.4000	33	112
i 1	12.000	0.4000	33	116
i 1	13.010	0.4000	33	112
i 1	14.010	0.4000	33	120
i 1	15.005	0.4000	33	112

f 64 0 64 -2	5500.0
		135.0

		5.3333
		1.0
		16.0

		880
		128
		0
		1
		8
		8
		0
		1

		0.5
		0
		0
		0.25
		0.7071
		1

		0.5
		0
		0
		0.25
		0.7071
		1

		0.5
		0
		0
		4
		2.0
		0

		0
		1.5
		0
		2.0
		1.0
		0

		16.0

		0
		16
		0
		0.0625
		0.7071
		1

		0
		16
		0
		0.0625
		0.7071
		1

f 1 0 262144 10 1

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
