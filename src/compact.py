"""Purpose-drawn 24-unit symbols. No auto-scaling of detailed artwork."""
from drawing import INK, IVORY, attrs


def p(d, fill='none', width=1.75):
    return f'<path {attrs(d=d,fill=fill,stroke=INK,stroke_width=width)}/>'


def r(x,y,w,h,radius=1):
    return f'<rect {attrs(x=x,y=y,width=w,height=h,rx=radius,fill="none",stroke=INK,stroke_width=1.75)}/>'


def dot(x,y,radius=1.5,fill=INK):
    return f'<circle {attrs(cx=x,cy=y,r=radius,fill=fill,stroke=INK,stroke_width=1.5)}/>'


def db(symbol=''):
    return p('M4 6 V18 C4 22 20 22 20 18 V6 M4 6 C4 2 20 2 20 6 C20 10 4 10 4 6')+symbol


def net():
    return p('M4 6 L12 8 L20 12 M4 18 L12 16 L20 12 M4 6 L12 16 M4 18 L12 8')+''.join(dot(x,y) for x,y in [(4,6),(4,18),(12,8),(12,16),(20,12)])


def symbols():
    """Map canonical technical IDs to compact drawings with distinct silhouettes."""
    return {
        'tokenizer':r(3,4,18,16,2)+p('M3 9 H21 M9 9 V20 M15 9 V20'),
        'gpu':r(3,6,18,12)+dot(9,12,3,'none')+p('M16 10 H18 M16 14 H18 M6 18 V21 M10 18 V21'),
        'microcontroller':r(5,3,14,18)+r(9,8,6,7)+p('M3 7 H5 M3 12 H5 M3 17 H5 M19 7 H21 M19 12 H21 M19 17 H21'),
        'neural-network':net(),
        'transformer':r(5,3,14,6)+r(5,15,14,6)+p('M12 9 V15 M5 18 H2 V6 H5 M19 18 H22 V6 H19 M8 6 H16 M8 18 H16'),
        'rag':r(3,3,11,15)+p('M6 7 H11 M6 11 H9 M12 21 H21 V10 H18')+dot(15,14,3,'none')+p('M17 16 L20 19'),
        'microservices':r(3,3,6,6)+r(15,3,6,6)+r(9,15,6,6)+p('M9 6 H15 M6 9 L10 15 M18 9 L14 15'),
        'pub-sub':r(3,9,5,6)+p('M8 12 H14 M14 4 V20 M14 4 H19 M14 12 H19 M14 20 H19')+dot(20,4)+dot(20,12)+dot(20,20),
        'service':r(4,5,16,14,2)+p('M2 9 H4 M2 15 H4 M20 9 H22 M20 15 H22 M8 9 L6 12 L8 15 M16 9 L18 12 L16 15'),
        'worker':r(3,5,18,15)+p('M3 10 H21 M9 13 L9 17 L14 15 Z',INK)+p('M8 3 V5 M16 3 V5'),
        'orchestrator':p('M12 6 V18 M6 12 H18')+r(9,9,6,6)+dot(12,3.5)+dot(20.5,12)+dot(12,20.5)+dot(3.5,12),
        'database':db(p('M4 12 C4 16 20 16 20 12')),
        'relational-database':db(p('M8 11 V18 M16 11 V18 M8 14 H16 M8 18 H16')),
        'vector-database':db(p('M8 18 L15 11 M11 11 H15 V15')),
        'graph-database':db(p('M8 12 L16 13 L11 18 Z')+dot(8,12,1)+dot(16,13,1)+dot(11,18,1)),
        'model-weights':r(3,3,18,18)+dot(7,7,.8)+dot(15,7,1.8)+dot(7,16,2.2)+dot(16,16,1),
        'matrix':p('M6 3 H3 V21 H6 M18 3 H21 V21 H18')+''.join(dot(x,y,1) for x in (9,15) for y in (6,12,18)),
        'cpu':r(6,6,12,12)+r(9,9,6,6)+p('M9 3 V6 M15 3 V6 M9 18 V21 M15 18 V21 M3 9 H6 M3 15 H6 M18 9 H21 M18 15 H21'),
        'server':r(5,3,14,18)+p('M5 10 H19 M5 16 H19 M8 6 H12 M8 13 H12')+dot(16,6,.6)+dot(16,13,.6),
        'cloud':p('M7 19 H17 C23 19 23 11 18 10 C18 3 8 2 6 10 C1 10 1 19 7 19 Z'),
        'text-document':p('M5 3 H14 L19 8 V21 H5 Z M14 3 V8 H19 M8 12 H16 M8 16 H14'),
        'agent':r(5,6,14,12)+p('M8 12 H10 L12 9 L14 15 L16 12 M3 7 V3 H10 M21 17 V21 H14'),
        'tokens':r(3,5,8,6)+r(14,5,7,6)+r(3,14,6,6)+r(12,14,9,6),
        'cache':db(p('M13 10 L9 15 H12 L11 19 L16 13 H13 Z',INK,1)),
        'message-queue':r(3,6,4,11)+r(10,6,4,11)+r(17,6,4,11)+p('M3 20 H21 M18 18 L21 20 L18 22',width=1.5),
        'table':r(3,4,18,16)+p('M3 9 H21 M3 14 H21 M9 9 V20 M15 9 V20'),
    }


