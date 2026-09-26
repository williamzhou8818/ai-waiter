# GitHub Pages 发布

当前关联仓库：`williamzhou8818/ai-waiter`。未指定自定义域名时，发布包按默认地址 `https://williamzhou8818.github.io/ai-waiter/` 生成。若实际地址不同，必须重新生成发布包；不要把旧地址作为 canonical 发布。

## 可直接上传的文件

解压 `release/MOGUNOA-github-pages.zip`，将里面的文件和文件夹放到用于 Pages 的分支根目录，保证 `index.html`、`.nojekyll`、`zh/`、`en/` 和 `media/` 位于同一级。

GitHub 仓库 → Settings → Pages → Build and deployment：

1. Source 选择 **Deploy from a branch**。
2. 选择放有发布包的分支（可用 `gh-pages`）及 **/(root)**。
3. 保存后等待 GitHub 部署完成，再访问站点并点击三语切换和视频。

不要再套一层 `dist/` 或 `github-pages/` 文件夹。无需上传项目外层的跳转页。

发布包只包含宣传网站资源，不包含内部 `docs/intro.md`、品牌调查、源文件、Sites 配置或 Git 历史。请不要为了发布网页而直接将整个工作目录设为公开仓库：Pages 发布目录不决定公开 Git 仓库中的文件可见性。

## 重新生成

在 `landing` 目录执行（Python 3.10 或更新版本，无额外依赖）：

```powershell
python scripts/build.py --site-url https://williamzhou8818.github.io/ai-waiter/ --output release/github-pages
python scripts/package_pages.py
```

如果以后使用自定义域名，先将 `--site-url` 改成最终 HTTPS 地址，再重新生成，并在 GitHub Pages 设置中配置对应域名。生成过程不会修改 DNS 或自动发布。

## SEO 与上线检查

- 每种语言有独立标题、描述、canonical、绝对地址 hreflang、分享卡片信息。
- `sitemap.xml` 包含日语、中文、英语三个页面。上线后可在 Google Search Console 验证站点并提交站点地图；这不保证收录或排名。
- 对于 `/ai-waiter/` 这样的项目站点，子目录内的 robots.txt 不控制爬虫，因此不生成无效的 robots.txt。自定义域名根目录部署时会生成。
- 目前联系入口是 mailto：打开访客的邮件应用，不会在网站内保存或自动发送咨询。邮箱的实际收件能力需要你自行确认。
- 视频有 WebM 与 MP4 两种格式、三语字幕、文字版说明，采用点击播放。动画和点餐交互为概念演示。
- GitHub Pages 的公网访问与当前 Sites 的私密访问是独立配置。

参考：[GitHub Pages 发布源](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)、[Google 多语言网址](https://developers.google.com/search/docs/specialty/international/localized-versions)、[Google 站点地图](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap)。
