---
title: "SQLite 数据库"
title_en: "SQLite"
source: https://sebastianraschka.com/Articles/2013_sqlite_database.html
crawled: 2026-09-06
translated: 2026-09-14
---

# SQLite 数据库

> 原文：[SQLite](https://sebastianraschka.com/Articles/2013_sqlite_database.html) · Sebastian Raschka's Articles

我的新项目让我面临一项任务：筛选一大堆海量的文本格式数据文件，每个文件都有数十亿条条目。
而且今后我还必须反复、频繁地检索这些数据。因此，我不禁想找一个比暴力扫描更好的方案——总不能每次都逐行扫过约 20 个各自包含约 60 亿条目、只有 1 列的独立文本文件吧。

## 概览

![Sqlite3 database database input txtfiles](https://sebastianraschka.com/images/blog/2013/sqlite3_database/database_input_txtfiles.webp)

归根结底，我想要的是一个统一的数据库结构，把所有这些列合并到一起——这些列代表的是目前分别列在那些独立文本文件中的不同特征。这个数据库应当可扩展，而且我的工作流程要求我能够高效地把具有交集特征的条目抽取出来，以做进一步计算。

于是我四处搜寻，没过多久就偶然发现了这个超棒的 [sqlite3](https://docs.python.org/3/library/sqlite3.html) Python 模块，专门用于操作 SQLite 数据库结构。幸运的是，你不必成为 SQL 专家就能上手。sqlite3 模块的文档写得非常出色，可以作为你很好的入门起点：
[http://docs.python.org/2/library/sqlite3.html](https://docs.python.org/2/library/sqlite3.html)

![Sqlite3 database sqlite logo](https://sebastianraschka.com/images/blog/2013/sqlite3_database/sqlite_logo.webp)

SQLite 是一个开源的数据库引擎，非常适合较小规模的工作团队，因为它是单个本地存储的数据库文件，不需要任何服务器基础设施。

此外，SQLite 可以在所有常见的操作系统上运行，并且同时兼容 32 位和 64 位机器。大量应用都让你能够使用强大的 SQL 语法，而且 SQLite 一直以非常可靠著称——Google、Mozilla、Adobe、Apple、Microsoft 等知名公司都在使用它。我能找到的唯一缺点是每个数据库文件有 140 TB 的大小限制，不过「外键」（foreign keys）允许在不同数据库文件之间进行交叉查询，所以即便是这个大小限制也不必太担心。

如果你想进一步了解 SQLite，可以访问它们的网站：<http://www.sqlite.org>。

## sqlite3 概要

在下面这一节中，我会给出一些代码，展示在 Python 中使用 sqlite3 模块有多简单。我添加了注释，希望让代码尽量做到不言自明。在代码示例之后，我还准备了一些有趣的基准测试，来演示 SQL 查询的效率。

### 创建 SQLite 数据库

```python
import sqlite3

# create new db and make connection
conn = sqlite3.connect('my_db.db')
c = conn.cursor()

# create table
c.execute('''CREATE TABLE my_db
 (id TEXT, my_var1 TEXT, my_var2 INT)''')

# insert one row of data
c.execute("INSERT INTO my_db VALUES ('ID_2352532','YES', 4)")

# insert multiple lines of data
multi_lines =[ ('ID_2352533','YES', 1),
               ('ID_2352534','NO', 0),
               ('ID_2352535','YES', 3),
               ('ID_2352536','YES', 9),
               ('ID_2352537','YES', 10)
              ]
c.executemany('INSERT INTO my_db VALUES (?,?,?)', multi_lines)

# save (commit) the changes
conn.commit()

# close connection
conn.close()
```

***注意：** 正如一位细心的读者在下方评论区指出的，如果相关标识符只由数字组成，那么使用整数而非字符串作为 ID 会提高计算效率。在我为这个例子所选的情形（ID\_2352533、ID\_2352534……）中，这些 ID 看起来遵循相同的模式："ID\_" + 数字。因此，与其原样使用，不如在把它插入数据库之前先转换成整数，例如用一个简单的 Python 表达式：int("ID\_2352533"[3:])

### 更新已有数据库

```python
import sqlite3

# make connection to existing db
conn = sqlite3.connect('my_db.db')
c = conn.cursor()

# update field
t = ('NO', 'ID_2352533', )
c.execute("UPDATE my_db SET my_var1=? WHERE id=?", t)
print "Total number of rows changed:", conn.total_changes

# delete rows
t = ('NO', )
c.execute("DELETE FROM my_db WHERE my_var1=?", t)
print "Total number of rows deleted: ", conn.total_changes

# add column
c.execute("ALTER TABLE my_db ADD COLUMN 'my_var3' TEXT")

# save changes
conn.commit()

# print column names
c.execute("SELECT * FROM my_db")
col_name_list = [tup[0] for tup in c.description]
print col_name_list

# close connection
conn.close()
```

### 查询 SQLite 数据库

```python
import sqlite3

# open existing database
conn = sqlite3.connect('my_db.db')

c = conn.cursor()

# print all lines ordered by integer value in my_var2
for row in c.execute('SELECT * FROM my_db ORDER BY my_var2'):
    print row

# print all lines that have "YES" as my_var1 value
# and have an integer value <= 7 in my_var2
t = ('YES',7,)
for row in c.execute('SELECT * FROM my_db WHERE my_var1=? AND my_var2 <= ?', t):
    print row

# print all lines that have "YES" as my_var1 value
# and have an integer value <= 7 in my_var2
t = ('YES',7,)
c.execute('SELECT * FROM my_db WHERE my_var1=? AND my_var2 <= ?', t)
rows = c.fetchall()
for r in rows:
    print r

# close connection
conn.close()
```

## 基准测试

在我摆弄了一番 sqlite3 模块之后，下一个重要问题是：SQLite 到底有多快？为了做一些简单的速度对比，我搭建了一个 610 万行（75 MB）的示例文件，来测量以下三种情形的 CPU 时间：
**a) 用简单的 Python 代码逐行读取文本文件
b) 读取文本文件来创建 SQLite 数据库
c) 查询整个数据库。**

我只是想看看，用查询数据库（c）来代替每次从头读取整个文件（a），能带来多大的收益。我还想知道，从头构建这个 SQLite 数据库需要多长时间。注意，这只是一个使用单个单列文本文件的简化示例。而在实际应用中，我要么得扫描 20 个各有 60 亿行的文件，要么得查询一个拥有 60 亿条条目、21 列的数据库。

下面是我用来测量上述 a)、b)、c) 三种场景 CPU 时间的 3 段简短 Python 脚本。

