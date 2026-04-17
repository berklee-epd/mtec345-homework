<CsoundSynthesizer>
<CsOptions>
</CsOptions>
<CsInstruments>
sr      =       96000
kr      =       96000
ksmps   =       1
nchnls  =       2

		instr	1
isc		=		.6

ksw		expseg	30, p3, 18000

a1		init		0
a2		init		0
a3		init		0
a4		init		0
a5		init		0
a6		init		0
anz		trirand	30000
a1		=		.997 * a1 + isc * .029591 * anz
a2		=		.985 * a2 + isc * .032534 * anz
a3		=		.950 * a3 + isc * .048056 * anz
a4		=		.850 * a4 + isc * .090579 * anz
a5		=		.620 * a5 + isc * .108990 * anz
a6		=		.250 * a6 + isc * .255784 * anz
apnz		=		a1 + a2 + a3 + a4 + a5 + a6
apnz		butterbp	apnz, ksw, ksw * .05
apnz		butterlp	apnz, ksw * 1.2
		outs		apnz, apnz
		endin

		instr	2

idur		=		p3
iamp		=		p4
ifqc		=		cpspch(p5)
ifctab	=		p6
iswrt	=		p7
ifade	=		p8

kmaxf	expseg	.1, idur, 1

kfc1		oscili	1, iswrt/idur, ifctab
kfc		=		kfc1*kmaxf*ifqc/440

isc		=		.6

anz		trirand	iamp*20

a1		pareq	anz, 625,	  .7079, .707, 2
a3		pareq	a1,	2500,  .3548, .707, 2
a5		pareq	a3,	10000, .1778, .707, 2
apnz		pareq	a5,	20000, .1259, .707, 2

apnz1	butterbp	apnz, kfc, kfc*.05
apnz2	butterbp	apnz, kfc*1.502, kfc*.05
apnz3	butterbp	apnz, kfc*1.498, kfc*.05

adclk	linseg	0, ifade, 1, idur-2*ifade, 1, ifade, 0

		outs		(apnz1+apnz2)*adclk, (apnz1+apnz3)*adclk

		endin

		instr	3

idur		=		p3
iamp		=		p4
ifqc		=		cpspch(p5)
ifade	=		.1

isc		=		.6

kfqc		expseg	ifqc, idur, 100*ifqc

anz		rand		iamp
kdi		oscili	.1, 4, 1

a1		pareq	anz, ifqc*(1+kdi),	 .1, 20, 1

adclk	linseg	0, ifade, iamp, idur-2*ifade, iamp, ifade, 0

		outs		a1*adclk/1000, a1*adclk/1000

		endin

		instr	4

idur		=		p3
iamp		=		p4
ifqc		=		cpspch(p5)
ires		=		p6
ivol		=		p7
	
isc		=		.6

kfqc1   	expseg	100*ifqc, idur, ifqc
kfqc2   	expseg	95*ifqc, idur, ifqc*1.05
kfqc3   	expseg	105*ifqc, idur, ifqc*.95

anz	 	rand		iamp
a1	 	pareq	anz, kfqc1, ivol, ires, 1
a2	 	pareq	anz, kfqc2, ivol, ires, 1
a3	 	pareq	anz, kfqc3, ivol, ires, 1

adclk 	expseg	1, .002, iamp, idur-.002, 1

	 	outs		(a1+a2)*adclk/3000, (a1+a3)*adclk/3000

	 	endin

	  	instr	5

idur	  	=		p3
iamp	  	=		p4
ifqc	  	=		cpspch(p5)
iq	  	=		p6
ivol	  	=		p7
iton	  	=		p8

kfqcl   	expseg	 .1*ifqc, idur, 2*ifqc
kq	   	expseg	 .1*ifqc, idur, 2*ifqc
kfqch   	expseg	 10*ifqc, idur, .5*ifqc

anz	 	rand		iamp

a1	 	pareq	anz, kfqcl, ivol,	iq, 1
a2	 	pareq	anz, ifqc,  1/ivol, kq, 0
a3	 	pareq	anz, kfqch, ivol,	iq, 2

adclk 	expseg	iamp/10, .002, iamp, idur-.002, iamp/100

aout	 	=		((a2-a3)+(a2-a1)*iton)

	 	outs		aout*adclk/5000, aout*adclk/5000

	 	endin


</CsInstruments>
<CsScore>
f1 0 1024 10 1

i5 0    .2   9000  8.00   1    .1         1
i5 +    .    .     8.00   1    .1         4
i5 .    .    .     8.00   1    .1         6
i5 .    .    .     8.00   1    .1         10
i5 .    .2   9000  8.00   1    .1         8
i5 .    .    .     7.00   1    .1         6
i5 .1   .2   9000  8.00   1    .1         1
i5 +    .    .     8.00   1    .1         4
i5 .    .    .     8.00   1    .1         6
i5 .    .    .     8.00   1    .1         10
i5 .55  .1   9000  8.00   1    .1         1
i5 +    .    .     8.00   1    .1         4
i5 .    .    .     8.00   1    .1         6
i5 .    .    .     8.00   1    .1         10

i5 1.6  .2   9000  8.00   1    .1         1
i5 +    .    .     8.00   1    .1         4
i5 .    .    .     8.00   1    .1         6
i5 .    .    .     8.00   1    .1         10
i5 .    .2   9000  8.00   1    .1         8
i5 .    .    .     7.00   1    .1         6
i5 1.7  .2   9000  8.00   1    .1         1
i5 +    .    .     8.00   1    .1         4
i5 .    .    .     8.00   1    .1         6
i5 .    .    .     8.00   1    .1         10

i5 3.2  .2   9000  8.00   1    .1         1
i5 +    .    .     8.00   1    .1         4
i5 .    .    .     6.07   1    .1         4
i5 .    .    .     6.00   1    .1         2
i5 .    .2   9000  8.00   1    .1         1
i5 .    .    .     7.00   10   .2         4
i5 .    .    .     6.07   20   .3         6
i5 .    .    .     6.00   40   .4         10

i5 4.1  .2   9000  7.00   10   .2         4
i5 +    .    .     6.07   20   .3         6
i5 .    .    .     6.00   40   .4         10

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
