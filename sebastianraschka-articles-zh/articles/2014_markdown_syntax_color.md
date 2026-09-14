---
title: "Markdown 转 HTML 的 5 个步骤"
title_en: "Markdown to HTML in 5 Steps"
source: https://sebastianraschka.com/Articles/2014_markdown_syntax_color.html
crawled: 2026-09-06
translated: 2026-09-14
---

# Markdown 转 HTML 的 5 个步骤

> 原文：[Markdown to HTML in 5 Steps](https://sebastianraschka.com/Articles/2014_markdown_syntax_color.html) · Sebastian Raschka's Articles

在这个小教程中，我想通过 5 个简单的步骤向你展示：为博客文章添加代码语法高亮其实非常容易。

也有一些使用静态网站生成器（例如 [nikola](https://github.com/getnikola/nikola)）的更成熟的方案，但这里的重点在于简要介绍一下它的一般工作原理。

我在本教程中用作示例的所有文件都可以从 GitHub 仓库
[/rasbt/python\_reference/tutorials/markdown\_syntax\_highlighting](https://github.com/rasbt/python_reference/tree/master/tutorials/markdown_syntax_highlighting) 下载

## 更新：

[Webucator](https://www.webucator.com/catalog/python-training/)（一家 Python 培训课程提供商）的同仁们根据这篇博文制作了一个很棒的视频教程，用不到 4 分钟就把所有关键步骤讲得清清楚楚！快去 YouTube 上看看吧：

## 1 - 安装包

我们将要用到的两个包是

- [Python-Markdown](https://python-markdown.github.io/)
- [Pygments](http://pygments.org)

顾名思义，Python-Markdown 是我们将用来把 Markdown 转换为 HTML 的 Python 包。第二个库
Pygments 则用来为代码块添加语法高亮。
方便的是，这两个库都可以通过 `pip` 安装：

```python
    pip install markdown
```

以及

```python
pip install Pygments
```

（关于安装 Python-Markdown 包的其他方式，请参阅[文档](https://python-markdown.github.io/install/)）

## 2 - 编写 Markdown 文档

现在，让我们在任意一款（或我们最喜欢的）Markdown 编辑器里，编写一个包含一些 Python 代码块的简单 Markdown 文档。

```python
##This is a test

Code blocks must be indented by 4 whitespaces.
Python-Markdown has a auto-guess function which works
pretty well:

    print("Hello, World")
    # some comment
    for letter in "this is a test":
        print(letter)

In cases where Python-Markdown has problems figuring out which
programming language we use, we can also add the language-tag
explicitly. One way to do this would be:

    :::python
    print("Hello, World")

or we can highlight certain lines to
draw the reader's attention:

    :::python hl_lines="1 5"
    print("highlight me!")
    # but not me!
    for letter in "this is a test":
    print(letter)
    # I want to be highlighted, too!
```

[some\_markdown.md](https://github.com/rasbt/python_reference/blob/master/tutorials/markdown_syntax_highlighting/some_markdown.md)

注意，语法高亮并不只支持 Python，也支持其他编程语言。

比如以 C++ 为例：

```python
:::c++
#include <iostream>

int main()
{
    std::cout << "Hello, world!" << std::endl;
   return 0;
}
```

由于 Python-Markdown 中的 CodeHilite 扩展使用的是 Pygments，因此凡是[在这里列出](http://pygments.org/languages/)的编程语言目前都支持语法高亮。

## 3 - 将 Markdown 文档转换为 HTML

创建好 Markdown 文档之后，我们将直接从命令行使用 Python-Markdown 把它转换成
HTML 文档。

注意，我们也可以在 Python 脚本中把 Python-Markdown 作为模块导入，它自带一整套丰富的函数，
这些都[列在库参考文档](https://python-markdown.github.io/reference/)中。

将 Markdown 文档转换为 HTML 的基本命令行用法是：

```python
python -m markdown input.md > output.html
```

不过，由于我们想要为 Python 代码加上语法高亮，我们会使用 Python-Markdown 的 [CodeHilite
扩展](https://python-markdown.github.io/extensions/code_hilite/)，即在命令行上额外提供一个 `-x codehilite` 参数：

```python
python -m markdown -x codehilite some_markdown.md > body.html
```

这会生成 HTML body，其中的 Markdown 代码已转换为 HTML，并且 Python 代码块已经标注好以便进行语法高亮。

## 4 - 生成 CSS

如果现在打开我们在上一节中创建的
[body.html](https://github.com/rasbt/python_reference/blob/master/tutorials/markdown_syntax_highlighting/body.html)
文件，我们会发现其中的 Python 代码还没有被着色。

![Markdown syntax color mk syntax body html](https://sebastianraschka.com/images/blog/2014/markdown_syntax_color/mk_syntax_body_html.webp)

缺少的是用来为标注好的 Python 代码块添加颜色的 CSS 代码。不过，我们可以直接在命令行通过 `Pygments` 生成这样一个 CSS 文件。

```python
pygmentize -S default -f html > codehilite.css
```

注意，我们通常只需要创建一次
[codehilite.css](https://github.com/rasbt/python_reference/blob/master/tutorials/markdown_syntax_highlighting/codehilite.css)
文件，然后在我们通过 Python-Markdown 创建的所有 HTML 文件中插入一个链接，即可获得语法着色效果

## 5 - 插入到你的 HTML body 中

为了在我们转换得到的 HTML 文件中引入用于语法着色的
[codehilite.css](https://github.com/rasbt/python_reference/blob/master/tutorials/markdown_syntax_highlighting/codehilite.css)
文件链接，我们需要在 header 部分添加下面这一行。

`<link rel="stylesheet" type="text/css" href="./codehilite.css">`

现在，我们可以把由 Markdown 文档生成的 HTML
body（[body.html](https://github.com/rasbt/python_reference/blob/master/tutorials/markdown_syntax_highlighting/body.html)）
直接插入到我们最终的 HTML 文件（例如我们的博客文章模板）中。

```python
<!DOCTYPE html>
<html lang="en">

<head>
<meta charset="utf-8">
<link rel="stylesheet" type="text/css" href="./codehilite.css">
</head>

<body>

<-- converted HTML contents go here

</body>
</html>
```

[template.html](https://github.com/rasbt/python_reference/blob/master/tutorials/markdown_syntax_highlighting/template.html)

现在，如果我们在 Web 浏览器中打开
[final.html](https://github.com/rasbt/python_reference/blob/master/tutorials/markdown_syntax_highlighting/template.html)
文件，就能看到漂亮的 Python 语法高亮了。

![Markdown syntax color mk syntax final html](https://sebastianraschka.com/images/blog/2014/markdown_syntax_color/mk_syntax_final_html.webp)

## 实用链接：

- [Python Markdown 包
  文档](https://python-markdown.github.io/)
- [CodeHilite
  文档](https://python-markdown.github.io/extensions/code_hilite/)
- [pygments.org](http://pygments.org)
- Pygments [支持的语言](http://pygments.org/languages/)
