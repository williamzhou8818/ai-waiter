# 桌面 AI 服务员 / Tabletop AI Waiter

### Restaurant AI Agent Project

**项目定位：**
为餐厅提供一个放在餐桌上的小型、可爱、会说话的 AI 服务员。

它不是送餐机器人，而是负责：

**理解客人 → 推荐菜品 → 回答问题 → 点单 → 追加点单 → 呼叫服务员 → 根据用餐状态提供下一步建议。**

---

# 一、项目愿景

传统餐厅正在经历三种数字化：

**QR：** 客人自己扫码、自己看菜单、自己下单。
**Tablet：** 客人通过店内平板操作。
**大型机器人：** 厨房完成订单后，机器人负责送餐。

我们的目标是增加第四种：

> **Tabletop AI Agent：桌上的 AI 服务员。**

让客人不用学习菜单结构，也不用研究按钮。

客人只需要说：

> 「おすすめある？」
> 「二人で1万円くらい」
> 「生魚は苦手」
> 「ビールに合うもの」
> 「これ追加して」
> 「店員さん呼んで」

机器人理解之后完成后续工作。

---

# 二、为什么现在值得做

日本餐饮数字化已经相当成熟。

例如 Dinii 已经把 Mobile Order、POS、客户管理等结合起来，官方目前展示约 3,000 家导入店铺、2,000 万用户，并支持消费者不安装 App、直接扫码下单。

同时，AI 幹事正在尝试另一种方向：把带摄像头的平板放在桌上，通过 AI 判断空酒杯、料理进度，并主动推荐下一杯。

另一方面，PUDU BellaBot 等大型配膳机器人已经形成成熟的餐饮配送场景；PUDU 甚至公布了与 Skylark 集团合作部署大量 BellaBot 的案例。

因此市场已经验证了：

**餐厅愿意接受数字点单。**
**餐厅愿意接受 AI 辅助接客。**
**餐厅愿意接受机器人。**

但我们要验证的是第四件事：

> **客人是否愿意把一个“小型 AI 服务员”放在桌上，并主动和它交流。**

这就是本项目第一阶段最核心的问题。

---

# 三、我们不做什么

这是项目非常重要的一部分。

第一年不做：

- 自研大型送餐机器人
- 自研轮式移动底盘
- SLAM 导航
- 机械臂
- 自己造 POS
- 自己做支付基础设施
- 复杂 ERP
- 排班系统
- 会计系统
- 外卖系统
- 订位系统
- 餐厅 CRM 大全
- 一开始支持所有餐饮业态

我们只解决一条链：

> **桌上 AI → 理解客人 → 推荐 → 下单 → 餐厅执行**

---

# 四、产品定义

## 4.1 产品名称暂定

英文：

**Tabletop AI Waiter**

产品类别：

**Restaurant AI Agent**

日文方向：

**AIテーブルスタッフ**

以后可以再独立设计品牌名。

---

# 五、产品形态

第一代不做“大机器人”。

尺寸目标：

**10～15 cm 左右**

外观：

- 两只“眼睛”
- 一个简洁的小脸
- Speaker
- Microphone
- 小型摄像头
- Wi-Fi
- LED
- 可轻微转头
- 桌面底座

整体感觉不是工业设备，而是：

> **餐厅里的一个小伙伴。**

---

# 六、核心用户体验

## 场景 1：主动推荐

客人坐下。

机器人：

> 「こんばんは。ご注文をお手伝いしましょうか？」

客人：

> 「おすすめある？」

机器人根据该餐厅实时菜单回答。

---

## 场景 2：自然语言点餐

客人：

> 「2人で、1万円くらい。ビール飲みたい。生魚は苦手。」

AI 理解：

- 人数 = 2
- 预算 ≈ ¥10,000
- 饮料 = Beer
- 禁忌 = Raw fish
- 当前桌 = Table 12

AI 输出一套组合：

> 生ビール ×2
> 焼き鳥
> 和牛
> だし巻き玉子
> 焼きおにぎり

然后：

> 「合計 約9,600円です。こちらで注文しますか？」

客人：

> 「お願い。」

系统创建订单。

---

