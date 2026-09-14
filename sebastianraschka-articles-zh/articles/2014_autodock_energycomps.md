---
title: "使用 AutoDock 进行分子对接"
title_en: "Molecular Docking with AutoDock"
source: https://sebastianraschka.com/Articles/2014_autodock_energycomps.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 使用 AutoDock 进行分子对接

> 原文：[Molecular Docking with AutoDock](https://sebastianraschka.com/Articles/2014_autodock_energycomps.html) · Sebastian Raschka's Articles

关于估计蛋白质-配体复合物（相对）结合自由能的方法、思路与工具的讨论和提问相当热门，而即便是最简单的工具，用起来也可能相当棘手。在本文中，我想简要总结分子对接（molecular docking）的思想，并简单介绍如何使用 AutoDock 4.2 的混合方法来评估结合亲和力。

## 引言

### 分子对接

通常来说，分子对接的目标是识别出能与特定受体结合位点相结合的配体（ligand），并确定其最优先的、能量上最有利的结合姿态（binding pose）。这里的「结合姿态」一词同时考虑了配体相对于受体的取向（orientation）以及配体自身的构象（conformation）。为了完成这一任务，分子对接工具会生成一组不同的配体结合姿态，并使用打分函数（scoring function）来估计所生成的配体姿态的结合亲和力，从而确定最佳的结合模式。

**关于配体取向、构象与姿态的简要说明**：

**配体取向（Ligand Orientation）**：

与「构象」不同，两个/多个配体之间的键角（以及化学组成）是相同的，但它们在空间中的取向（平移、整体旋转）各不相同。

![Autodock energycomps ligand orientation](https://sebastianraschka.com/images/blog/2014/autodock/ligand_orientation.webp)

**配体构象（Ligand Conformation）**：

配体/蛋白质可以以不同的构象存在。通常，「构象」指的是两个/多个配体或蛋白质具有相同的化学组成，但键角发生了改变。

![Autodock energycomps ligand conformation](https://sebastianraschka.com/images/blog/2014/autodock/ligand_conformation.webp)

**配体姿态（Ligand Pose）**：

配体姿态描述的是配体在蛋白质结合位点中的结合模式。通常认为它是取向与构象的组合。

视具体应用而定，目标配体既可以充当受体激动剂（agonist）——即在结合时触发生物系统响应的分子——也可以充当受体拮抗剂（antagonist）——即抑制激动剂所介导响应的分子。在实践中，往往需要对庞大的类药小分子库进行筛选，才能识别出有前景的先导化合物（lead compound）。因此，在分子对接软件的开发中，人们不仅关注准确率，计算效率也是一大重点。

当前各类分子对接工具和打分函数所采用的不同方法，大致可以归入以下几类之一：

1. 采用隐式或显式溶剂模型的精细分子动力学，计算结合自由能的绝对值
2. 基于知识的统计势，在来自蛋白质结构数据库（例如
   [PDB](http://www.rcsb.org) 或
   [CSD](https://www.ccdc.cam.ac.uk/solutions/software/csd/)）
   的蛋白质-配体复合物上训练得到
3. 经验方法，采用基于回归的思路来拟合实验数据（例如来自
   [PDBbind](http://www.pdbbind.org.cn) 等数据库的数据）

同样，偏好哪种工具也要视应用场景而定：对于少量不同的配体-蛋白质复合物，计算开销更大的基于力场的方法可以提供更细致的洞察；而基于知识与经验的方法则更偏向高通量场景。通常，第 2、3 类工具计算的是作为相对量的结合亲和力，适合用于排序；相比之下，基于力场的方法则试图估计绝对的结合自由能（例如分别以 kcal/mol 或 kJ/mol 计算）。请注意，虽然基于非分子动力学的方法更强调简单性和计算效率，但这并不必然意味着它们在所评估蛋白质-配体复合物的相对排序上精度更低。

在接下来的章节中，我们将假设已经生成了一组蛋白质-配体复合物，即不同的配体姿态已经被对接（「摆放」）到蛋白质同一个（或类似的）结合位点中。

在下图中，我展示了两个由我生成的示例对接姿态，旁边是通过 X 射线晶体学[实验观测](http://www.rcsb.org/pdb/explore/explore.do?structureId=1A9X)到的 L-鸟氨酸（L-Ornithine）配体结合姿态。

![Autodock energycomps prot lig complexes](https://sebastianraschka.com/images/blog/2014/autodock/prot_lig_complexes.webp)

在评估打分函数时，可以将实验观测到的蛋白质-配体复合物用作阳性对照：理想情况下，与实验结构最接近的那些生成配体姿态应当获得最高排名。为了量化天然配体与生成的配体姿态之间的相似度，可以在两个结构之间计算 RMSD（均方根偏差，Root-Mean-Square Deviation）：RMSD 通过下面这个简单的公式来度量两个蛋白质或配体结构的原子之间的平均距离

![Autodock energycomps rmsd equation](https://sebastianraschka.com/images/blog/2014/autodock/rmsd_equation.webp)

其中 *a~i~* 表示分子 1 的原子，*b~i~* 表示分子 2 的原子。下标 *x, y, z* 表示每个原子的 x-y-z 坐标。

当然，在实际应用中我们拿不到天然配体姿态，但这种以晶体姿态为参照的简单 RMSD 度量，对于训练、测试和比较不同的打分函数非常有用。

对于任何涉及结合能预测的分析，我们都必须牢记：这项任务仍然极具挑战性，而且有许多不同的方法和思路（统计势、分子力学/分子动力学、实验数据等）会给出精度各异的估计结果。

![Autodock energycomps scatter 1 1](https://sebastianraschka.com/images/blog/2014/autodock/scatter_1_1.webp)

另外请记住，下面的方法可能只有在比较类似结构时才有意义，例如把对接到同一蛋白质结合位点上的不同配体姿态拿来做一个相对排序。由于存在种种缺陷、假设与简化，**我既不建议将这些估计出的能量当作绝对值来使用，也不建议在不同的蛋白质之间对它们进行比较。**

结合自由能计算中需要考虑的因素几乎不胜枚举，首先是可用三维（晶体/NMR）结构本身的质量。其他需要考虑的重要因素还包括：配体与蛋白质结合时构象变化的采样方式、水分子与离子的建模，以及在考虑局部 pKa 值和结合引起的 pKa 漂移的前提下对质子化状态的正确预测……

我们将尝试估计的结合自由能按下式计算：
ΔG~bind~ = ΔH - TΔS，
其中 ΔH 代表焓贡献，TΔS 代表熵贡献（只有 ΔG 为负值时，在能量上才是有利的）。典型情况下，当配体与蛋白质结合时，由于有利的分子间相互作用以及分子间键的形成，焓项会下降（尽管溶剂化能以及与水分子的相互作用也起着重要作用）；而熵项则往往会上升，例如由于自由度的损失。

### 关于 AutoDock

AutoDock 使用一种计算成本（相对）低廉的「混合」力场，其中既包含基于分子力学的项，也包含经验项。与计算开销更大、纯基于力场的方法相比，它对绝对结合能的预测可能没有那么准确，但这种半经验方法被认为非常适合用于相对排序。

AutoDock 的半经验力场包含分子内项、一个「完整的」去溶剂化模型，并且还考虑了氢键的方向性。构象熵由扭转自由度的总和计算得到。不过，水分子并没有被显式建模，而是使用成对原子项来估计水的贡献（色散/排斥、氢键、静电以及去溶剂化），并通过添加权重进行校准（基于实验数据）。
简单概括评估步骤：第一步，计算未结合状态下配体和蛋白质的能量；第二步，计算蛋白质-配体复合物的能量；然后取二者之差。

![Autodock energycomps eq autodock1](https://sebastianraschka.com/images/blog/2014/autodock/eq_autodock1.webp)

其中 *P* 代表蛋白质，*L* 代表配体，*V* 是上面提到的成对评估项，ΔS~conf~ 表示结合时构象熵的损失（R Huey 等，2006 ^1^）。

^1^ Huey, Ruth, Garrett M. Morris, Arthur J. Olson, and David S. Goodsell. ["A Semiempirical Free Energy Force Field with Charge-Based Desolvation."](http://onlinelibrary.wiley.com/doi/10.1002/jcc.20634/abstract) Journal of Computational Chemistry 28, no. 6 (April 30, 2007): 1145–52. doi:10.1002/jcc.20634.

---

## 通过 AutoDock 4.2 估计结合能的步骤

我按照以下步骤生成的示例文件存放在我的 GitHub 仓库
[protein-science](https://github.com/rasbt/protein-science) 中。

### 环境准备

在以下步骤中，我们需要用到这些工具：

- [AutoDock
  4.2](https://autodock.scripps.edu/download-autodock4/)
- [MGLTools](http://mgltools.scripps.edu)

AutoDock 4.2 可以免费[下载](https://autodock.scripps.edu/download-autodock4/)，并采用 GNU GPL 许可证。安装非常简单：在 MacOS 或 Linux 上，你只需把下载好的二进制文件 `autodock4` 和 `autogrid4` 移动到 `/usr/local/bin` 目录即可。更多信息请参阅[本页面](https://autodock.scripps.edu/download-autodock4/)上更详细的说明。

[MGLTools](http://mgltools.scripps.edu/downloads) 是一个相当庞大的工具与 GUI 软件包，用于处理分子结构，其中包含 AutoDockTools。在这里，我们只需要其中的两个 Python 脚本来为 AutoDock 准备蛋白质和配体的结构文件。另外，我们也可以使用 [OpenBabel](https://openbabel.org/docs/) 来生成所需的输入 PDBQT 文件（[用法示例](https://github.com/rasbt/protein-science/blob/master/scripts-and-tools/more_protein-science_tools.md#openbabel)）。

### 1) 准备蛋白质

在这一步中，我们将为蛋白质（或称受体）创建一个 PDBQT 文件，其中包含氢原子以及部分电荷（partial charges）。

现有的部分电荷估计方法有很多种。按照下面的流程，我们将使用所谓的「Gasteiger 电荷」。Gasteiger 电荷基于一种经验方案，只需要了解分子的拓扑结构，因此以其简单、快速的计算而广受欢迎（J. Gasteiger、M. Marsili，1980 ^2^）。

通常来说，假设我们已经执行过一次分子对接，手头的蛋白质结构文件是已经添加了氢原子的 PDB 格式文件。否则，你只需在下面用来准备受体 PDBQT 文件的命令后面追加 `-A "hydrogens"` 标志即可。给蛋白质添加氢原子的工具有很多，一个流行的替代方案是「Reduce」（参考文献和用法示例见[这里](https://github.com/rasbt/protein-science/blob/master/scripts-and-tools/more_protein-science_tools.md#reduce)）。

^2^ Gasteiger, Johann, and Mario Marsili. ["Iterative Partial
Equalization of Orbital Electronegativity—a Rapid Access to Atomic
Charges."](http://www.sciencedirect.com/science/article/pii/0040402080801682#)
Tetrahedron 36, no. 22 (1980): 3219–28.
doi:10.1016/0040-4020(80)80168-2.

- **输入：**

  ```python
    protein.pdb
  ```
- **输出：**

  ```python
    protein.pdbqt
  ```
- **命令：**

  ```python
    prepare_receptor4.py -r protein.pdb [options]
    # -A "hydrogens" (to add hydrogen atoms if not present)
  ```
- **示例**：

  ```python
    /Library/MGLTools/1.5.6/bin/pythonsh /Library/MGLTools/1.5.6/MGLToolsPckgs/AutoDockTools/Utilities24/prepare_receptor4.py -r protein.pdb
  ```

关于准备受体坐标的更多信息，请参阅 [AutoDock 4.2.6 User Guide (PDF)](https://autodock.scripps.edu/wp-content/uploads/sites/56/2022/04/AutoDock4.2.6_UserGuide.pdf#page=13)。

### 2) 准备配体

这一步与受体的准备（见第 1 步）非常相似。同样地，我们要从配体分子创建一个 PDBQT 文件，配体分子可以是 MOL2 或 PDB 等格式。
通常，我会先通过 AMBER 力场为配体分子添加氢原子和 AM1-BCC 电荷（Jakalian 等，2002 ^3^），从而得到 MOL2 格式的配体分子。不过我在实践中发现，如果让 `prepare_ligand4.py` 脚本重新指派氢原子和 Gasteiger 电荷，AutoDock4.2 的重新打分（re-scoring）精度会略高一些（更利于给接近天然状态的姿态打出好分数）。

^3^ Jakalian, Araz, David B. Jack, and Christopher I. Bayly. ["Fast,
Efficient Generation of High-Quality Atomic Charges. AM1-BCC Model: II.
Parameterization and
Validation."](http://onlinelibrary.wiley.com/doi/10.1002/jcc.10128/abstract)
Journal of Computational Chemistry 23, no. 16 (October 18, 2002):
1623–41. doi:10.1002/jcc.10128.

- **输入：**

  ```python
    ligand.pdb or ligand.mol2
  ```
- **输出：**

  ```python
    ligand.pdbqt
  ```
- **命令：**

  ```python
    prepare_ligand4.py -l ligand.mol2 [options]
    # -C -U "" (to preserve existing hydrogens and charges)
  ```
- **示例**：

  ```python
    /Library/MGLTools/1.5.6/bin/pythonsh /Library/MGLTools/1.5.6/MGLToolsPckgs/AutoDockTools/Utilities24/prepare_ligand4.py -l ligand.mol2
  ```

关于准备配体坐标的更多信息，请参阅 [AutoDock 4.2.6 User Guide (PDF)](https://autodock.scripps.edu/wp-content/uploads/sites/56/2022/04/AutoDock4.2.6_UserGuide.pdf#page=13)。

### 3) 生成格点参数文件

现在，我们必须定义 AutoDock 进行对接时所考虑的 3D 空间，通常是围绕受体潜在结合位点的一块体积区域。由于在我们的场景中已经有一个「摆放」好的配体，我们可以使用 `-y` 标志让格点以配体中心为中心。

在这一步中，我们将创建「AutoGrid4」的输入文件；如下一节所述，AutoGrid4 会生成各种不同的「map（映射图）」文件以及格点数据文件。

请注意，虽然我们在这里并不想执行对接，而只是想对已对接的复合物进行「重新打分」，但为了让 AutoDock 的重新打分能够工作，我们仍然需要完成这些步骤。

- **输入：**

  ```python
    ligand.pdbqt
    protein.pdbqt
  ```
- **输出：**

  ```python
    protein.gpf
  ```
- **命令：**

  ```python
    prepare_gpf4.py -l ligand.pdbqt -r protein.pdbqt -y [options]
  ```
- **示例**：

  ```python
    /Library/MGLTools/1.5.6/bin/pythonsh /Library/MGLTools/1.5.6/MGLToolsPckgs/AutoDockTools/Utilities24/prepare_gpf4.py -l ligand.pdbqt -r protein.pdbqt -y
  ```

更多信息请参阅文档：<https://web.archive.org/web/20170208183253/http://autodock.scripps.edu:80/faqs-help/how-to/how-to-prepare-a-grid-parameter-files-for-autogrid4>。

### 4) 生成映射图与格点数据文件

我们在上一步中创建了格点参数文件，现在可以使用 AutoGrid4.2 来生成一系列不同的映射图文件和主格点数据文件。

- **输入：**

  ```python
    protein.pdbqt
    protein.gpf
  ```
- **输出：**

  ```python
    protein.*.map       # affinity maps for different atoms
    protein.maps.fld    # Grid data file
    protein.d.map       # desolvation map
    protein.e.map       # electrostatic map
  ```
- **命令：**

  ```python
    autogrid4 -p protein.gpf
  ```
- **更多用法信息：**

  ```python
    usage: AutoGrid     -p parameter_filename
        -l log_filename
        -d (increment debug level)
        -h (display this message)
        --version (print version information, copyright, and license)
  ```

### 5) 生成对接参数文件

就快完成了！在正式运行重新打分之前，最后一步是准备对接参数文件，它打包了 AutoDock 所需的各项信息。

- **输入：**

  ```python
    ligand.pdbqt
    protein.pdbqt
  ```
- **输出：**

  ```python
    ligand_protein.dpf
  ```
- **命令：**

  ```python
    prepare_dpf4.py -l ligand.pdbqt -r protein.pdbqt [options]
  ```
- **示例**：

  ```python
    /Library/MGLTools/1.5.6/bin/pythonsh /Library/MGLTools/1.5.6/MGLToolsPckgs/AutoDockTools/Utilities24/prepare_dpf4.py -l ligand.pdbqt -r protein.pdbqt
  ```

更多信息请参阅文档：<https://web.archive.org/web/20161129042615/http://autodock.scripps.edu/faqs-help/how-to/how-to-prepare-a-docking-parameter-file-for-autodock4-1/>。

**在拿到对接参数文件之后，一个关键的步骤是对它进行修改，使 AutoDock 对其重新打分，而不是执行对接。**

这其实非常简单：我们只需删除所有与对接流程相关的行，然后追加参数 `epdb` 即可。

修改后的对接参数文件大致如下：

```python
autodock_parameter_version 4.2  # used by autodock to validate parameter set
outlev 1                        # diagnostic output level
intelec                         # calculate internal electrostatics
ligand_types C H HD N OA        # atoms types in ligand
fld protein.maps.fld            # grid_data_file
map protein.C.map               # atom-specific affinity map
map protein.H.map               # atom-specific affinity map
map protein.HD.map              # atom-specific affinity map
map protein.N.map               # atom-specific affinity map
map protein.OA.map              # atom-specific affinity map
elecmap protein.e.map           # electrostatics map
desolvmap protein.d.map         # desolvation map
move ligand.pdbqt               # small molecule
about 32.7295 15.019 52.7701    # small molecule center
epdb                            # **add** this to evaluate the small molecule
```

### 6) 运行 AutoDock

到这一步，我们应该已经创建了一大堆不同的文件，可以开始为蛋白质-配体复合物打分了。

![Autodock energycomps files before score](https://sebastianraschka.com/images/blog/2014/autodock/files_before_score.webp)

- **输入：**

  ```python
    ligand_protein.dpf
  ```
- **输出：**

  ```python
    scoring_result.log
  ```
- **命令：**

  ```python
    autodock4 -p ligand_protein.dpf -l scoring_result.log
  ```

### 7) 结果

AutoDock 成功完成重新打分后，我们应该可以在日志文件中看到结果，其内容大致如下：

```python
AutoDock 4.2 Release 4.2.5.1
(C) 1989-2012 The Scripps Research Institute
AutoDock comes with ABSOLUTELY NO WARRANTY.
AutoDock is free software, and you are welcome
to redistribute it under certain conditions;
for details type 'autodock4 -C'
[...]

Total Intermolecular Interaction Energy          =  -3.1862 kcal/mol
Total Intermolecular vdW + Hbond + desolv Energy =  -0.2499 kcal/mol
Total Intermolecular Electrostatic Energy        =  -2.9362 kcal/mol
Total Intermolecular + Intramolecular Energy     =  -5.6314 kcal/mol

epdb: USER    Estimated Free Energy of Binding    =   -1.40 kcal/mol  [=(1)+(2)+(3)-(4)]
epdb: USER    Estimated Inhibition Constant, Ki   =   94.72 mM (millimolar)  [Temperature = 298.15 K]
epdb: USER
epdb: USER    (1) Final Intermolecular Energy     =   -3.19 kcal/mol
epdb: USER        vdW + Hbond + desolv Energy     =   -0.25 kcal/mol
epdb: USER        Electrostatic Energy            =   -2.94 kcal/mol
epdb: USER    (2) Final Total Internal Energy     =   -2.45 kcal/mol
epdb: USER    (3) Torsional Free Energy           =   +1.79 kcal/mol
epdb: USER    (4) Unbound System's Energy  [=(2)] =   -2.45 kcal/mol
```

在最底部，我们可以看到估计的结合自由能，以及参与其计算的其他各分量。

如果我们针对一批配体姿态把这个流程自动化，就得到了可用于各种分析的数据。下面，我对两个通过对晶体结构进行对接得到的「糟糕」配体姿态重复了上述流程。

![Autodock energycomps energy components fig](https://sebastianraschka.com/images/blog/2014/autodock/energy_components_fig.webp)

正如我们在上面的柱状图（左）中看到的那样，只有晶体结构姿态的估计结合自由能是有利的（即负值），其中分子间能量在这里是决定性项。如果我们进一步分解估计的分子间自由能（右侧柱状图），可以推测：不利的范德华半径和/或更弱的氢键网络，可能是晶体状态与所生成对接姿态之间能量差异的成因。

## 其他打分函数与工具

下面，我只想列出几个其他的可用于为一组蛋白质-配体复合物打分的工具。它们主要基于统计势而非物理学原理。这些工具计算高效，其价值在于对同一或类似蛋白质结合界面上不同配体姿态的高通量评估。

### AutoDock Vina

Vina 被视为 AutoDock4.2 的继任者，它带来了一种新的基于知识的统计打分函数，取代了 AutoDock 的半经验力场。Vina 相对于 AutoDock4.2 的优势在于更高的预测精度和更快的速度，这不仅得益于打分函数的简化，也得益于在多核 CPU 环境下的多线程能力。

虽然这个简化后的打分函数仍然试图以 kcal/mol 为单位估计结合自由能，但诸如疏水贡献和氢键这样的各个分量在输出中只以相对权重的形式给出。

网站：<http://vina.scripps.edu>

*Trott, Oleg, and Arthur J. Olson. “AutoDock Vina: Improving the Speed
and Accuracy of Docking with a New Scoring Function, Efficient
Optimization, and Multithreading.” Journal of Computational Chemistry,
2009, NA–NA. doi:10.1002/jcc.21334.*

**用于重新打分的用法：**

```python
vina --config config.txt --score_only
```

其中，每个蛋白质-配体复合物都需要准备一个 config.txt 文件，例如：

```python
receptor = protein.pdbqt
ligand = ligand.pdbqt
center_x = -2.491 # Center of Grid points X
center_y = 30.038 # Center of Grid points Y
center_z = -10.765 # Center of Grid points Z
size_x = 25 # Number of Grid points in X direction
size_y = 25 # Number of Grid points in Y Direction
size_z = 25 # Number of Grid points in Z Direction
```

所需的 `pdbqt` 文件可以通过例如 [OpenBabel](#openbabel) 或 AutoDock 的 [MGLTools](http://mgltools.scripps.edu) 生成。
关于准备配体和受体坐标的更多细节，请参阅 [AutoDock 4.2.6 User Guide (PDF)](https://autodock.scripps.edu/wp-content/uploads/sites/56/2022/04/AutoDock4.2.6_UserGuide.pdf#page=13)。

**版本：**

```python
vina --version
AutoDock Vina 1.1.2 (May 11, 2011)
```

**示例输出：**

```python
Affinity: -2.06943 (kcal/mol)

Intermolecular contributions to the terms, before weighting:
gauss 1     : 51.97697
gauss 2     : 1133.84012
repulsion   : 7.41516
hydrophobic : 34.56441
Hydrogen    : 0.00000
```

### DrugScoreX

DrugScoreX 是一个新的、独立的 DrugScore 实现，在为蛋白质-配体复合物打分方面比其前身精度更高。这个打分函数同样基于距离依赖的统计势。

网站：<https://cpclab.uni-duesseldorf.de/index.php/Software>

*Neudert, Gerd, and Gerhard Klebe. “[DSX: A Knowledge-Based Scoring
Function for the Assessment of Protein–Ligand
Complexes.](http://pubs.acs.org/doi/abs/10.1021/ci200274q)” Journal of
Chemical Information and Modeling 51, no. 10 (October 24, 2011):
2731–45. doi:10.1021/ci200274q.*

**用法：**

```python
dsx_mac_64.mac -h

...

pro_file    :  A pdb or mol2 file of your protein.
              In pdb format metals in this file will be treated as part
              of the protein. => Be sure to delete metals in the pdb file
              if you want to supply some metals seperately (-M met_file)!
              All other HETATMs will be ignored!
              In mol2 format everything will be taken as part of the
              protein. => Be sure to delete molecules you want to supply
              seperately (-C, -W, -M) from the protein-mol2-file!
lig_file    :  A mol2- or autodock dlg-file containing all molecules that
              should be scored.

...
```

**版本：**

```python
dsx_mac_64.mac -h

+---------------------------------------------------------------------------+
| 'DSX'           Knowledge-based scoring function for the assessment       |
|                 of receptor-ligand interactions                           |
|  author     :   Gerd Neudert                                              |
|  supervisor :   Prof. Dr. G. Klebe                       ___    _ _       |
|  mailto     :   [email protected]             ))_    )`)      |
|  version    :   0.88   (26.04.2011)                     ((_( o ((( o     |
+---------------------------------------------------------------------------+
```

**示例：**

```python
dsx_mac_64.mac -P protein.pdb -L ligand.mol2 -D pdb_pot_0511
```

存放 PDB 势能的目录在下载 DrugScoreX 之后通常位于其主目录中：

```python
dsx/
    ACC_DON_AnD_HYD_ARO_map.def
    mac64/            # directory that contains the binaries
    README.txt
    pdb_pot_0511/     # potentials
```

**示例输出：**

```python
@RESULTS

  number  |              name              |  rmsd  |   score   |   rank   |    PCS    | tors_score | sas_score
----------|--------------------------------|--------|-----------|----------|-----------|------- -----|-----------
 0        | *****                          |  none  | -36.643   | 1        | -0.157    | 0.000          | 0.000
```

### LigScore

LigScore 同样采用基于知识的方法，使用距离依赖的统计打分函数，它有两种变体：RankScore 训练用于对对接到给定结合位点上的不同化学结构的配体进行排序；PoseScore 则针对同一配体的不同姿态的排序进行了优化。

LigScore 的预测精度似乎相对较高。在配套的研究论文（见下方参考文献）中，作者报告了 74% 的预测准确率——在由 100 个蛋白质-配体复合物组成的测试集上（且被分析集合中不包含晶体姿态时），预测出的配体结合姿态与天然配体的 RMSD < 2 A。此外，他们还评估了旧版本的 AutoDock 和 DrugScore，它们在同一测试集上的预测准确率「只有」66%。

LigScore 既以独立程序的形式提供（作为 IMP 工具包的一部分），也以 Web 服务器的形式提供。

网站：[http://salilab.org/imp/](https://salilab.org/imp/)（IMP 软件包）

Web 服务器：<http://modbase.compbio.ucsf.edu/ligscore/>

*Fan, Hao, Dina Schneidman-Duhovny, John J. Irwin, Guangqiang Dong,
Brian K. Shoichet, and Andrej Sali. “[Statistical Potential for Modeling
and Ranking of Protein–Ligand Interactions.](https://doi.org/10.1021/ci200377u)” Journal of Chemical
Information and Modeling 51, no. 12 (December 27, 2011): 3078–92.
doi:10.1021/ci200377u.*

**用法**：

需要安装 IMP 工具包

```python
ligand_score -h
Usage: ligand_score file.mol2 file.pdb [libfile]
```

其中，`protein_ligand_pose_score.lib` 用于为同一蛋白质-配体复合物的不同配体姿态打分（PoseScore），而 `protein_ligand_rank_score.lib`（RankScore）则用于为给定结合界面上的不同配体打分。

（在 Mac 上，库文件通常位于：
`/usr/local/share/IMP/atom/protein_ligand_pose_score.lib` 和
`/usr/local/share/IMP/atom/protein_ligand_rank_score.lib`）

**示例：**

```python
ligand_score my.mol2 my.pdb /usr/local/share/IMP/atom/protein_ligand_pose_score.lib
```

**版本：**

`ligand_score` 没有单独的版本号，请参看 IMP 的版本（IMP
2.2.0）。

**示例输出：**

```python
Score for omega_1_1 is 20.53
```
