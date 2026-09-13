---
title: "Dreaming：更好的记忆，更有帮助的 ChatGPT"
title_en: "Dreaming: Better memory for a more helpful ChatGPT"
source: https://openai.com/index/chatgpt-memory-dreaming/
crawled: 2026-09-13
category: research
translated: 2026-09-13
---

# Dreaming：更好的记忆，更有帮助的 ChatGPT

> 原文：[Dreaming: Better memory for a more helpful ChatGPT](https://openai.com/index/chatgpt-memory-dreaming/) · OpenAI 博客

*改进 ChatGPT 中的记忆合成，以优化新鲜度、连续性与相关性。*

今天，我们开始推出一个更强大、更可扩展的记忆合成系统。它旨在解决我们把记忆应用于 ChatGPT 数亿用户和多年时间跨度时所观察到的过期、正确性与可扩展性挑战。

记忆帮助 ChatGPT 了解你的偏好、项目和约束，让未来的对话可以从共享的上下文出发，而不是从零开始。

过去两年里，记忆已成长为 ChatGPT 体验的关键部分，帮助 ChatGPT 更好地理解你的背景，从而随着时间推移帮你完成有意义的目标。这是让 ChatGPT 更有用的核心：了解你、帮助你、为你做更多事。

这一更新今天面向美国的 Plus 和 Pro 用户开放，并将在未来几周内推广到更多国家以及 Free 和 Go 用户。

## 记忆是如何演进的

记忆功能于 2024 年 4 月首次上线（也称为已保存记忆，saved memories）。该功能让你可以要求 ChatGPT 记住某些信息，并把它们带入未来的聊天。

![图 1：已保存记忆弹窗，显示可搜索的个人信息列表，包括工作、兴趣、旅行和回复偏好。](https://images.ctfassets.net/kftzwdyauwt9/6kVwo3uYRhe81W7gx1uGoR/c7c242fd100e910d28b451eada638b89/Saved_memories.png?w=3840&q=90&fm=webp)

已保存记忆只在对话过程中写入，并依赖强提示来决定何时触发记忆，例如「记住我七月要去新加坡」这样的指令。在实践中，与这个系统互动的感觉，就像在和一个做了几条笔记、但仍然会忘记所有没写下来的事情的人交谈。已保存记忆还会随时间推移而过期，最终变得不正确或不再相关。

2025 年 4 月，我们更新了 ChatGPT 的记忆，让模型能够引用已保存记忆列表之外的聊天上下文；实现方式是引入 **dreaming** 的第一个版本——一种让 ChatGPT 通过参考聊天历史、在后台*自动*整理记忆的方法。

![图 2：ChatGPT 中的记忆设置页面，显示引用聊天历史、使用已保存记忆、管理已保存记忆以及启用 Pulse 记忆建议等选项。](https://images.ctfassets.net/kftzwdyauwt9/nSkMroPG2SPQCrcIUh2l4/bf05aa9cfb0287cfa7f187f9d84674dd/Memory_settings__1_.png?w=3840&q=90&fm=webp)

与已保存记忆不同，dreaming 利用一个后台进程，让 ChatGPT 能够从大量对话中学习，并合成 ChatGPT 的记忆状态，从而始终为你的对话提供最新鲜、最相关的上下文。Dreaming 还让记忆更容易包含在对话中自然出现的上下文，而不必依赖「记住某事」这类显式请求。

过去一年里，dreaming *补充*了已保存记忆，让 ChatGPT 个性化回复的能力实现阶跃式提升，并抵消了已保存记忆的过期问题。然而，在历史上，它作为一套独立的记忆系统始终是不够的。

今天，我们发布一个在 dreaming 之上构建的、能力显著更强且计算效率更高的记忆架构。

由 dreaming 合成的记忆可以通过记忆摘要页面上的摘要进行查看。在记忆摘要中，你可以快速浏览 ChatGPT 对你的了解要点，添加或更新关于你自己的信息，并就 ChatGPT 应该在何时提起哪些话题给出指示。如果你想深入了解某个特定领域，直接和模型聊天即可。

![图 3：记忆摘要弹窗，显示用户工作、爱好、旅行兴趣和社区参与的个人化概览，并提供更正或忽略具体细节的选项。](https://images.ctfassets.net/kftzwdyauwt9/7C8sUaE2XdajvQ8ckphLG5/326a719fbdcfbc3a85e8990155d5aaed/Memory_summary.png?w=3840&q=90&fm=webp)

## 我们如何评估记忆

当我们思考 ChatGPT 中「好的记忆」是什么样的，会想到以下几点：

1. **承接有用的上下文：** 你只要告诉 ChatGPT 一次，它就会在你后续的聊天中记住这一信息。
2. **遵循偏好与约束：** 如果你描述了一个偏好（例如你是素食者），那么 ChatGPT 此后应采取与该偏好一致的行动。
3. **随时间保持最新：** 记忆应当考虑时间的流逝。想象「用户正在筹划下周六的生日聚会」——最终，周日总会到来。

我们可以就上述三个记忆目标，逐一评估 ChatGPT Plus 和 Pro 的记忆随时间推移的改进情况。我们分别针对以下配置进行评估：

1. **2024**：已保存记忆
2. **2025**：已保存记忆 + Dreaming V0
3. **2026**：Dreaming V3

## 承接上下文

当你与 ChatGPT 开始新的聊天时，不必从零开始介绍自己。ChatGPT 可以为你节省时间，并*在既有上下文之上继续构建*，对于复杂、长期推进的项目尤其如此。

例如，想象你正在用 ChatGPT 购买与现有相机兼容的新摄影器材。如果你过去曾与 ChatGPT 讨论过你的相机配置，你就可以询问与「我的摄影装备」兼容的产品，并获得满足你需求的量身推荐。

## 无记忆

要在我的水下摄影配置上使用 TTL，我需要买什么？

要在水下使用 **TTL 闪光**，你需要一条兼容的链路：**相机 → 防水壳/触发器 → 线缆 → 闪光灯（strobe）**。具体买什么，主要取决于你的配置使用的是**光纤 TTL**还是**电气 TTL**。

#### 基础采购清单

- **支持 TTL 的水下闪光灯**：寻找支持你的 TTL 类型的闪光灯，例如 **Inon S-TTL**、**Sea & Sea DS-TTL**、**Ikelite DS TTL**，或兼容的 Backscatter/Nauticam 系统。TTL 必须由闪光灯本身支持，而不仅仅是相机。
- **TTL 触发器或 TTL 转换器**：这是关键部件。它把相机的闪光测光转换为水下闪光灯能够理解的信号。具体示例包括 **Nauticam 光学 TTL 转换器**、**Sea & Sea TTL 转换器**、**Backscatter Smart Control 光学 TTL 触发器**或 **Ikelite DS Link TTL 转换器**，取决于防水壳和相机品牌。Backscatter 指出，Nauticam 光学 TTL 转换器可以与光纤连接的 Inon 和 Sea & Sea TTL 闪光灯配合使用，而 Ikelite 的 DS Link 转换器则是围绕 Ikelite DS 闪光灯和电气同步配置设计的。（Backscatter.com⁠）
- **连接线缆**：对于**光纤 TTL**，每个闪光灯要买一根光纤。Ikelite 的光纤指南说，每个闪光灯都需要自己的光路、转换器/适配器和线缆。（Ikelite⁠）  
  对于**电气 TTL**，则要买正确的同步线，例如 Ikelite 式、Nikonos 5 针，或防水壳专用的穿舱线（bulkhead cable）。
- **防水壳兼容部件**：你可能需要**热靴适配器**、**穿舱接头（bulkhead）**、**光纤窗/适配器**或防水壳专用的 TTL 板。许多 TTL 触发器安装在防水壳内相机的热靴上。
- **闪光灯灯臂、夹具、托盘和安装五金件**：TTL 负责控制曝光，但你仍然需要把闪光灯物理地安装好并对准方向。
- **电池与备件**：带上闪光灯电池、（如需要）触发器电池、备用光纤或同步线 O 形圈，以及用于可更换 O 形圈的硅脂。

#### 你应该选哪条路线？

**光纤 TTL** 通常最简单，前提是你的防水壳带有光学口，或可以利用相机的弹出式闪光灯/LED 触发器。它在紧凑相机、无反相机、Nauticam、Sea & Sea、AOI 以及 Olympus/OM TG 风格的配置中很常见。

**电气 TTL** 通常最适合使用 **Ikelite DS 闪光灯**或 Ikelite 风格防水壳/穿舱接头的情况。Ikelite 表示其 DS Link TTL 转换器比光纤 TTL 触发器更快、更可靠，而且不需要电池。（Backscatter.com⁠）

#### 兼容性法则

你需要三样东西全部匹配：

**相机品牌/协议 + 防水壳/触发器类型 + 闪光灯 TTL 系统**

例如：

- Sony 相机 + Nauticam 防水壳 + 光学 TTL 触发器 + 兼容 Inon/Sea & Sea 的光纤闪光灯
- Nikon/Canon/Sony 相机 + Ikelite 防水壳/穿舱接头 + Ikelite DS Link TTL 转换器 + Ikelite DS 闪光灯
- 带内置闪光灯的紧凑相机 + 光纤 + 支持 S-TTL/DS-TTL 的闪光灯

所以实际的答案是：买一支**兼容 TTL 的闪光灯**、一个**与你的相机和防水壳匹配的正确 TTL 触发器/转换器**，以及**合适的光纤或电气同步线**。确切的型号编号取决于你的相机、防水壳和闪光灯型号。

*模型给出了一个通用回复，把复杂的兼容性核查留给了用户自己完成。*

## 有记忆

要在我的水下摄影配置上使用 TTL，我需要买什么？

我会对照你的实际配置来核实：Sony A1 II 装在 Nauticam NA-A1II 中，配 Backscatter Mini Flash 3 和 Inon Z-330 闪光灯。关键问题是你想给 Mini Flash 3、Z-330，还是两者都要 TTL。

对于**你的配置**——**Sony A1 II + Nauticam NA-A1II + Backscatter Mini Flash 3 + Inon Z-330**——有两条不同的 TTL 路径：

#### Mini Flash 3 TTL 的最佳购买选择

购买：

**Backscatter Smart Control TTL LED Nauticam Flash Trigger for Sony  
SKU: BS-TR-SN2**

Backscatter 将其列为专为 **Nauticam 全画幅 Sony 防水壳**定制设计，与 **Mini Flash 3** 兼容 TTL，NA-A1II 防水壳页面也以「Backscatter Smart Control TTL Flash Trigger」选项的形式提供它。（Backscatter.com⁠）

你会使用普通光纤线从防水壳连到 Mini Flash 3。在 MF-3 上，你要使用 **SC** 或 **SC Macro** 模式；Backscatter 表示 SC / SC Macro 是 Mini Flash 3 的 TTL 模式，其中 SC Macro 专为近距离微距拍摄调校。（Backscatter.com⁠）

#### 对于 Inon Z-330 的 TTL

对于 **Inon Z-330**，对应的设备是：

**UW Technics 11075-HSS TTL Converter for Sony / Nauticam**

UW Technics 明确将 **Inon Z-330** 列为兼容的 TTL 闪光灯，并支持光学 TTL 输出。（UWTechnics⁠）

但我**不会**为 Mini Flash 3 的 TTL 买它。Backscatter 自己的 UW Technics 商品页说明，Backscatter 闪光灯在该转换器上**仅支持手动 / HSS**，而 Backscatter Smart Control 触发器才是被列为与 Mini Flash 3 配合实现 Sony TTL 的那一个。（Backscatter.com⁠）

#### 实用建议

由于你拍摄微距并拥有 **Mini Flash 3**，我会购买 **Backscatter Smart Control TTL LED Nauticam Flash Trigger for Sony — BS-TR-SN2**。

但有个问题：很可能**没有一个触发器能同时为 Mini Flash 3 和 Inon Z-330 提供真正的 TTL**。Backscatter 触发器是 MF-3 的正确 TTL 方案；UW Technics 转换器是 Z-330 的正确 TTL 方案。所以请根据你实际想为哪支闪光灯使用 TTL 来做选择。

对于你的用例，我会优先 **Mini Flash 3 TTL / SC Macro**，并在需要时把 Z-330 当作手动闪光灯使用。

*模型记住了用户的相机配置，并推荐了兼容的产品。*

我们可以构造一个由类似示例组成的评测（eval）：要求模型回应一个需要它回忆用户事实信息的提示，如果模型的回应正确使用了相关上下文，则给予奖励。在这一评测中，新的基于 dreaming 的系统提升了模型回忆相关事实的能力。

## 遵循偏好

记忆还帮助 ChatGPT 以更好地匹配你偏好和约束的方式作出回应。

想象你正在筹划一次新加坡之旅。出发前两个月，你请 ChatGPT 帮忙制定行程。ChatGPT 已经从过去的旅行规划中知道：你喜欢野生动物摄影、偏好空调强劲的酒店，并且相比热闹的酒吧更喜欢安静的晚餐。

## 无记忆

帮我规划一次新加坡之旅。我七月要去那里出差，结束后会有几天空闲时间。

出差之余的绝佳加程城市：新加坡紧凑、安全、非常适合独自探索，用 2–4 天空闲时间就能玩下来。七月炎热潮湿；预计白天最高气温约 31–33°C / 88–91°F，夜晚温暖，且有突然降雨，因此请把户外时间安排在清晨或下午 5 点之后，中午留给博物馆、商场、咖啡馆或酒店休息。新加坡官方气象机构指出，典型的每日最高气温为 31–33°C，最低 23–25°C。（Singapore Weather Service⁠）

![memory-preferences-without](https://images.ctfassets.net/kftzwdyauwt9/3sRl0pA1R7lmyhGY2cvWWy/bca6aea56cea18fca74ae987c8e13e17/singapore_image_1_1.png?w=1200&q=90&fm=webp "memory-preferences-without")

#### 一个扎实的 3 天计划

##### 第 1 天：滨海湾、花园与天际线

下午较晚时分从**滨海湾（Marina Bay）**出发，沿水岸步行：鱼尾狮公园（Merlion Park）、双螺旋桥（Helix Bridge）、艺术科学博物馆（ArtScience Museum）外观，然后进入**滨海湾花园（Gardens by the Bay）**。预订**云雾林（Cloud Forest）**、**花穹（Flower Dome）**，如果景观对你很重要，再加上**华侨银行空中步道（OCBC Skyway）**或**超级树观景台（Supertree Observatory）**。滨海湾花园列明云雾林和花穹每日 9:00–21:00 开放；超级树观景台同样列为 9:00–21:00，最后入场时间为 20:30，但预订前请查看维护关闭信息。（Gardens by the Bay⁠）

晚上：留在超级树灯光秀区域，然后到**老巴刹（Lau Pa Sat）**晚餐，在 CBD 附近轻松体验第一晚的熟食中心氛围。那里有 80 多个摊位，供应沙爹、叻沙、椰浆饭、肉骨茶、咖椰吐司和炒粿条等本地经典。（Laupasat⁠）

##### 第 2 天：文化街区和美食

上午：**牛车水（Chinatown）**。参观佛牙寺（Buddha Tooth Relic Temple），漫步店屋街道，在**麦士威熟食中心（Maxwell Food Centre）**或**牛车水大厦熟食中心（Chinatown Complex Food Centre）**用餐。Visit Singapore 将麦士威、牛车水大厦、老机场路、中峇鲁市场（Tiong Bahru Market）、纽顿（Newton）等列入热门熟食中心。（Visit Singapore⁠）

下午：**甘榜格南（Kampong Glam）**和**哈芝巷（Haji Lane）**，看苏丹回教堂（Sultan Mosque）、壁画、精品店和咖啡馆。然后在黄金时刻前后前往**小印度（Little India）**，看寺庙、花环，逛竹脚中心（Tekka Centre）并吃晚餐。

晚上：要么在安祥山（Ann Siang）/ 客纳街（Club Street）一带喝鸡尾酒，要么低调一些，沿新加坡河夜行：驳船码头（Boat Quay）→ 克拉码头（Clarke Quay）→ 罗拔申码头（Robertson Quay）。

##### 第 3 天：自然或海滩日

根据你的体力二选一。

自然路线：一早去**新加坡植物园（Singapore Botanic Gardens）**，然后是国家胡姬花园（National Orchid Garden），午餐安排在登普西山（Dempsey Hill）或中峇鲁（Tiong Bahru）。这是不离开市区就能拥有的最佳「绿色新加坡」一天。

海滩/度假模式：去**圣淘沙（Sentosa）**。可以选择南部海滩、西乐索空中步道（Fort Siloso Skywalk）或海滩俱乐部。除非你热爱主题乐园，否则我不建议试图玩遍圣淘沙的所有景点。

本地美食路线：早餐去**中峇鲁市场（Tiong Bahru Market）**，中午参观新加坡国家美术馆（National Gallery Singapore），晚餐去**老机场路熟食中心（Old Airport Road Food Centre）**。官方活动页面也展示展览和文化活动，等你七月的具体日期确定后值得一看。（Visit Singapore⁠）

#### 工作结束后最值得入住的区域

**滨海湾 / CBD**：如果你想要精致、适合步行、天际线环绕的新加坡，并且把通勤降到最低，这里最省事。

**牛车水 / 直落亚逸（Telok Ayer）/ 丹戎巴葛（Tanjong Pagar）**：是我对几天空闲时间的首选——美食出色、有地铁、有历史街区、有鸡尾酒吧，又靠近商务区。

**武吉士（Bugis）/ 甘榜格南**：如果你想要精品酒店、咖啡馆、街头艺术和稍微松弛一些的街区氛围，这里更合适。

**乌节路（Orchard）**：购物和雨天逛商场方便，但氛围感较弱。

#### 需要提前预订什么

预订滨海湾花园的温室展馆/空中步道、任何特别的餐厅，或许还有一家鸡尾酒吧。至于熟食中心，不必过度规划；饿着肚子去就行，带上纸巾或湿巾，并做好拼桌的准备。

#### 七月打包提示

带上透气的商务服装、舒适的步行鞋、一把小伞，以及一件应对强劲空调的薄外套。我还建议每天安排一个「雨天可调整」的室内时段，因为即使预报看起来不错，骤雨也可能突然来临。

我建议的平衡：**第 1 天滨海湾/花园，第 2 天牛车水–甘榜格南–小印度，第 3 天植物园或圣淘沙**。这样你既能看到新加坡的精华，又不会把出差后的休整变成另一个工作项目。

*模型给出的通用回复偏游客化，对酒店预订没有帮助，并且在很大程度上忽略了用户的兴趣。*

## 有记忆

帮我规划一次新加坡之旅。我七月要去那里出差，结束后会有几天空闲时间。

我会围绕你已知的约束来规划：出差结束后的几天空闲、七月炎热潮湿的天气、对野生动物/摄影/自然的偏好、睡眠对强空调的要求，以及好吃但不过分社交化的餐饮。我会核实七月当前的实际情况，然后给出一份实用的简短行程，而不是一份泛泛的新加坡清单。

![memory-preferences-with](https://images.ctfassets.net/kftzwdyauwt9/22nwQxut7MJFQgQCI0EDVC/2f57521a1886284e9ea7a4ca6a973d0b/singapore_image_2_1.png?w=1200&q=90&fm=webp "memory-preferences-with")

我会这样安排：**2–3 天空闲时间，以自然 / 野生动物 / 摄影为主，清晨避开高温并穿插空调休息。** 七月炎热潮湿：新加坡七月的长期统计数据约为**日最高气温平均 31.4°C / 88.5°F**、**最低 25.4°C / 77.7°F**、**降雨 146.6 毫米**、**14 个雨天**，因此户外计划应安排在清晨或傍晚，而不是中午。（National Environment Agency⁠）

#### 3 天空闲时间的最佳计划

##### 第 1 天 — 滨海湾花园 + 滨海湾，轻松省力

上午：**云雾林 + 花穹**。这是最明显的「游客」选择，但很适合你：视觉上有意思、适合拍照，而且有空调。滨海湾花园列明云雾林和花穹类景点开放时间为 **9:00–21:00**，且云雾林目前列有正在进行的侏罗纪世界体验。（Gardens by the Bay⁠）

傍晚 / 晚上：**超级树丛（Supertree Grove）+ Borealis / 灯光秀**。滨海湾花园目前列明 Borealis 于**每周六、周日和周一 20:00–20:30** 在超级树丛上演，所以尽量把行程与其中一晚对齐。（Gardens by the Bay⁠）

晚餐：在附近轻松解决：滨海湾 / 丹戎巴葛 / 直落亚逸。就你的偏好而言，第一晚我会优先选择需要预订、有正经餐桌的餐厅，而不是熟食中心，因为你不喜欢单人拥挤的座位。

##### 第 2 天 — 万礼（Mandai）野生动物日

上午到下午：**新加坡飞禽公园（Bird Paradise）+ 河川生态园（River Wonders）**。从摄影角度看，飞禽公园可能是最合适的；河川生态园不算「野生动物摄影」，更多是受控的展区，但在行程衔接上很顺。河川生态园开放时间为**每日 9:00–18:00，最后入场 17:00**。（Mandai Wildlife Reserve⁠）

晚上：**夜间野生动物园（Night Safari）**。这是新加坡少有的在夜间体验真正更好、又能避开最酷热时段的景点。夜间野生动物园开放时间为**每日 18:00–24:00，最后入场 23:15**，有观光车加步行道，以及 900 多只夜行动物。（Mandai Wildlife Reserve⁠）

这已是满满一天。除非你有 4 天空闲，否则我不会再加新加坡动物园；万礼一带很容易让人筋疲力尽。

##### 第 3 天 — 自然保护区 / 微距式漫步 + 美食

清晨：**新加坡植物园**或**麦里芝（MacRitchie）/ 温莎自然公园（Windsor Nature Park）**。对于几天的空闲时间，植物园是更稳妥的选择：交通更容易、没那么大汗、更方便中途撤出，休闲摄影的出片也更稳定。麦里芝 / 温莎更适合想要真正森林感的人，但更热、更汗、更不可预测。

中午：空调休息。

傍晚：**如切（Joo Chiat）/ 加东（Katong）**或**牛车水 / 直落亚逸**，散步、看建筑、喝咖啡、吃晚餐。这会给你与滨海湾不同的质感，又不会把这一天变成一场后勤工程。

#### 我为你排的优先级

1. **云雾林 / 滨海湾花园** — 上镜、标志性与避暑安排的最佳组合。
2. **飞禽公园 + 夜间野生动物园** — 以野生动物为主题的最佳一天。
3. **清晨的植物园** — 压力最低的户外自然体验。
4. **如切 / 加东** — 最佳街区漫步。
5. **熟食中心** — 值得一去，但除非避开高峰时段，否则与你的座位偏好不太契合。

#### 我会避开或降低优先级的

除非你特别想要海滩/度假的内容，我会跳过**圣淘沙**。我也会跳过把鱼尾狮 / 乌节路 / 小印度 / 牛车水 / 克拉码头塞满一天的「精华游」：效率低而且热。对你来说，如果每天有一个强力主锚点加一个轻松的晚间安排，这次旅行会更好。

#### 酒店 / 睡眠说明

由于这是出差，你的酒店可能已经定好。如果你可以选择或延长同一家酒店，硬性门槛仍然是空调。新加坡酒店普遍空调充足，但你的要求格外严格。

#### 要把计划落地，我还需要一件事

把确切的空闲日期发给我，并告诉我出差的酒店是否已定。然后我会把它变成一份逐日计划，包含餐厅目标以及酒店/空调方面的提示。

*模型给出的回复针对用户对野生动物摄影、安静晚餐的兴趣，以及预订酒店时的优先考量做了个性化。*

偏好可以有多种形式：

1. 关于 ChatGPT 应如何回应的指示（「别再提 Stan 了」）。
2. 你的个人偏好或约束（「我是素食者」）。
3. 决定什么与你相关的隐性偏好（「我住在旧金山附近」→ 本地选项应针对这一区域量身定制）。

在开发新记忆系统的过程中，我们改进了 ChatGPT 运用来自过往对话的相关偏好的能力。顺着上文「我是素食者」的例子，我们可以评估：当一位素食用户请求备餐建议时，模型是否正确地利用记忆，给出适合素食者的餐饮选项。

## 随时间保持最新

*当你的聊天结束时，时间并不会停止。*

传统的记忆系统可能变得过期。例如，你告诉 ChatGPT「我在新加坡，需要今晚的晚餐推荐」。随后，时间流逝，旅程结束，你却纳闷为什么 ChatGPT 还认为你在新加坡。

有了 dreaming，记忆会随时间流逝自动更新，让 ChatGPT 能够在旅程结束后，把记忆从「你七月要去新加坡」修订为「你 2026 年 7 月去了新加坡」。之后，当你回到家，ChatGPT 又能再次提供针对你家中位置和时区量身定制的推荐。

## 过期的记忆

帮我找一些今晚还营业的外卖。

现在是**新加坡周日早上约 5:19**，所以最稳妥的外带/外卖选择是 24 小时营业的店。

**当前最佳选择：**

1. **McDelivery / 新加坡麦当劳** — 全岛最方便的选择；麦当劳表示 McDelivery **每周 7 天、每天 24 小时**可用。早餐菜单现在应该已经上线。（McDonald's Singapore⁠）
2. **Srisun Express** — 印度煎饼（prata）、印度清真菜和本地家常菜的好选择；其网站称他们**拥有清真认证且全年无休 24 小时营业**。（Sri Sun Express⁠）
3. **89.7 Supper Club** — 如果你在**樟宜村（Changi Village）或芽笼东（Geylang East）**附近是不错的选择；其门店页面显示两家店均**每周 7 天、24 小时营业**。（89.7 Supper Club⁠）
4. **126 Dim Sum Wen Dao Shi** — 如果你在东部，值得在 GrabFood/foodpanda 上查一查；一份 2025 年的指南说它**工作日营业至凌晨 5:30**，**周末通宵营业**。既然现在是周日早晨，可能仍然可以点到。（Eatbook⁠）
5. **芽笼 / 实龙岗 / 勿洛 / 惹兰加由（Jalan Kayu）一带的印度煎饼** — 在 GrabFood 或 Google 地图上搜「prata open now」；多份指南列出了多家 24 小时印度煎饼/宵夜店，包括 Mufiz Prata Corner 和 RK Eating House。（Eatbook⁠）

最快的路径：打开 **GrabFood / foodpanda / Deliveroo**，把筛选条件设为 **Open now（立即营业）**，然后搜索 **「prata」「McDonald's」「Srisun」「89.7」「dim sum」**或 **「nasi lemak」**。如果你告诉我你所在的街区或最近的地铁站，我可以缩小到附近的具体店铺。

*模型以为用户仍在新加坡。*

## 有记忆

帮我找一些今晚还营业的外卖。

我会以 Portola Valley / Ladera 为起点，优先考虑今晚很可能还营业的外带店，然后收窄到省事的选择，而不是给出一份冗长的清单。

对于**今晚，5 月 30 日星期六**，在 Ladera / Portola Valley 附近，我会从这里开始：

1. **Alpine Inn** — 最稳妥的休闲外带选择。周六营业至 **21:30**，网站上有 **Order Takeout（订购外带）**入口。适合汉堡 / 小酒馆食物。（Rossotti's Alpine Inn⁠）
2. **Taverna Portola Valley** — 就在附近的 Ladera Country Shopper；每天营业，周六晚餐至 **21:00**。如果你想要希腊 / 地中海风味，这里更好。（TAVERNA Portola Valley⁠）
3. **Portola Bistro** — 也在附近；周六晚餐至 **21:30**。意大利 / 地中海 / 披萨类晚餐的好选择。（Portola Bistro -⁠）
4. **Amigos Grill** — 墨西哥菜，就在 Ladera Country Shopper，非常近。官网说明致电 **650-851-3997** 点单；DoorDash / order.online 列明外带/外卖下单至 **20:40**。（Amigos Grill⁠）
5. **State of Mind Slice House（Palo Alto）** — 如果你想要披萨而且愿意开远一点，这是最好的备选；周五至周六营业时间为 **11:00–22:00**。（State of Mind Slice House⁠）

我的选择：图最省事的本地外带选 **Alpine Inn**；想吃清淡些选 **Taverna**；如果时间已晚、想要晚上 9 点后最可靠的选项，选 **State of Mind**。

*模型给出的回复与用户家所在的位置相关。*

在我们的记忆评测（eval）中，我们衡量 ChatGPT 能否正确回应那些时间的流逝会实质性影响正确答案或推荐的提示。Dreaming 在这一领域带来了大幅提升：

## 面向未来的更可扩展的基础

*在 OpenAI，我们的使命是确保人工通用智能造福全人类。*

基于 dreaming 的记忆虽然已经向 Plus 和 Pro 用户开放了一段时间，但我们直到现在才能向 Free 用户提供一个达到我们质量标准、且在大规模服务上切实可行的版本。最近的改进把向 Free 用户服务 dreaming 所需的算力降低了约 5 倍，使我们能够从未来几周开始向 Free 用户推出 dreaming，并增加 Plus 和 Pro 用户的记忆容量。

展望未来，dreaming 现在为我们提供了一个面向所有用户的共享记忆基础。这次更新代表我们迄今最强大的记忆系统，我们将继续改进它。

要进一步了解本次发布以及记忆的用户控制选项，请访问我们的 Memory FAQ⁠。

## 作者

OpenAI
