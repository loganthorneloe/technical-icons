#!/usr/bin/env python3
"""Build all committed assets using Python 3.10+ and the standard library."""
import base64
import json
import math
import sys
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from drawing import *
from catalog_model import CATEGORIES, library, exports, inverse

ALL = library()
BY_ID = {icon['id']: icon for icon in ALL}


def write(path, content):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    if str(path).endswith('.md'):
        content=content.rstrip()+'\n'
    target.write_text(content, encoding='utf-8')


def caption(value,x,y,size=22,color=IVORY,anchor='middle',heading=False):
    return f'<text {attrs(x=x,y=y,fill=color,font_family="Sora" if heading else "Roboto",font_size=size,font_weight=600 if heading else 400,text_anchor=anchor)}>{escape(value)}</text>'


def font_defs():
    rules=[]
    for family,file,weight in [('Roboto','Roboto-Regular.ttf',400),('Sora','Sora-SemiBold.ttf',600)]:
        font=base64.b64encode((ROOT/'catalog/fonts'/file).read_bytes()).decode()
        rules.append(f"@font-face{{font-family:'{family}';font-weight:{weight};src:url(data:font/ttf;base64,{font}) format('truetype')}}")
    return '<defs><style>'+''.join(rules)+'</style></defs>'


def canvas(body,title,width=1600,height=900,description=''):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">'
            f'<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>'
            +font_defs()+f'<g stroke-linecap="round" stroke-linejoin="round">'
            +rect(0,0,width,height,INK,stroke='none')+body+'</g></svg>\n')


def title_block(kicker,title,subtitle,width=1600):
    return (rect(60,57,31,5,RED,stroke='none')+caption(kicker.upper(),105,66,15,STEEL_TOP,'start')
            +caption(title,60,126,38,IVORY,'start',True)+caption(subtitle,60,164,20,STEEL_TOP,'start')
            +line(60,198,width-60,198,'#303544',1))


def icon_at(slug,x,y,size=190,label=None):
    icon=BY_ID[slug]
    body=inverse(icon['body']) if icon['style'] in ('compact','brand') else icon['body']
    return move(body,x,y,size/icon['size'])+(caption(label,x+size/2,y+size+27,21) if label else '')


