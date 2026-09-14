---
title: "OpenEye 子结构叠合"
title_en: "OpenEye Substructure Alignments"
source: https://sebastianraschka.com/Articles/2014_openeye_alignments_overlays.html
crawled: 2026-09-06
translated: 2026-09-14
---

# OpenEye 子结构叠合

> 原文：[OpenEye Substructure Alignments](https://sebastianraschka.com/Articles/2014_openeye_alignments_overlays.html) · Sebastian Raschka's Articles

这是一份快速指南，介绍如何使用 OpenEye 软件的命令行工具，基于子结构匹配把目标分子叠合（align）到查询分子上，以及如何从两组低能构象中找出最佳的分子叠加（overlay）。

---

## 章节

---

## 使用 OpenEye OEChem RMSD 进行子结构叠合

### 任务：

我们想将一组分子叠合到一个参照子结构上（这与「常规」的整分子对整分子的叠合不同，后者的重点在于使整个分子结构上的原子距离最小化）。

**环境要求：**

- OpenEye OEChem RMSD 叠合工具
- 蛋白质结构可视化工具（例如 PyMOL）
- Python 3.x - `.mol2` 或 `.pdb` 格式的参照分子 - 以 multi-mol2 或单个 mol2 文件形式存在的目标分子结构。

### 1) 通过 PyMOL 提取子结构

在 PyMOL 中打开参照分子的 `.mol2` 或 `.pdb` 文件，提取出你想叠合到查询分子上的那个子结构（保存为 PDB 文件）。在本例中，我从 ZINC 数据库（<http://zinc.docking.org/substance/80135621>）中随机挑选了一个含甾环的结构，这里我们想专门聚焦于甾环环体本身的叠合。

**PyMOL 操作流程：**

1. 顶部面板：Mouse（鼠标） -> Selection Mode（选择模式） -> Atoms（原子）
2. 点击感兴趣的原子，把它们标记为选中
3. 在新建的选区上：Action（操作） -> copy to object（复制为对象）
4. 将子结构保存为 PDB 文件：File（文件） -> Save Molecule…（保存分子…）

#### 原始参照分子（ZINC80135621）：

![Openeye alignments overlays reference molecule](https://sebastianraschka.com/images/blog/2014/openeye_alignments_overlays/reference_molecule.webp)

![Openeye alignments overlays pymol copy substructure](https://sebastianraschka.com/images/blog/2014/openeye_alignments_overlays/pymol_copy_substructure.webp)

#### 得到的参照子结构：

![Openeye alignments overlays reference substructure](https://sebastianraschka.com/images/blog/2014/openeye_alignments_overlays/reference_substructure.webp)

### 2) 将子结构转换为 SMILES 字符串

我推荐使用 <http://cactus.nci.nih.gov/translate/> 上的免费在线 SMILES 转换器，上传你转换好的 PDB 格式子结构，以获得对应的 SMILES 字符串。

或者，你也可以通过 ZINC 网站（<http://zinc.docking.org/search/structure>）上的「Search Structure」分子编辑器来绘制子结构，从而获得该子结构的 SMILES 字符串。在这种情况下，你就不需要再用 PyMOL 从主分子中提取子结构了。对于像这个甾环构造一样简单的子结构来说，这可能也是更方便的做法。

### 3) 运行 OpenEye 的 RMSD 工具

运行 OpenEye 的 OEChem RMSD 工具，基于提取出的子结构将目标分子叠合到参照分子上。叠合后的分子对将被写入一个新文件。OEChem RMSD 工具典型用法的命令行语法如下：

```python
/soft/linux64/openeye/.../oechem-utilities/rmsd\
-in /home/.../ query.mol2\
-ref ~/Desktop/reference_molecule.mol2\
-overlay\
-out /home/.../output.mol2\
-automorph false\
-smarts C1CCC2C(C1)CCC3C4CCCC4CCC23
```

关于各个参数的**更多细节**（来自
`.../oechem-utilities/rmsd --help`）：

```python
rmsd -in <filename> -ref <reference filename>

Options:
 -automorph (default false): assign best atom association. By setting
  this option to true, rmsd will ignore atom names and orders present in the
  file and will use structural and chemical information to make the best
  matches.  This should fix the problem of abnormally high RMSD values for
  symmetric molecules/functional groups that have been rotated.

 -heavyonly (default true): ignores hydrogens in rmsd calculation

 -overlay (default true): performs a least squares fit and superimposes
  the molecules prior to making the RMSD calculation.

 -origconfout : output original conformation too

 -out : output file name

 -refout : output reference mol

 -smarts : rmsd of corresponding matched atoms only
```

### 4) 用于自动化流程的脚本

#### 4 a) 拆分 multi-mol2 文件的 Python 脚本

如果你的目标分子存放在一个 multi-mol2 文件中，可以使用 Python 脚本
[`split_multimol2.py`](https://github.com/rasbt/protein-science/blob/master/tutorials/substructure_alignment/Scripts/split_multimol2.py)
把它拆分成一个个单独的 mol2 文件：

```python
USAGE: python3 multimol2.mol2 output_directory
```

#### 4 b) Python subprocess.call() 封装脚本

要在各个单独的 mol2 文件上自动执行 RMSD 子结构叠合，可以使用脚本
[`multimol2_rmsd_align.py`](https://github.com/rasbt/protein-science/blob/master/tutorials/substructure_alignment/Scripts/multimol2_rmsd_align.py)，你只需要修改其中 OpenEye RMSD 可执行文件的路径即可。

```python
USAGE: python3 mmol2_rmsd_align.py input_dir/ output_dir/ ref.mol2 smiles_string
```

#### 4 c) 拼接结果

最后，你可以把得到的叠合结果重新拼接成单个 multi-mol2 文件，以便进一步的分析和可视化：

```python
cat mol2_dir/*.mol2 > my_multimol2 file
```

## 低能构象的生成与叠加

### 任务：

我们想基于几何形状与官能团化学，找出两个分子之间最佳的叠加。

**环境要求：**

- OpenEye OMEGA2 与 OpenEye ROCS
- 蛋白质结构可视化工具（例如 PyMOL）
- Python 3.x
- 两个 `.mol2` 格式的分子

### 1) 生成目标分子与查询分子的低能构象

在本教程中，我将使用两个从 [ZINC](http://zinc.docking.org) 数据库中随机挑选并下载的分子。ZINC 是一个收录市售化合物的免费数据库。

#### ZINC00062008：

![Openeye alignments overlays ZINC00062008](https://sebastianraschka.com/images/blog/2014/openeye_alignments_overlays/ZINC00062008.webp)

#### ZINC00082321：

![Openeye alignments overlays ZINC00082321](https://sebastianraschka.com/images/blog/2014/openeye_alignments_overlays/ZINC00082321.webp)

为了找到得分最高的叠加，我建议先通过 OpenEye 的 OMEGA2 工具，分别为目标分子和查询分子生成低能构象。

```python
/soft/linux64/openeye/bin/omega2\
-in .../ZINC00062008.mol2\
-out .../ZINC00062008_confs.mol2\
-warts true\
-fraglib /soft/linux64/openeye/data/omega2/fraglib.oeb.gz\
-commentEnergy true\
-prefix om2
```

有关 OMEGA2 构象生成背后算法的细节，可以参见 Paul C. D. Hawkins、A. Geoffrey
Skillman、Gregory L. Warren、Benjamin A. Ellingson 以及 Matthew T.
Stahl 所著的这篇论文：  
[Conformer Generation with OMEGA: Algorithm and Validation Using High
Quality Structures from the Protein Databank and Cambridge Structural
Database](http://pubs.acs.org/doi/abs/10.1021/ci100031x)

如果你想进一步了解命令行界面的各个参数，请参阅 [OpenEye OMEGA2
文档](http://www.eyesopen.com/docs/omega/current/html/usage.html#command-line-interface)。

下图展示了 ZINC\_00062008 的低能构象集大致的样子：

![Openeye alignments overlays ZINC 00062008 confs 2](https://sebastianraschka.com/images/blog/2014/openeye_alignments_overlays/ZINC_00062008_confs_2.webp)

### 2) 叠加低能构象

现在，我们已经为目标分子和查询分子各生成了约 200 个低能构象（200 是默认最大值），接下来可以使用 OpenEye ROCS 把所有低能构象彼此叠加（即约 200 x ~200 次叠加）。在这里，我们只关心得分最高的叠加对：

```python
/soft/.../rocs\
-query\
-dbase\
-randomstarts 20\
-stats best\
-besthits 0\
-maxhits 0\
-maxconfs 1\
-rankby TanimotoCombo\
-mcquery\
-prefix rcs\
-reportfile rocs.rpt\
-oformat mol2\
-report one\
```

值得一提的是，我们这里按 `TanimotoCombo` 排序，它是 `ShapeTanimoto`（通过体积优化得到的 3D 形状相似度）与 `ColorTanimoto`（官能团匹配）的组合。视你的侧重点而定，你可能需要为 `rankby` 参数指定不同的参数值。关于命令行界面的更多信息请见：
<http://www.eyesopen.com/docs/rocs/current/html/usage.html#command-line-interface>。

### 3) 获取最佳叠加对

使用上一节所列参数运行 OpenEye ROCS 命令行界面后，我们会得到一个报告文件，其中包含得分最高的叠加对；在本例中，它是 ZINC00082321 的第 20 个低能构象与 ZINC00062008 的第 168 个低能构象：

![Openeye alignments overlays rocs report](https://sebastianraschka.com/images/blog/2014/openeye_alignments_overlays/rocs_report.webp)

ROCS 还会生成一个 `.mol2` 文件，其中包含所有采样到的叠加结果。根据报告文件，我们知道自己感兴趣的是哪一对，因此只需写一个简单的脚本，从 ROCS 的 multimol2 输出文件中取出那 2 个 `.mol2` 结构即可；或者也可以用简单的文本搜索来定位这些结构，并把它们保存为单独的 `.mol2` 文件用于可视化：

![Openeye alignments overlays locating overlay](https://sebastianraschka.com/images/blog/2014/openeye_alignments_overlays/locating_overlay.webp)

下图展示了我们得分最高的叠加对的样子：
![Openeye alignments overlays top overlay](https://sebastianraschka.com/images/blog/2014/openeye_alignments_overlays/top_overlay.webp)

### 4) 用于自动化流程的脚本

一个将上述两个步骤封装起来的简单脚本可以在这里找到：
[`lowenergy_conf_overlay.py`](https://github.com/rasbt/protein-science/blob/master/tutorials/low_energy_conformer_overlay/Scripts/lowenergy_conf_overlay.py)