# 七、真正的技术核心

机器人不是最重要的。

真正的产品是：

# Restaurant AI Brain

整体架构：

```text
                 客人
                  ↓
          ┌──────────────┐
          │ Tabletop AI  │
          │    Robot     │
          └──────┬───────┘
                 ↓
              Wi-Fi
                 ↓
       ┌────────────────────┐
       │ Restaurant AI OS   │
       │                    │
       │ AI Agent           │
       │ Menu Context       │
       │ Table Context      │
       │ Customer Context   │
       │ Order Context      │
       └─────────┬──────────┘
                 ↓
       ┌────────────────────┐
       │     Order Service  │
       └─────────┬──────────┘
                 ↓
        ┌────────┴─────────┐
        ↓                  ↓
      Kitchen             POS
        ↓
   Staff / Robot
```

---

# 八、AI 的边界

这是整个系统最重要的工程原则之一。

**LLM 不允许直接写订单数据库。**

正确流程：

```text
客人说话
   ↓
AI 理解
   ↓
AI 生成 Tool Call
   ↓
Order Service
   ↓
业务规则验证
   ↓
库存 / 菜品状态验证
   ↓
数据库 Transaction
   ↓
Order Created
```

例如 AI 想点：

> “啤酒两杯”

不能直接：

```text
INSERT order
```

必须：

```text
add_item(
  table_id,
  menu_item_id,
  quantity
)
```

然后服务器检查：

- 菜品是否存在
- 是否售罄
- 数量是否合法
- 是否属于当前餐厅
- 当前桌是否有效
- 价格是否正确

最后才创建订单。

---

# 九、Restaurant Context Graph

未来最核心的技术护城河，可以是：

> **Restaurant Context Graph**

AI 不只是知道“菜单”。

它知道：

```text
Customer
   +
Companion
   +
Table
   +
Time
   +
Budget
   +
Taste
   +
Allergy
   +
Order History
   +
Current Order
   +
Served Food
   +
Restaurant Inventory
   +
Kitchen State
```

例如：

客人第一次：

> 「ビールに合うもの。」

第二次：

> 「前と同じ感じで。」

AI 可以理解：

> 上次喜欢什么
> 上次点什么
> 哪些东西没吃
> 哪些东西喜欢追加

最终形成：

> **Customer Dining Memory**

---

# 十、第一代机器人功能

V0 Demo 只做 6 件事：

### 1. 唤醒

> 「Hey」

或者按按钮。

### 2. 语音识别

日语优先。

之后：

- 中文
- English
- Korean

### 3. AI 对话

可以询问：

- 推荐
- 辣不辣
- 有没有猪肉
- 适合两个人吗
- 什么配啤酒
- 什么是お通し

### 4. 推荐

AI 只能从当前真实菜单推荐。

### 5. 确认点单

> 「これで注文しますか？」

### 6. 发送真实订单

订单进入我们的 Restaurant OS。

---

# 十一、第一台 Demo 硬件

第一台不要自己造 PCB。

使用：

**M5Stack ATOMS3R-CAM AI Chatbot Kit**

原因：

- ESP32-S3
- Wi-Fi
- Microphone
- Speaker
- Camera
- 小型
- 成本低
- 适合原型
- 后续可以继续扩展

第一台的目标不是量产。

目标是：

> **把 AI Dining Experience 跑通。**

---

# 十二、第一代 BOM

目标：

**¥2,000～6,000 级 Prototype**

核心：

```text
ATOMS3R-CAM
      ↓
3D Printed Body
      ↓
LED
      ↓
Servo
      ↓
USB-C
```

第一版甚至可以没有 Servo。

---

# 十三、第一代不需要做“移动”

机器人：

**不走路。**

**不送餐。**

**不导航。**

**不避障。**

它只坐在桌上。

这样我们可以把项目从：

> Robotics Company

变成：

> AI Restaurant Company

这是战略上非常重要的区别。

---

# 十四、为什么小机器人有机会

大型机器人最大的商业价值：

> 一台机器人服务很多桌。

我们的价值不同：

> **一个 AI 服务入口服务一张桌。**

它类似：

```text
QR
Tablet
Robot
```

