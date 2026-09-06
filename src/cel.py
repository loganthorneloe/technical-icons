"""Hard-edged metal and paper forms for the website and social collections."""
import math
from drawing import *


def contour_path(contours):
    return ' '.join('M'+' L'.join(f'{x:.3f} {y:.3f}' for x,y in contour)+' Z' for contour in contours)


def extrude(d,contours,color=IVORY,depth=10,front_attrs=None):
    """Extruded silhouette with explicitly shaded side planes and an unchanged front path."""
    dx,dy=depth,-depth*.7
    top,side=facets(color)
    result=move(path(d,side,fill_rule='evenodd'),dx,dy)
    for contour in contours:
        for a,b in zip(contour,contour[1:]+contour[:1]):
            if a==b:continue
            ex,ey=b[0]-a[0],b[1]-a[1]
            shade=top if abs(ex)>abs(ey) or (abs(abs(ex)-abs(ey))<.001 and ex*ey>0) else side
            result+=poly([a,b,(b[0]+dx,b[1]+dy),(a[0]+dx,a[1]+dy)],shade,stroke='none',sw=0)
    result+=path(d,color,fill_rule='evenodd',**(front_attrs or {}))
    return result


def solid(points,color=IVORY,depth=10):return extrude(contour_path([points]),[points],color,depth)


def ellipse_points(cx,cy,rx,ry=None,n=64):
    ry=rx if ry is None else ry
    return [(cx+rx*math.cos(2*math.pi*i/n),cy+ry*math.sin(2*math.pi*i/n)) for i in range(n)]


def disc(cx,cy,r,color=STEEL,depth=9):return solid(ellipse_points(cx,cy,r),color,depth)


def ring(cx,cy,r,inner,color=STEEL,depth=9):
    contours=[ellipse_points(cx,cy,r),list(reversed(ellipse_points(cx,cy,inner)))]
    return extrude(contour_path(contours),contours,color,depth)


def rotate(points,angle,cx=128,cy=128):
    a=math.radians(angle)
    return [(cx+(x-cx)*math.cos(a)-(y-cy)*math.sin(a),cy+(x-cx)*math.sin(a)+(y-cy)*math.cos(a)) for x,y in points]


def chevron(direction,color=IVORY):
    points=[(87,51),(111,51),(179,124),(111,197),(87,197),(151,124)]
    return solid(rotate(points,{'right':0,'down':90,'left':180,'up':270}[direction]),color,12)


def arrow_shape(direction='down',color=RED,scale=1,x=0,y=0):
    points=[(110,47),(140,47),(140,139),(178,139),(125,197),(72,139),(110,139)]
    points=rotate(points,{'down':0,'left':90,'up':180,'right':270}[direction],125,122)
    points=[(x+px*scale,y+py*scale) for px,py in points]
    return solid(points,color,10*scale)


def pill(x,y,w,h,color=STEEL,depth=8):
    radius=min(w,h)/2
    points=[]
    for cx,cy,start in [(x+w-radius,y+radius,-90),(x+w-radius,y+h-radius,0),(x+radius,y+h-radius,90),(x+radius,y+radius,180)]:
        for i in range(9):
            a=math.radians(start+90*i/8);points.append((cx+radius*math.cos(a),cy+radius*math.sin(a)))
    return solid(points,color,depth)


def envelope(x=36,y=85,w=174,h=117,open_flap=False):
    body=''
    if open_flap:body+=solid([(x,y),(x+w/2,y-60),(x+w,y),(x+w,y+h),(x,y+h)],PAPER_SHADE,9)
    body+=box(x,y,w,h,IVORY,11)
    body+=poly([(x+3,y+3),(x+w/2,y+h*.62),(x+w-3,y+3)],PAPER)
    body+=poly([(x+3,y+h-3),(x+w/2,y+h*.47),(x+w-3,y+h-3)],IVORY)
    body+=line(x+4,y+h-2,x+w-4,y+h-2,PAPER_SHADE,2)
    return body


def paper(x=61,y=33,w=126,h=178):
    return box(x,y,w,h,IVORY,7)+line(x+20,y+32,x+w-20,y+32,RED,6)+line(x+20,y+55,x+w-20,y+55,STEEL,4)+line(x+20,y+75,x+w-36,y+75,STEEL,4)


def bubble(x=37,y=61,w=169,h=120,color=IVORY,tail='left'):
    tx=x+29 if tail=='left' else x+w-49
    points=[(x+9,y),(x+w-9,y),(x+w,y+9),(x+w,y+h-9),(x+w-9,y+h),(tx+23,y+h),(tx,y+h+29),(tx,y+h),(x+9,y+h),(x,y+h-9),(x,y+9)]
    return solid(points,color,10)


def handset(color=RED):
    points=[(50,51),(81,39),(109,83),(91,103),(107,128),(132,151),(152,137),(197,161),(185,199),(164,205),(127,187),(93,159),(63,122),(45,81)]
    return solid(points,color,12)+line(62,58,82,52,RED_TOP,2)+line(161,148,187,163,RED_TOP,2)


def loupe():
    return solid([(151,154),(171,141),(220,195),(199,215)],RED,10)+ring(101,100,62,44,STEEL,12)+path('M66 86 Q77 63 101 62',stroke=IVORY,sw=4)


def folded_card(face=''):
    return box(39,53,171,149,STEEL,12)+rect(52,68,144,116,IVORY,2)+face


def brand_object(mark,index=0):
    color={'youtube':RED,'pinterest':RED,'reddit':RED,'patreon':RED,'substack':RED,'gitlab':RED,'linkedin':STEEL,'facebook':STEEL,'discord':STEEL,'mastodon':STEEL,'telegram':STEEL,'twitch':STEEL}.get(mark['id'],IVORY)
    scale=177/max(mark['width'],mark['height']);x=(244-mark['width']*scale)/2;y=(263-mark['height']*scale)/2
    # Scale the body after constructing its extrusion so the front path remains source-exact.
    art=extrude(mark['path'],mark['contours'],color,13/scale,front_attrs={'data_brand_face':'true'})
    # Stroke remains optically consistent after scaling.
    art=art.replace('stroke-width="2.5"',f'stroke-width="{2.5/scale:.5f}"')
    return move(art,x,y,scale)
