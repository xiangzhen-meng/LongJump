---
abstract: |
  立定跳远是一项依赖全身协调发力的运动，姿态调整对跳远成绩有显著提升作用。
  本文首先建立二刚体模型，仅用一个收腿角速度作为主动输入，
  描述腾空阶段通过收腿增加落地前伸量的过程。该模型比 Ashby & Delp (2006)
  的五刚体模型少三个自由度，且不依赖最优控制算法，并且能将 JRA 条件下的
  落地前伸量预测到 $0.298$ m，与实验值 $0.29$ m 偏差小于 $3\%$。
  在此基础上，本文进一步建立三刚体模型，直接导出手臂、躯干和双腿之间
  的角动量分配关系，并通过数值积分分析手臂姿态对落地前伸量的影响。
  结果表明，仅改变手臂的静态固定姿态，就可使落地前伸量从 $0.294$ m 升至
  $0.311$ m，变化量为 $0.017$ m，与实验 JFA$-$JRA 的 $+0.02$ m 同量级；
  相比之下，在同一姿态下，动态摆臂的额外贡献小于 $0.002$ m。
  这提示：实验中手臂对落地前伸量的增益可能主要来自静态姿态改变了上体惯性分布，
  而非腾空阶段的主动摆动。
author:
- xxx
date: 2026-05-21
title: 立定跳远中姿态对成绩影响的力学分析
---

立定跳远是一项典型的全身协调爆发性运动，其成绩不仅取决于下肢蹬伸能力，
还受到上肢摆动、身体姿态控制和腾空阶段角动量分配的影响。
关于立定跳远的理论研究，已有工作的关注重点是手臂摆动如何改变起跳动力、
身体平衡控制以及落地姿态，从而提高最终跳跃距离。

Ashby & Heegaard (2002) 通过三维运动捕捉和测力台实验，
比较了自由摆臂（JFA）与限制摆臂（JRA）两种条件下的立定跳远表现，
并利用二维六环节人体连杆模型估算人体质心运动。
实验结果表明，自由摆臂可使成绩提高约 $21.2\%$， 其中约 $71\%$
的增益来自起跳质心速度提高，约 $22\%$ 来自起跳前质心水平位移增加，
其余约 $7\%$ 来自落地时脚相对于质心位置的前伸。
该研究还指出，手臂摆动为运动员提供了额外的平衡和姿态控制能力：
自由摆臂条件下，运动员可在腾空阶段通过手臂后摆修正身体绕质心的过度前旋；
而限制摆臂条件下，运动员必须在离地前抑制这种前旋，
从而出现竖直地面反力提前下降和起跳前不利后旋力矩等现象。

在上述实验基础上，Ashby & Delp (2006)
进一步建立五刚体、四自由度的人体模型，
并通过最优控制仿真复现了自由摆臂提高立定跳远成绩的实验结果。
该模型能够较精确地描述手臂运动对起跳速度、身体姿态和落地位置的综合影响，
并指出手臂对成绩的主要贡献来自起跳阶段。
然而，这类模型虽然精确，但自由度较多、计算过程复杂，
难以直接给出各刚体之间角动量分配的解析关系； 同时，Ashby & Heegaard
(2002) 的实验研究主要从现象和数据分解层面说明手臂的作用，
尚不能用简洁的力学模型解释腾空阶段姿态调整的主要机制。

本文的出发点是：能否用远少于五刚体模型的自由度，
建立一个可解析推导的模型， 并仍然定量解释实验中的落地前伸量？
为此，本文首先建立二刚体模型（躯干+双腿）， 仅以收腿角速度作为主动输入。
该模型比 Ashby & Delp (2006) 的五刚体模型少三个自由度，
且不需要复杂优化算法；在采用均匀杆估算转动惯量后， 模型预测的 JRA
落地前伸量为 $0.298$ m， 与实验值 $0.29$ m 的偏差小于 $3\%$。

随后，本文将模型推广至三刚体（躯干+双臂+双腿），直接推导手臂、躯干和双腿之间的角动量分配关系。数值结果表明，仅改变手臂的静态固定姿态，就可使落地前伸量变化
$0.017$ m，这一量级与实验 JFA$-$JRA 的 $\Delta x$
差异（$+0.02$ m）相当；相比之下，在同一姿态下，手臂动态摆动对 $\Delta x$
的额外贡献远小于此。

本文的主要创新点有三点。第一，建立了一个仅含单一主动输入的二刚体模型，在自由度比
Ashby & Delp (2006) 五刚体模型少三个的情况下，仍以小于 $3\%$
的误差复现了 JRA
条件下的落地前伸量。第二，建立了三刚体解析模型，直接导出了手臂、躯干与双腿之间的角动量分配关系，使该问题可以在不依赖最优控制的前提下进行定量分析。第三，借助三刚体模型的全角度数值积分，本文指出实验中
JFA 相较于 JRA
在落地前伸量上的优势，可能主要来自手臂静态位置改变了上体惯性分布，而非腾空阶段的主动摆动。

# 立定跳远模型构建

## 模型定义

将人体简化为两个刚体：

