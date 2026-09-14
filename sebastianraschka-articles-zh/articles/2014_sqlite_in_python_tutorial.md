---
title: "Python SQLite 全面指南"
title_en: "Python SQLite: A Thorough Guide"
source: https://sebastianraschka.com/Articles/2014_sqlite_in_python_tutorial.html
crawled: 2026-09-06
translated: 2026-09-14
---

# Python SQLite 全面指南

> 原文：[Python SQLite: A Thorough Guide](https://sebastianraschka.com/Articles/2014_sqlite_in_python_tutorial.html) · Sebastian Raschka's Articles

## 章节

我在本教程中使用的完整 Python 代码可以从我的 GitHub 仓库下载：
[https://github.com/rasbt/python\_reference/tree/master/sqlite3\_howto](https://github.com/rasbt/python_reference/tree/master/tutorials/sqlite3_howto)

---

## 连接 SQLite 数据库

我们在本教程中通篇使用的 sqlite3 是 Python 标准库的一部分，是操作 SQLite 数据库的一个简洁易用的接口：不需要服务器进程，不需要任何配置，也没有其他需要操心的障碍。

一般来说，在我们通过 Python 的 `sqlite3` 模块对 SQLite 数据库执行任何操作之前，唯一需要做的事情，就是打开与某个 SQLite 数据库文件的连接：

```python
import sqlite3
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()
```

其中数据库文件（`sqlite_file`）可以位于我们磁盘上的任意位置，例如：

```python
sqlite_file = '/Users/Sebastian/Desktop/my_db.sqlite'
```

一个方便之处在于：当我们第一次尝试连接某个数据库时，会自动创建一个新的数据库文件（`.sqlite` 文件）。不过要注意，此时它还不包含任何表。在下一节中，我们将通过一些示例代码，看看如何创建带有表、能够存储数据的新 SQLite 数据库文件。

作为「连接 SQLite 数据库文件」这一节的收尾，还有两个操作值得一提。当我们完成了对数据库文件的操作后，必须通过 `.close()` 方法关闭连接：

```python
conn.close()
```

而如果我们对数据库执行过发送查询以外的任何操作，就需要在关闭连接之前，先通过 `.commit()` 方法提交这些更改：

```python
conn.commit()
conn.close()
```

## 创建新的 SQLite 数据库

让我们看一段示例代码，它创建一个包含两个表的新 SQLite 数据库文件：其中一个表带 PRIMARY KEY 列，另一个不带（别担心，本节稍后会给出关于 PRIMARY KEY 的更多信息）。

```python
import sqlite3

sqlite_file = 'my_first_db.sqlite'    # name of the sqlite database file
table_name1 = 'my_table_1'  # name of the table to be created
table_name2 = 'my_table_2'  # name of the table to be created
new_field = 'my_1st_column' # name of the column
field_type = 'INTEGER'  # column data type

# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

# Creating a new SQLite table with 1 column
c.execute('CREATE TABLE {tn} ({nf} {ft})'\
        .format(tn=table_name1, nf=new_field, ft=field_type))

# Creating a second table with 1 column and set it as PRIMARY KEY
# note that PRIMARY KEY column must consist of unique values!
c.execute('CREATE TABLE {tn} ({nf} {ft} PRIMARY KEY)'\
        .format(tn=table_name2, nf=new_field, ft=field_type))

# Committing changes and closing the connection to the database file
conn.commit()
conn.close()
```

在以下地址下载该脚本：
[`create_new_db.py`](https://github.com/rasbt/python_reference/blob/master/tutorials/sqlite3_howto/code/create_new_db.py)

---

**提示：**
一个用来可视化和访问 SQLite 数据库的好用工具，是免费的 FireFox 插件
[SQLite Manager](https://lazierthanthou.github.io/sqlite-manager/)。
在整篇文章中，我都会使用这个工具，在相应代码小节的下方给出我们所创建的数据库结构的截图。

---

![Sqlite in python tutorial 1 sqlite3 init db](https://sebastianraschka.com/images/blog/2014/sqlite_in_python/1_sqlite3_init_db.webp)

使用上面的代码，我们创建了一个包含 2 个表的新 `.sqlite` 数据库文件。目前每个表都只有一列，其类型为 INTEGER。

---

**下面快速一览 SQLite 3 支持的全部数据类型：**

- INTEGER：有符号整数，最多 8 字节，具体取决于数值的大小。
- REAL：8 字节浮点数。
- TEXT：文本字符串，通常为 UTF-8 编码（取决于数据库编码）。
- BLOB：用于存储二进制数据的数据块（binary large object，二进制大对象）。
- NULL：NULL 值，表示缺失的数据或空单元格。

---

看完上面的列表，你或许已经注意到 SQLite 3 并没有专门的布尔（Boolean）数据类型。不过这并不是什么问题，因为我们可以干脆把 INTEGER 类型改用来表示布尔值（0 = false，1 = true）。

**关于 PRIMARY KEY 简要说几句：**

在上面的示例代码中，我们把第二个表中的那一列设为了 PRIMARY KEY。PRIMARY KEY 索引的好处在于：当我们把 PRIMARY KEY 列用作查询条件来访问表中的行时，可以获得显著的性能提升。每个表最多只能有 1 个 PRIMARY KEY（单列或多列），而且这一列中的值必须唯一！关于列索引的更多内容，请参见[后面的小节](#unique_indexes)。

## 添加新列

如果想向已有的 SQLite 数据库表添加一个新列，我们可以让每一行的单元格留空（NULL 值），也可以为每个单元格设置一个默认值——这对某些应用来说相当方便。
让我们看一段代码：

```python
import sqlite3

sqlite_file = 'my_first_db.sqlite'    # name of the sqlite database file
table_name = 'my_table_2'   # name of the table to be created
id_column = 'my_1st_column' # name of the PRIMARY KEY column
new_column1 = 'my_2nd_column'  # name of the new column
new_column2 = 'my_3nd_column'  # name of the new column
column_type = 'TEXT' # E.g., INTEGER, TEXT, NULL, REAL, BLOB
default_val = 'Hello World' # a default value for the new column rows

# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

# A) Adding a new column without a row value
c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
        .format(tn=table_name, cn=new_column1, ct=column_type))

# B) Adding a new column with a default row value
c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct} DEFAULT '{df}'"\
        .format(tn=table_name, cn=new_column2, ct=column_type, df=default_val))

# Committing changes and closing the connection to the database file
conn.commit()
conn.close()
```

下载脚本：
[add\_new\_column.py](https://github.com/rasbt/python_reference/blob/master/tutorials/sqlite3_howto/code/add_new_column.py)

![Sqlite in python tutorial 2 sqlite3 add col](https://sebastianraschka.com/images/blog/2014/sqlite_in_python/2_sqlite3_add_col.webp)

我们刚刚为 SQLite 数据库的 `my_table_2` 在 PRIMARY KEY 列 `my_1st_column` 旁边新增了 2 列（`my_2nd_column` 和 `my_3rd_column`）。
这两个新列的区别在于：`my_3rd_column` 用一个默认值（这里是 'Hello World'）做了初始化，对于该列下所有已存在的单元格，以及我们之后要往表中添加的每一行（只要我们不插入或更新为别的值），都会填入这个默认值。

## 插入与更新行

在已有的 SQLite 数据库表中插入和更新行——仅次于发送查询——大概是最常见的数据库操作了。结构化查询语言（SQL）提供了一个便捷的 `UPSERT` 功能，它基本上就是 UPDATE 和 INSERT 的合体：如果某个 PRIMARY KEY 值尚不存在，它就向数据库表中插入带该 PRIMARY KEY 值的新行；如果该 PRIMARY KEY 值已存在，则更新对应的行。遗憾的是，我们在这里使用的这个更紧凑的 SQLite 数据库实现并不支持这个便捷的语法。不过也有一些变通办法。但先让我们看看示例代码：

```python
import sqlite3

sqlite_file = 'my_first_db.sqlite'
table_name = 'my_table_2'
id_column = 'my_1st_column'
column_name = 'my_2nd_column'

# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

# A) Inserts an ID with a specific value in a second column
try:
    c.execute("INSERT INTO {tn} ({idf}, {cn}) VALUES (123456, 'test')".\
        format(tn=table_name, idf=id_column, cn=column_name))
except sqlite3.IntegrityError:
    print('ERROR: ID already exists in PRIMARY KEY column {}'.format(id_column))

# B) Tries to insert an ID (if it does not exist yet)
# with a specific value in a second column
c.execute("INSERT OR IGNORE INTO {tn} ({idf}, {cn}) VALUES (123456, 'test')".\
        format(tn=table_name, idf=id_column, cn=column_name))

# C) Updates the newly inserted or pre-existing entry            
c.execute("UPDATE {tn} SET {cn}=('Hi World') WHERE {idf}=(123456)".\
        format(tn=table_name, cn=column_name, idf=id_column))

conn.commit()
conn.close()
```

下载脚本：
[update\_or\_insert\_records.py](https://github.com/rasbt/python_reference/blob/master/tutorials/sqlite3_howto/code/update_or_insert_records.py)

![Sqlite in python tutorial 3 sqlite3 insert update](https://sebastianraschka.com/images/blog/2014/sqlite_in_python/3_sqlite3_insert_update.webp)

A) `INSERT` 和 B) `INSERT OR IGNORE` 的共同之处在于：当给定的 PRIMARY KEY 值在数据库表中尚不存在时，它们都会向数据库追加新行。然而，如果我们试图追加一个不唯一的 PRIMARY KEY 值，简单的 `INSERT` 会抛出 `sqlite3.IntegrityError` 异常——这个异常既可以用 try-except 语句来捕获（情形 A），也可以用 SQLite 的 `INSERT OR IGNORE` 调用来规避（情形 B）。如果我们想在 SQLite 中构造出 `UPSERT` 的等价物，这一点就相当有用了。例如，当我们想把一个数据集添加到已有的数据库表中，而这个数据集的 PRIMARY KEY 列里既有已存在的 ID、也有新的 ID 时。

创建唯一索引
———————–

与哈希表（hashtable）数据结构类似，索引（index）充当指向表中数据的直接指针，作用于某个特定列（即被索引的列）。例如，PRIMARY KEY 列默认就带有这样一个索引。索引的缺点是：该列中每一行的值都必须唯一。不过，如果条件允许，为某些列建立索引是推荐做法，而且相当有用，因为它会在数据检索时给我们带来显著的性能回报。
下面的示例代码展示了如何向 SQLite 数据库表中的已有列添加这样一个唯一索引。而如果我们日后决定向被索引的列插入非唯一的值，代码中也演示了一种便捷的删除该索引的方法。

```python
import sqlite3

sqlite_file = 'my_first_db.sqlite'    # name of the sqlite database file
table_name = 'my_table_2'   # name of the table to be created
id_column = 'my_1st_column' # name of the PRIMARY KEY column
new_column = 'unique_names'  # name of the new column
column_type = 'TEXT' # E.g., INTEGER, TEXT, NULL, REAL, BLOB
index_name = 'my_unique_index'  # name for the new unique index

# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

# Adding a new column and update some record
c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
        .format(tn=table_name, cn=new_column, ct=column_type))
c.execute("UPDATE {tn} SET {cn}='sebastian_r' WHERE {idf}=123456".\
        format(tn=table_name, idf=id_column, cn=new_column))

# Creating an unique index
c.execute('CREATE INDEX {ix} on {tn}({cn})'\
        .format(ix=index_name, tn=table_name, cn=new_column))

# Dropping the unique index
# E.g., to avoid future conflicts with update/insert functions
c.execute('DROP INDEX {ix}'.format(ix=index_name))

# Committing changes and closing the connection to the database file
conn.commit()
conn.close()
```

下载脚本：
[create\_unique\_index.py](https://github.com/rasbt/python_reference/blob/master/tutorials/sqlite3_howto/code/create_unique_index.py)

![Sqlite in python tutorial 4 sqlite3 unique index](https://sebastianraschka.com/images/blog/2014/sqlite_in_python/4_sqlite3_unique_index.webp)

查询数据库——选取行
————————————–

在了解了如何创建和修改 SQLite 数据库之后，是时候来做一些数据检索了。下面的代码演示了当行条目匹配某些条件时，我们如何检索它们在全部或部分列中的内容。

```python
import sqlite3

sqlite_file = 'my_first_db.sqlite'    # name of the sqlite database file
table_name = 'my_table_2'   # name of the table to be queried
id_column = 'my_1st_column'
some_id = 123456
column_2 = 'my_2nd_column'
column_3 = 'my_3rd_column'

# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

# 1) Contents of all columns for row that match a certain value in 1 column
c.execute('SELECT * FROM {tn} WHERE {cn}="Hi World"'.\
        format(tn=table_name, cn=column_2))
all_rows = c.fetchall()
print('1):', all_rows)

# 2) Value of a particular column for rows that match a certain value in column_1
c.execute('SELECT ({coi}) FROM {tn} WHERE {cn}="Hi World"'.\
        format(coi=column_2, tn=table_name, cn=column_2))
all_rows = c.fetchall()
print('2):', all_rows)

# 3) Value of 2 particular columns for rows that match a certain value in 1 column
c.execute('SELECT {coi1},{coi2} FROM {tn} WHERE {coi1}="Hi World"'.\
        format(coi1=column_2, coi2=column_3, tn=table_name, cn=column_2))
all_rows = c.fetchall()
print('3):', all_rows)

# 4) Selecting only up to 10 rows that match a certain value in 1 column
c.execute('SELECT * FROM {tn} WHERE {cn}="Hi World" LIMIT 10'.\
        format(tn=table_name, cn=column_2))
ten_rows = c.fetchall()
print('4):', ten_rows)

# 5) Check if a certain ID exists and print its column contents
c.execute("SELECT * FROM {tn} WHERE {idf}={my_id}".\
        format(tn=table_name, cn=column_2, idf=id_column, my_id=some_id))
id_exists = c.fetchone()
if id_exists:
    print('5): {}'.format(id_exists))
else:
    print('5): {} does not exist'.format(some_id))

# Closing the connection to the database file
conn.close()
```

下载脚本：
[selecting\_entries.py](https://github.com/rasbt/python_reference/blob/master/tutorials/sqlite3_howto/code/selecting_entries.py)

![Sqlite in python tutorial 4 sqlite3 unique index](https://sebastianraschka.com/images/blog/2014/sqlite_in_python/4_sqlite3_unique_index.webp)

如果我们使用 `.fetchall()` 方法，数据库查询会返回一个由元组组成的列表，其中每个元组代表一行条目。上面代码中 5 种不同情形的打印输出会是这样（注意我们这里的表只有 1 行）：

![Sqlite in python tutorial 6 sqlite3 print selecting rows](https://sebastianraschka.com/images/blog/2014/sqlite_in_python/6_sqlite3_print_selecting_rows.webp)

## 安全性与注入攻击

到目前为止，我们一直在使用 Python 的字符串格式化方法，把表名、列名之类的参数插入 `c.execute()` 函数。如果只是我们自己使用这个数据库，这样做没什么问题。然而，这会让数据库容易遭到注入攻击（injection attack）。例如，如果我们的数据库是某个 Web 应用的一部分，这会让黑客得以直接与数据库通信，从而绕过登录和密码验证并窃取数据。
为了防止这种情况，建议在 SQLite 命令中使用 `?` 占位符，而不是本教程一直在使用的 `%` 格式化表达式或 `.format()` 方法。
例如，在上面的[查询数据库——选取行](#querying)一节中，与其使用

```python
# 5) Check if a certain ID exists and print its column contents
c.execute("SELECT * FROM {tn} WHERE {idf}={my_id}".\
        format(tn=table_name, cn=column_2, idf=id_column, my_id=some_id))
```

我们更希望对查询的列值使用 `?` 占位符，并把要插入的变量（这里是 `123456`）作为元组放在 `c.execute()` 字符串的末尾。

```python
# 5) Check if a certain ID exists and print its column contents
c.execute("SELECT * FROM {tn} WHERE {idf}=?".\
        format(tn=table_name, cn=column_2, idf=id_column), (123456,))
```

不过，这种方法的问题在于它只对值有效，对列名或表名无效。那么，如果我们想保护自己免受注入攻击，字符串的其余部分该怎么办呢？简单的解决方案是：尽量避免在 SQLite 查询中使用变量；如果实在避不开，我们就应该用一个函数把变量所存内容中所有非字母数字的字符都剔除掉，例如

```python
def clean_name(some_var):
    return ''.join(char for char in some_var if char.isalnum())
```

## 日期与时间操作

SQLite 从 SQL 那里继承了便捷的日期和时间操作，这是结构化查询语言中我最喜欢的特性之一：它不仅允许我们以多种不同的格式插入日期和时间，还可以执行简单的 `+` 和 `-` 算术运算，例如查找 xxx 天前添加的条目。

```python
import sqlite3

sqlite_file = 'my_first_db.sqlite'    # name of the sqlite database file
table_name = 'my_table_3'   # name of the table to be created
id_field = 'id' # name of the ID column
date_col = 'date' # name of the date column
time_col = 'time'# name of the time column
date_time_col = 'date_time' # name of the date & time column
field_type = 'TEXT'  # column data type

# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

# Creating a new SQLite table with 1 column
c.execute('CREATE TABLE {tn} ({fn} {ft} PRIMARY KEY)'\
        .format(tn=table_name, fn=id_field, ft=field_type))

# A) Adding a new column to save date insert a row with the current date
# in the following format: YYYY-MM-DD
# e.g., 2014-03-06
c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}'"\
         .format(tn=table_name, cn=date_col))
# insert a new row with the current date and time, e.g., 2014-03-06
c.execute("INSERT INTO {tn} ({idf}, {cn}) VALUES('some_id1', DATE('now'))"\
         .format(tn=table_name, idf=id_field, cn=date_col))

# B) Adding a new column to save date and time and update with the current time
# in the following format: HH:MM:SS
# e.g., 16:26:37
c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}'"\
         .format(tn=table_name, cn=time_col))
# update row for the new current date and time column, e.g., 2014-03-06 16:26:37
c.execute("UPDATE {tn} SET {cn}=TIME('now') WHERE {idf}='some_id1'"\
         .format(tn=table_name, idf=id_field, cn=time_col))

# C) Adding a new column to save date and time and update with current date-time
# in the following format: YYYY-MM-DD HH:MM:SS
# e.g., 2014-03-06 16:26:37
c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}'"\
         .format(tn=table_name, cn=date_time_col))
# update row for the new current date and time column, e.g., 2014-03-06 16:26:37
c.execute("UPDATE {tn} SET {cn}=(CURRENT_TIMESTAMP) WHERE {idf}='some_id1'"\
         .format(tn=table_name, idf=id_field, cn=date_time_col))

# The database should now look like this:
# id         date           time        date_time
# "some_id1" "2014-03-06"   "16:42:30"  "2014-03-06 16:42:30"

# 4) Retrieve all IDs of entries between 2 date_times
c.execute("SELECT {idf} FROM {tn} WHERE {cn} BETWEEN '2013-03-06 10:10:10' AND '2015-03-06 10:10:10'".\
    format(idf=id_field, tn=table_name, cn=date_time_col))
all_date_times = c.fetchall()
print('4) all entries between ~2013 - 2015:', all_date_times)

# 5) Retrieve all IDs of entries between that are older than 1 day and 12 hrs
c.execute("SELECT {idf} FROM {tn} WHERE DATE('now') - {dc} >= 1 AND DATE('now') - {tc} >= 12".\
    format(idf=id_field, tn=table_name, dc=date_col, tc=time_col))
all_1day12hrs_entries = c.fetchall()
print('5) entries older than 1 day:', all_1day12hrs_entries)

# Committing changes and closing the connection to the database file
conn.commit()
conn.close()
```

下载脚本：
[date\_time\_ops.py](https://github.com/rasbt/python_reference/blob/master/tutorials/sqlite3_howto/code/date_time_ops.py)

![Sqlite in python tutorial 5 sqlite3 date time](https://sebastianraschka.com/images/blog/2014/sqlite_in_python/5_sqlite3_date_time.webp)

下面这些返回当前时间和日期的函数真的非常方便：

---

```python
DATE('now') # returns current date, e.g., 2014-03-06
TIME('now') # returns current time, e.g., 10:10:10
CURRENT_TIMESTAMP # returns current date and time, e.g., 2014-03-06 16:42:30
#  (or alternatively: DATETIME('now'))
```

---

下面的截图展示了我们所用代码的打印输出，这些代码分别用

```python
BETWEEN '2013-03-06 10:10:10' AND '2015-03-06 10:10:10'
```

查询位于指定日期区间内的条目，并用

```python
WHERE DATE('now') - some_date
```

查询早于 1 天的条目。
注意，这里我们不必提供完整的时间戳，同样的语法也适用于单纯的日期或单纯的时间。

![Sqlite in python tutorial 5 sqlite3 date time 2](https://sebastianraschka.com/images/blog/2014/sqlite_in_python/5_sqlite3_date_time_2.webp)

### 2014 年 3 月 16 日更新：

如果我们想计算两个 `DATETIME()` 时间戳之间相隔的小时数，可以使用方便的 `STRFTIME()` 函数，像这样

```python
SELECT (STRFTIME('%s','2014-03-14 14:51:00') - STRFTIME('%s','2014-03-16 14:51:00'))
 / -3600
```

在上面这个特定例子中，它会计算出两个日期之间相差的小时数（此处为 `48`）。
而要计算当前 `DATETIME` 与给定 `DATETIME` 字符串之间相差的小时数，我们可以使用下面的 SQLite 语法：

```python
SELECT (STRFTIME('%s',DATETIME('now')) - STRFTIME('%s','2014-03-15 14:51:00')) / 3600
```

## 获取列名

在前两节中，我们已经看到了如何查询 SQLite 数据库的数据内容。现在让我们来看看如何获取它的元数据（这里是列名）：

```python
import sqlite3

sqlite_file = 'my_first_db.sqlite'
table_name = 'my_table_3'

# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

# Retrieve column information
# Every column will be represented by a tuple with the following attributes:
# (id, name, type, notnull, default_value, primary_key)
c.execute('PRAGMA TABLE_INFO({})'.format(table_name))

# collect names in a list
names = [tup[1] for tup in c.fetchall()]
print(names)
# e.g., ['id', 'date', 'time', 'date_time']

# Closing the connection to the database file
conn.close()
```

下载脚本：
[get\_columnnames.py](https://github.com/rasbt/python_reference/blob/master/tutorials/sqlite3_howto/code/get_columnnames.py)

![Sqlite in python tutorial 7 sqlite3 get colnames 1](https://sebastianraschka.com/images/blog/2014/sqlite_in_python/7_sqlite3_get_colnames_1.webp)

由于我们没有为 `my_table_3` 创建 PRIMARY KEY 列，SQLite 会自动提供一个带索引的 `rowid` 列，其值为唯一递增的整数，在本例中它会被我们忽略。对表使用 `PRAGMA TABLE_INFO()` 函数会返回一个元组列表，其中每个元组都包含表中每一列的如下信息：`(id, name, type, notnull, default_value, primary_key)`。
所以，要得到表中每一列的名称，我们只需取返回列表中每个元组的第 2 个值，做法是在调用 `PRAGMA TABLE_INFO()` 之后执行

```python
names = [tup[1] for tup in c.fetchall()]
```

如果我们现在打印变量 `names` 的内容，输出会是这样：

![Sqlite in python tutorial 7 sqlite3 get colnames 2](https://sebastianraschka.com/images/blog/2014/sqlite_in_python/7_sqlite3_get_colnames_2.webp)

## 打印数据库概览

我希望前面的几节已经覆盖了 SQLite 数据库操作的大部分基础知识，到现在为止，我们应该已经装备齐全，可以在 Python 中使用 SQLite 干一些正经的活了。
作为本教程的收尾，照例来一句「压轴登场的往往最重要」（last but not least），我提供一个便捷的脚本，用于打印 SQLite 数据库表的漂亮概览：

```python
import sqlite3

def connect(sqlite_file):
    """ Make connection to an SQLite database file """
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    return conn, c

def close(conn):
    """ Commit changes and close connection to the database """
    # conn.commit()
    conn.close()

def total_rows(cursor, table_name, print_out=False):
    """ Returns the total number of rows in the database """
    cursor.execute('SELECT COUNT(*) FROM {}'.format(table_name))
    count = cursor.fetchall()
    if print_out:
        print('\nTotal rows: {}'.format(count[0][0]))
    return count[0][0]

def table_col_info(cursor, table_name, print_out=False):
    """ Returns a list of tuples with column informations:
    (id, name, type, notnull, default_value, primary_key)
    """
    cursor.execute('PRAGMA TABLE_INFO({})'.format(table_name))
    info = cursor.fetchall()

    if print_out:
        print("\nColumn Info:\nID, Name, Type, NotNull, DefaultVal, PrimaryKey")
        for col in info:
            print(col)
    return info

def values_in_col(cursor, table_name, print_out=True):
    """ Returns a dictionary with columns as keys
    and the number of not-null entries as associated values.
    """
    cursor.execute('PRAGMA TABLE_INFO({})'.format(table_name))
    info = cursor.fetchall()
    col_dict = dict()
    for col in info:
        col_dict[col[1]] = 0
    for col in col_dict:
        c.execute('SELECT ({0}) FROM {1} '
                  'WHERE {0} IS NOT NULL'.format(col, table_name))
        # In my case this approach resulted in a
        # better performance than using COUNT
        number_rows = len(c.fetchall())
        col_dict[col] = number_rows
    if print_out:
        print("\nNumber of entries per column:")
        for i in col_dict.items():
            print('{}: {}'.format(i[0], i[1]))
    return col_dict

if __name__ == '__main__':

    sqlite_file = 'my_first_db.sqlite'
    table_name = 'my_table_3'

    conn, c = connect(sqlite_file)
    total_rows(c, table_name, print_out=True)
    table_col_info(c, table_name, print_out=True)
    # next line might be slow on large databases
    values_in_col(c, table_name, print_out=True)

    close(conn)
```

下载脚本：
[`print_db_info.py`](https://github.com/rasbt/python_reference/blob/master/tutorials/sqlite3_howto/code/print_db_info.py)

![Sqlite in python tutorial 8 sqlite3 print db info 1](https://sebastianraschka.com/images/blog/2014/sqlite_in_python/8_sqlite3_print_db_info_1.webp)

![Sqlite in python tutorial 8 sqlite3 print db info 2](https://sebastianraschka.com/images/blog/2014/sqlite_in_python/8_sqlite3_print_db_info_2.webp)

## 总结

真心希望这篇教程能帮助你顺利入门用 Python 进行 SQLite 数据库操作。最近我大量使用 `sqlite3` 模块，它已经进入了我的大多数较大规模数据分析程序之中。
目前，我正在开发一款新的药物筛选软件，需要为约 1300 万个化合物存储 3D 结构和其他功能数据，SQLite 已经成为我这个程序中无比宝贵的一部分，让我能够快速地存储、查询、分析和共享数据。
另一个在 Python 中使用 `sqlite3` 的较小项目是 smilite——一个从免费的 ZINC 在线数据库检索并比较化合物 SMILE 字符串的模块。如果你有兴趣，可以在这里查看：<https://github.com/rasbt/smilite>。
