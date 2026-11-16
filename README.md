# 2026 导考资料库 · 云南昆明中文类

## ⚠️ AI／Agent 先读：个人学习进度与四科分类记忆

**接手辅导请先读 [AGENT必读：学习记忆与续练规则](AGENT必读_学习记忆与续练规则.md)，不要重问已答对的具体考点。**

- [四科分类记忆总入口：茶叶、古籍、法规、业务与全国地方知识](study/README.md)
- [2026-11-15 答题记录与六个待巩固点](study/2026-11-15_答题记录.md) · [机器可读进度](study/progress.json)

此区是当前学习者的个体记录，复习材料中未测试的条目不自动视为已掌握。

**在线阅读网站：https://6sjsmmzn8z-cmd.github.io/daoyou-2026-yunnan/**

网站与仓库均公开，无须登录。全部页面导航、目录和学习指引使用中文，支持手机浏览。资料截点：2026年11月14日。

## 建议学习顺序

|顺序|内容|在线入口|
|---|---|---|
|第一步|确认2026考试规则、重点与最后一周计划|[考试与复习重点](https://6sjsmmzn8z-cmd.github.io/daoyou-2026-yunnan/articles/priorities.html)|
|第二步|按四科辨析条件与易混点|[100道原创进阶训练](https://6sjsmmzn8z-cmd.github.io/daoyou-2026-yunnan/quiz.html)|
|第三步|准备12景点、对应团型及24道问答|[云南中文面试](https://6sjsmmzn8z-cmd.github.io/daoyou-2026-yunnan/articles/yunnan.html)|
|第四步|按名称、分类和阅读形式补充查阅|[全部资料目录](https://6sjsmmzn8z-cmd.github.io/daoyou-2026-yunnan/#library)|
|需要补课时|选择课程、教材和题库|[课程与教材指南](https://6sjsmmzn8z-cmd.github.io/daoyou-2026-yunnan/articles/courses.html)|

## 网站包含什么

- 251条可追溯来源，提供原始网址、年份提示和资料分类。
- **141份可直接阅读的PDF**：原始文件、从公开资料包中展开的内容、Office转换件以及复习册。包含重复来源去重，口径与最初104份原始PDF不同。
- 100道原创进阶练习：60单选、40多选，替换低区分度旧题；合理近似干扰项配逐题解析，支持科目／题型筛选和隐藏本页已答对题。统计仅针对当前页面会话，不上传答题记录。
- [四科分类记忆网页](https://6sjsmmzn8z-cmd.github.io/daoyou-2026-yunnan/study/index.html)与[Agent先读网页](https://6sjsmmzn8z-cmd.github.io/daoyou-2026-yunnan/study/agent.html)，同步个人答题证据和待巩固点；[题库修订说明](reports/06_训练题质量修订说明.md)。
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
study/                  四科分类记忆、个人答题记录和结构化进度
official/               官方原文件
papers/                 回忆题、模拟题和复习PDF
pages/                  原网页档案（不作为网站发布目录）
text/                   提取文字与扫描OCR
scripts/                网站生成与检查工具
```

## 维护网站

使用Python 3和Pandoc重新生成页面，再提交到 `main`；GitHub Pages从 `main` 的 `/docs` 目录发布。

```bash
python3 scripts/build_practice.py --book
python3 scripts/build_site.py
python3 scripts/check.py
```

用户学习页面不需要Python、账号或下载压缩包。后续考务以官方最新通知与准考证为准。

题库JSON为唯一数据源。修改题目或四科表后先同步下载复习册（`--book` 另需PyMuPDF），再构建网页；只改网页外观时可以直接运行网站构建。

## 来源与使用说明

[网站使用说明](https://6sjsmmzn8z-cmd.github.io/daoyou-2026-yunnan/about.html) · [原始资料目录](资源目录.md) · [来源表](资源总表.csv) · [资料权利说明](RIGHTS.md)

原创“预测”是依据大纲与有限样本制定的复习优先级，不是官方考题、未公开试卷或通过保证。回忆题、旧版笔记及OCR可能有错漏，引用与背诵前请核对官方原件。原始资料版权和使用条件属于原发布方，不重新授予开源许可。
