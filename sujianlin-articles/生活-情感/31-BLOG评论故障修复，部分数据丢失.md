---
title: "BLOG评论故障修复，部分数据丢失"
date: "2009-07-23"
author: "苏剑林"
category: "生活/情感"
tags: ["网站", "故障", "数据"]
url: "https://kexue.fm/archives/31"
blog: "科学空间 | Scientific Spaces"
---

**今天一早起来，兴致勃勃地发表着日志，却发现评论用不了了，侧边栏也故障了**。
如图：

[![](https://kexue.fm/usr/uploads/2009/07/20090723132232.JPG)](https://kexue.fm/usr/uploads/2009/07/20090723132232.JPG "点击查看原图")

**紧接着，尝试更新缓存、重新安装、换空间，都无法解决。**

于是只好到官方网站求助，谁知道发现，**只要删除cookies就好了**（真冤枉，害我丢失了数据）

**为了一劳永逸，按以下方式进行了修改：**

**解决方法：**
打开class/cls_article.asp找到

> Ts_Content = Split(Split(Split(Ts, "|-|")(1), "|\$|")(1), "|+|")(0)

改成

> Ts_Content = Split(Split(Split(Ts, "|-|")(1), "|\$|")(0), "|+|")(0)

试验过，删除这行也没有什么影响。
