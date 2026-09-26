"""Build complete static JA/ZH/EN pages with no runtime translation dependency."""
from pathlib import Path
from html.parser import HTMLParser
from html import escape
import argparse,json,re,shutil
from urllib.parse import urlsplit,urljoin
from xml.etree.ElementTree import Element,SubElement,ElementTree,register_namespace

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'src'; OUT=ROOT/'dist'
options=argparse.ArgumentParser(description=__doc__)
options.add_argument('--site-url',help='Final public HTTPS base URL, including the repository path if any')
options.add_argument('--output',type=Path,help='Optional standalone output folder; only public assets are copied')
args=options.parse_args()
site_url=None
if args.site_url:
    parsed=urlsplit(args.site_url)
    if parsed.scheme!='https' or not parsed.netloc or parsed.username or parsed.password or parsed.query or parsed.fragment:
        options.error('--site-url must be a public HTTPS base URL without credentials, query or fragment')
    site_url=args.site_url.rstrip('/')+'/'
if args.output:
    OUT=args.output.resolve()
    if OUT==ROOT or OUT==SRC or ROOT.is_relative_to(OUT):
        options.error('--output must not overwrite the project or its parent directories')
    OUT.mkdir(parents=True,exist_ok=True)
    if OUT!=(ROOT/'dist').resolve():
        for name in ('styles.css','investor.css','multilingual.css','app.js','hero.png'):
            shutil.copy2(ROOT/'dist'/name,OUT/name)
        shutil.copytree(ROOT/'dist/media',OUT/'media',dirs_exist_ok=True)
rows={}
for row in (SRC/'translations.tsv').read_text(encoding='utf-8').splitlines():
    if row.strip():
        zh,ja,en=row.split('\t')
        rows[zh]={'ja':ja,'en':en,'zh':zh}

class Translate(HTMLParser):
    def __init__(self,lang):super().__init__(convert_charrefs=False);self.lang=lang;self.parts=[]
    def translate(self,s):
        key=s.strip()
        if key in rows:return s.replace(key,rows[key][self.lang])
        if re.search('[\u4e00-\u9fff]',key):raise ValueError(f'Missing translation: {key}')
        return s
    def handle_starttag(self,tag,attrs):
        raw=self.get_starttag_text()
        for k,v in attrs:
            if v and k in ('aria-label','alt','content'):
                translated=self.translate(v)
                raw=raw.replace(escape(v,quote=True),escape(translated,quote=True))
                if v in raw:raw=raw.replace(v,escape(translated,quote=True))
        self.parts.append(raw)
    def handle_startendtag(self,tag,attrs):self.handle_starttag(tag,attrs)
    def handle_endtag(self,tag):self.parts.append(f'</{tag}>')
    def handle_data(self,s):self.parts.append(escape(self.translate(s),quote=False))
    def handle_entityref(self,name):self.parts.append(f'&{name};')
    def handle_charref(self,name):self.parts.append(f'&#{name};')
    def handle_decl(self,s):self.parts.append(f'<!{s}>')
    def handle_comment(self,s):self.parts.append(f'<!--{s}-->')

template=(SRC/'template.html').read_text(encoding='utf-8')
template=template.replace('<h1>让点餐，<br>从<span class="orange">一句话</span><br>开始。</h1>','{{HERO_TITLE}}')
template=template.replace('お食事の相談、おまかせください。','用餐建议，交给你的桌边伙伴。')
template=template.replace('<link rel="stylesheet" href="investor.css">','<link rel="stylesheet" href="investor.css">\n  <link rel="stylesheet" href="multilingual.css">\n  {{ALTERNATES}}')
template=template.replace('    <nav aria-label="主导航">','    <div class="header-tools"><nav aria-label="主导航">')
template=template.replace('</nav>\n  </header>','</nav>{{LANGUAGES}}</div>\n  </header>')
template=template.replace('href="#experience">体验产品构想','href="#film">观看点单短片')
film='''    <section id="film" class="film section-shell section-space">
      <div class="section-heading"><div><span class="eyebrow">A MOMENT AT THE TABLE / 18 SEC</span><h2>先看一段，<br>桌边的小故事。</h2></div><p>两位客人、一台机器人，从说出偏好到确认推荐。</p></div>
      <div class="film-shell"><video id="ordering-film" controls playsinline preload="none" poster="media/ordering-poster.jpg" aria-label="点单场景概念动画" aria-describedby="film-description"><source src="media/ordering-scene.webm" type="video/webm"><source src="media/ordering-scene.mp4" type="video/mp4">{{TRACKS}}<p>视频无法播放时，可以下载 MP4 或阅读文字版。</p></video></div>
      <div class="film-meta"><span>18 秒 · 无声概念动画 · 可切换字幕</span><a class="text-link" href="media/ordering-scene.mp4" download="MOGUNOA-concept-film.mp4">下载短片 MP4 <span aria-hidden="true">↓</span></a></div>
      <p id="film-description" class="film-note">动画用于说明目标体验，不是真实产品实拍，不会产生订单。</p>
      <details class="film-transcript"><summary>查看视频文字版</summary><ol><li>客人：两个人，预算一万日元，想喝啤酒，不吃生鱼。</li><li>MOGUNOA：推荐几道适合分享的菜，加两杯啤酒，示例合计 ¥7,200。</li><li>客人：就这些吧。MOGUNOA 展示确认步骤，实际订单需要系统接收。</li></ol></details>
    </section>
'''
template=template.replace('    <section id="experience"',film+'    <section id="experience"')
titles={
 'zh':'<h1>让点餐，<br>从<span class="orange">一句话</span><br>开始。</h1>',
 'ja':'<h1>注文は、<br><span class="orange">ひとこと</span><br>から。</h1>',
 'en':'<h1>A great meal.<br><span class="orange">One little</span><br>conversation.</h1>'}
