#!/usr/bin/env python3
"""Optional source preparation. Requires fonttools; ordinary builds use stored contours."""
import json,math
from pathlib import Path
from fontTools.pens.basePen import BasePen
from fontTools.svgLib.path import parse_path
ROOT=Path(__file__).resolve().parents[1]

class OutlinePen(BasePen):
    def __init__(self,tolerance):
        super().__init__(None);self.contours=[];self.current=[];self.tolerance=tolerance
    def _moveTo(self,p):
        if self.current:self._endPath()
        self.current=[p]
    def _lineTo(self,p):self.current.append(p)
    def _curveToOne(self,p1,p2,p3):
        def flatten(a,b,c,d,depth=0):
            length=math.hypot(d[0]-a[0],d[1]-a[1])
            distance=lambda p: abs((d[0]-a[0])*(a[1]-p[1])-(a[0]-p[0])*(d[1]-a[1]))/max(length,.001)
            if depth>12 or max(distance(b),distance(c))<=self.tolerance:
                self.current.append(d);return
            mid=lambda u,v:((u[0]+v[0])/2,(u[1]+v[1])/2)
            ab=mid(a,b);bc=mid(b,c);cd=mid(c,d);abc=mid(ab,bc);bcd=mid(bc,cd);center=mid(abc,bcd)
            flatten(a,ab,abc,center,depth+1);flatten(center,bcd,cd,d,depth+1)
        flatten(self.current[-1],p1,p2,p3)
    def _qCurveToOne(self,p1,p2):
        p0=self.current[-1]
        self._curveToOne(tuple(p0[i]+2*(p1[i]-p0[i])/3 for i in (0,1)),tuple(p2[i]+2*(p1[i]-p2[i])/3 for i in (0,1)),p2)
    def _closePath(self):self._endPath()
    def _endPath(self):
        if self.current:
            self.contours.append([[round(x,4),round(y,4)] for x,y in self.current]);self.current=[]

source=ROOT/'src/brands/marks.json'
record=json.loads(source.read_text())
for mark in record['icons']:
    pen=OutlinePen(max(mark['width'],mark['height'])/600)
    parse_path(mark['path'],pen);pen._endPath()
    mark['contours']=pen.contours
    if mark.get('provider')!='Simple Icons':
        names={'facebook':'facebook-f','reddit':'reddit-alien','pinterest':'pinterest-p','dev-to':'dev','linkedin':'linkedin-in','x':'x-twitter'}
        mark['source']=f"https://fontawesome.com/icons/{names.get(mark['id'],mark['id'])}?f=brands&s=brands"
source.write_text(json.dumps(record,indent=2)+'\n')
print(f'Prepared cel-shading contours for {len(record["icons"])} source marks.')