- 刚体1（躯干+头+臂）：质量 $m_1$，绕自身质心 $G_1$ 的转动惯量
  $I_1$。质心 $G_1$ 到髋关节 $O$ 的距离为
  $d_1$，方向沿躯干向上，与水平方向夹角 $\theta_1$。

- 刚体2（双腿+足）：质量 $m_2$，绕自身质心 $G_2$ 的转动惯量 $I_2$。质心
  $G_2$ 到髋关节 $O$ 的距离为 $d_2$，方向沿腿指向脚底，单位向量
  $\hat{\mathbf{u}}_2$（见下），与水平方向夹角 $\theta_2$。

总质量 $M = m_1 + m_2$，约化质量 $\mu = \dfrac{m_1 m_2}{M}$。

## 运动学关系

取髋关节 $O$ 为参考点，质心位置： $$\begin{align}
\vec{r}_{G_1} &= \vec{r}_O + d_1 \hat{u}_1, \quad \hat{u}_1 = (\cos\theta_1,\sin\theta_1), \\
\vec{r}_{G_2} &= \vec{r}_O + d_2 \hat{u}_2, \quad \hat{u}_2 = (\cos\theta_2,\sin\theta_2), \\
\vec{r}_{12} &= \vec{r}_{G_1} - \vec{r}_{G_2} = d_1\hat{u}_1 - d_2\hat{u}_2.
\end{align}$$ 速度： $$\begin{align}
\dot{\vec{r}}_{G_1} &= \dot{\vec{r}}_O + d_1 \dot\theta_1 \hat{k} \times \hat{u}_1, \\
\dot{\vec{r}}_{G_2} &= \dot{\vec{r}}_O + d_2 \dot\theta_2 \hat{k} \times \hat{u}_2, \\
\dot{\vec{r}}_{12} &= d_1 \dot\theta_1 (\hat{k}\times\hat{u}_1) - d_2 \dot\theta_2 (\hat{k}\times\hat{u}_2).
\end{align}$$ 其中 $\hat{k}$ 为垂直于运动平面的单位向量。