def additions():
    """New controls, flowchart primitives, and channel symbols."""
    ui={
        'menu':('Menu',p('M4 6 H20 M4 12 H20 M4 18 H20'),'navigation hamburger'),
        'close':('Close',p('M5 5 L19 19 M19 5 L5 19'),'dismiss cancel x'),
        'chevron-left':('Chevron left',p('M15 5 L8 12 L15 19'),'previous back navigation'),
        'chevron-right':('Chevron right',p('M9 5 L16 12 L9 19'),'next forward navigation'),
        'chevron-up':('Chevron up',p('M5 15 L12 8 L19 15'),'collapse navigation'),
        'chevron-down':('Chevron down',p('M5 9 L12 16 L19 9'),'expand dropdown navigation'),
        'external-link':('External link',p('M14 3 H21 V10 M21 3 L10 14 M10 5 H4 V20 H19 V14'),'new tab open website'),
        'download':('Download',p('M12 3 V16 M7 11 L12 16 L17 11 M4 17 V21 H20 V17'),'save export'),
        'upload':('Upload',p('M12 16 V3 M7 8 L12 3 L17 8 M4 17 V21 H20 V17'),'import send'),
        'copy':('Copy',r(8,8,13,13)+p('M16 5 V3 H3 V16 H5'),'clipboard duplicate'),
        'plus':('Plus',p('M12 4 V20 M4 12 H20'),'add create increase'),
        'minus':('Minus',p('M4 12 H20'),'remove decrease'),
        'check':('Check',p('M4 12 L9 17 L20 6'),'success done selected'),
        'refresh':('Refresh',p('M20 8 a8 8 0 1 0 0 8 M20 3 V8 H15'),'reload sync update'),
        'home':('Home',p('M3 11 L12 3 L21 11 M5 9 V21 H10 V15 H14 V21 H19 V9'),'navigation landing'),
        'ui-settings':('Settings control',p('M4 6 H20 M4 12 H20 M4 18 H20')+dot(8,6,2,IVORY)+dot(16,12,2,IVORY)+dot(10,18,2,IVORY),'configuration preferences sliders'),
        'sun':('Light theme',dot(12,12,4,'none')+p('M12 2 V4 M12 20 V22 M2 12 H4 M20 12 H22 M5 5 L6.5 6.5 M17.5 17.5 L19 19 M5 19 L6.5 17.5 M17.5 6.5 L19 5'),'theme light mode'),
        'moon':('Dark theme',p('M20 15 A8.5 8.5 0 0 1 9 4 A8 8 0 1 0 20 15 Z'),'theme dark mode'),
        'link':('Link',p('M10 7 L13 4 a5 5 0 0 1 7 7 L17 14 M14 17 L11 20 a5 5 0 0 1-7-7 L7 10 M8 16 L16 8'),'url hyperlink chain'),
        'ui-search':('Search control',dot(10.5,10.5,6.5,'none')+p('M15 15 L21 21'),'find magnifier navigation'),
    }
    flow={
        'start':('Start',dot(12,12,8,INK),'entry begin initial'),
        'end':('End',dot(12,12,9,'none')+dot(12,12,5,INK),'exit finish terminal'),
        'decision':('Decision',p('M12 2 L22 12 L12 22 L2 12 Z'),'condition branch diamond'),
        'process':('Process',r(3,5,18,14,1),'step operation rectangle'),
        'input-output':('Input / output',p('M7 5 H22 L17 19 H2 Z'),'io parallelogram input output'),
    }
    channels={
        'email':('Email',r(3,5,18,14,2)+p('M3 7 L12 13 L21 7'),'mail contact newsletter inbox'),
        'rss':('RSS',dot(5,19,1.5)+p('M4 11 a9 9 0 0 1 9 9 M4 4 a16 16 0 0 1 16 16'),'feed subscribe syndication'),
    }
    result=[]
    for category,items in [('interface',ui),('flowchart',flow),('channels',channels)]:
        for slug,(name,body,tags) in items.items():
            result.append(dict(id=slug,name=name,category=category,body=body,style='compact',size=24,
                               recommendedMinSize=24,description=f'{name} symbol drawn on a 24-unit grid.',tags=(tags+' '+slug.replace('-',' ')).split()))
    return result
