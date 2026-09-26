"""Validate and zip only the standalone GitHub Pages release, never private source."""
from pathlib import Path
import zipfile

ROOT=Path(__file__).resolve().parents[1]
release=ROOT/'release/github-pages'
allowed={'index.html','project-brief.txt','styles.css','investor.css','multilingual.css','app.js','hero.png','.nojekyll','sitemap.xml','robots.txt','zh/index.html','zh/project-brief.txt','en/index.html','en/project-brief.txt','media/ordering-poster.jpg','media/ordering-scene.mp4','media/ordering-scene.webm','media/captions-ja.vtt','media/captions-zh.vtt','media/captions-en.vtt'}
required=allowed-{'robots.txt'}
files={p.relative_to(release).as_posix():p for p in release.rglob('*') if p.is_file()}
if not required<=files.keys():raise SystemExit('Missing release assets: '+str(required-files.keys()))
if not files.keys()<=allowed:raise SystemExit('Unexpected files in release: '+str(files.keys()-allowed))
target=ROOT/'release/MOGUNOA-github-pages.zip'
with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED) as archive:
    for name,path in sorted(files.items()):archive.write(path,name)
print(f'Packaged {len(files)} public files: {target}')