计算叉积的 $z$ 分量（标量）： $$
\begin{align}
(\vec{r}_{12} \times \dot{\vec{r}}_{12})_z = \;& d_1^2 \dot\theta_1 + d_2^2 \dot\theta_2 \nonumber \\
&- d_1 d_2 \cos(\theta_1-\theta_2) (\dot\theta_1 + \dot\theta_2).
\end{align}
$$ {#eq:orbit_exact}
 推导利用了恒等式
$(\hat{u}_i \times (\hat{k}\times\hat{u}_j))_z = \hat{u}_i\cdot\hat{u}_j = \cos(\theta_i-\theta_j)$。

## 角动量守恒

在本模型中，采用假设 $L_0 = 0$。从实验角度看，Ashby & Heegaard (2002)
实测起跳时刻质心与压力中心的水平偏差在 5--8 cm 以内（JRA 条件），
据此估算的地面反作用力角冲量很小，$L_0\approx 0$ 合理。

腾空后仅重力作用，对总质心 $G$ 的角动量守恒，则：

$$L_G = I_1\dot\theta_1 + I_2\dot\theta_2 + \mu\,(\vec{r}_{12} \times \dot{\vec{r}}_{12})_z = 0.$$
代入式[@eq:orbit_exact]得：
$$
\boxed{I_1\dot\theta_1 + I_2\dot\theta_2 + \mu\left[ d_1^2 \dot\theta_1 + d_2^2 \dot\theta_2 - d_1 d_2 \cos(\theta_1-\theta_2) (\dot\theta_1 + \dot\theta_2) \right] = 0}.
$$ {#eq:angular_momentum_exact}


## 用相对角速度表示

定义相对角 $\phi = \theta_2 - \theta_1$，则
$\dot\theta_2 = \dot\theta_1 + \dot\phi$。代入式[@eq:angular_momentum_exact]整理得：
$$\bigl[ I_1 + \mu d_1^2 - \mu d_1 d_2 \cos\phi \bigr] \dot\theta_1
+ \bigl[ I_2 + \mu d_2^2 - \mu d_1 d_2 \cos\phi \bigr] (\dot\theta_1 + \dot\phi) = 0.$$
解得： $$
\dot\theta_1 = -\,\frac{I_2 + \mu d_2^2 - \mu d_1 d_2 \cos\phi}{I_1+I_2 + \mu(d_1^2+d_2^2) - 2\mu d_1 d_2 \cos\phi}\; \dot\phi,
$$ {#eq:dt1}

$$
\dot\theta_2 = \dot\theta_1 + \dot\phi = \frac{I_1 + \mu d_1^2 - \mu d_1 d_2 \cos\phi}{I_1+I_2 + \mu(d_1^2+d_2^2) - 2\mu d_1 d_2 \cos\phi}\; \dot\phi.
$$ {#eq:dt2}
 其中 $\dot\phi(t)$ 由运动员主动控制（例如匀速收腿）。

## 落地前伸量

脚的位置： $$x_B = x_O + l_2 \cos\theta_2.$$ 总质心 $G$ 的水平坐标：
$$x_G = x_O + \frac{m_1 d_1 \cos\theta_1 + m_2 d_2 \cos\theta_2}{M}.$$
脚相对于质心的水平偏移为：
$$
\boxed{\Delta x = l_2\cos\theta_2 - \frac{m_1 d_1 \cos\theta_1 + m_2 d_2 \cos\theta_2}{M}}.
$$ {#eq:Dx}

利用式[@eq:dt1]和[@eq:dt2]积分得到
$\theta_1(t),\theta_2(t)$，代入[@eq:Dx]即可得 $\Delta x(t)$。落地时刻 $t=T$ 的 $\Delta x(T)$
即为通过姿态调整获得的额外跳跃距离。

## 数值求解

上述方程可采用数值积分求解。人体参数取值如表1所示，腾空时间
$T=0.5\,\text{s}$，收腿角速度
$\dot\phi = 180^\circ/\text{s}$。笔者编写了Python程序进行数值积分，在
$t=T$ 时的数值由式[@eq:Dx] 给出（结果见第 3.2 节）。

::: {#tab:two_body_params}
  参数                      符号               参考值
  -------------------- --------------- ----------------------
  躯干+头+臂质量            $m_1$              44 kg
  双腿+足质量               $m_2$              28 kg
  躯干质心到髋距离          $d_1$              0.35 m
  双腿质心到髋距离          $d_2$              0.35 m
  腿长（髋到脚底）          $l_2$              0.95 m
  躯干绕质心转动惯量        $I_1$           1.8 kg m$^2$
  双腿绕质心转动惯量        $I_2$           2.1 kg m$^2$
  起跳时躯干倾角        $\theta_1(0)$        $60^\circ$
  起跳时腿倾角          $\theta_2(0)$       $-95^\circ$
  收腿角速度             $\dot\phi$     $180^\circ/\text{s}$
  腾空时间                   $T$               0.5 s

  : 表 1 二刚体模型参数
:::

## 模型参数的估算依据

正文表 1
中的转动惯量和收腿角速度按以下方式估算。

转动惯量：两刚体分别近似为均匀杆，绕自身质心的转动惯量为
$I = \frac{1}{12}mL^2$。

- **刚体 1（躯干+头+手臂）**：质心到髋关节距离
  $d_1=0.35$ m，均匀杆质心在中点，杆长 $L_1 = 2d_1 = 0.70$ m。则
  $$I_1 = \frac{1}{12}m_1 L_1^{\,2}
          = \frac{1}{12}\times 44 \times 0.70^2
          = 1.80\;\text{kg\,m$^2$}
          \approx 1.8\;\text{kg\,m$^2$}.$$

- **刚体 2（双腿+足）**：腿总长 $l_2 = 0.95$ m。则
  $$I_2 = \frac{1}{12}m_2 l_2^{\,2}
          = \frac{1}{12}\times 28 \times 0.95^2
          = 2.11\;\text{kg\,m$^2$}
          \approx 2.1\;\text{kg\,m$^2$}.$$

收腿角速度：起跳时
$\phi(0) = -155^\circ$，落地时腿需收至躯干前方。取恒速
$\dot\phi = 180^\circ/\mathrm{s}$（$\approx 3.14\ \mathrm{rad/s}$），总幅度
$\Delta\phi = 90^\circ$，落地
$\phi(T) = -65^\circ$。实际收腿非恒速，此处为平均近似。

# 二刚体模型与实验数据的对比

上一节建立的二刚体模型仅描述了腾空阶段，起跳参数（起跳速度
$v_0$、起跳角度 $\theta$、起跳时质心高度 $y_0$
等）需作为外部输入给定。本节将模型的预测与 Ashby & Heegaard (2002)
的实测数据进行对比。

## 实验数据

Ashby & Heegaard (2002) 对三名男性受试者（身高 $1.81\pm0.03$ m，体重
$72.3\pm13.0$ kg）在自由摆臂（JFA）和限制摆臂（JRA）两种条件下分别测量了立定跳远的运动学参数。关键实验数据汇总于表 2。

::: {#tab:exp_data}
  参数                                 JFA             JRA         差值
  ------------------------------ --------------- --------------- ---------
  跳跃距离 $L$ (m)                $2.09\pm0.03$   $1.72\pm0.03$   $+0.37$
  起跳速度 $v_0$ (m/s)            $3.32\pm0.03$   $2.95\pm0.03$   $+0.37$
  起跳角度 $\theta$ ($^\circ$)    $38.6\pm1.1$    $40.2\pm1.1$    $-1.6$
  落地超前量 $\Delta x$ (m)       $0.31\pm0.01$   $0.29\pm0.01$   $+0.02$

  : 表 2 自由臂（JFA）与限制臂（JRA）实验数据对比。$\Delta x$
  为落地瞬间脚超前质心的水平距离。数据源自 Ashby & Heegaard (2002)。
:::

## 二刚体模型对落地前伸量的预测

腾空阶段仅受重力，质心的平抛运动与身体绕质心的转动相互独立。质心轨迹由起跳瞬间的
$v_0$、$\theta$、$y_0$
唯一确定，不受腾空姿态变化的影响；身体各环节绕质心的相对运动仅改变脚与质心的相对位置。因此，总运动过程可分解为质心平动和身体的转动。本文模型仅涉及后者，起跳参数由实验提供。

模型的输出为落地的脚超前质心距离
$\Delta x(t)$，其由腾空阶段的角动量守恒和收腿运动决定。取表 1 中的参数（对应 JRA）及收腿角速度
$\dot\varphi = 180^\circ/\text{s}$，腾空时间 $T=0.5$ s，数值积分得到
$\Delta x(t)$。

起跳瞬间（$t=0$）：$\theta_1=60^\circ$，$\theta_2=-95^\circ$，相对角
$\phi(0)=-155^\circ$， $$\begin{equation}
\Delta x(0)=l_2\cos\theta_2(0)-\frac{m_1 d_1\cos\theta_1(0)+m_2 d_2\cos\theta_2(0)}{M}\approx -0.178\ \text{m}.
\end{equation}$$ 落地时刻（$t=0.5$ s）： $$\begin{equation}
\boxed{\Delta x(T) \approx 0.298\ \text{m}}.
\end{equation}$$

## 二刚体模型分析与讨论

**数值对比**：实验 JRA 的落地前伸量为
$\Delta x=0.29\pm0.01$ m，二刚体模型预测为 $0.298$ m，偏差约
$+0.008$ m（$\ll 3\%$）。二刚体模型在采用杆模型转动惯量估计后，与实验数据基本吻合。起跳时
$\Delta x(0) = -0.178$ m，落地时
$\Delta x(T) = 0.298$ m，腾空阶段收腿使脚相对于质心向前净移 $0.476$ m。

**与现有模型的对比**：Ashby & Delp (2006)
用五刚体四自由度模型通过数值优化达到了与实验吻合的结果；本文二刚体模型仅含一个线性的主动输入（恒定收腿角速度），不需任何优化过程，以
$\ll 3\%$ 的偏差复现了 JRA 的落地前伸量。这说明腾空阶段收腿对 $\Delta x$
的主要贡献可以由二自由度刚体模型较为准确地描述。

二刚体模型分离了腾空阶段收腿对于落地超前量的贡献。由于没有考虑手臂的动作，其为后续的三刚体模型提供了对照。

# 三刚体模型 {#sec:three_body}

二刚体模型将双臂与躯干视为单一刚体，仅能描述JRA情形。本节将模型推广为三个刚体：躯干、双臂和双腿。

## 模型定义

将人体分为三个刚体：

- **刚体T（躯干+头）**：质量 $m_T$，绕自身质心的转动惯量 $I_T$。质心
  $G_T$ 位于髋关节 $O$ 上方距离 $d_T$ 处。肩关节 $S$ 位于髋关节上方距离
  $L_T$ 处（即躯干长度）。

- **刚体A（双臂）**：质量 $m_A$，绕自身质心的转动惯量 $I_A$。质心 $G_A$
  位于肩关节 $S$ 沿手臂方向距离 $d_A$ 处。

- **刚体L（双腿+足）**：质量 $m_L$，绕自身质心的转动惯量 $I_L$。质心
  $G_L$ 位于髋关节 $O$ 沿腿方向距离 $d_L$ 处，腿长（髋至脚底）为 $l_L$。

总质量 $M = m_T + m_A + m_L$。各刚体长轴与水平方向的夹角分别为
$\theta_T$、$\theta_A$、$\theta_L$，对应的单位方向向量：
$$\hat{\mathbf{u}}_T = (\cos\theta_T,\;\sin\theta_T),\quad
\hat{\mathbf{u}}_A = (\cos\theta_A,\;\sin\theta_A),\quad
\hat{\mathbf{u}}_L = (\cos\theta_L,\;\sin\theta_L).$$ 角速度记作
$\omega_T \equiv \dot\theta_T$、$\omega_A \equiv \dot\theta_A$、$\omega_L \equiv \dot\theta_L$。

  参数                    符号       典型值
  ---------------------- ------- --------------
  躯干+头质量             $m_T$      37 kg
  双臂质量                $m_A$       7 kg
  双腿+足质量             $m_L$      28 kg
  躯干质心至髋距离        $d_T$      0.32 m
  臂质心至肩距离          $d_A$      0.28 m
  腿质心至髋距离          $d_L$      0.35 m
  髋至肩距离（躯干长）    $L_T$      0.60 m
  腿长（髋至脚底）        $l_L$      0.95 m
  躯干绕质心转动惯量      $I_T$   1.5 kg m$^2$
  双臂绕质心转动惯量      $I_A$   0.3 kg m$^2$
  双腿绕质心转动惯量      $I_L$   2.1 kg m$^2$

  : 三刚体模型参数。质量按 Ashby
  受试者体型分配（$m_T+m_A = m_1$，$m_L = m_2$），转动惯量由杆模型估算

## 运动学关系

取髋关节 $O$ 为参考点，各刚体质心和肩关节的位矢： $$
\mathbf{r}_T = \mathbf{r}_O + d_T \hat{\mathbf{u}}_T,
$$ {#eq:rT}

$$
\mathbf{r}_S = \mathbf{r}_O + L_T \hat{\mathbf{u}}_T,
$$ {#eq:rS}

$$
= \mathbf{r}_O + L_T \hat{\mathbf{u}}_T + d_A \hat{\mathbf{u}}_A,
$$ {#eq:rA}

$$
\mathbf{r}_L = \mathbf{r}_O + d_L \hat{\mathbf{u}}_L.
$$ {#eq:rL}


总质心位置： $$
\begin{equation}
\mathbf{r}_G = \mathbf{r}_O + \beta_T \hat{\mathbf{u}}_T + \beta_A \hat{\mathbf{u}}_A + \beta_L \hat{\mathbf{u}}_L,
\end{equation}
$$ {#eq:rG_three}
 为简洁，定义系数： $$
\begin{equation}
\boxed{\beta_T \equiv \frac{m_T d_T + m_A L_T}{M},\quad
       \beta_A \equiv \frac{m_A d_A}{M},\quad
       \beta_L \equiv \frac{m_L d_L}{M}}.
\end{equation}
$$ {#eq:beta_def}


速度关系： $$
\mathbf{v}_T = \mathbf{v}_O + d_T \omega_T (\hat{\mathbf{k}}\times\hat{\mathbf{u}}_T),
$$ {#eq:vT}

$$
\mathbf{v}_A = \mathbf{v}_O + L_T \omega_T (\hat{\mathbf{k}}\times\hat{\mathbf{u}}_T) + d_A \omega_A (\hat{\mathbf{k}}\times\hat{\mathbf{u}}_A),
$$ {#eq:vA}

$$
\mathbf{v}_L = \mathbf{v}_O + d_L \omega_L (\hat{\mathbf{k}}\times\hat{\mathbf{u}}_L),
$$ {#eq:vL}

$$
\mathbf{v}_G = \mathbf{v}_O + \beta_T \omega_T (\hat{\mathbf{k}}\times\hat{\mathbf{u}}_T) + \beta_A \omega_A (\hat{\mathbf{k}}\times\hat{\mathbf{u}}_A) + \beta_L \omega_L (\hat{\mathbf{k}}\times\hat{\mathbf{u}}_L).
$$ {#eq:vG_three}
 其中 $\hat{\mathbf{k}}$ 为垂直于运动平面的单位向量（$z$
轴正方向）。

## 角动量守恒

腾空阶段仅重力作用，角动量守恒。与二体模型一致，三刚体模型也采用
$L_0 = 0$
的假设。在本模型中，零初态角动量假设相当于控制初态角动量这一变量，集中考察腾空阶段手臂对落地前伸量的影响，进而反过来确定初态角动量对于落地前伸量的影响。在此设定下，角动量守恒方程简化为：
$$
\begin{equation}
L_G \equiv I_T\omega_T + I_A\omega_A + I_L\omega_L
       + \sum_{i\in\{T,A,L\}} m_i\bigl[(\mathbf{r}_i-\mathbf{r}_G)\times(\mathbf{v}_i-\mathbf{v}_G)\bigr]_z = 0.
\end{equation}
$$ {#eq:LG_three}


相对位置
$\boldsymbol{\rho}_i \equiv \mathbf{r}_i - \mathbf{r}_G$（$i=T,A,L$）。由式[@eq:rT]--[@eq:rG_three]： $$
\boldsymbol{\rho}_T = (d_T - \beta_T)\hat{\mathbf{u}}_T - \beta_A\hat{\mathbf{u}}_A - \beta_L\hat{\mathbf{u}}_L,
$$ {#eq:rhoT}

$$
\boldsymbol{\rho}_A = (L_T - \beta_T)\hat{\mathbf{u}}_T + (d_A - \beta_A)\hat{\mathbf{u}}_A - \beta_L\hat{\mathbf{u}}_L,
$$ {#eq:rhoA}

$$
\boldsymbol{\rho}_L = -\beta_T\hat{\mathbf{u}}_T - \beta_A\hat{\mathbf{u}}_A + (d_L - \beta_L)\hat{\mathbf{u}}_L.
$$ {#eq:rhoL}


同理计算相对速度
$\boldsymbol{\nu}_i \equiv \mathbf{v}_i - \mathbf{v}_G$：
$$
- \beta_L\omega_L(\hat{\mathbf{k}}\times\hat{\mathbf{u}}_L),
$$ {#eq:nuT}

$$
- \beta_L\omega_L(\hat{\mathbf{k}}\times\hat{\mathbf{u}}_L),
$$ {#eq:nuA}

$$
+ (d_L - \beta_L)\omega_L(\hat{\mathbf{k}}\times\hat{\mathbf{u}}_L).
$$ {#eq:nuL}


计算叉积 $\boldsymbol{\rho}_i \times \boldsymbol{\nu}_i$ 的 $z$
分量，利用恒等式
$$(\hat{\mathbf{u}}_p \times (\hat{\mathbf{k}}\times\hat{\mathbf{u}}_q))_z = \hat{\mathbf{u}}_p\cdot\hat{\mathbf{u}}_q = \cos(\theta_p - \theta_q).$$

记
$c_{TA} \equiv \cos(\theta_T-\theta_A)$、$c_{TL} \equiv \cos(\theta_T-\theta_L)$、$c_{AL} \equiv \cos(\theta_A-\theta_L)$。对每个刚体展开
$\boldsymbol{\rho}_i \times \boldsymbol{\nu}_i$，得到 $9$
项线性表达式。按 $\omega_T$、$\omega_A$、$\omega_L$
合并同类项，最终将式[@eq:LG_three]化为： $$
\begin{equation}
\boxed{A_T(\boldsymbol{\theta})\,\omega_T \;+\; A_A(\boldsymbol{\theta})\,\omega_A \;+\; A_L(\boldsymbol{\theta})\,\omega_L \;=\; 0},
\end{equation}
$$ {#eq:three_body_am}
 其中系数函数 $A_i(\boldsymbol{\theta})$
仅依赖当前姿态角度： $$
A_T = I_T + K_{TT} + K_{TT}^{(TA)} c_{TA} + K_{TT}^{(TL)} c_{TL},
$$ {#eq:AT}

$$
A_A = I_A + K_{AA} + K_{AA}^{(TA)} c_{TA} + K_{AA}^{(AL)} c_{AL},
$$ {#eq:AA}

$$
A_L = I_L + K_{LL} + K_{LL}^{(TL)} c_{TL} + K_{LL}^{(AL)} c_{AL}.
$$ {#eq:AL}


这里 $K_{ii}$ 为常数项（与角度无关），$K_{ii}^{(pq)}$ 为
$\cos(\theta_p-\theta_q)$ 的系数，其完整表达式如下：

常数项： $$
K_{TT} = m_T(d_T - \beta_T)^2 + m_A(L_T - \beta_T)^2 + m_L\beta_T^2,
$$ {#eq:KTT}

$$
K_{AA} = (m_T + m_L)\beta_A^2 + m_A(d_A - \beta_A)^2,
$$ {#eq:KAA_const}

$$
K_{LL} = (m_T + m_A)\beta_L^2 + m_L(d_L - \beta_L)^2.
$$ {#eq:KLL_const}


$\cos(\theta_T-\theta_A)$ 的系数： $$
\begin{align}
K_{TT}^{(TA)} = K_{AA}^{(TA)} &= -\,m_T\beta_A(d_T-\beta_T)
                                 + m_A(d_A-\beta_A)(L_T-\beta_T)
                                 + m_L\beta_A\beta_T.
\end{align}
$$ {#eq:K_TA}


$\cos(\theta_T-\theta_L)$ 的系数： $$
\begin{align}
K_{TT}^{(TL)} = K_{LL}^{(TL)} &= -\,m_T\beta_L(d_T-\beta_T)
                                 - m_A\beta_L(L_T-\beta_T)
                                 - m_L\beta_T(d_L-\beta_L).
\end{align}
$$ {#eq:K_TL}


$\cos(\theta_A-\theta_L)$ 的系数： $$
\begin{align}
K_{AA}^{(AL)} = K_{LL}^{(AL)} &= m_T\beta_A\beta_L
                                 - m_A\beta_L(d_A-\beta_A)
                                 - m_L\beta_A(d_L-\beta_L).
\end{align}
$$ {#eq:K_AL}


将式[@eq:three_body_am]改写为： $$
\begin{equation}
\boxed{\omega_T = -\frac{A_A}{A_T}\,\omega_A \;-\; \frac{A_L}{A_T}\,\omega_L}.
\end{equation}
$$ {#eq:mechanical_connection}


它表明：躯干的旋转角速度由手臂和腿的角速度线性给出。

## 以相对角速度表示

为便于与二体模型对比，写出相对于躯干的相对角度： $$
\varphi_{TA} \equiv \theta_A - \theta_T, \quad \dot\varphi_{TA} = \omega_A - \omega_T,
$$ {#eq:phiTA}

$$
\varphi_{LT} \equiv \theta_L - \theta_T, \quad \dot\varphi_{LT} = \omega_L - \omega_T.
$$ {#eq:phiLT}
 其中 $\dot\varphi_{LT}$ 即为前文二体模型中的\"收腿角速度\"
$\dot\phi$，$\dot\varphi_{TA}$ 为\"摆臂角速度\"。

将
$\omega_A = \omega_T + \dot\varphi_{TA}$、$\omega_L = \omega_T + \dot\varphi_{LT}$
代入式[@eq:three_body_am]，整理得： $$
\begin{equation}
\boxed{\omega_T = -\frac{A_A\,\dot\varphi_{TA} \;+\; A_L\,\dot\varphi_{LT}}{A_T + A_A + A_L}}.
\end{equation}
$$ {#eq:omega_T_relative}


当手臂相对于躯干固定（$\dot\varphi_{TA} = 0$），即JRA情形，式[@eq:omega_T_relative]简化为
$$\omega_T = -\frac{A_L}{A_T + A_A + A_L}\,\dot\varphi_{LT},$$

## 落地前伸量

三刚体模型中，脚的位置（刚体 $L$ 末端）： $$\begin{equation}
\mathbf{r}_B = \mathbf{r}_O + l_L \hat{\mathbf{u}}_L,
\qquad x_B = x_O + l_L \cos\theta_L.
\end{equation}$$

由式[@eq:rG_three]，总质心水平坐标： $$\begin{equation}
x_G = x_O + \frac{m_T d_T \cos\theta_T + m_A (L_T \cos\theta_T + d_A \cos\theta_A) + m_L d_L \cos\theta_L}{M}.
\end{equation}$$

因此落地前伸量（脚超前质心的水平距离）： $$
\begin{equation}
\boxed{\Delta x = l_L\cos\theta_L - \frac{m_T d_T \cos\theta_T + m_A (L_T \cos\theta_T + d_A \cos\theta_A) + m_L d_L \cos\theta_L}{M}}.
\end{equation}
$$ {#eq:Dx_three_body}


## 数值求解

三体模型的数值求解包含两个自由度：

1.  摆臂规律：给定手臂相对于躯干的角速度 $\dot\varphi_{TA}(t)$。

2.  收腿规律：给定腿相对于躯干的角速度 $\dot\varphi_{LT}(t)$。

取如下输入：

- 收腿角速度维持 $\dot\varphi_{LT}=180^\circ/\text{s}$（与二体模型一致）

- 摆臂输入是分段函数：前 $0.25$ s 以
  $\dot\varphi_{TA}=+180^\circ/\text{s}$ 前摆，后 $0.25$ s 以
  $\dot\varphi_{TA}=-180^\circ/\text{s}$ 后摆。

初始姿态 $\theta_T(0)=60^\circ$，$\varphi_{LT}(0)=-155^\circ$；JFA 与
JRA 均取 $\varphi_{TA}(0)=145^\circ$（臂贴于身前）， JRA 另计算
$\varphi_{TA}(0)=180^\circ$（臂与躯干平行，指向髋部）作为与二体模型的对照。数值积分得到表 3。

::: {#tab:three_body_results}
                                  二体模型      三体JRA(145$^\circ$)   三体JRA(180$^\circ$)   三体JFA
  ---------------------------- --------------- ---------------------- ---------------------- ---------
  落地 $\theta_T$ ($^\circ$)    $\approx 14$            13.2                   11.7            13.3
  落地 $\theta_L$ ($^\circ$)    $\approx -52$         $-51.8$                $-53.3$          $-51.8$
  落地 $\Delta x$ (m)               0.298              0.311                  0.294            0.312

  : 表 3 三刚体模型典型算例结果对比。三体JRA(145$^\circ$)为臂贴于身前，三体JRA(180$^\circ$)为臂与躯干平行指向髋部
:::

# 讨论

## 三体与二体模型的一致性

取
$\varphi_{TA}=180^\circ$（手臂质心与躯干质心近乎重合），三体模型退化为
与二体模型等效的惯性分布，预测 $\Delta x=0.294$ m，与二体结果的
$0.298$ m 吻合，验证了两套模型之间的内部自洽性。

## 静态手臂位置效应

将三体模型的手臂固定于不同姿态（$\dot\varphi_{TA}=0$），计算 JRA 条件下
$\Delta x$ 随 $\varphi_{TA}$
的变化，结果如图 1 所示。

![三体 JRA 中手臂静态固定姿态 φTA 对落地前伸量 Δx 的影响。 水平虚线分别标注实验 JFA（Δx = 0.31 m）和 JRA（Δx = 0.29 m）。 曲线在 φTA = 180∘（臂平行躯干）处取极小值 0.294 m， 在 φTA = 0∘ 或 360∘（臂与躯干同向）附近取极大值 ∼ 0.383 m。](fig_phiTA_sweep.pdf){#fig:sweep width=85.0%}

该曲线的物理含义可由角动量守恒中 $\cos(\theta_T-\theta_A)$ 理解。
$\varphi_{TA}=180^\circ$ 时，手臂方向与躯干相反（余弦为 $-1$），
手臂质心最靠近躯干转动轴，上体有效转动惯量较小；
在给定收腿输入下，躯干角速度的绝对值较大，$\theta_T$ 的净转动也更明显，
因此落地时腿相对于躯干的前伸幅度较大，$\Delta x$ 取极小。 随
$\varphi_{TA}$ 偏离 $180^\circ$，$\cos(\theta_T-\theta_A)$ 增大，
手臂质量与躯干质心的几何分离增大上体有效惯量， 躯干转动减慢，$\Delta x$
单调上升。

在实验 JFA 的 $\Delta x=0.31$ m 附近，曲线与水平线交点位于
$\varphi_{TA}\approx 145^\circ$ 和 $\varphi_{TA}\approx 215^\circ$（两处
$\cos(\varphi_{TA})$ 相同，但 $\cos(\theta_A-\theta_L)$
不同，因此曲线并不对称）。
前者对应手臂位于躯干前侧的姿态，与自由摆臂条件下可能出现的手臂前置状态相容；
后者对应手臂后摆至身侧偏后的位置，虽然数值接近，但并不属于典型的 JFA
姿态。 取 $\varphi_{TA}=145^\circ$ 时 $\Delta x=0.311$ m，
$\varphi_{TA}=180^\circ$ 时 $\Delta x=0.294$ m， 两者的差值为
$0.017$ m，与实验 JFA$-$JRA 的 $+0.02$ m 在量级上接近。

## 动态摆臂的作用

在同一初始姿态（$\varphi_{TA}=145^\circ$）下比较动态摆臂（JFA，
$\dot\varphi_{TA}=\pm 180^\circ/\mathrm{s}$
分段恒速）与静态固定（JRA）， 落地 $\Delta x$ 分别为 $0.312$ m 和
$0.311$ m，差值 $<0.002$ m。 这说明在 $L_0=0$
条件下，腾空阶段中手臂主动摆动对落地前伸量的直接影响极小。 该结果与
Ashby & Delp (2006) "手臂对成绩的增益约 80% 来自起跳阶段"
的结论定性一致。

## 对 Ashby 实验的讨论

以上两个结果提示，Ashby (2002, 2006) 中 JFA$-$JRA 的 $\Delta x$ 差异，
未必都需要归因于腾空阶段手臂的主动摆动。图 1 显示，
仅改变手臂固定姿态而不引入任何动态摆动，即可产生 $0.017$ m 的 $\Delta x$
变化，已经接近实验中的 $+0.02$ m；而在同一姿态下，
动态摆臂带来的额外贡献仅 $<0.002$ m。

因此，实验中自由摆臂相较于约束摆臂在 $\Delta x$ 上的优势，
可能至少有一部分与手臂静态位置改变了上体惯性分布有关，
而不完全来自腾空阶段的摆臂动力学。换句话说，JFA 受试者的手臂自由姿态 与
JRA 受试者的约束姿态很可能同时改变了"能否摆动"和"静态位置"这两个变量。
在原始实验设计中，这两种影响并未被分离；本文借助
$\Delta x$--$\varphi_{TA}$
曲线，将静态位置这一因素单独提取出来，并表明它本身的量级已经接近实验差异。

## 模型假设与局限

本文模型采用零初态角动量（$L_0=0$）作为简化前提，关注腾空阶段的姿态调节。
JRA 条件下起跳角冲量较小，该近似合理；但若需讨论 JFA 情况中起跳阶段手臂
对总跳跃距离的完整贡献（约 $80\%$，主要作用于提高起跳速度 $v_0$），
则需将 $L_0\neq 0$ 的起跳动力学纳入模型。此外，当前模型的身体参数采用均
匀杆近似估计，更精确的人体环节惯性参数可直接替换以提升数值精度。

# 结论

本文围绕立定跳远中腾空阶段姿态调整对落地前伸量的影响，
建立了由二刚体模型到三刚体模型的低自由度力学分析框架。
与已有五刚体最优控制模型相比，本文模型自由度更少，推导过程更直接，
能够在不依赖复杂优化算法的条件下给出身体各刚体之间角动量分配的解析关系。

首先，二刚体模型表明，仅将人体简化为"躯干+双腿"两个刚体，
并以一个恒定收腿角速度作为主动输入，就能够较好地描述腾空阶段脚相对于质心的前伸过程。
在采用均匀杆估算转动惯量后，模型预测 JRA 条件下的落地前伸量为
$\Delta x=0.298$ m，与 Ashby & Heegaard (2002) 的实验值 $0.29$ m
偏差小于 $3\%$。这说明，腾空阶段收腿运动对落地前伸量的主要贡献，
可以由低自由度刚体模型较准确地捕捉。

其次，三刚体模型进一步将手臂从躯干中分离出来，
直接给出了手臂、躯干和双腿之间的角动量分配关系。
数值结果表明，手臂固定姿态本身即可显著改变落地前伸量： 当
$\varphi_{TA}=180^\circ$ 时，模型预测 $\Delta x=0.294$ m； 当
$\varphi_{TA}=145^\circ$ 时，模型预测 $\Delta x=0.311$ m， 两者差值为
$0.017$ m，与实验中 JFA 相比 JRA 的落地前伸量增益 $+0.02$ m
在量级上接近。这表明，手臂并非只有通过主动摆动才影响跳远成绩；
其静态位置改变上体惯性分布，也会通过角动量守恒影响躯干和双腿的相对转动。

再次，在相同初始手臂姿态下比较动态摆臂与静态固定手臂，
模型得到二者落地前伸量差异小于 $0.002$ m。
这说明在本文采用的零初态角动量假设下，
腾空阶段主动摆臂对落地前伸量的直接贡献较小。 结合 Ashby & Delp (2006)
关于手臂主要通过起跳阶段提高成绩的结论，
本文结果提示：实验中自由摆臂条件下落地前伸量的优势，
可能相当一部分来自手臂自由姿态改变了人体惯性分布，
而不完全来自腾空阶段的主动摆臂动力学。

综上，本文的主要结论是：立定跳远腾空阶段的落地前伸量，
可以通过角动量守恒和身体姿态调整得到简洁解释；
收腿运动决定了脚相对于质心前伸的主要过程，
而手臂姿态则通过改变上体有效转动惯量影响这一过程。
本文模型为理解手臂在立定跳远中的作用提供了一个解析、低自由度的力学视角。
其局限在于尚未完整纳入起跳阶段的地面反作用力、肌肉发力和非零初态角动量。
后续若将本文的腾空阶段模型与起跳动力学模型结合，
可进一步解释手臂摆动对总跳跃距离的完整贡献。

::: thebibliography
10

B. M. Ashby and J. H. Heegaard. Role of arm motion in the standing long
jump. , 35(12):1631--1637, 2002.

B. M. Ashby and S. L. Delp. Optimal control simulations reveal
mechanisms by which arm movement improves standing long jump
performance. , 39(9):1726--1734, 2006.
:::
