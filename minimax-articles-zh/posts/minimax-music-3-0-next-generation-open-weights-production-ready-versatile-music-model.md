---
title: "MiniMax Music 3.0：新一代开放权重、生产可用、多用途的音乐模型"
date: 2026-08-13
source: https://www.minimax.io/blog/minimax-music-3-0-next-generation-open-weights-production-ready-versatile-music-model
crawled: 2026-09-22
title_en: "MiniMax Music 3.0: Next-Generation Open-Weights, Production-Ready & Versatile Music Model"
translated: 2026-09-22
---

# MiniMax Music 3.0：新一代开放权重、生产可用、多用途的音乐模型

> 原文：[MiniMax Music 3.0: Next-Generation Open-Weights, Production-Ready & Versatile Music Model](https://www.minimax.io/blog/minimax-music-3-0-next-generation-open-weights-production-ready-versatile-music-model) · MiniMax

2026-08-13

MiniMax Music 3.0音乐生成开放权重

![](https://filecdn.minimax.chat/public/minimax-music-3-banner-en-20260818112500.png)

今天，我们推出新一代音乐生成模型 MiniMax Music 3.0。给定一个创意构思和可选的歌词，模型即可在单次生成中完成作曲、编曲、演唱和制作，产出一首完整的歌曲。

Music 3.0 聚焦于那些最难用一句简单提示词捕捉的音乐创作面向：理解创作者的表达意图；让这份意图贯穿一首长达五分钟的完整歌曲；以清晰而具物理真实感的方式渲染乐器；以及生成听起来像是「唱」出来而非「合成」出来的人声。

为此，我们重新设计了整条生成管线——从音乐描述与语言建模到音频渲染。细粒度的时间性描述捕捉情绪、配器与人声呈现的演变；全局-局部混合语言模型（Hybrid-LM）联合建模长程结构与声学细节；多层残差向量量化（RVQ）、隐状态融合（hidden-state fusion）、流匹配（flow matching）与 Flow-VAE 进一步提升输出保真度。这些进展共同带来三大升级：对创意意图更准确的诠释、更完整更多变的编曲，以及更清晰、更自然的声音。

## Music 3.0：技术架构

Music 3.0 由三个相互关联的核心组件构成：分词器（tokenizer）、Hybrid-LM 与合成栈。它们分别解决音乐信息如何表示、长程结构与局部细节如何建模、以及音频如何高保真重建的问题。完整工作流程如下所示。

![MiniMax Music 3.0 技术架构](https://filecdn.minimax.chat/public/music3-architecture-en-202608132135.png)

MiniMax Music 3.0 技术架构

### 多层 RVQ：分离核心结构与声学细节

一个八层 RVQ 以分层方式表示音乐信息。第一层捕捉核心语义与结构，其余七层逐层编码声学残差。在分阶段训练中，第一层先学习稳定的信息主干；随后所有码本联合训练以建模细粒度声音。这一设计为长序列预测提供了更稳定的离散表示，避免把结构性信息与保真度相关的信息同时压在单一 token 层上。

### Hybrid-LM：全局结构与局部声学的联合建模

8B 的全局 LLM 从 Qwen3.5-8B 初始化，在建模全局上下文的同时对语义 token 进行逐帧预测。一个随机初始化的 0.6B 局部 LLM 沿深度轴预测帧内声学 token。训练分两个阶段：先通过全局对齐建立全局 LLM 预测音乐语义的能力，再对全局与局部模型做全参数联合训练。这种分层协作使模型既能保持歌曲级结构稳定，又能解析每一帧内的声学细节。

### 隐状态融合：从离散预测到连续音频渲染

常规系统通常把离散声学 token 直接送入解码器。Music 3.0 则不同：它融合来自全局 LLM 与局部 LLM 的连续隐状态，并用它们为 2.4B 的流匹配模块提供条件，再由 123M 的 Flow-VAE 解码音频。完整路径为：

融合后的 LLM 特征 → 流匹配 → VAE 隐状态 → Flow-VAE 解码器 → 最终音频

这一设计通过连续表示，把语言模型的结构理解与声学模型的音频重建直接连接起来。它在保持长程一致性的同时，提升了发音准确度、乐器连贯性和细节保真度。

|  |  |  |
| --- | --- | --- |
| 用户prompt | 歌词 | Demo |
| 经典上海爵士 / soul，带有轻柔的 lo-fi 温暖质感。深情怀旧的主歌铺陈出柔和明亮的副歌，由一位克制咬字的亲密女声领唱，配以温润的钢琴、低音提琴（upright bass）、刷鼓、温暖的铜管点缀，以及带有复古房间感的混音。 | ``` [Verse 1] 信封带着阳光味， 角边微卷，像在笑。 我拆得慢，怕太快， 把好梦抖落了。  [Verse 2] 字迹软得像云絮， 写：“近来可安好？” 没大事，没长句， 却让我眼眶忽地潮。  [Chorus] 信里有晴， 落在掌心不响。 可整日房间， 都亮得像在唱。 我不藏它，不裱它， 只轻轻， 压在茶杯下—— 让暖，慢慢， 泡进日子的茶。  [Verse 3] 窗外雨还在下， 可我心里晴了。 因你记得问一句， “花开了吗？”  [Chorus] 信里有晴， 不炫，不嚷，不张。 却让我—— 把昨日的灰， 折成纸船， 放向有你的光。  [Bridge]  [Final Chorus] 信里有晴， 是我小小的天。 若世界偶有寒霜， 我就读一遍—— 那句“安好”， 如何， 把我的心， 轻轻， 哄成春天。  [Outro] 信旧了， 字淡了， 可晴…… 还在。 ``` |  |
| 未来感旋律型 EDM / progressive house。关于记忆与数字身份的内省主歌，推向昂扬、以 hook 为驱动的副歌，配以富有感染力的主唱、明亮的分层合成器、脉动的低音、干脆的四踩鼓（four-on-the-floor）、细腻的 glitch 质感，以及宽阔而 polished 的音乐节混音。 | ``` [Verse 1] Upload my heart to the cloud tonight Save every spark of neon light If this body starts to fade away Let my code keep dancing in the data stream Stay [Chorus] Cloud copy of me Living on when these bones finally break free Every joke, every scar Every cheap memory we made Save it, save it Cloud copy of me If the screen goes dark, I’m still in the machine Every glitch, every dream Every version you ever did see Save it, save it [Verse 2] Tag every laugh in a secret folder Archive the nights we outran the thunder If the wiring turns to rust and gray Hit restore… press replay [Chorus] Cloud copy of me Living on when these bones finally break free Every joke, every scar Every cheap memory we made Save it, save it Cloud copy of me If the screen goes dark, I’m still in the machine Every glitch, every dream Every version you ever did see Save it, save it (oh) [Bridge] Even the crashes, the late-night confessions The parts of me I never learned to mention Don’t let the silence swallow me whole Keep a ghost in the glow… So I never go [Final Chorus] Cloud copy of me Still laughing somewhere in the binary Every joke, every scar Every moment you saved for me Save it, save it Cloud copy of me When the lights go out, I’ll still be in the machine Dancing in the code that you still believe Save it… Save me ``` |  |
| Progressive house / EDM，126 BPM，降 B 大调（B-flat major）。内省而怀旧的主歌升腾为宣泄般的狂喜副歌，配以平滑气声的男高音、脉动的侧链合成器、有力的俱乐部低音、干脆的鼓点，以及宽阔的大厅混响。 | ``` [Verse 1] I wish I’d called you back that night Not stared so long at my own pride I wish I’d said what scared me most Instead of turning into smoke  [Chorus] I wish you were here Right now Right here Laughing at my bad ideas Spilling secrets in my ear I wish you were here Right now This year Every little thing I do Keeps circling back to you  [Verse 2] I wish I’d learned to let things go To lose an argument Not you though I wish I’d held you in that storm Not tried to tough it out alone  [Chorus] I wish you were here Right now Right here Laughing at my bad ideas Spilling secrets in my ear I wish you were here Right now This year Every little thing I do Keeps circling back to you  [Bridge] I wish on traffic lights On receipts and license plates On every almost-kind-of sign That says it’s not too late  [Chorus] I wish you were here Right now Right here Tracing circles on my sleeve Saying what you really mean I wish you were here Right now This year Every little thing I do Keeps circling back to you ``` |  |
| 明亮的 power pop / pop rock，112 BPM，降 E 大调（E-flat major）。怀旧而苦乐参半的主歌迸发出宣泄式的副歌，由清澈的女中音（mezzo-soprano）领唱，配以跃升八度的 hook、有力的鼓点、宽阔的分层吉他、细腻的合成器和 polished 的现代混音。 | ``` (Verse 1) We were the kind who never stayed in one place, Running through the city with the wind in our face. Trading every secret like a currency of trust, Didn’t know the moment when it started turning dust.  (Pre-Chorus) I still scroll back just to see your name, But the messages feel like another game.  (Chorus) Forever friends – we promised it one day, And we haven’t seen each other since the following day. Guess forever’s quicker than we thought it’d be, Faded like a sticker on a teenage diary. Yeah, we said we’d never change… but life got in the way.  (Verse 2) Now you’re a highlight in a story I outgrew, A blurry little moment in a world that was new. Funny how the rhythm doesn’t hit the same beat, When the people that you dance with walk off down another street.  (Pre-Chorus) I could call you up, but what would I say? “Hey, remember us?”—it feels too far away.  (Chorus) Forever friends – we promised it one day, And we haven’t seen each other since the following day. Guess forever’s quicker than we thought it’d be, Faded like a sticker on a teenage diary. Yeah, we said we’d never change… but life got in the way.  (Bridge) Maybe we just ran out of the same headline, And maybe that’s okay — stories shift over time. Still I hope you’re smiling somewhere out there tonight, Living loud, living free, living your own life.  (Final Chorus) Forever friends – we promised it one day, And we haven’t seen each other since the following day. But the beat keeps moving and I’ll be okay, Even if our forever only lasted one day. ``` |  |

## 理解创意意图

AI 生成的音乐可能听起来像一首完整的歌，却偏离最初的创作要求。指定的乐器可能逐渐从编曲中消失，预期的情绪气质可能随歌曲推进而减弱，要求的人声风格可能只出现在某一段落，而非贯穿全曲保持连贯。

Music 3.0 引入了更具表达力的音乐描述框架。它不再用单一的全局标签概括整首作品，而是使用结构化描述（Structured Caption），以细粒度的时间粒度描述音乐。这些描述既指定流派、速度、拍号、调性、使用场景和制作质感，也同时追踪情绪轮廓；主奏与伴奏乐器的进出；律动（groove）与低频能量的发展；以及段落级的人声呈现、和声与人声效果变化。

这些描述把主观的听感印象转化为模型可以学习并执行的专业编曲框架。其结果是，模型能更准确地把创意语言翻译为具体的音乐表达，在歌曲展开过程中保持连贯的音乐身份，同时仍引入必要的动态变化。

为了让专业音乐创作更触手可及，我们还开发了基于模板的提示词增强系统（Prompt Enhancement System）。它从精心维护的结构化描述模板库中选择合适的语言，运用成熟的音乐术语和编曲原理，把一句简单的用户描述扩展为详细且音乐上连贯的指令。创作者因此无需掌握专业词汇也能实施精确控制——无论是想要一场亲密克制的 unplugged 演出；一首由连绵 hi-hat 和深沉 808 低音驱动的深夜 R&B；还是一首从内省走向宏大强度的电影感器乐曲。

|  |  |  |
| --- | --- | --- |
| 用户prompt | 歌词 | Demo |
| 温暖的华语流行 / 传统中文叙事曲（ballad），74 BPM，降 A 大调（A-flat major）。温柔怀旧的开篇铺陈出喜庆的副歌，由成熟的男中-高音（baritone-tenor）演绎，配以细腻的古筝、轻柔的弦乐、温和的原声质感、富有表现力的颤音，以及自然的现场房间感。 | ``` [Verse] 屋檐下青苔长 木窗边月影扬 炊烟升起 炉火温暖 笑声穿过院墙  [Chorus] 岁月如歌 歌声悠长 我们牵手走过风霜 孩子长大 家庭满堂 一壶茶温暖了心房  [Verse 2] 摇椅轻晃夕阳下 旧相册笑容如花 指尖缝补 记忆缝扎 每道皱纹藏着回答  [Prechorus] 是谁说流年太快 白发换来心如海  [Chorus] 岁月如歌 歌声悠长 我们牵手走过风霜 孩子长大 家庭满堂 一壶茶温暖了心房  [Bridge] 庭前树影摇曳成画 月下竹影诉说牵挂 人间烟火 平淡无瑕 岁月留香在心底发芽 ``` |  |
| 恢弘的体育场流行摇滚（stadium pop rock），132 BPM，E 大调。轻盈上扬的主歌堆叠进肾上腺素拉满的副歌，配以有力的女中音、跃升八度的 hook、疾驰的鼓点、宽阔的吉他、闪烁的氛围垫，以及一小段失重感的桥段。 | ``` [Verse] Up in the sky I feel alive Wind in my hair feel the dive Hold my breath I see the ground Heart is racing no turning around  [Verse 2] Jump into the blue without a fear Clouds are whispering you’re near Open wide let the colors show Parachute flyin\' high in the glow  [Chorus] Falling free just you and me Parachute spread like wings we see Touch the earth we\'re born anew In the sky I found the truth  [Bridge] Weightless moments pure delight Riding currents day and night Just a canvas in the air Painting dreams without a care  [Chorus] Falling free just you and me Parachute spread like wings we see Touch the earth we\'re born anew In the sky I found the truth  [Outro] Safe landing coming in Start again where dreams begin Parachute my safety net Sky’s the limit no regrets ``` |  |
| 巴洛克流行 / emo rock，162 BPM，降 e 小调（E-flat minor）。庄重哀恸的开篇驶向帝王般的音墙（wall-of-sound）终章，配以沙哑而戏剧化的男中高音（baritenor）、管弦弦乐、大键琴、失真吉他、猛烈的鼓点，以及一段桀骜不驯的 breakdown。 | ``` [Verse] Accept your share of suffering  as a soldier of Jesus our King Soldiers don’t aimlessly wander They work to please their officer  Athletes in the competition Don’t make up rules as their goin\' The farmer who works hard sowing Should have first share of the reaping  [Pre-Chorus] Think about what I am sayin\' God will give you understandin\'  [Chorus] Be strong in the grace of Jesus. The sound teachings you have witnessed Entrust to ones who will teach well Not just look out for themselves  Be strong in the grace of Jesus. The sound teachings you have witnessed Entrust to ones who will teach well Not just look out for themselves  [Verse] Accept your share of suffering  as a soldier of Jesus our King Soldiers don’t aimlessly wander They work to please their officer  Athletes in the competition Don’t make up rules as their goin\' The farmer who works hard sowing Should have first share of the reaping  [Pre-Chorus] Think about what I am sayin\' God will give you understandin\'  [Chorus] Be strong in the grace of Jesus. The sound teachings you have witnessed Entrust to ones who will teach well Not just look out for themselves  Be strong in the grace of Jesus. The sound teachings you have witnessed Entrust to ones who will teach well Not just look out for themselves  [Bridge] The gospel truth of Jesus The descendant of David Who\'s died and resurrected For which I am in chains  The gospel truth of Jesus The descendant of David Who\'s died and resurrected It cannot be contained  They can put me in prison BUT THE GOSPEL CAN\'T BE CHAINED!  [Breakdown to drums-Chorus] Be strong in the grace of Jesus. The sound teachings you have witnessed Entrust to ones who will teach well Not just look out for themselves  [All in Chorus] Be strong in the grace of Jesus. The sound teachings you have witnessed Entrust to ones who will teach well Not just look out for themselves ``` |  |

## 更完整、更多变的编曲

长篇歌曲生成的挑战不只是把时长拉长，而是让段落之间形成可信的推进。情绪要铺垫并解决，乐器要在恰当的时机进入、叠加和退场，主歌、副歌、桥段和器乐段落都要服务于统一的方向。

Music 3.0 在两个层面应对这一挑战。第一，歌词中的段落标签——如 [intro]、[verse]、[pre-chorus]、[chorus]、[bridge]、[instrumental]、[solo] 和 [outro]——定义了歌曲的宏观结构。第二，结构化描述规定了每个阶段的情绪发展、配器变化、人声呈现、节奏基础、点缀音色和空间效果，把「什么在变、在哪里变」变成显式的生成条件。

在模型层面，Music 3.0 采用全局-局部协作的 Hybrid-LM。8B 全局 LLM 逐帧预测核心语义与结构 token，并维护全曲上下文。0.6B 局部 LLM 在每帧内沿深度轴预测声学 token，补充局部的声音细节。这种职责分工让模型在最长五分钟的歌曲中保持时间稳定性，同时在各个段落内保留丰富的变化。

|  |  |  |
| --- | --- | --- |
| 用户prompt | 歌词 | Demo |
| 昂扬的 progressive house / EDM，126 BPM，降 A 大调（A-flat major）。专注的灵感成长为狂喜的高潮，配以温暖微沙哑的男高音、跃升的五声音阶 hook、有力的俱乐部鼓点、克制的低音、明亮的合成器，以及 polished 的全景混音。 | ``` (Verse 1) I grab my pen, heart starts to race, Time to escape, to claim my space. Each stroke of ink breathes life anew, Worlds awaken where dreams come true. (Chorus) I’m weaving tales untold, characters bold, Adventures unfold in colors and gold. Through ink and paper, I carve my way, In this realm of wonder, forever I stay. (Verse 2) From the shadows of mind, stories ignite, Panels bloom under late-night light. Lines and curves carry all my soul, Where impossible dreams find control. (Chorus) I’m weaving tales untold, characters bold, Adventures unfold in colors and gold. Through ink and paper, I carve my way, In this realm of wonder, forever I stay. (Bridge) Every stroke sparks a rush inside, Bringing visions I can’t hide. In this endless sea of creation, I chase the thrill, my true salvation. (Chorus – with lift) I’m weaving tales untold, characters bold, Adventures explode in stories retold. Through ink and paper, I find my fire, In imagination’s glow, I never tire. (Outro) So I’ll keep creating, with passion so free, This world of my making is where I belong—me. Pen in hand, heart open wide, In stories forever, my spirit will ride. ``` |  |
| 欢快的 funk / nu-disco，112 BPM，降 E 大调（E-flat major）。自信、趾高气扬而喜庆，配以顺滑深情的男高音、俏皮的断音咬字、假声翻转（falsetto flips）、干脆的鼓点、弹性的低音、节奏吉他、光亮的键盘，以及宽阔的舞池混音。 | ``` [Verse 1] I\'m feeling like a million bucks today Nothing\'s gonna stand in my way The sun is shining and the sky is blue I\'ve got a feeling that I\'m gonna make it through  [Chorus] Oh oh oh, I\'m on top of the world Oh oh oh, I\'m on top of the world Nothing can stop me now I\'m reaching for the stars and I\'m never coming down ``` |  |
| 阴暗的 E-punk 嘻哈 / 工业 rap，108 BPM，降 b 小调（B-flat minor）。布道般的不祥张力转为俱乐部式的宣泄，配以沙哑的男高音，在失真电子、硬朗鼓点和饱和低音之上混合了攻击性的说唱、朋克嘶吼和萦绕的吟唱。 | ``` [Hook] I\'ve been having revelations Repenting for my sins In attempt to make amends  Before the end begins Lord knows that we\'re holy But only god can win Prophecy fulfilling slowly  Before the end begins   [Verse] Jesus came to save us He died so we could live So his will could carry on  Before the end begins And god he sent his only son To bear the weight of what we\'ve done Our evil deeds must weigh a ton. (Somewhere the end has just begun)...  [Instrumental dance bridge] Uuuuuuuuun Just Beguuuuuuu Uuuuuuuuun  [Hook] I\'ve been having revelations Repenting for my sins In attempt to make amends  Before the end begins Lord knows that we\'re holy But only god can win Prophecy fulfilling slowly  Before the end begins ``` |  |

## 音频质量的进步

有说服力的作曲需要同样有说服力的声音。Music 3.0 在音频质量上带来了实质性提升，产出的混音更开阔、更清晰、更均衡，拥塞感和浑浊感更少。

音频建模从多层残差向量量化（RVQ）开始。第一层使用 16,384 项的码本，专注于音乐的核心语义与结构。第 2–8 层各自使用 1,024 项的码本，逐层编码残差声学细节。训练时，我们先独立训练初始层，让它尽可能全面地捕捉核心信息；随后八层全部联合训练。这种分层设计在语义容量、生成稳定性与细节重建之间取得平衡，同时减少长序列生成中的误差累积。

不过，Music 3.0 的最终音频渲染超越了离散 token。推理时，合成栈并不加载离散分词器的解码路径，而是融合 8B 全局 LLM 与 0.6B 局部 LLM 最后几层的连续隐状态，然后直接通过流匹配和 Flow-VAE 生成音频。与仅用离散 token 相比，这些连续特征保留了更丰富的高维声学信息，提升了人声发音的准确度和乐器声音的物理连贯性。

2.4B 的流匹配模块把融合后的语言模型特征映射到 VAE 隐空间。123M 的 Flow-VAE 继承了 MiniMax Speech 架构，并针对音乐特有的动态范围和频谱分布重新训练，以重建最终波形。这使模型能够遵循更精确的乐器指令，并再现滑音（glissando）、连奏（legato）等真实的演奏技法。乐器在编曲中的角色更加分明，低频保持冲击力而不遮蔽混音，即使在层次密集的制作中，细微的声音细节依然清晰。

这些改进贯穿音乐表达的全范围：独奏乐器中弦的触弦与运弓、鼓与低音的冲击力、密集电子编曲中的源分离，以及人声周围的空间感。Music 3.0 让这些元素都更接近一张完整制作唱片的聆听体验。

|  |  |  |
| --- | --- | --- |
| 用户prompt | 歌词 | Demo |
| 未来感旋律型 EDM / progressive house。关于记忆与数字身份的内省主歌，推向昂扬、以 hook 为驱动的副歌，配以富有感染力的主唱、明亮的分层合成器、脉动的低音、干脆的四踩鼓（four-on-the-floor）、细腻的 glitch 质感，以及宽阔而 polished 的音乐节混音。 | ``` [Verse 1] Upload my heart to the cloud tonight Save every spark of neon light If this body starts to fade away Let my code keep dancing in the data stream Stay [Chorus] Cloud copy of me Living on when these bones finally break free Every joke, every scar Every cheap memory we made Save it, save it Cloud copy of me If the screen goes dark, I’m still in the machine Every glitch, every dream Every version you ever did see Save it, save it [Verse 2] Tag every laugh in a secret folder Archive the nights we outran the thunder If the wiring turns to rust and gray Hit restore… press replay [Chorus] Cloud copy of me Living on when these bones finally break free Every joke, every scar Every cheap memory we made Save it, save it Cloud copy of me If the screen goes dark, I’m still in the machine Every glitch, every dream Every version you ever did see Save it, save it (oh) [Bridge – new, optional but recommended] Even the crashes, the late-night confessions The parts of me I never learned to mention Don’t let the silence swallow me whole Keep a ghost in the glow… So I never go [Final Chorus – softer / layered] Cloud copy of me Still laughing somewhere in the binary Every joke, every scar Every moment you saved for me Save it, save it Cloud copy of me When the lights go out, I’ll still be in the machine Dancing in the code that you still believe Save it… Save me ``` |  |
| 轻快的 bossa nova / 巴西流行（Brazilian pop），88 BPM，升 D 大调（D-flat major）。宁静冥想，渐渐生长出安静的自信，配以清澈亲密的女高音、松弛的咬字、轻柔上扬的 hook、柔和的吉他、钢琴、克制的低音和细腻的打击乐。 | ``` I breathe in peace, the simple joy of now I honor all the wisdom that the present allows My cup is full, I have everything I need right here Surrounded by soft connections, holding love so near I give and receive freely, a beautiful, steady flow I am seen, I am cherished, loved deeply as I go.  Now the ground is firm beneath my gentle feet A powerful knowing, perfectly complete. I listen close to the inner guidance I hold true.  I am steady light, unbothered by the noise outside I am confidence, where courage loves to reside I step forward now, with clear intent and heart ablaze I move mountains gently, in a thousand patient ways I succeed now, I achieve now, the outcome is clear and bright My inner strength is my constant guiding light.  My intuition speaks softly, a wisdom that guides my way The Universe unfolds beauty, every single day Everything arrives for me, in the perfect, knowing time I trust the flow of life, a rhythm so sublime My body is resilient, strong and full of grace My spirit is vibrant, illuminating every space.  Like a river flowing, perfectly on time Every drop is necessary, a beautiful design I release all worry, all the need to rush I am brave, I am persistent, and success is in my touch. My whole being is filled with strength, glowing, alive, and free.  I am steady light, unbothered by the noise outside I am confidence, where courage loves to reside I step forward now, with clear intent and heart ablaze I move mountains gently, in a thousand patient ways I succeed now, I achieve now, the outcome is clear and bright My inner strength is my constant guiding light.  "Strong and peaceful..." "Loved and thriving..." "The perfect time is always now..." "It is done, it is complete, it is well..." ``` |  |
| 温暖治愈的华语流行叙事曲（Mandopop ballad），情感深沉并带轻摇滚元素，中年成熟男女对唱，父母声线年龄约 50-70 岁；母亲以温暖成熟柔和的女声温柔领唱，音色略带岁月感、智慧而温柔的语气；父亲以深沉低稳的和声衬托，浑厚的成熟男声，略经风霜的沙哑低音区；以钢琴和丰沛弦乐开场，副歌随鼓和电吉他层层推进，结尾渐弱回到纯原声的温柔收束；情感真挚不做过度戏剧化，含蓄克制的中国式父母之爱，骄傲而温柔的不言明的鼓励，人声带浓重台湾口音，动情、真诚、温暖的父母视角，推向充满希望的提升式结尾，轻声耳语般的亲密尾奏如同轻唤归家的低语，怀旧而又赋能的亲情歌曲，老练有阅历的声线，不要年轻明亮的音色 | ``` [Intro] [Verse 1] 当她 在十岁以前 纯粹 天真的快乐 她总是 很多话 问个不停 [Verse 2] 在十 岁过了以后 就开 始有点忧愁 也变得话不多 不知道为什么  [Pre-Chorus] 她 终于 慢慢 长大 懵懂 的岁月 它 不停 歇  [Chorus 1] 她担心  这游戏 刚开始  玩不起 她担心  那游戏 刚开始  就结束 她担心  玩不起 这游戏  那游戏 这是梦 还是我 还是戏 ... [Chorus] 她 要  努 力 也 要  放 松 她要 她 的 幸 福 ~ 更要 她 的 快 乐 ~ 快 ~ 乐 在三十岁  以 后 会 是  怎 样？ 三十 而 立 呀 [Guitar Break] [Bridge] 她担心  这游戏 刚开始  玩不起 她担心  那游戏 刚开始  就结束 她担心  玩不起 这游戏  那游戏 这是梦 还是我 还是戏 ... [Chorus] 她 要  努 力 也 要  放 松 她要 她 的 幸 福 ~ 更要 她 的 快 乐 ~ 她 要  努 力 也 要  放 松 她要 她 的 幸 福 ~ 更要 她 的 快 乐 ~ 快 ~ 乐 在三十岁  以 后 会 是  怎 样？ 三十 而 立 呀  [Outro] ``` |  |

## 更自然的人声

人声往往是生成音乐的「合成感」最显眼的地方。高频伪影、僵硬的咬字、含混的发音和不自然的呼吸，即便在歌曲其他方面高度精致时，也会打断听众的情感连接。

Music 3.0 引入了一套新的音频渲染系统，旨在产出更自然、录音室品质的人声表演。结构化描述以细粒度刻画人声音色、呈现方式、气声与假声等技法、和声编排，以及延迟和 Auto-Tune 等效果。从全局与局部语言模型融合而来的连续隐状态把这些表演信息带入流匹配与 Flow-VAE 的生成过程。这些机制共同减少了生成人声中常见的高频数字伪影，同时改善了旋律、发音、呼吸和分层和声的可控性。

人声能更连贯地回应情绪与节奏的变化——从克制的主歌进入舒展的副歌，或从紧凑的节奏型咬字转入绵长开阔的旋律线。和声在主唱周围更自然地展开，呼吸成为表演的一部分，而不是叠在其上的人造痕迹。

|  |  |  |
| --- | --- | --- |
| 用户prompt | 歌词 | Demo |
| 原声 bossa nova / 民谣（folk），88 BPM，升 F 大调（F-sharp major）。宁静、田园而俏皮，副歌轻盈上扬，配以气声蜜意的女高音、松弛的说唱式吟唱咬字（speech-song phrasing）、指弹原声吉他、温暖的低音、轻打击乐，以及柔和萦绕的淡出。 | ``` [Verse] Blue sky whispers don\'t be late Green grass stretches like a plate The sun is winking through the trees A day like this is made to tease  [Chorus] Blue sky green grass sunny day Let the world spin the other way No need to run no need to stay Just blue sky green grass sunny day  [Verse 2] Birds are laughing high and wide Clouds are playing seek and hide I feel the breeze it tells a joke The kind that lingers when it\'s spoke  [Chorus] Blue sky green grass sunny day Troubles fade like shadows play Dance with time let it delay Just blue sky green grass sunny day  [Bridge] No map no plan no ticking clocks Barefoot feet on skipping rocks Catch the air hold it tight This is ours this feels right  [Chorus] Blue sky green grass sunny day Let the worries float away The world can wait come what may Just blue sky green grass sunny day ``` |  |
| 欢快的 funk / 当代 R&B，带 glossy 的 nu-disco 锋芒。俏皮夜色的主歌滑入喜庆的舞池副歌，配以顺滑深情的主唱、弹性低音、切分节奏吉他、明亮键盘、干脆鼓点、霓虹合成器点缀，以及温暖宽敞的俱乐部混音。 | ``` ( intro )  (Verse 1) Neon shadows on the avenue tonightTaxi horns and people passing in the lightThe rhythm of the street begins to playAnd every heartbeat’s dancing anyway  (Pre-Chorus) Footsteps echo down the boulevardA thousand stories written in the dark  (Chorus) Boogie in the city lights tonightFeel the rhythm glowing neon brightEvery heartbeat moving to the soundLost and free while the world spins aroundBoogie in the city lights so wildWhere every stranger dances like a childIn the glow where the midnight ignitesWe’re alive in the city lights  (Verse 2) Windows shining like a million starsMusic drifting softly from the barsEvery corner hides a melodyAnd every dream feels closer to be free  (Pre-Chorus) Streetlights flicker like a disco ballThe night is calling, hear the music call  (Chorus) Boogie in the city lights tonightFeel the rhythm glowing neon brightEvery heartbeat moving to the soundLost and free while the world spins aroundBoogie in the city lights so wildWhere every stranger dances like a childIn the glow where the midnight ignitesWe’re alive in the city lights  (Bridge) The skyline sways like a moving seaAnd the night keeps singing endlesslyFrom rooftop highs to subway beatsThe whole wide city’s dancing in the streets  (Final Chorus) Boogie in the city lights tonightLet the darkness turn to shining lightEvery dream is burning in the airAnd the music’s everywhere we stareBoogie till the sunrise paints the skiesWhile the rhythm never says goodbyeIn the glow where our hearts uniteWe keep dancing in the city lights  ( outro ) ``` |  |
| 温暖的流行摇滚 / 灵魂乐（soul），88 BPM，降 B 大调（B-flat major）。亲密的自省膨胀为一首关于自我价值的赋权颂歌，由老练的女中音（alto）领唱，带丝绒般的轻沙哑，配以模拟温暖感的吉他、沉稳的鼓、深情的键盘、抚慰的 hook，以及宽阔的电影感副歌。 | ``` Your face is in the mail You left it here  Forgot all about it  As you packed your gear  I know you don’t Want to hear this  But  I really don’t think  You need it   You look in the mirror  You don’t like what you see   You can’t leave home  Without it  You’re beautiful  I’m telling you  But  You just don’t believe  Me anyway  You look in the mirror  You don’t like what you see   You just think I’m saying it  Because I’m your mum  But really  It’s a fact  You don’t need that  Make up  Love   You look in the mirror  don’t like what you see  In that way You’re just like me  When I was so much younger I didn’t like me either  So I just looked away  Couldn’t face a mirror  without a frown Hated my own features  Couldn’t see a redeeming Thing in there  I looked in the mirror  I didn’t like what I saw   So you’re just like your mother  Just like any other  Teenager out there  It’s all the same nowadays  Everybody wants to be  Perfect  Nobody feels they’re worth it  Everybody needs to see that  We can’t all be beauty models   We all look in that mirror  Nobody likes what they see  But  We are all beautiful  On the inside  Our hearts and souls  Are what we need to show That essence within  Needs to be seen  True beauty shines within… ``` |  |

从创意意图与歌曲结构，到局部声学细节与最终音频渲染，Music 3.0 把音乐生成从「产出貌似合理的音频」推进到「实现完整而连贯的创意愿景」。我们期待听到你的作品。
