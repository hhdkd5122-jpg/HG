import charts
t=open('template.html').read()
qr=open('qr.svg').read().replace('<svg ','<svg width="170" height="170" ',1)
for k,v in {'MECH':charts.mechanism(),'LINE':charts.linechart(),'DONUT':charts.donut(),'LDL':charts.ldlbars(),'LIVER':charts.liverbars(),'PROC':charts.process(),'QR':qr}.items():
    t=t.replace('{{'+k+'}}',v)
open('poster.html','w').write(t)