但它比 QR 和 Tablet 多了一层：

> **Conversation**

它不是操作 UI。

而是：

> **用语言操作餐厅。**

---

# 十五、最终产品可能形成三种形态

## A. QR AI

成本最低。

客人手机直接使用。

## B. AI Table Robot

成本略高。

餐厅桌面放一个小机器人。

## C. Restaurant AI Brain

把我们的 AI 接入：

- QR
- Tablet
- POS
- KDS
- 大型配膳机器人
- 门店系统

最终：

> **我们不一定卖机器人。**

我们可以卖：

> **Restaurant AI Infrastructure**

---

# 十六、与大型机器人公司的关系

不要和 PUDU、KEENON、Bear Robotics 正面竞争。

它们提供：

> Body / Mobility / Delivery

我们提供：

> Brain / Conversation / Dining Intelligence

未来甚至可以：

```text
客人
 ↓
我们的 AI
 ↓
订单
 ↓
PUDU / KEENON / 店员
 ↓
送餐
```

也就是说：

> **大型机器人负责身体。**
>
> **我们负责大脑。**

---

# 十七、目标客户

第一批不要找大型连锁。

目标：

### Tokyo Independent Restaurants

尤其是：

- 10～40 个座位
- 居酒屋
- 烧肉
- 和食
- Yakitori
- 小型酒吧
- Foreign Customer 较多
- 菜单比较复杂
- 老板亲自经营
- Staff 不够
- 高峰期忙
- 经常需要解释菜单

这些店更适合验证。

---

# 十八、第一批餐厅为什么应该免费

第一阶段：

**3～5 家 Pilot Restaurant**

价格：

> ¥0

换取：

- 实际使用数据
- 客人反馈
- 店员反馈
- 菜单数据
- 点单数据
- AI 对话数据
- AOV 数据
- Case Study
- 视频素材

第一目标不是赚钱。

第一目标：

> **证明餐厅真的需要。**

---

# 十九、产品价值必须用 ROI 证明

不能跟老板说：

> “AI 很酷。”

应该说：

> “它可以帮你减少重复问答、帮助外国客人理解菜单，并增加追加点单机会。”

未来 KPI：

### AOV

Average Order Value

### AI Assisted Order Rate

多少订单经过 AI。

### Staff Intervention Rate

多少 AI 订单需要人工介入。

### Conversation → Order Conversion

聊完后有多少真正下单。

### Upsell Rate

AI 推荐后增加多少额外商品。

### Foreign Customer Conversion

外国客人的点单成功率。

### Staff Time Saved

减少多少重复工作。

---

# 二十、商业模式

第一阶段建议：

### Free Trial

¥0

基础 QR / AI。

### AI Table

约：

**¥9,800 / 店 / 月**

### AI Pro

约：

**¥19,800 / 店 / 月**

包含：

- AI Agent
- 多语言
- Table Robot
- Analytics
- Customer Memory
- Upsell
- Staff tools

### AI OS

约：

**¥39,800 / 店 / 月**

加入：

- POS integration
- KDS
- advanced analytics
- multi-table intelligence
- customer CRM
- AI manager

价格现在只是工作假设，必须通过 Pilot 验证。

---

# 二十一、未来硬件商业模式

硬件不要成为主要利润来源。

例如：

```text
Robot
¥5,000～20,000
```

然后：

```text
AI SaaS
¥9,800～39,800/月
```

这样我们真正赚的是：

> **Software + AI + Restaurant Data**

而不是机器人本身。

---

# 二十二、技术栈

第一阶段：

### Frontend

Next.js
TypeScript
PWA
Tailwind

### Backend

NestJS
TypeScript

### Database

PostgreSQL
pgvector

### Cache

Redis

### Realtime

WebSocket / SSE

### AI

LLM API
AI Gateway
Tool Calling

### Monitoring

Sentry
OpenTelemetry

### Hosting

Vercel
AWS

### Storage

S3

---

# 二十三、系统模块

```text
Restaurant
Menu
Table
Customer
Order
Payment
AI
Kitchen
Staff
Analytics
```

第一阶段重点：

```text
Menu
Table
Order
AI
Kitchen
```