names={'ja':'日本語','zh':'中文','en':'English'}
html_lang={'ja':'ja','zh':'zh-CN','en':'en'}
for lang in names:
    parser=Translate(lang);parser.feed(template)
    s=''.join(parser.parts).replace('lang="zh-CN"',f'lang="{html_lang[lang]}"',1)
    base='./' if lang=='ja' else '../'
    links={'ja':base,'zh':base+'zh/','en':base+'en/'}
    language_label={'ja':'言語を選択','zh':'切换语言','en':'Choose a language'}[lang]
    language_links=''.join(f'<a href="{links[k]}" lang="{html_lang[k]}" hreflang="{html_lang[k]}"'+(' aria-current="page"' if k==lang else '')+f'>{v}</a>' for k,v in names.items())
    s=s.replace('{{LANGUAGES}}',f'<nav class="language-switch" aria-label="{language_label}">{language_links}</nav>')
    if site_url:
        urls={k:urljoin(site_url,'' if k=='ja' else k+'/') for k in names}
        canonical=urls[lang]
        title=rows['MOGUNOA — 让点餐，从一句话开始。'][lang]
        description=rows['MOGUNOA 桌面 AI 服务员正在寻找东京餐厅试点伙伴。探索对话推荐、菜单问答与确认点单的体验，联系 Candsystem 咨询试点合作。'][lang]
        seo=['<link rel="canonical" href="'+escape(canonical,quote=True)+'">']
        seo += [f'<link rel="alternate" hreflang="{html_lang[k]}" href="{escape(urls[k],quote=True)}">' for k in names]
        seo += [f'<link rel="alternate" hreflang="x-default" href="{escape(site_url,quote=True)}">']
        for property,value in {'og:type':'website','og:site_name':'MOGUNOA','og:title':title,'og:description':description,'og:url':canonical,'og:image':urljoin(site_url,'hero.png'),'og:image:alt':rows['概念效果图：一台有橙色眼睛的奶白色小机器人，坐在餐厅木桌上。'][lang],'og:locale':{'ja':'ja_JP','zh':'zh_CN','en':'en_US'}[lang]}.items():
            seo.append(f'<meta property="{property}" content="{escape(value,quote=True)}">')
        seo.append('<meta name="twitter:card" content="summary_large_image">')
        structured={'@context':'https://schema.org','@graph':[{'@type':'Organization','@id':site_url+'#organization','name':'Candsystem','email':'customerservice@candsystem.com','url':site_url},{'@type':'WebSite','@id':site_url+'#website','name':'MOGUNOA','url':site_url,'inLanguage':['ja','zh-CN','en'],'publisher':{'@id':site_url+'#organization'}}]}
        seo.append('<script type="application/ld+json">'+json.dumps(structured,ensure_ascii=False).replace('<','\\u003c')+'</script>')
        s=s.replace('{{ALTERNATES}}','\n  '.join(seo))
    else:
        # Do not invent a production URL for local previews.
        s=s.replace('{{ALTERNATES}}','')
    s=s.replace('{{HERO_TITLE}}',titles[lang])
    s=s.replace('{{TRACKS}}',''.join(f'<track kind="subtitles" src="media/captions-{k}.vtt" srclang="{html_lang[k]}" label="{v}"'+(' default' if k==lang else '')+'>' for k,v in names.items()))
    if lang!='ja':
        for attr in ('src','poster','href'):
            s=re.sub(rf'{attr}="(styles\.css|investor\.css|multilingual\.css|app\.js|hero\.png|media/[^"\s]+)"',lambda m:f'{attr}="../{m[1]}"',s)
    s=s.replace('download="MOGUNOA-pilot-brief.txt"',f'download="MOGUNOA-pilot-brief-{lang}.txt"')
    folder=OUT if lang=='ja' else OUT/lang;folder.mkdir(exist_ok=True)
    (folder/'index.html').write_text(s,encoding='utf-8')
    (folder/'project-brief.txt').write_text((SRC/f'brief-{lang}.txt').read_text(encoding='utf-8'),encoding='utf-8')
(OUT/'.nojekyll').write_text('',encoding='utf-8')
if site_url:
    register_namespace('','http://www.sitemaps.org/schemas/sitemap/0.9')
    sitemap=Element('{http://www.sitemaps.org/schemas/sitemap/0.9}urlset')
    for lang in names:
        entry=SubElement(sitemap,'{http://www.sitemaps.org/schemas/sitemap/0.9}url')
        SubElement(entry,'{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text=urljoin(site_url,'' if lang=='ja' else lang+'/')
    ElementTree(sitemap).write(OUT/'sitemap.xml',encoding='utf-8',xml_declaration=True)
    # robots.txt only governs crawling when served at the domain root.
    if urlsplit(site_url).path=='/':
        (OUT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+site_url+'sitemap.xml\n',encoding='utf-8')
    else:
        (OUT/'robots.txt').unlink(missing_ok=True)
else:
    (OUT/'sitemap.xml').unlink(missing_ok=True)
    (OUT/'robots.txt').unlink(missing_ok=True)
print('Built Japanese (default), Chinese and English pages, localized briefs, links and subtitle tracks.')
if site_url:print('SEO base URL: '+site_url)
