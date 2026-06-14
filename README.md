# 立定跳远姿态影响的力学分析

本项目是一篇普通物理课程论文及其配套数值模型，研究立定跳远中腾空阶段的姿态调整如何影响落地时脚相对于人体质心的前伸量。论文通过低自由度刚体模型分析收腿、手臂姿态和摆臂对成绩的影响，并与 Ashby & Heegaard (2002)、Ashby & Delp (2006) 的实验和仿真结果进行对比。

## 核心结论

- 二刚体模型将人体简化为“躯干+头+臂”和“双腿+足”，仅以恒定收腿角速度作为主动输入，预测 JRA 条件下落地前伸量约为 `0.298 m`，与实验值 `0.29 m` 偏差小于 `3%`。
- 三刚体模型将双臂从躯干中分离出来，直接给出手臂、躯干和双腿之间的角动量分配关系。
- 在三刚体模型中，仅改变手臂静态固定姿态即可使落地前伸量从约 `0.294 m` 增至 `0.311 m`，变化量约 `0.017 m`，与实验中 JFA 相比 JRA 的 `+0.02 m` 同量级。
- 在相同初始手臂姿态下，动态摆臂对腾空阶段落地前伸量的额外贡献小于 `0.002 m`。这表明实验中的部分手臂增益可能来自静态姿态改变上体惯性分布，而不完全来自腾空阶段的主动摆动。

## 项目结构

```text
.
├── main.tex               # 论文主体
├── two_body_model.py      # 二刚体模型数值积分
├── three_body_model.py    # 三刚体模型及 JFA/JRA 对照
├── fig_phiTA_sweep.pdf    # 手臂固定姿态扫描图，供论文引用
├── fig_phiTA_sweep.png    # 同一图像的 PNG 版本
└── README.md              # 项目说明
```

## 模型概览

### 二刚体模型

二刚体模型将人体划分为：

- 刚体 1：躯干、头和手臂
- 刚体 2：双腿和足

模型假设腾空阶段仅受重力作用，人体绕总质心的角动量守恒，并取初态角动量 `L0 = 0`。主动输入为腿相对于躯干的收腿角速度。通过数值积分得到落地时脚相对于质心的水平前伸量 `Delta_x`。

### 三刚体模型

三刚体模型将人体划分为：

- 刚体 T：躯干和头
- 刚体 A：双臂
- 刚体 L：双腿和足

该模型引入手臂相对于躯干的角度 `phi_TA` 和双腿相对于躯干的角度 `phi_LT`，用于分析手臂固定姿态和动态摆臂对落地前伸量的影响。

## 环境依赖

### Python

运行数值模型需要 Python 3，以及以下依赖：

```bash
pip install numpy matplotlib
```

其中：

- `two_body_model.py` 使用 `numpy` 和 `matplotlib`
- `three_body_model.py` 使用 `numpy`

### LaTeX

论文使用中文排版，需要支持 XeLaTeX。主要依赖包包括：

- `amsmath`
- `amssymb`
- `booktabs`
- `graphicx`
- `xeCJK`

## 运行方式

运行二刚体模型：

```bash
python two_body_model.py
```

运行三刚体模型：

```bash
python three_body_model.py
```

编译论文：

```bash
xelatex main.tex
```

如果需要自动处理多轮编译，也可以使用：

```bash
latexmk -xelatex main.tex
```

## 结果复现

`two_body_model.py` 会输出二刚体模型在 `T = 0.5 s` 时的落地前伸量。论文中对应结果约为：

```text
Delta_x = 0.298 m
```

`three_body_model.py` 会输出三刚体模型的关键中间系数和几组对照结果，包括：

- 三体 JFA：手臂按分段恒速前摆、后摆
- 三体 JRA，`phi_TA = 145 deg`：手臂固定于身前
- 三体 JRA，`phi_TA = 180 deg`：手臂近似与躯干平行，作为二体模型对照
- 二体模型 JRA 对照值：`Delta_x = 0.298 m`

论文中的手臂静态姿态扫描图由 `fig_phiTA_sweep.pdf` 引用，展示了三体 JRA 中固定手臂角度 `phi_TA` 对落地前伸量 `Delta_x` 的影响。

## 论文内容

论文主体位于 `main.tex`，主要包括：

- 立定跳远姿态调整问题的研究背景
- 二刚体模型的运动学关系、角动量守恒推导和数值结果
- 三刚体模型的角动量分配关系和数值积分方法
- 手臂静态姿态与动态摆臂对落地前伸量的影响分析
- 与 Ashby 系列实验和最优控制模型的对比讨论

## 参考文献

- B. M. Ashby and J. H. Heegaard. “Role of arm motion in the standing long jump.” Journal of Biomechanics, 35(12):1631-1637, 2002.
- B. M. Ashby and S. L. Delp. “Optimal control simulations reveal mechanisms by which arm movement improves standing long jump performance.” Journal of Biomechanics, 39(9):1726-1734, 2006.
