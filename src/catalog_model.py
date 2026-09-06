"""Assemble concepts and explicit renditions without counting variants as concepts."""
import json
from pathlib import Path
from drawing import *
from icons import build_icons
from extensions import extend
from compact import additions, symbols
from website import website_art
from cel import brand_object

CATEGORIES = {
    'socials': 'Social brands', 'channels': 'Contact & feeds', 'interface': 'Website controls',
    'flowchart': 'Flowchart primitives', 'compute': 'Compute & hardware', 'networking': 'Cloud & networking',
    'storage': 'Storage & databases', 'data': 'Data & media', 'ai': 'AI & machine learning',
    'agents': 'Agents & orchestration', 'development': 'Software development',
    'delivery': 'Infrastructure & delivery', 'security': 'Security & identity',
    'observability': 'Observability & operations', 'architecture': 'System architecture',
    'math': 'Math & structures', 'connectors': 'Connectors & boundaries',
}


def library():
    icons=extend(build_icons())+additions()
    web=website_art()
    previous={i['id']:i for i in icons}
    for slug,art in web.items():
        if slug in previous:
            icon=previous[slug]
            compact_body=icon['body']
            icon.update(art,compactBody=compact_body,compactMinSize=24,style='illustrated',size=256,recommendedMinSize=64)
        else:
            icons.append(dict(**art,style='illustrated',size=256,recommendedMinSize=64))
    brands=json.loads((Path(__file__).parent/'brands/marks.json').read_text())
    for n,mark in enumerate(brands['icons']):
        scale=20/max(mark['width'],mark['height'])
        x=(24-mark['width']*scale)/2; y=(24-mark['height']*scale)/2
        brand_body=move(path(mark['path'],INK,'none',0,data_brand_face='true'),x,y,scale)
        provider=mark.get('provider','Font Awesome Free')
        version=mark.get('version',brands['version'])
        license=mark.get('license','CC-BY-4.0')
        attribution=(f"{provider} {version}; "+('Fonticons, Inc. (https://fontawesome.com), CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). ' if license=='CC-BY-4.0' else 'CC0 1.0 (https://creativecommons.org/publicdomain/zero/1.0/). ')+"Original front path preserved. Illustrated version adds cel-shaded extrusion; flat version is scaled and centered. Colors use the repository palette.")
        icons.append(dict(id=mark['id'],name=mark['name'],category='socials',body=brand_object(mark,n),brandBody=brand_body,style='illustrated',size=256,
                          recommendedMinSize=64,description=f"{mark['name']} mark as a solid, cel-shaded emblem with an unchanged source silhouette.",
                          tags=[mark['id'],'social','logo','brand','profile','cel shaded'],source=mark['source'],provider=provider,
                          attribution=attribution,license=license,sourcePathSha256=mark['sha256']))
    compact=symbols()
    for icon in icons:
        icon.setdefault('style','illustrated')
        icon.setdefault('size',256)
        icon.setdefault('recommendedMinSize',96)
        if icon['id'] in compact:
            icon['compactBody']=compact[icon['id']]
    order={key:index for index,key in enumerate(CATEGORIES)}
    return sorted(icons,key=lambda icon:order[icon['category']])


def inverse(body):
    # Swap ink and paper for dark surfaces; preserve any brand geometry and all other colors.
    return body.replace(INK,'__INK__').replace(IVORY,INK).replace('__INK__',IVORY)


def exports(icon):
    """Each rendition has its own dimensions and tone paths; canonical paths remain stable."""
    slug=icon['id']; category=icon['category']; style=icon['style']; size=icon['size']
    canonical=f'icons/{category}/{slug}.svg'
    result=[]
    def render(body):
        return svg(body,icon['name'],icon['description']+' '+icon.get('attribution',''),size=size,viewbox=f'0 0 {size} {size}')
    tones={'default':canonical}
    result.append((canonical,render(icon['body'])))
    if style in ('compact','brand'):
        tone=f'variants/ivory/{category}/{slug}.svg'
        tones={'ink':canonical,'ivory':tone}
        result.append((tone,render(inverse(icon['body']))))
    elif category=='connectors':
        tone=f'variants/ink/{category}/{slug}.svg'
        tones={'ivory':canonical,'ink':tone}
        result.append((tone,render(icon['body'].replace(IVORY,INK))))
    renditions={style:dict(file=canonical,size=size,viewBox=[0,0,size,size],recommendedMinSize=icon['recommendedMinSize'],tones=tones)}
    if 'compactBody' in icon:
        paths={}
        for tone,body in [('ink',icon['compactBody']),('ivory',inverse(icon['compactBody']))]:
            file=(f'variants/ivory/{category}/{slug}.svg' if tone=='ivory' and category in ('interface','channels') else f'variants/compact{ "-ivory" if tone=="ivory" else ""}/{category}/{slug}.svg')
            paths[tone]=file
            result.append((file,svg(body,icon['name']+' — compact',icon['description'],size=24,viewbox='0 0 24 24')))
        renditions['compact']=dict(file=paths['ink'],size=24,viewBox=[0,0,24,24],recommendedMinSize=icon.get('compactMinSize',32),tones=paths)
    if 'brandBody' in icon:
        paths={}
        for tone,body in [('ink',icon['brandBody']),('ivory',inverse(icon['brandBody']))]:
            file=f'variants/{"brand" if tone=="ink" else "ivory"}/{category}/{slug}.svg'
            paths[tone]=file
            result.append((file,svg(body,icon['name']+' — flat mark',icon['description']+' '+icon['attribution'],size=24,viewbox='0 0 24 24')))
        renditions['brand']=dict(file=paths['ink'],size=24,viewBox=[0,0,24,24],recommendedMinSize=24,tones=paths)
    record={key:value for key,value in icon.items() if key not in ('body','compactBody','compactMinSize','brandBody')}
    record.update(file=canonical,viewBox=[0,0,size,size],
                  anchors={'left':[0,size/2],'right':[size,size/2],'top':[size/2,0],'bottom':[size/2,size]},
                  renditions=renditions)
    # Retain the old canonical variant field for consumers; new consumers should use renditions.
    record['variants']={key:path for key,path in tones.items() if path!=canonical}
    return record,result
