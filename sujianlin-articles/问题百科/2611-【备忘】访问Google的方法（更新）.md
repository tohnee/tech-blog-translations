---
title: "【备忘】访问Google的方法（更新）"
date: "2014-06-04"
author: "苏剑林"
category: "问题百科"
tags: ["网站", "帮助"]
url: "https://kexue.fm/archives/2611"
blog: "科学空间 | Scientific Spaces"
---

**6月13日：更新了一个新的可用IP，不知道能够用多久。**

以前大家顶多看到利用这个技巧访问facebook、youtube之类的网站，现在无奈到连Google都得用这个方法访问了。

近日，笔者发现直接输入<http://www.google.com.hk>无法访问Google搜索，要知道对于学术来说，没有Google是多么严重的事情，很多有用的学术资料，尤其是外文资料，都得靠Google来搜。主观性来说，在学术方面，百度不可能赶得上Google，望其项背都不可能。

上网搜索了一下，发现这并不是我一个人的问题，甚至都已经传出“谷歌全面退出中国？香港域名google.com.hk打不开！”之类的猜测了。当然，不管事实如何，我还是得使用Google，不能直接访问，就得另想办法。其实这方法也是老生常谈了。直接访问http://www.google.com.hk不行，但是可以直接访问某些Google的IP，比如[203.208.46.177](http://203.208.46.177)、[203.208.46.178](http://203.208.46.178)、[203.208.46.146](http://203.208.46.146)、[173.194.127.19](http://173.194.127.19)等。找到对应的IP后，修改C:\Windows\System32\drivers\etc目录下的hosts文件即可（在Windows 8中，不能直接用记事本打开修改，需要把这个文件复制到非系统目录中，修改后再复制回来，覆盖原文件。），在hosts下加入

> 173.194.127.19 www.google.com.hk
> 173.194.127.19 google.com.hk
> 173.194.127.19 www.google.com
> 173.194.127.19 google.com

这样就可以用<http://www.google.com.hk>访问Google了。不管搜索引擎如何变化，使用Google是不会变化的。
