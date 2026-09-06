"""Small, dependency-free SVG drafting vocabulary. Coordinates are in a 256px square."""
from html import escape

INK = '#101527'
IVORY = '#E9DDC7'
PAPER = '#FFF4DE'
PAPER_SHADE = '#B8AC99'
STEEL = '#526B7A'
STEEL_TOP = '#78909B'
STEEL_SHADE = '#304654'
RED = '#CC3333'
RED_TOP = '#E4604E'
RED_SHADE = '#8F292C'
WHITE = '#FFFFFF'
PALETTE = dict(ink=INK, ivory=IVORY, paper=PAPER, paper_shade=PAPER_SHADE,
               steel=STEEL, steel_top=STEEL_TOP, steel_shade=STEEL_SHADE,
               red=RED, red_top=RED_TOP, red_shade=RED_SHADE, white=WHITE)


def attrs(**values):
    return ' '.join(f'{k.replace("_", "-")}="{escape(str(v), quote=True)}"' for k, v in values.items() if v is not None)


def el(tag, **kw):
    return f'<{tag} {attrs(**kw)}/>'


def path(d, fill='none', stroke=INK, sw=2.5, **kw):
    return el('path', d=d, fill=fill, stroke=stroke, stroke_width=sw, **kw)


def rect(x, y, w, h, fill=IVORY, r=0, stroke=INK, sw=2.5):
    return el('rect', x=x, y=y, width=w, height=h, rx=r, fill=fill, stroke=stroke, stroke_width=sw)


def line(x1, y1, x2, y2, color=INK, sw=2.5, **kw):
    return el('line', x1=x1, y1=y1, x2=x2, y2=y2, stroke=color, stroke_width=sw, **kw)


def circle(x, y, r, fill=IVORY, stroke=INK, sw=2.5):
    return el('circle', cx=x, cy=y, r=r, fill=fill, stroke=stroke, stroke_width=sw)


def ellipse(x, y, rx, ry, fill=IVORY, stroke=INK, sw=2.5):
    return el('ellipse', cx=x, cy=y, rx=rx, ry=ry, fill=fill, stroke=stroke, stroke_width=sw)


def poly(points, fill=IVORY, stroke=INK, sw=2.5):
    return el('polygon', points=' '.join(f'{x},{y}' for x, y in points), fill=fill, stroke=stroke, stroke_width=sw)


def group(body, transform=None, **kw):
    return f'<g {attrs(transform=transform, **kw)}>{body}</g>'


def move(body, x=0, y=0, scale=1):
    return group(body, f'translate({x} {y}) scale({scale})')


def facets(color):
    return {IVORY: (PAPER, PAPER_SHADE), STEEL: (STEEL_TOP, STEEL_SHADE), RED: (RED_TOP, RED_SHADE),
            INK: (STEEL, STEEL_SHADE)}.get(color, (PAPER, STEEL_SHADE))


def box(x, y, w, h, color=STEEL, depth=14):
    """Three visible planes, projection toward the upper right."""
    top, side = facets(color)
    dy = round(depth * .7, 2)
    return (poly([(x,y),(x+depth,y-dy),(x+w+depth,y-dy),(x+w,y)], top)
            + poly([(x+w,y),(x+w+depth,y-dy),(x+w+depth,y+h-dy),(x+w,y+h)], side)
            + rect(x,y,w,h,color,3)
            + line(x+4,y+2,x+w-4,y+2,top,1.5))


def screws(x,y,w,h):
    return ''.join(circle(a,b,2.4,INK,INK,1) for a,b in [(x+8,y+8),(x+w-8,y+8),(x+8,y+h-8),(x+w-8,y+h-8)])


def vents(x,y,w,count=3,color=INK):
    return ''.join(line(x,y+i*8,x+w,y+i*8,color,4) for i in range(count))


def cabinet(face='', color=STEEL):
    return box(43,52,154,160,color,18)+screws(43,52,154,160)+face


def screen(face='', x=38,y=52,w=166,h=126):
    return box(x,y,w,h,STEEL,12)+rect(x+9,y+10,w-18,h-27,INK,4)+face+circle(x+w/2,y+h-8,2,IVORY,IVORY,1)


def monitor(face=''):
    return box(110,173,32,30,STEEL,8)+box(82,208,88,10,STEEL,10)+screen(face)


def document(face='',color=IVORY):
    return (path('M59 36 H155 L194 75 V219 H59 Z', PAPER_SHADE)
            + path('M51 30 H151 L188 67 V213 H51 Z',color)
            + path('M151 30 V67 H188',facets(color)[1])
            + line(57,33,147,33,facets(color)[0],1.5)+face)


