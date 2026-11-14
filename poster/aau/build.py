import re, charts, art
t=open('template.html').read()
qr=open('qr.svg').read().replace('<svg ','<svg width="170" height="170" ',1)
rep={'MECH':charts.mechanism(),'LINE':charts.linechart(),'DONUT':charts.donut(),'LDL':charts.ldlbars(),
     'LIVER':charts.liverbars(),'PROC':charts.process(),'QR':qr,
     'BRANCH':art.branch_header_color('#d9a940'),'ARTERY':art.artery_strip(560),'PLATE':art.fruit_plate('#d9a940',230),
     'SPRIG':art.sprig('#2e5a26',180),'SPRIG2':art.sprig('#b9852a',300,flip=True,seed=5),'ORN':art.ornament('#d9a940',420)}
for k,v in rep.items(): t=t.replace('{{'+k+'}}',v)
t=re.sub(r'\{\{I:(\w+)\}\}',lambda m:art.icon(m.group(1)),t)
open('poster.html','w').write(t)
