# 2026 导考资料库 · 云南昆明中文类

**在线阅读网站：https://6sjsmmzn8z-cmd.github.io/daoyou-2026-yunnan/**

网站与仓库均公开，无须登录。全部页面导航、目录和学习指引使用中文，支持手机浏览。资料截点：2026年11月14日。

## 建议学习顺序

|顺序|内容|在线入口|
|---|---|---|
|第一步|确认2026考试规则、重点与最后一周计划|[考试与复习重点](https://6sjsmmzn8z-cmd.github.io/daoyou-2026-yunnan/articles/priorities.html)|
|第二步|按四科作答，查缺补漏|[100道在线训练](https://6sjsmmzn8z-cmd.github.io/daoyou-2026-yunnan/quiz.html)|
|第三步|准备12景点、对应团型及24道问答|[云南中文面试](https://6sjsmmzn8z-cmd.github.io/daoyou-2026-yunnan/articles/yunnan.html)|
|第四步|按名称、分类和阅读形式补充查阅|[全部资料目录](https://6sjsmmzn8z-cmd.github.io/daoyou-2026-yunnan/#library)|
|需要补课时|选择课程、教材和题库|[课程与教材指南](https://6sjsmmzn8z-cmd.github.io/daoyou-2026-yunnan/articles/courses.html)|

## 网站包含什么

- 251条可追溯来源，提供原始网址、年份提示和资料分类。
- **141份可直接阅读的PDF**：原始文件、从公开资料包中展开的内容、Office转换件以及复习册。包含重复来源去重，口径与最初104份原始PDF不同。
- 100道原创练习，支持按科目筛选、判断/单选/多选作答和答案解析。统计仅针对当前页面会话，不上传答题记录。
- 云南12景点的团型适配、讲解提纲和24道中文面试预测问答。
- 官方大纲、合同、法规、历年回忆题、模拟题、时政、思维导图与课程入口。

PDF可在浏览器查看；iPhone内嵌PDF无法翻页时，选择“在浏览器中打开完整PDF”。

## 压缩资料如何处理

当前分支不再提供ZIP或RAR文件；两份复习ZIP已展开成单独PDF，可读取的合同、样章和现场事项文件已转换为PDF。部分出版社内层课件受密码保护，网站显示“获取受限”并链接出版社原站，不声称已取得课件正文，也未尝试解密。

公开课程条目提供介绍和原站入口，不等于已取得离线视频或完整付费课程。原始网页存档在网站中以经过转义的纯文字展示，避免执行第三方脚本。

## 仓库结构

```text
docs/                   直接发布到GitHub Pages的静态网站
  index.html            中文阅读首页与完整资料目录
  quiz.html             在线训练
  viewer.html           PDF阅读页
  articles/             复习重点、面试提纲、题目和解析
  assets/               可直接查看的PDF
  archives/             已展开资料与受限课件说明
  sources/              来源介绍与纯文字存档
materials/              从公开资料包展开、转换的PDF
reports/                原创文稿与题目数据
official/               官方原文件
papers/                 回忆题、模拟题和复习PDF
pages/                  原网页档案（不作为网站发布目录）
text/                   提取文字与扫描OCR
scripts/                网站生成与检查工具
```

## 维护网站

使用Python 3和Pandoc重新生成页面，再提交到 `main`；GitHub Pages从 `main` 的 `/docs` 目录发布。

```bash
python3 scripts/build_site.py
python3 scripts/check.py
```

用户学习页面不需要Python、账号或下载压缩包。后续考务以官方最新通知与准考证为准。

## 来源与使用说明

[网站使用说明](https://6sjsmmzn8z-cmd.github.io/daoyou-2026-yunnan/about.html) · [原始资料目录](资源目录.md) · [来源表](资源总表.csv) · [资料权利说明](RIGHTS.md)

原创“预测”是依据大纲与有限样本制定的复习优先级，不是官方考题、未公开试卷或通过保证。回忆题、旧版笔记及OCR可能有错漏，引用与背诵前请核对官方原件。原始资料版权和使用条件属于原发布方，不重新授予开源许可。