def cylinder(face='',tiers=3,color=STEEL):
    result=''
    for i in reversed(range(tiers)):
        y=59+i*46
        result += path(f'M55 {y} V{y+43} C55 {y+69} 195 {y+69} 195 {y+43} V{y} Z', color)
        result += path(f'M163 {y+9} V{y+60} Q187 {y+56} 195 {y+43} V{y} Z',facets(color)[1],sw=0)
        result += path(f'M73 {y+15} V{y+54} L83 {y+57} V{y+18} Z',facets(color)[0],sw=0)
        result += ellipse(125,y,70,22,facets(color)[0])
    return result+ellipse(125,59,70,22,RED)+path('M61 60 C66 83 183 84 189 60',stroke=IVORY,sw=1.5)+face


def arrow(x1,y1,x2,y2,color=IVORY,sw=3):
    import math
    a=math.atan2(y2-y1,x2-x1)
    return (line(x1,y1,x2,y2,color,sw)
            + path(f'M{x2-10*math.cos(a-.65):.2f} {y2-10*math.sin(a-.65):.2f} L{x2} {y2} L{x2-10*math.cos(a+.65):.2f} {y2-10*math.sin(a+.65):.2f}',stroke=color,sw=sw))


def check(x,y,size=22,color=RED):
    return path(f'M{x} {y+size*.5} l{size*.35} {size*.35} l{size*.65} {-size*.85}',stroke=color,sw=4)


def cross(x,y,size=20,color=RED):
    return line(x,y,x+size,y+size,color,4)+line(x+size,y,x,y+size,color,4)


def code(x=85,y=106,color=IVORY):
    return path(f'M{x+13} {y} l-14 16 l14 16 M{x+62} {y} l14 16 l-14 16 M{x+47} {y-7} l-16 46',stroke=color,sw=4)


def grid(x,y,cols=3,rows=3,cell=22,gap=4,highlight=True):
    return ''.join(rect(x+c*(cell+gap),y+r*(cell+gap),cell,cell,RED if highlight and c==r else IVORY,2)
                   for r in range(rows) for c in range(cols))


def network(layers=(3,4,3),x=71,y=76,dx=51,dy=30,color=IVORY):
    pts=[[(x+i*dx,y+(max(layers)-n)*dy/2+j*dy) for j in range(n)] for i,n in enumerate(layers)]
    result=''.join(line(*p,*q,STEEL_TOP,2) for left,right in zip(pts,pts[1:]) for p in left for q in right)
    return result+''.join(circle(*p,7,RED if i==1 else color) for i,layer in enumerate(pts) for p in layer)


def magnifier(x=130,y=112,r=42):
    return (line(x+r*.7,y+r*.7,x+r*1.5,y+r*1.5,INK,17)
            + line(x+r*.7,y+r*.7,x+r*1.5,y+r*1.5,RED,10)
            + circle(x,y,r,IVORY)+circle(x,y,r-9,STEEL_SHADE)
            + path(f'M{x-r*.48} {y-4} Q{x-r*.45} {y-r*.5} {x-2} {y-r*.5}',stroke=IVORY,sw=3))


def gear(x=126,y=124,r=60):
    import math
    points=[]
    for i in range(48):
        a=i*math.pi/24
        rr=r if i%4 in (1,2) else r*.83
        points.append((round(x+rr*math.cos(a),2),round(y+rr*math.sin(a),2)))
    return poly(points,STEEL)+circle(x,y,r*.47,IVORY)+circle(x,y,r*.22,RED)


def chip(face='',color=STEEL):
    result=''
    for i in range(6):
        q=78+i*19
        result += rect(q,35,9,22,IVORY,2)+rect(q,200,9,22,IVORY,2)+rect(34,q,22,9,IVORY,2)+rect(200,q,22,9,IVORY,2)
    return result+box(57,62,139,137,color,10)+rect(73,78,106,105,INK,5)+face


def badge(body,x=163,y=166,r=31):
    return circle(x,y,r,IVORY)+body


def svg(body,title,description='',size=256,viewbox='0 0 256 256',background=None):
    bg=rect(0,0,*map(float,viewbox.split()[2:]),background,stroke='none',sw=0) if background else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="{viewbox}" role="img" aria-labelledby="title desc">\n'
            f'<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>\n'
            f'<g stroke-linecap="round" stroke-linejoin="round">{bg}{body}</g>\n</svg>\n')
