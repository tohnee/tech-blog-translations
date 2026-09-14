---
title: "IPython Notebook 目录与内部链接"
title_en: "IPython Notebook Table of Contents"
source: https://sebastianraschka.com/Articles/2014_ipython_internal_links.html
crawled: 2026-09-06
translated: 2026-09-14
---

# IPython Notebook 目录与内部链接

> 原文：[IPython Notebook Table of Contents](https://sebastianraschka.com/Articles/2014_ipython_internal_links.html) · Sebastian Raschka's Articles

很多人问过我，我是如何为 GitHub 上的 IPython Notebook 和 Markdown 文档创建带内部链接的目录的。其实这并没有什么（IPython）魔法，只需要一点点 HTML 而已，不过我想，把这篇小小的 how-to 教程写出来或许还是值得的。

你可以在我的 GitHub 仓库中找到并下载许多示例 IPython Notebook：

[python\_reference](https://github.com/rasbt/python_reference)。
![Ipython internal links ipython links ex](https://sebastianraschka.com/images/blog/2014/ipython_internal_links/ipython_links_ex.webp)

举个例子，[点击这个链接](#bottom)可以跳转到页面底部。

## 创建内部链接的两个组件

那么，它究竟是怎么工作的呢？基本上，你只需要这两个组件：

1. 目标位置（destination）
2. 指向目标位置的内部超链接

![Ipython internal links ipython links overview](https://sebastianraschka.com/images/blog/2014/ipython_internal_links/ipython_links_overview.webp)

### 1. 目标位置

要定义目标位置（即你想跳转到的页面上的小节或单元格），你只需插入一个空的 HTML 锚点（anchor）标签，并给它一个 **`id`**，
例如 **`<a id='the_destination'></a>`**

在 IPython Notebook 中以 Markdown 渲染时，这个锚点标签是不可见的。
注意，如果我们使用 **`name`** 属性而不是 **`id`** 属性，也同样可行；但由于 **`name`** 属性已不再被 HTML5 支持，我建议直接使用 **`id`** 属性，而且它敲起来也更简短。

### 2. 内部超链接

现在，我们要为刚创建的 **`<a id='the_destination'></a>`** 锚点标签创建超链接。
我们既可以用古老而经典的 HTML 写法——在名称前面加上一个以井号（`#`）表示的片段标识符（fragment identifier），
例如
**`<a href='#the_destination'>Link to the destination'</a>`**

或者，我们也可以直接使用稍微更方便一点的 Markdown 语法：
**`[Link to the destination](#the_destination)`**

**就这么简单！**

## 再多说一句建议

当然，比较合理的做法是把空锚点标签放在目录中每个包含标题的单元格的紧上方。
例如

```python
<a id='section2'></a>
###Section 2
some text ...
```

在很长一段时间里我都是这么做的……直到我发现，当你把 IPython Notebook 转换成 HTML 时（例如为了通过打印预览选项进行打印），这样写会导致 Markdown 无法被正确渲染。

它不会被渲染成

### Section 2

而是会被渲染成

`###Section 2`

这显然不是我们想要的（注意，在 IPython Notebook 中它看起来是正常的，但在转换后的 HTML 版本中就不正常了）。所以，我最喜欢的补救办法是把 `id` 锚点标签放到该小节上方一个单独的单元格里，为了更美观，最好再加上几个换行。

![Ipython internal links ipython links format](https://sebastianraschka.com/images/blog/2014/ipython_internal_links/ipython_links_format.webp)

### 解决方案 1：把 id 锚点标签放在单独的单元格里

![Ipython internal links ipython links remedy](https://sebastianraschka.com/images/blog/2014/ipython_internal_links/ipython_links_remedy.webp)

### 解决方案 2：使用标题单元格

而指向这个「标题单元格」的超链接锚点，就是把「标题单元格」的文本内容用连字符连接起来。例如：

![Ipython internal links ipython table header](https://sebastianraschka.com/images/blog/2014/ipython_internal_links/ipython_table_header.webp)

`[link to another section](#Another-section)`

[[点击这个链接，跳转到页面顶部](#top)]

你看不见它，但这个单元格里、这段文字的正下方，有一个 `<a id='bottom'></a>` 锚点标签。
