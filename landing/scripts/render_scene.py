"""Render an original illustrated concept film, without third-party footage.
Requires Pillow and imageio-ffmpeg. No customer data or live product footage.
"""
from pathlib import Path
import math
import subprocess
import sys
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

OUT = Path(__file__).resolve().parents[1] / 'dist/media'
OUT.mkdir(parents=True, exist_ok=True)
W, H, FPS, SECONDS = 1280, 720, 24, 18
INK='#292d27'; ORANGE='#f75422'; PAPER='#fbf8ef'; LIME='#e6ee9b'; SKIN='#dfad85'
fonts={n:ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',n) for n in (16,20,24,30,42)}

def frame(t):
    im=Image.new('RGB',(W,H),PAPER)
    d=ImageDraw.Draw(im)
    def rr(box,fill,r=18,outline=None,width=1):d.rounded_rectangle(tuple(map(int,box)),r,fill,outline,width)
    def ellipse(box,fill,outline=None,width=1):d.ellipse(tuple(map(int,box)),fill,outline,width)
    def line(points,fill,width=3):d.line([(int(x),int(y)) for x,y in points],fill,width=width)
    def text(x,y,label,size=20,fill=INK):d.text((x,y),label,font=fonts[size],fill=fill)
    def person(x,y,color,flip=1,phase=0):
        bob=math.sin(t*1.6+phase)*2
        y+=bob
        # Chair, shoulders, shirt, neck, hair, then face.
        rr((x-94,y+95,x+94,y+270),'#d7c5aa',38)
        rr((x-80,y+85,x+80,y+280),color,60)
        rr((x-19,y+52,x+19,y+110),SKIN,15)
        ellipse((x-60,y-45,x+60,y+85),INK)
        ellipse((x-49,y-20,x+49,y+85),SKIN)
        d.pieslice((x-62,y-49,x+58,y+45),180,355,fill=INK)
        ellipse((x+flip*46-10,y+28,x+flip*46+10,y+50),SKIN)
        for ex in (x-16+flip*8,x+17+flip*8):ellipse((ex-3,y+32,ex+3,y+40),INK)
        d.arc((x-10+flip*10,y+44,x+17+flip*10,y+63),5,165,fill=INK,width=3)
        # An arm reaches naturally toward the table.
        hand_y=y+195+math.sin(t*2+phase)*4
        line([(x-flip*50,y+134),(x+flip*30,hand_y),(x+flip*115,hand_y+9)],color,36)
        ellipse((x+flip*115-18,hand_y-7,x+flip*115+18,hand_y+27),SKIN)
    def beer(x,y,scale=1):
        rr((x+22*scale,y+8*scale,x+40*scale,y+39*scale),None,7,INK,3)
        rr((x,y,x+29*scale,y+48*scale),'#edb341',6,INK,2)
        rr((x-2*scale,y-4*scale,x+31*scale,y+9*scale),'#fffdf7',5)
    def plate(x,y):
        ellipse((x-59,y-20,x+59,y+20),'#fcfbf4',INK,2)
        for k in range(3):
            sy=y-11+k*10
            line([(x-37,sy),(x+39,sy+2)],'#b38349',3)
            for j in range(3):rr((x-28+j*19,sy-5,x-14+j*19,sy+6),'#a95c37',3)
        ellipse((x+29,y-13,x+43,y-1),'#8da570')

    # Architectural backdrop with a generous editorial header.
    text(44,30,'MOGUNOA',30)
    rr((1030,28,1236,64),LIME,18)
    text(1050,36,'CONCEPT FILM',16)
    rr((59,112,1221,527),'#eee6d7',28)
    rr((802,132,1190,416),'#ccdacb',20)
    for wx in (897,996,1095):line([(wx,132),(wx,416)],PAPER,7)
    line([(802,261),(1190,261)],PAPER,7)
    # Pendant lamps.
    for lx in (160,645):
        line([(lx,112),(lx,155)],INK,3)
        d.pieslice((lx-41,140,lx+41,214),180,360,fill='#bb7754')
        ellipse((lx-26,170,lx+26,180),'#f3cf94')
    # Booth and illustrated adult diners.
    rr((114,386,1167,555),'#aaa98a',28)
    person(289,288,'#c67d5a',1,0)
    person(1000,287,'#718a79',-1,1)
    ellipse((169,492,1130,594),'#c3ab8b')
    rr((567,541,714,620),INK,12)
    ellipse((149,425,1140,561),'#c7996d',INK,3)
    ellipse((170,430,1118,541),'#dfbb8e')
    ellipse((521,462,737,513),'#b99e7c')
    # Tabletop robot echoes the site's friendly cream/orange character.
    ry=math.sin(t*2)*2
    rr((566,382+ry,703,490+ry),'#f9f5e9',42,INK,3)
    rr((549,294+ry,720,429+ry),'#fffcf2',53,INK,3)
    rr((566,312+ry,705,409+ry),INK,32)
    blink=(t%4.5)>4.3
    for ex in (600,669):
        if blink:line([(ex-10,358+ry),(ex+10,358+ry)],ORANGE,5)
        else:
            ellipse((ex-12,339+ry,ex+12,374+ry),ORANGE)
            ellipse((ex-5,345+ry,ex+5,366+ry),INK)
    d.arc((624,367+ry,646,382+ry),0,180,fill=ORANGE,width=3)
    for dx,dy in ((0,0),(-5,5),(5,5),(0,10)):ellipse((631+dx,449+dy,634+dx,452+dy),INK)
    # A quiet menu and glass on the table.
    rr((358,473,431,513),PAPER,6)
    for k in range(3):line([(371,482+k*9),(417,482+k*9)],'#abb198',2)
    beer(886,453,.8)

    stage=min(2,int(t//6))
    local=t-stage*6
    progress=min(1,local/.55)
    slide=int((1-progress)*-12)
    if stage==0:
        rr((350,174+slide,840,273+slide),PAPER,22)
        d.polygon([(484,272+slide),(468,295+slide),(528,272+slide)],fill=PAPER)
        text(377,192+slide,'2',30)
        # two person icons, budget, beer, preference.
        for px in (427,455):
            ellipse((px-7,193+slide,px+7,207+slide),INK)
            rr((px-10,211+slide,px+10,235+slide),INK,8)
        text(489,195+slide,'<  ¥10,000',30)
        beer(697,194+slide,.75)
        text(757,204+slide,'...',30)
        for k in range(5):
            h=9+abs(math.sin(t*5+k*.8))*20
            rr((471+k*12,326-h/2,477+k*12,326+h/2),ORANGE,3)
    elif stage==1:
        rr((355,164+slide,845,278+slide),PAPER,22)
        d.polygon([(607,277+slide),(635,301+slide),(641,277+slide)],fill=PAPER)
        plate(430,211+slide)
        beer(518,183+slide,.85);beer(555,183+slide,.85)
        line([(613,185+slide),(613,256+slide)],'#dedfd7',2)
        text(640,184+slide,'FOR TWO',16)
        text(638,211+slide,'¥7,200',42)
        for k in range(3):
            r=19+k*10+math.sin(t*4)*3
            d.arc((635-r,357-r,635+r,357+r),210,330,fill=ORANGE,width=2)
    else:
        rr((349,175+slide,505,263+slide),PAPER,22)
        d.polygon([(412,261+slide),(388,286+slide),(449,261+slide)],fill=PAPER)
        line([(399,218+slide),(418,236+slide),(451,201+slide)],'#668245',7)
        rr((749,165+slide,907,294+slide),PAPER,17,INK,2)
        text(769,181+slide,'TABLE 08',16)
        for k in range(3):line([(772,215+k*12+slide),(840,215+k*12+slide)],'#b6bf9c',3)
        ellipse((851,245+slide,883,277+slide),LIME)
        line([(859,259+slide),(866,266+slide),(878,252+slide)],INK,3)
        if local>1.2:
            plate(496,491)
            beer(754,456,.8)
        for k in range(3):
            x=713+k*17;y=203+math.sin(t*2+k)*9
            ellipse((x-3,y-3,x+3,y+3),ORANGE)
    # A clean chapter/progress rail. The lower band is reserved for subtitles.
    labels=['01  ASK','02  SUGGEST','03  CONFIRM']
    for k,label in enumerate(labels):
        x=48+k*399
        rr((x,570,x+382,615),INK if k==stage else '#e9e5da',10)
        text(x+18,582,label,16,PAPER if k==stage else '#76796c')
        if k==stage:rr((x,614,x+max(6,int(382*local/6)),618),ORANGE,2)
    return im

frame(8).save(OUT/'ordering-poster.jpg',quality=92)
ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
proc=subprocess.Popen([ffmpeg,'-y','-f','rawvideo','-vcodec','rawvideo','-s',f'{W}x{H}','-pix_fmt','rgb24','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','medium','-crf','22','-pix_fmt','yuv420p','-movflags','+faststart',str(OUT/'ordering-scene.mp4')],stdin=subprocess.PIPE,stderr=subprocess.PIPE)
for i in range(FPS*SECONDS):proc.stdin.write(frame(i/FPS).tobytes())
proc.stdin.close()
error=proc.stderr.read().decode(errors='replace')
if proc.wait()!=0:raise RuntimeError(error[-1500:])
subprocess.run([ffmpeg,'-y','-i',str(OUT/'ordering-scene.mp4'),'-c:v','libvpx-vp9','-b:v','0','-crf','34','-an',str(OUT/'ordering-scene.webm')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
print(f'Rendered {SECONDS}s, {W}x{H}, {FPS} fps, {(OUT/"ordering-scene.mp4").stat().st_size:,} bytes.')
