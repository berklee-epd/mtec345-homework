<CsoundSynthesizer>
<CsOptions>
</CsOptions>
<CsInstruments>
sr      =       96000
kr      =       96000
ksmps   =       1
nchnls  =       2

	instr 1

iatt	=  0.002
imaxamp	=  1.333
idec	=  0.005
irel	=  0.05

imaxfrq	=  4
ifrqdec	=  0.0025

p3	=  p3+irel
imaxamp	=  sqrt(imaxamp)

icps	=  440.0*exp(log(2.0)*(p4-69.0)/12.0)
kcps	port 1,ifrqdec,imaxfrq
kcps	=  kcps*icps

iamp	=  0.0039+p5*p5/16192
kamp	linseg 0,iatt,imaxamp,idec,1,p3-(iatt+idec+irel),1,irel,0,1,0
kamp	=  iamp*kamp*kamp

a1	oscil3 1,kcps,1,0
a2	phasor kcps, 0.75
a2	butterhp a2, kcps*4.0
kffrq	expon 2093, (60/140)*0.5, 1046.5
a2	butterlp a2, kffrq
a1	=  kamp*(a1+a2*2)*15000

	outall a1

	endin



</CsInstruments>
<CsScore>

f 1 0 16384 10		1	0	0.25	0.0625	0	0.125	0	0.03125

t 0 140

#define Macro1(S#N1#N2) #

i 1	[$S+0.5000]	0.43	$N1	125
i 1	[$S+1.5100]	0.4375	$N1	120
i 1	[$S+2.5100]	0.43	$N2	122
i 1	[$S+3.5050]	0.4375	$N2	120

i 1	[$S+0.0000]	0.2	[$N1-12]	88
i 1	[$S+1.0050]	0.2	[$N1-12]	88
i 1	[$S+2.0050]	0.2	[$N2-12]	88
i 1	[$S+3.0050]	0.2	[$N2-12]	88

i 1	[$S+0.5050]	0.2	[$N1-12]	88
i 1	[$S+1.5050]	0.2	[$N1-12]	88
i 1	[$S+2.5050]	0.2	[$N2-12]	88
i 1	[$S+3.5050]	0.2	[$N2-12]	88

#

$Macro1(0#25#25)
$Macro1(4#33#35)
$Macro1(8#25#25)
$Macro1(12#33#35)

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