---

# 二十四、订单状态

严格设计：

```text
DRAFT
 ↓
CONFIRMED
 ↓
ACCEPTED
 ↓
PREPARING
 ↓
READY
 ↓
SERVED
 ↓
COMPLETED
```

取消：

```text
CANCELLED
```

支付独立：

```text
UNPAID
 ↓
PAYING
 ↓
PAID
```

---

# 二十五、MVP 系统闭环

我们的第一条完整 Demo：

```text
QR
 ↓
AI Robot
 ↓
「おすすめ」
 ↓
AI 推荐
 ↓
客人确认
 ↓
Cart
 ↓
Order
 ↓
Kitchen Dashboard
 ↓
店员确认
 ↓
READY
 ↓
Robot / Staff Serving
 ↓
Customer
```

这一条跑通，就是：

> **MVP 1.0**

---

# 二十六、视觉能力

第二阶段加入摄像头。

用途不是“监控客人”。

而是：

- 看当前桌面状态
- 识别是否有菜品
- 辅助判断用餐进度
- 识别机器人是否被移动
- 识别一些可交互物体

但是必须遵守：

**Privacy by Design**

尤其日本餐厅场景。

第一阶段甚至可以关闭视觉，只验证语音。

---

# 二十七、最有潜力的未来功能

## AI Upsell

不是疯狂推销。

而是根据 Context：

> 「ビール、もう一杯いかがですか？」

## AI Course Builder

客人：

> “两个人，8000～10000円。”

自动组合套餐。

## AI Translation

不是简单翻译。

而是解释日本文化：

> 「お通しとは……」

## AI Memory

记住：

> 不吃生鱼
> 喜欢啤酒
> 喜欢烧鸟
> 喜欢清淡
> 不喜欢太辣

## AI Dining Guide

甚至告诉外国客人：

> “这道料理怎么吃。”

---

# 二十八、与竞争者的区别

| 产品       | 核心价值                                   |
| ---------- | ------------------------------------------ |
| QR Order   | 自助点单                                   |
| Tablet     | 自助点单                                   |
| Dinii      | Mobile Order + POS + CRM + Restaurant OS   |
| AI 幹事    | 观察桌面并进行 AI 接客/追加推荐            |
| 大型机器人 | 配膳、运输                                 |
| 我们       | **桌面 AI 服务员 + 对话 + 点单 + Context** |

Dinii 的规模已经非常大，所以我们不应该复制它的完整 Restaurant OS，而应该从“Customer Decision Layer”切入。

AI 幹事则说明“AI 了解餐桌状态并主动接客”已经出现，因此我们的差异化必须进一步做到**对话 + 真正下单 + Table Context + Restaurant Context**。

---

# 二十九、日本市场 → 澳洲市场

第一阶段：

**Tokyo**

第二阶段：

**Osaka / Kyoto**

第三阶段：

**Australia**

澳洲不是现在马上做。

先在日本验证：

> “人会不会跟桌面 AI 服务员讲话？”

这个行为成立以后，再做英语市场。

澳洲已有餐厅机器人和自助点单产品，因此进入澳洲时也不应该主打“机器人送餐”，而应该继续强调 AI 服务层。比如当地已经有 BellaBot 等餐饮配送机器人销售渠道。

---

# 三十、12 个月路线图

## Month 1

### Prototype

目标：

**AI 会说话。**

完成：

- ATOMS3R-CAM
- Voice input
- Voice output
- LLM
- 简单角色
- Wi-Fi

---

## Month 2

### AI Menu

完成：

- Restaurant
- Menu
- Menu Item
- Category
- Table

AI 可以回答：

> “有什么推荐？”

> “这个辣吗？”

> “两个人够吗？”

---

## Month 3

### Real Ordering

完成：

- Cart
- Order
- Order Item
- Confirmation
- Kitchen Dashboard

实现：

> “帮我点这个。”

真正进入后台。

---

## Month 4

### Physical Design

做：

- 外壳
- 眼睛
- LED
- 小幅动作
- Table Number

开始做 Demo Video。

---

## Month 5～6

### Tokyo Pilot

找到：

**3～5 家餐厅**