### a) read\_lines.py

```python
import time

start_time = time.clock()

lines = 0
    with open("feature1.txt", "rb") as fileobj:
    for line in fileobj:
    lines += 1

elapsed_time = time.clock() - start_time
print "Time elapsed: {} seconds".format(elapsed_time)
print "Read {} lines".format(lines)
```

### b) create\_sqlite\_db.py

```python
import sqlite3
import time

start_time = time.clock()

conn = sqlite3.connect('my_db1.db')
c = conn.cursor()

c.execute('''CREATE TABLE my_db1 (id TEXT, feature1 TEXT, feature2 INT)''')

lines = 0
lst = list()

with open("feature1.txt", "rb") as myfile:
    for line in myfile:
    line = line.strip()
    lst.append((line, "Yes", None))
    lines += 1
c.executemany("INSERT INTO my_db1 VALUES (?,?,?)", lst)

conn.commit()
conn.close()

elapsed_time = time.clock() - start_time
print "Time elapsed: {} seconds".format(elapsed_time)
print "Read {} lines".format(lines)
```

### c) query\_sqlite\_db.py

```python
import sqlite3
import time

start_time = time.clock()

conn = sqlite3.connect('my_db1.db')
c = conn.cursor()

lines = 0
lst = list()
t = ('YES',)
for row in c.execute('SELECT * FROM my_db1 WHERE feature1=?', t):
    lst.append(row)
    lines += 1

conn.close()

elapsed_time = time.clock() - start_time
print "Time elapsed: {} seconds".format(elapsed_time)
print "Read {} lines".format(lines)
```

## 结果与结论

正如你在下图中看到的那样，结果着实令人印象深刻，SQLite 没有让人失望。

![Sqlite3 database sqlite3 benchmark1.001](https://sebastianraschka.com/images/blog/2013/sqlite3_database/sqlite3_benchmark1.001.webp)

（在我的机器上）Python 逐行读完 600 万行文本（第一列）只需要不超过 20 秒——这还是在没有任何额外计算或分析的情况下。而把这些行添加到 SQLite 数据库时，CPU 时间会增加三分之一（第二列）。逐行读取文本文件无疑比我预想的要快，但 sqlite3 让普通 Python 代码黯然失色：查询我整个 600 万条目的数据库并把它们全部取出来，只需要大约 1 秒（第三列）！这大约比用 Python 代码扫描纯文本文件快 20 倍（记住，实际场景中我有 20 个文本文件，每个都比这个示例文件大 1000 倍）。

如果做一个非常简化的对比：假设 Python 遍历每个真实数据集文件需要约 5 分钟，而这样的文件我有 20 个。如果我要对具有交集特征的数据进行交叉比对，很容易就会花掉超过 2 小时的 CPU 时间，而且每次建立新的筛选流程时都得把这一过程重复一遍。但如果我有了自己的 SQLite 数据库，同样的事情不到 1 分钟就能完成。所以对于每天都要进行的筛选来说，到第一周结束时，对比就已经是 10 小时的 Python 逐行筛选对阵 5 分钟的 SQL 查询了。我觉得这简直太棒了。