def examples():
    body=title_block('01 / language processing','From text to token IDs','Tokenization separates text into pieces, then looks up each piece in a vocabulary.')
    text_page=document(''.join(caption(value,73,y,16,INK,'start') for value,y in [('The cat',101),('sat on',131),('the mat.',161)]))
    body+=move(text_page,45,337,235/256)+caption('Text',162,599,21)+icon_at('tokenizer',338,337,260,'Tokenizer')
    body+=arrow(277,459,351,459)+arrow(572,459,667,459)
    tokens=['The','cat','sat','on','the','mat','.']
    ids=['791','2368','3621','319','279','4820','13']
    for i,(token,token_id) in enumerate(zip(tokens,ids)):
        y=248+i*68
        body+=box(704,y,142,47,IVORY,12)+caption(token,774,y+31,24,INK)
        body+=arrow(874,y+24,939,y+24)
        body+=box(968,y,149,47,STEEL,12)+caption(token_id,1042,y+31,24,IVORY)
    body+=caption('Tokens',781,778,22)+caption('Token IDs',1048,778,22)
    body+=path('M1150 270 H1171 Q1191 270 1191 290 V678 Q1191 698 1171 698 H1150',stroke=IVORY,sw=3)+arrow(1191,484,1273,484)
    body+=icon_at('database',1262,349,260,'Token sequence')
    body+=caption('Illustrative vocabulary IDs; actual token boundaries and IDs depend on the tokenizer.',60,846,17,STEEL_TOP,'start')
    write('examples/tokenization.svg',canvas(body,'Text to token IDs',description='An illustrative tokenization pipeline with seven tokens and example vocabulary IDs.'))

    body=title_block('02 / retrieval augmented generation','Ground generation in retrieved context','Index source passages first. Retrieve relevant passages for each incoming question.')
    body+=caption('INDEX',60,267,15,STEEL_TOP,'start',True)
    for slug,x,label in [('text-document',95,'Documents'),('chunking',400,'Chunk'),('embeddings',705,'Embed passages'),('vector-database',1010,'Vector database')]:
        body+=icon_at(slug,x,279,175,label)
    for x in (264,569,874): body+=arrow(x,365,x+128,365)
    body+=caption('QUERY',60,567,15,STEEL_TOP,'start',True)
    for slug,x,label in [('prompt',75,'Question'),('embeddings',356,'Embed query'),('vector-search',637,'Retrieve'),('language-model',918,'Generate'),('completion',1230,'Answer')]:
        body+=icon_at(slug,x,581,175,label)
    for x,end in [(247,347),(529,628),(810,909),(1091,1221)]: body+=arrow(x,668,end,668)
    body+=path('M1182 365 H1450 V519 H725 V586',stroke=IVORY,sw=3)+path('M718 576 L725 586 L732 576',stroke=IVORY,sw=3)
    body+=caption('Search index + return passages',1110,508,17,STEEL_TOP)
    body+=caption('Question is also included in the generation prompt.',60,855,17,STEEL_TOP,'start')
    write('examples/rag.svg',canvas(body,'Retrieval augmented generation',description='Separate indexing and query paths for retrieval augmented generation.'))

    body=title_block('03 / service architecture','Serve requests. Process work asynchronously.','An application writes durable data and queues background jobs for a worker.')
    for slug,x,label in [('user',60,'Client'),('cdn',329,'CDN'),('load-balancer',598,'Load balancer'),('service',867,'Application'),('database',1230,'Database')]:
        body+=icon_at(slug,x,291,180,label)
    for x,end in [(240,327),(507,596),(775,865),(1050,1228)]: body+=arrow(x,379,end,379)
    body+=path('M957 503 V667 H751',stroke=IVORY,sw=3)+path('M761 660 L751 667 L761 674',stroke=IVORY,sw=3)
    body+=icon_at('message-queue',560,585,185,'Job queue')+arrow(749,723,945,723)+icon_at('worker',947,628,150,'Worker')
    body+=path('M1097 701 H1445 V395 H1373',stroke=IVORY,sw=3)+path('M1383 388 L1373 395 L1383 402',stroke=IVORY,sw=3)+caption('Write result',1380,625,18,STEEL_TOP)
    body+=caption('Arrows show initiating request or data flow; response paths are omitted.',60,855,17,STEEL_TOP,'start')
    write('examples/service-architecture.svg',canvas(body,'Service architecture',description='Client request path with persistent storage and asynchronous background processing.'))

    body=title_block('04 / delivery pipeline','Turn a source change into a running service','Each stage produces the input required by the next stage.')
    stages=[('code-file','Source'),('unit-test','Test'),('build','Build'),('container-registry','Store image'),('deployment','Deploy'),('service','Run')]
    for i,(slug,label) in enumerate(stages):
        x=45+i*251
        body+=caption(f'{i+1:02}',x+99,327,17,STEEL_TOP)+icon_at(slug,x,374,190,label)
        if i<5: body+=arrow(x+190,471,x+244,471)
    body+=caption('A minimal successful path; approval gates, rollbacks, and failure branches can be added with the connector set.',60,744,18,STEEL_TOP,'start')
    write('examples/delivery-pipeline.svg',canvas(body,'Software delivery pipeline',description='A six-stage directed acyclic delivery pipeline from source to running service.'))