免费试用。

观察：

- 客人使用率
- AI→Order Conversion
- AOV
- Staff feedback
- Failure rate

---

## Month 7～9

### Productization

完成：

- Restaurant Admin
- Menu Management
- Sold-out
- Analytics
- Customer Memory
- Multi-language
- Basic POS Adapter

---

## Month 10～12

### Paid Pilot

目标：

**10～30 家店**

开始收费。

同时准备：

- Sales deck
- Website
- Demo video
- Case study
- Hardware production
- Investor material

---

# 三十一、第一年目标

不是：

> “卖 10,000 个机器人。”

第一年应该验证三个数字：

### 1

**客人愿意使用**

### 2

**餐厅老板愿意继续使用**

### 3

**餐厅愿意付钱**

三个都成立之后，再规模化。

---

# 三十二、核心 KPI

第一阶段：

**100 次真实 AI 对话**

然后：

**50 次 AI 推荐**

然后：

**30 次真实订单**

然后：

**5 家餐厅 Pilot**

然后：

**至少 3 家愿意继续使用**

最终：

> **有人愿意付费。**

这是我们的 North Star。

---

# 三十三、最大的风险

## 风险 1：客人不愿意跟机器人讲话

这是最大风险。

所以必须尽早测试。

---

## 风险 2：机器人太贵

解决：

> 极简硬件 + 云端 AI。

---

## 风险 3：餐厅觉得“QR 就够了”

解决：

不能卖：

> “一个更酷的点单工具。”

而要卖：

> **“一个不会下班的 AI 服务员。”**

---

## 风险 4：AI 点错菜

解决：

AI 绝不直接控制 DB。

所有订单经过：

> Order Service + Business Rules。

---

## 风险 5：餐厅不愿意换 POS

解决：

建立：

> POS Adapter Layer

不要求餐厅把原来的 POS 全部换掉。

---

# 三十四、知识产权策略

第一阶段：

使用成熟开发板做 Prototype。

产品成熟以后：

> OEM → 自有 PCB → 自有外壳 → 自有品牌。

真正需要保护的不是某一块 ESP32，而是：

- Restaurant AI Agent
- Context Engine
- Dining Memory
- AI → Order Tool Architecture
- 餐厅场景交互设计
- 数据结构
- 软件
- 品牌
- 外观设计

未来可以根据实际创新点评估：

**商标 + 外观设计 + 软件著作权/相关版权 + 专利**

---

# 三十五、我们现在真正要做的第一件事

不要做商业网站。

不要做融资 PPT。

不要研究机器人底盘。

不要找工厂。

不要做 20 种功能。

而是：

# 做第一台。

第一台只需要实现：

```text
客人：

「おすすめ何？」

↓

🤖

「2名様でしたら、
焼き鳥と生ビールがおすすめです。」

↓

客人：

「じゃ、それお願い。」

↓

🤖

「承知しました。」

↓

Restaurant AI OS

↓

Order #001

↓

Kitchen
```

如果这个东西真的能运行起来，

我们就可以带着它去东京的一家餐厅。

然后观察：

> **客人到底会不会主动对它说话。**

---

# 三十六、项目当前版本定义

### Project

**Tabletop AI Waiter**

### Vision

**Put an AI waiter on every table.**

### 第一市场

**Tokyo, Japan**

### 第二市场

**Australia**

### 第一产品

**小型桌面 AI 服务员**

### 第一硬件

**ATOMS3R-CAM Prototype**

### 第一能力

**Voice → AI → Recommendation → Order**

### 第一商业验证

**3～5 家餐厅 Pilot**

### 第一商业目标

**证明餐厅愿意为它付费**

### 长期目标

> **成为餐厅的 AI Service Layer。**

不是机器人公司。

不是 QR 点单公司。

而是：

# Restaurant AI Company

---

# 三十七、我们的第一条创业原则

> **先验证“人为什么需要它”，再优化“机器人长什么样”。**

机器人可以很可爱。

但是：

**可爱负责让客人想接触它。**

**AI 负责让客人留下来。**

**订单系统负责让餐厅愿意付钱。**

这三层必须同时成立，项目才真正成立。
