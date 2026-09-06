"""Distinct cel-shaded objects for web actions and ways to connect."""
import math
from drawing import *
from cel import *


def arc_points(cx,cy,r,start,end,n=48):
    return [(cx+r*math.cos(math.radians(start+(end-start)*i/n)),cy+r*math.sin(math.radians(start+(end-start)*i/n))) for i in range(n+1)]


def arc_band(cx,cy,r,inner,start,end,color=STEEL):
    return solid(arc_points(cx,cy,r,start,end)+arc_points(cx,cy,inner,end,start),color,9)


def pin():
    points=arc_points(124,100,62,155,385)+[(124,224)]
    body=solid(points,RED,11)
    return body+circle(124,96,23,INK)+circle(124,92,17,IVORY)


def calendar():
    return box(43,60,158,150,IVORY,11)+rect(43,60,158,36,RED,3)+pill(70,38,12,38,STEEL,5)+pill(159,38,12,38,STEEL,5)+''.join(rect(x,y,22,20,RED if (x,y)==(109,157) else STEEL,2) for x in (67,109,151) for y in (117,157))


def clock_face():
    return disc(122,132,85,STEEL,11)+circle(122,132,67,IVORY)+''.join(line(122+56*math.cos(a),132+56*math.sin(a),122+62*math.cos(a),132+62*math.sin(a),STEEL,3) for a in [i*math.pi/6 for i in range(12)])+path('M122 84 V132 L159 151',stroke=RED,sw=7)+circle(122,132,5,INK)


def head_and_shoulders(cx=123,cy=93,color=IVORY):
    return disc(cx,cy,30,color,7)+solid([(cx-63,cy+109),(cx-60,cy+72),(cx-37,cy+48),(cx+37,cy+48),(cx+60,cy+72),(cx+63,cy+109)],color,9)


def eye():
    outer=[(30,125)]+[(30+182*t,125-61*math.sin(math.pi*t)) for t in [i/40 for i in range(1,41)]]+[(30+182*t,125+61*math.sin(math.pi*t)) for t in [i/40 for i in range(39,-1,-1)]]
    return solid(outer,IVORY,9)+disc(121,125,30,STEEL,5)+circle(121,125,14,INK)+circle(112,116,5,PAPER)


def speaker():
    return solid([(35,103),(77,103),(129,63),(129,195),(77,158),(35,158)],STEEL,10)+poly([(45,112),(75,112),(75,148),(45,148)],STEEL_SHADE)


def headphones(mic=False):
    body=arc_band(122,113,76,60,180,360,STEEL)+pill(39,113,29,78,RED,8)+pill(174,113,29,78,RED,8)+rect(67,130,10,40,INK,3)+rect(162,130,10,40,INK,3)
    if mic:body+=path('M198 179 V201 H144',stroke=STEEL_TOP,sw=10)+pill(119,190,44,19,IVORY,5)
    return body


def microphone():
    return pill(95,33,57,115,STEEL,10)+''.join(line(111,y,136,y,INK,3) for y in (56,71,86,101))+path('M73 109 V127 C73 195 178 195 178 127 V109',stroke=IVORY,sw=10)+box(119,177,15,35,STEEL,5)+box(81,214,91,10,STEEL,7)


