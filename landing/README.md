# MOGUNOA 宣传网站

面向潜在餐厅试点伙伴的日语、中文、英语静态宣传网站。默认首页为日语，中文位于 `zh/`，英语位于 `en/`。使用原生 HTML、CSS、JavaScript，无运行时依赖、无需 API 密钥。

## 编辑与构建

在 landing 目录运行 `python scripts/build.py`。页面由 `src/template.html` 与 `src/translations.tsv` 生成，下载简介来自 `src/brief-*.txt`。缺少翻译会中止构建。修改文案后重新构建，不直接改生成的 HTML。

## 概念短片

`dist/media/ordering-scene.webm` 和 `.mp4` 是 18 秒、1280×720、24 fps 无声原创插画概念动画。WebM 优先，MP4 为后备和下载格式。`captions-*.vtt` 提供三语字幕，默认字幕跟随页面语言；页面同时提供文字说明和原生播放控制，不自动播放。

`scripts/render_scene.py` 用 Pillow 和 imageio-ffmpeg 重建动画及封面。这两个 Python 包只用于制作视频，不属于网站运行依赖。动画不是实机记录，三语网站不代表产品已实现三语语音服务。

## 本地预览

在此目录运行 `python scripts/preview.py`，访问 http://127.0.0.1:4173/。该预览服务显式配置字幕与视频的 MIME 类型，避免 Windows 本机映射差异。

发布 GitHub Pages 请看 `PUBLISH-GITHUB-PAGES.md`。可用 `python scripts/build.py --site-url 最终HTTPS网址 --output release/github-pages` 生成带 canonical、绝对地址 hreflang、分享卡片和 sitemap 的独立发布包，再运行 `python scripts/package_pages.py` 打包。只上传发布包，不上传整个工作目录。

## 文件

- `dist/index.html`：页面内容、导航、产品介绍和试点计划。
- `dist/styles.css`：桌面和移动端样式，包含键盘焦点和减少动态效果的支持。
- `dist/investor.css`：合作步骤、项目阶段与联系区块样式。
- `dist/project-brief.txt`：可下载的项目简介。
- `dist/app.js`：三语预设交互情景，推荐金额从示例清单计算；语言切换保留页面锚点。
- `dist/multilingual.css`：三语排版、语言导航和视频区域样式。
- `dist/hero.png`：AI 生成的原创产品概念图，不代表真实硬件外观。

## 内容边界

页面明确标注原型筹备阶段。对话、菜单、价格及确认结果均为演示，不接入 AI API，不提交订单、不联系店员、不收集个人信息。试点数量为计划目标，具体时间和支持条件需沟通确认。下载按钮提供实际简介文件。公司名称为 Candsystem；“咨询试点合作”通过 mailto 打开访客的邮件应用，收件人为 customerservice@candsystem.com，不自动发送邮件。对外分发前还需配置站点访问权限。

## 验证

`node --check dist/app.js` 检查脚本语法。通过浏览器检查三种情景、确认结果、重播、移动布局及页面锚点。
