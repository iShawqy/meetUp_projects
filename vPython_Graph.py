from vpython import*

oscillation = graph( xtitle='time', ytitle='value', fast=True, width=800)
funct1 = gcurve(color=color.blue, width=4, markers=True, marker_color=color.orange, label='curve')
funct2 = gvbars(delta=0.4, color=color.green, label='bars')
funct3 = gdots(color=color.red, size=6, label='dots')

for t in range(-300, 0, 1):
    rate(50)
    funct1.plot( t, 5.0+5.0*cos(-0.2*t)*exp(0.015*t) )
    funct2.plot( t, 2.0+5.0*cos(-0.1*t)*exp(0.015*t) )
    funct3.plot( t, 5.0*cos(-0.03*t)*exp(0.015*t) )