def website_art():
    results={}
    def add(slug,name,body,description,tags='',category='interface'):
        results[slug]=dict(id=slug,name=name,category=category,body=body,description=description,tags=sorted(set((tags+' '+slug.replace('-',' ')).split())))

    # Navigation and actions: exposed metal forms, paper, and functional mechanisms.
    add('menu','Menu',''.join(box(43,55+i*61,160,22,IVORY if i==0 else STEEL,11) for i in range(3)),'Three separate raised metal navigation slats.','navigation hamburger')
    cross_shape=[(64,44),(124,104),(184,44),(205,65),(145,125),(205,185),(184,206),(124,146),(64,206),(43,185),(103,125),(43,65)]
    add('close','Close',solid(cross_shape,RED,11),'Intersecting red metal bars with a visible cut edge.','dismiss cancel')
    for direction in ('left','right','up','down'):
        add('chevron-'+direction,'Chevron '+direction,chevron(direction,IVORY),'A folded metal chevron pointing '+direction+'.','navigation previous next expand collapse')
    add('external-link','External link',box(38,88,140,120,STEEL,11)+rect(53,106,110,85,INK,2)+solid([(103,42),(211,42),(211,150),(183,150),(183,91),(110,164),(88,142),(162,69),(103,69)],RED,10),'Open browser frame with a raised arrow leaving its corner.','new tab open website')
    tray=box(44,188,159,27,STEEL,12)+box(44,159,20,50,STEEL,9)+box(183,159,20,50,STEEL,9)
    add('download','Download',tray+arrow_shape('down',RED,.88,13,-6),'A red arrow descending into a steel receiving tray.','save export')
    add('upload','Upload',tray+arrow_shape('up',IVORY,.88,13,-6),'An ivory arrow lifting out of a steel sending tray.','import send')
    add('copy','Copy',box(47,48,120,147,STEEL,12)+box(80,80,120,147,IVORY,10)+line(102,120,174,120,RED,6)+line(102,145,174,145,STEEL,4)+line(102,170,156,170,STEEL,4),'Two overlapping sheets with separate visible edges.','clipboard duplicate')
    plus=[(108,44),(141,44),(141,108),(205,108),(205,141),(141,141),(141,205),(108,205),(108,141),(44,141),(44,108),(108,108)]
    add('plus','Plus',solid(plus,IVORY,13),'A raised cross made from thick ivory metal.','add create increase')
    add('minus','Minus',box(44,108,161,33,STEEL,13),'A single horizontal steel bar with a machined edge.','remove decrease')
    add('check','Check',solid([(39,126),(61,104),(108,151),(189,61),(213,83),(110,197)],IVORY,12),'A broad check cut from ivory metal.','success done selected')
    add('refresh','Refresh',arc_band(122,127,78,53,38,310,STEEL)+solid([(158,51),(210,112),(142,92)],RED,10),'A sweeping steel return arrow with a red folded head.','reload sync update')
    add('home','Home',box(62,107,119,100,IVORY,17)+solid([(30,111),(119,39),(212,111),(197,130),(119,70),(45,130)],RED,12)+rect(107,148,34,59,INK)+rect(73,132,20,24,STEEL,2),'Ivory house with a pitched red roof and visible side wall.','navigation landing')
    controls=box(44,46,163,163,STEEL,12)+screws(44,46,163,163)
    for y,x in ((84,85),(127,155),(170,115)):
        controls+=rect(64,y-3,120,7,INK,3)+box(x-13,y-14,25,28,IVORY,6)
    add('ui-settings','Settings control',controls,'Mechanical sliders in a recessed steel control panel.','configuration preferences')
    sun=''
    for i in range(8):
        sun+=solid(rotate([(113,32),(130,32),(130,59),(113,59)],i*45,122,125),IVORY,5)
    sun+=disc(122,125,45,RED,10)+path('M94 113 Q103 93 124 94',stroke=RED_TOP,sw=3)
    add('sun','Light theme',sun,'A red sun disc surrounded by eight separate ivory rays.','theme light mode')
    distance=math.hypot(35,-14);along=(85**2-70**2+distance**2)/(2*distance);height=math.sqrt(85**2-along**2)
    center=(124+35*along/distance,126-14*along/distance)
    upper=(center[0]-14*height/distance,center[1]-35*height/distance)
    lower=(center[0]+14*height/distance,center[1]+35*height/distance)
    angle=lambda point,cx,cy:math.degrees(math.atan2(point[1]-cy,point[0]-cx))
    crescent=arc_points(124,126,85,angle(upper,124,126),angle(lower,124,126)-360,70)+arc_points(159,112,70,angle(lower,159,112),angle(upper,159,112)+360,50)
    add('moon','Dark theme',solid(crescent,IVORY,12),'A solid ivory crescent with a shaded inner cutout.','theme dark mode')
    # Two interlocking rigid links; the offset distinguishes their front and back planes.
    link_art=move(ring(87,127,44,27,STEEL,9),0,-10)+move(ring(160,127,44,27,IVORY,9),0,19)+solid([(99,111),(114,98),(161,144),(146,158)],RED,5)
    add('link','Link',link_art,'Two interlocking metal loops joined by a red bridge.','url hyperlink chain')
    add('ui-search','Search control',loupe(),'A magnifying lens with a steel bezel and red handle.','find magnifier')

    add('bookmark','Bookmark',solid([(65,37),(179,37),(179,218),(122,179),(65,218)],RED,13)+line(83,62,158,62,RED_TOP,3),'A thick red ribbon with a notched lower edge.','save reading saved')
    heart=arc_points(85,95,45,180,315,25)+[(122,77)]+arc_points(159,95,45,225,360,25)+[(198,125),(122,214),(46,125)]
    add('heart','Heart',solid(heart,RED,12),'A raised red heart with two lobes and a pointed base.','like favorite love')
    star=[(122+(87 if i%2==0 else 38)*math.cos(-math.pi/2+i*math.pi/5),129+(87 if i%2==0 else 38)*math.sin(-math.pi/2+i*math.pi/5)) for i in range(10)]
    add('star','Star',solid(star,IVORY,11),'A five-point metal star with crisp shaded edges.','rating favorite featured')
    bell=[(50,176),(70,153),(73,103),(84,69),(108,54),(135,54),(161,69),(173,103),(175,153),(195,176)]
    add('notification','Notification',disc(122,196,16,RED,6)+solid(bell,IVORY,11)+pill(113,35,18,25,STEEL,5)+line(88,91,86,146,PAPER,4),'A hanging bell with a red clapper.','alert notifications subscribe')
    share=solid([(69,120),(176,58),(187,77),(79,139)],STEEL,7)+solid([(77,119),(183,179),(172,198),(67,138)],STEEL,7)+disc(63,130,25,IVORY,8)+disc(184,66,25,RED,8)+disc(184,189,25,IVORY,8)
    add('share','Share',share,'Three raised hubs joined by two angled metal arms.','social send forward')
    add('trash','Trash',solid([(66,80),(180,80),(167,215),(79,215)],STEEL,12)+box(50,66,146,17,RED,10)+box(95,42,58,20,STEEL,8)+path('M101 106 L105 190 M144 106 L140 190',stroke=INK,sw=7),'A tapered steel waste bin with a red lid.','delete remove discard')
    pencil=[(63,157),(162,58),(191,87),(92,186),(49,200)]
    add('edit','Edit',solid(pencil,IVORY,9)+solid([(162,58),(181,39),(210,68),(191,87)],RED,9)+poly([(63,157),(92,186),(49,200)],PAPER_SHADE)+poly([(49,200),(56,179),(70,193)],INK),'An angled pencil with a red eraser and exposed graphite tip.','write compose pencil')
    add('ui-filter','Filter control',solid([(34,58),(210,58),(147,131),(147,202),(108,218),(108,131)],STEEL,13)+poly([(45,65),(196,65),(137,123),(117,123)],STEEL_TOP),'A wide metal funnel narrowing into a single outlet.','refine results funnel')
    add('calendar','Calendar',calendar(),'A tear-off desk calendar with binding rings and a marked date.','date booking schedule')
    add('clock','Clock',clock_face(),'An ivory clock face in a steel case with red hands.','time history recent')
    door=box(116,43,85,172,STEEL,12)+rect(129,56,60,146,INK,1)
    add('log-in','Log in',door+arrow_shape('right',RED,.71,2,39),'A red arrow entering a recessed doorway.','login sign in enter')
    add('log-out','Log out',door+arrow_shape('left',IVORY,.71,2,39),'An ivory arrow leaving a recessed doorway.','logout sign out exit')
    add('more-horizontal','More options',''.join(disc(x,128,22,STEEL,9) for x in (55,122,189)),'Three separate raised circular controls.','overflow ellipsis menu')
    expand='';collapse=''
    for a in (0,90,180,270):
        expand+=solid(rotate([(38,39),(95,39),(95,56),(67,56),(101,90),(89,102),(55,68),(55,96),(38,96)],a),IVORY,6)
        collapse+=solid(rotate([(83,82),(83,42),(66,42),(66,53),(41,28),(29,40),(54,65),(42,65),(42,82)],a),STEEL,6)
    add('expand','Expand',expand,'Four corner brackets with outward-pointing diagonal tips.','fullscreen maximize')
    add('collapse','Collapse',collapse,'Four inward corner arrows reducing the viewing area.','minimize exit fullscreen')
    add('play','Play',solid([(66,40),(211,126),(66,213)],RED,13),'A solid triangular red playback key.','video start media')
    add('pause','Pause',box(58,45,42,163,IVORY,12)+box(151,45,42,163,IVORY,12),'Two separate ivory pause keys.','media hold')
    add('stop','Stop',box(53,53,141,151,RED,13),'A square red stop key with a machined top and side.','media halt')
    add('volume','Volume',speaker()+arc_band(128,129,53,45,-50,50,IVORY)+arc_band(128,129,84,76,-50,50,IVORY),'A steel loudspeaker with two raised sound-wave arcs.','audio speaker sound')
    add('volume-off','Muted',speaker()+solid([(139+x*.44,74+y*.44) for x,y in cross_shape],RED,6),'A steel loudspeaker crossed by a red mute mark.','mute silent audio off')
    cart=path('M29 55 H48 L75 177 H198',stroke=STEEL_TOP,sw=10)+solid([(61,79),(215,79),(194,150),(80,150)],IVORY,9)+path('M107 92 L115 139 M160 92 L152 139',stroke=STEEL,sw=5)+disc(91,207,18,STEEL,7)+disc(182,207,18,STEEL,7)
    add('shopping-cart','Shopping cart',cart,'A wheeled wire basket with a raised handle.','store basket checkout purchase')
    add('credit-card','Payment card',box(34,69,182,129,STEEL,11)+rect(34,88,182,26,INK)+box(54,139,39,27,IVORY,4)+line(115,161,190,161,IVORY,4),'A payment card with a dark strip and metal chip.','billing checkout credit debit payment')
    add('eye','Visible',eye(),'An almond-shaped eye with a raised steel iris.','show visibility view')
    add('eye-off','Hidden',eye()+solid([(51,42),(69,31),(208,205),(190,217)],RED,6),'An eye covered by a diagonal red privacy bar.','hide invisible visibility')
    add('ui-user','Profile',head_and_shoulders(color=STEEL),'A sculpted head and shoulder silhouette.','account avatar user person')
    add('help','Help',disc(122,127,82,STEEL,12)+path('M94 94 C94 61 151 64 151 96 C151 116 124 118 124 146',stroke=IVORY,sw=15)+circle(124,173,8,IVORY),'A raised question mark on a steel help medallion.','question faq assistance')
    add('info','Information',disc(122,127,82,IVORY,12)+box(115,111,18,69,STEEL,5)+disc(124,81,11,RED,4),'An information marker with a red dot and steel stem.','about details information')
    add('warning','Warning',solid([(123,34),(224,211),(24,211)],RED,10)+box(113,94,19,62,IVORY,5)+disc(123,181,11,IVORY,4),'A triangular red warning plate with a raised exclamation mark.','caution attention danger')

    # Contact objects have their own physical construction and purpose.
    def contact(slug,name,body,description,tags=''):add(slug,name,body,description,tags,'channels')
    contact('email','Email',envelope(),'A folded ivory envelope with overlapping paper flaps.','mail contact inbox')
    rss=disc(60,193,14,RED,5)+arc_band(50,201,91,68,270,360,IVORY)+arc_band(50,201,160,137,270,360,STEEL)
    contact('rss','RSS',rss,'Two raised broadcast arcs emerging from a red feed dot.','feed subscribe syndication')
    contact('phone','Phone',handset(),'A red telephone handset with separate receiver and mouthpiece.','telephone call contact')
    contact('contact-card','Contact card',box(32,62,185,136,IVORY,11)+circle(78,112,19,STEEL)+path('M51 164 V152 C51 124 105 124 105 152 V164 Z',STEEL)+line(126,107,190,107,RED,6)+line(126,132,187,132,STEEL,4)+line(126,157,171,157,STEEL,4),'An ivory address card with a portrait and contact lines.','vcard address book business card')
    contact('address','Address',pin(),'A red location pin with a recessed ivory center.','location map pin office visit')
    contact('chat','Chat',bubble(67,47,137,107,STEEL,'right')+bubble(31,104,144,97,IVORY)+''.join(circle(x,147,5,RED) for x in (66,98,130)),'Two offset conversation bubbles with distinct shaded edges.','conversation discussion live chat')
    contact('message','Message',bubble()+line(65,97,174,97,RED,6)+line(65,122,174,122,STEEL,5)+line(65,147,144,147,STEEL,5),'A single folded speech bubble carrying three message lines.','direct message dm comment')
    contact('send','Send',solid([(30,103),(221,39),(156,223),(118,141)],IVORY,10)+poly([(118,141),(221,39),(142,166)],STEEL)+poly([(30,103),(118,141),(221,39)],PAPER),'A folded paper airplane with a visible center crease.','submit paper plane outgoing')
    contact('newsletter','Newsletter',envelope(37,106,172,102,True)+paper(72,43,104,137)+poly([(40,110),(125,161),(206,110),(206,205),(40,205)],IVORY)+path('M40 205 L125 151 L206 205',stroke=PAPER_SHADE,sw=3),'A printed letter emerging from an opened envelope.','subscribe mailing list publication')
    contact('contact-form','Contact form',paper(53,37,141,180)+rect(74,136,99,23,STEEL,2)+rect(74,170,66,22,RED,2)+circle(176,55,22,RED)+path('M165 55 L173 63 L188 45',stroke=IVORY,sw=3),'A filled contact sheet with a submission button and confirmation seal.','inquiry form submit request')
    contact('video-call','Video call',box(39,73,124,114,STEEL,12)+solid([(163,103),(217, 72),(217,193),(163,166)],IVORY,9)+circle(100,117,19,IVORY)+path('M67 170 V155 C67 130 132 130 132 155 V170 Z',IVORY),'A video camera body with a profile silhouette and projecting lens.','meeting conference video webcam')
    contact('microphone','Microphone',microphone(),'A ribbed studio microphone in a pivoting stand.','voice recording audio podcast')
    contact('headset','Headset',headphones(),'Over-ear headphones with red pads and a steel headband.','listen audio headphones')
    contact('support','Support',headphones(True),'A communications headset with a boom microphone.','help customer service contact')
    at=ring(124,128,83,68,STEEL,10)+ring(126,124,33,19,IVORY,6)+pill(152, 91,16,76,IVORY,5)+path('M168 158 Q187 171 201 148',stroke=IVORY,sw=13)
    contact('at-sign','At sign',at,'A raised address spiral wrapped around a central letterform.','mention email handle username')
    return results
