"""Additional illustrated concepts and targeted revisions to ambiguous silhouettes."""
from drawing import *


def extend(icons):
    def add(category,slug,name,body,description,tags):
        icons.append(dict(id=slug,name=name,category=category,body=body,description=description,tags=sorted(set((tags+' '+slug.replace('-',' ')).split()))))

    # A worker executes queued jobs; a service exposes an interface. Keep both concepts distinct.
    updates={
        'worker':(box(48,54,153,155,STEEL,14)+rect(63,72,122,89,INK,3)+''.join(rect(72,y,35,16,IVORY,2) for y in (84,110,136))+poly([(133,94),(169,117),(133,140)],RED)+rect(69,177,112,17,IVORY,2),'Job execution appliance with queued tickets and a play-shaped execution control.'),
        'model-weights':(box(46,52,154,156,STEEL,10)+rect(61,69,123,121,INK,3)+''.join(circle(81+j*40,90+i*40,r,RED if r>=11 else IVORY,stroke=STEEL_TOP,sw=1.5) for i,row in enumerate(((4,11,6),(13,5,9),(7,10,3))) for j,r in enumerate(row)),'Parameter matrix whose varying dot sizes represent different weight magnitudes.'),
        'table':(box(42,55,164,151,STEEL,10)+rect(55,71,137,119,IVORY,2)+rect(55,71,137,26,RED,2)+path('M55 124 H192 M55 157 H192 M96 97 V190 M145 97 V190',stroke=STEEL,sw=3),'Rows and columns beneath a distinct header row.'),
    }
    for icon in icons:
        if icon['id'] in updates: icon['body'],icon['description']=updates[icon['id']]

    add('data','chunking','Chunking',document(''.join(rect(72,y,94,29,STEEL,2) for y in (79,127,175))+path('M37 117 H207 M37 165 H207',stroke=RED,sw=3,stroke_dasharray='7 6')),'Document segmented into bounded passages with explicit cut lines.','rag passages split segmentation')
    add('data','join','Join',box(29,61,76,117,IVORY,9)+box(149,61,76,117,STEEL,9)+path('M57 91 H81 M57 121 H81 M168 91 H193 M168 121 H193',stroke=RED,sw=4)+path('M77 195 H179 M77 195 V182 M179 195 V182',stroke=IVORY,sw=3)+circle(126,119,24,RED)+path('M112 119 H140 M126 105 V133',stroke=IVORY,sw=4),'Two tabular inputs combined on a shared key.','sql merge relational combine')
    add('data','sort','Sort',box(44,51,168,158,STEEL,11)+''.join(rect(64,76+i*36,w,21,IVORY,2) for i,w in enumerate((34,62,93)))+arrow(181,83,181,182,RED,5),'Records ordered from shorter to longer bars.','order ascending descending ranking')
    add('data','deduplicate','Deduplicate',box(36,55,78,98,IVORY,9)+box(52,72,78,98,IVORY,9)+box(166,98,56,83,STEEL,9)+arrow(133,136,158,136,RED,4)+path('M72 102 H107 M72 124 H107',stroke=INK,sw=3)+check(178,121,30,IVORY),'Repeated input records reduced to one retained record.','unique distinct dedup cleaning')
    add('data','data-validation','Data validation',document(grid(72,81,3,3,25,8))+circle(171,181,35,STEEL)+check(151,163,41,IVORY),'Structured input checked against a data contract.','validate quality schema constraints clean')
    add('data','train-test-split','Train/test split',box(44,65,164,131,STEEL,10)+''.join(rect(57+j*28,85+i*29,21,21,RED if j==4 else IVORY,2) for i in range(3) for j in range(5))+path('M163 53 V212',stroke=RED,sw=4,stroke_dasharray='7 7'),'Dataset divided into a larger training partition and a held-out test partition.','evaluation holdout partition training testing')
    add('ai','kv-cache','KV cache',cylinder('',2)+rect(72,97,109,65,INK,3)+''.join(rect(x,y,38,18,IVORY if x==82 else RED,2) for x in (82,132) for y in (108,135)),'Paired key and value rows retained during autoregressive generation.','key value attention inference reuse cache')
    add('ai','positional-encoding','Positional encoding',box(39,57,178,148,STEEL,12)+rect(52,73,150,112,INK,3)+path('M59 110 C77 63 98 159 121 110 S162 63 190 110 M59 147 C97 104 137 190 190 147',stroke=IVORY,sw=4)+''.join(line(x,168,x,176,RED,3) for x in (67,93,119,145,171)),'Ordered position ticks aligned with sinusoidal signal channels.','position rotary rope sinusoidal sequence')
    add('ai','sampling','Sampling',box(39,57,174,147,STEEL,12)+rect(52,71,146,116,INK,3)+''.join(rect(64+i*29,173-h,18,h,RED if i==2 else IVORY,2) for i,h in enumerate((34,75,51,24)))+arrow(131,37,131,105,RED,4),'A selected candidate drawn from a categorical probability distribution.','temperature topk topp probability decode')
    add('ai','quantization','Quantization',path('M38 211 V43 M38 211 H225',stroke=IVORY,sw=3)+path('M50 190 C84 190 90 61 210 61',stroke=STEEL_TOP,sw=4)+path('M50 190 H80 V162 H110 V134 H140 V106 H170 V78 H210',stroke=RED,sw=6),'Smooth numerical values mapped onto a finite set of discrete levels.','int8 int4 precision compression rounding')
    add('architecture','browser','Browser',screen(rect(51,66,140,22,IVORY,3)+circle(62,77,3,RED)+line(78,77,177,77,STEEL,3)+rect(60,104,47,48,STEEL,2)+line(119,109,178,109,IVORY,4)+line(119,130,167,130,IVORY,4)),'Browser window with an address bar and webpage content.','web client chrome firefox safari')
    add('architecture','frontend-app','Frontend app',monitor(rect(52,73,36,86,RED,2)+rect(99,75,87, 30,STEEL,2)+rect(99,117,39,41,IVORY,2)+rect(148,117,38,41,STEEL,2)),'Application interface with navigation, content, and action panels.','frontend ui website client spa')
    add('networking','reverse-proxy','Reverse proxy',box(82,58,89,148,STEEL,12)+rect(98, 80,57,98,INK,3)+path('M111 97 H140 V163 H111 Z',IVORY)+arrow(24,117,77,117)+path('M186 117 H207 V72 H230 M207 117 V187 H230',stroke=IVORY,sw=3),'Intermediary presenting one entrance and forwarding traffic to upstream services.','proxy nginx envoy ingress upstream')
    add('networking','websocket','WebSocket',box(31,67,60,130,STEEL,10)+box(166,67,60,130,STEEL,10)+arrow(79,109,180,109,IVORY,4)+arrow(180,155,79,155,RED,4)+path('M104 60 H151 M104 204 H151',stroke=STEEL_TOP,sw=5),'Persistent bidirectional channel between client and server endpoints.','duplex realtime connection ws socket')
    add('data','dead-letter-queue','Dead-letter queue',path('M31 70 V197 H224 V70',stroke=STEEL_TOP,sw=7)+box(48,89,65,87,IVORY,8)+box(135,89,65,87,RED,8)+cross(149,109,39,IVORY)+arrow(43,219,213,219),'Failed message isolated in a queue for inspection or reprocessing.','dlq failure retry messaging poison')
    return icons