def sheets():
    for category,name in CATEGORIES.items():
        icons=[i for i in ALL if i['category']==category]
        cols=4; rows=math.ceil(len(icons)/cols); width=1080; height=260+rows*260
        body=title_block(f'{len(icons):02} artifacts / {category}',name,'Standalone SVG · '+('24-unit symbols' if category=='flowchart' else '256-unit illustrated objects'),width)
        for n,icon in enumerate(icons):
            x=38+(n%cols)*255; y=220+(n//cols)*260
            body+=icon_at(icon['id'],x+35,y,180)
            body+=caption(icon['name'],x+125,y+211,17)
            body+=caption(icon['id'],x+125,y+236,12,STEEL_TOP)
        write(f'docs/contact-sheets/{category}.svg',canvas(body,name,width,height))
    picks=['tokenizer','database','gpu','text-document','language-model','container','embeddings','agent','api-gateway','vector-database','lock','neural-network']
    body=title_block('AI for Software Engineers / artifact library','Technical icons, with a physical vocabulary.',f'{len(ALL)} concepts · Software engineering + AI · Editable SVG')
    for i,slug in enumerate(picks):
        x=52+(i%6)*253; y=246+(i//6)*284
        body+=icon_at(slug,x,y,205,BY_ID[slug]['name'])
    write('docs/overview.svg',canvas(body,'Icons — technical collection overview',1600,900))


def comparison_sheet():
    selected=[i for i in ALL if 'compactBody' in i and i['category'] not in ('interface','channels')]
    height=250+len(selected)*145
    body=title_block('Size study / compact renditions','Fewer details. Clearer small symbols.','Illustrated at 96px; compact geometry shown at actual pixel sizes.',1080)
    for x,label in [(365,'96px illustrated'),(555,'96px compact'),(726,'48px'),(859,'32px'),(969,'24px')]:
        body+=caption(label,x,236,15,STEEL_TOP)
    for n,icon in enumerate(selected):
        y=270+n*145
        body+=caption(icon['name'],50,y+55,17,IVORY,'start')
        body+=icon_at(icon['id'],317,y,96)
        for x,size in [(507,96),(702,48),(843,32),(957,24)]:
            body+=move(inverse(icon['compactBody']),x,y+(96-size)/2,size/24)
    write('docs/compact-comparison.svg',canvas(body,'Compact icon comparison',1080,height))


def web_overview():
    picks=['github','linkedin','youtube','instagram','discord','substack','email','phone','newsletter','address','microphone','support','home','download','ui-search','notification','calendar','shopping-cart']
    width=1440;height=1030
    body=title_block('Social / web / contact','Familiar forms. A shared material language.','Sculpted marks, folded paper, and functional metal objects.',width)
    for n,slug in enumerate(picks):
        x=26+n%6*235;y=240+n//6*253
        body+=icon_at(slug,x,y,205,BY_ID[slug]['name'])
    write('docs/web-overview.svg',canvas(body,'Social, web and contact collection',width,height))


def main():
    manifest=[]; assets={}
    for icon in ALL:
        record,files=exports(icon)
        manifest.append(record)
        for file,content in files:
            write(file,content)
            assets[file]=content
    styles={style:sum(style in i['renditions'] for i in manifest) for style in ('illustrated','compact','brand')}
    metadata={'schemaVersion':2,'version':'1.2.0','count':len(manifest),'assetCount':len(assets),'styles':styles,'categories':CATEGORIES,'palette':PALETTE,'icons':manifest}
    write('manifest.json',json.dumps(metadata,indent=2)+'\n')
    write('catalog/data.js','// Generated by scripts/build.py. Do not edit.\nwindow.ICON_LIBRARY = '+json.dumps({**metadata,'assets':assets},ensure_ascii=False,separators=(',',':'))+';\n')
    write('docs/catalog.md','# Icon index\n\nOpen `index.html` for search, style selection, and SVG downloads. Compact renditions and tone variants are listed in `manifest.json`.\n\n'+''.join(
        f"## {name}\n\n| Icon | File | Styles | Representation |\n| --- | --- | --- | --- |\n"+''.join(
            f"| {i['name']} | [{i['id']}](../{i['file']}) | {', '.join(i['renditions'])} | {i['description']} |\n" for i in manifest if i['category']==category)+'\n'
        for category,name in CATEGORIES.items()))
    write('docs/inventory.md',f"# Inventory\n\n{len(manifest)} concepts across {len(CATEGORIES)} categories; {len(assets)} SVG files including styles and tone variants.\n\n| Category | Concepts |\n| --- | ---: |\n"+''.join(f"| {name} | {sum(i['category']==category for i in manifest)} |\n" for category,name in CATEGORIES.items())+'\n| Style | Concepts with this style |\n| --- | ---: |\n'+''.join(f"| {style} | {count} |\n" for style,count in styles.items()))
    examples(); sheets(); comparison_sheet(); web_overview()
    print(f'Built {len(manifest)} concepts / {len(assets)} SVG files, {len(CATEGORIES)} contact sheets, 4 examples, and the catalog. Styles: {styles}')


if __name__=='__main__': main()
