---
title: "Grok 3 Beta——推理智能体的时代"
title_en: "Grok 3 Beta — The Age of Reasoning Agents"
date: 2025-03-11
source: https://x.ai/news/grok-3
crawled: 2026-09-22
translated: 2026-09-22
---

# Grok 3 Beta——推理智能体的时代

> 原文：[Grok 3 Beta — The Age of Reasoning Agents](https://x.ai/news/grok-3) · xAI

2025 年 2 月 19 日

我们很高兴地揭晓 Grok 3 的早期预览——我们迄今最先进的模型，将卓越的推理与广泛的预训练知识融为一体。

---

## 来自 xAI 的新一代智能

我们很高兴介绍 Grok 3，我们迄今最先进的模型：将强大的推理与广泛的预训练知识融为一体。
Grok 3 在我们的 Colossus 超算集群上训练，算力达到此前最先进模型的 10 倍，在推理、数学、编码、世界知识和指令遵循任务上都有显著提升。
Grok 3 的推理能力经过大规模强化学习打磨，可以思考数秒到数分钟，纠正错误、探索替代方案并给出准确的答案。Grok 3 在学术基准和真实世界用户偏好上都处于领先水平，在 Chatbot Arena 取得 1402 的 Elo 分数。与之一同发布的还有 Grok 3 mini，它代表着高性价比推理的新前沿。两个模型仍在训练中，并将随着你的反馈快速演进。我们将在未来几天向用户推出 Grok 3，并同步提供其推理能力的早期预览。

## 更努力地思考：测试时算力与推理

今天，我们宣布两个 beta 推理模型：Grok 3 (Think) 和 Grok 3 mini (Think)。它们以前所未有的规模用强化学习（RL）训练，以打磨其思维链过程，从而以数据高效的方式实现高级推理。借助 RL，Grok 3 (Think) 学会了改进解题策略、通过回溯纠正错误、简化步骤，并利用预训练中习得的知识。就像人类处理复杂问题一样，Grok 3 (Think) 可以花上几秒到几分钟来推理，常常同时考虑多种方法、验证自己的解法，并评估如何精确满足题目要求。

两个模型仍在训练中，但已经在一系列基准上表现出色。我们在 2025 年美国数学邀请赛（AIME）上测试了这些模型——该赛事于 7 天前的 2 月 12 日刚刚发布。在最高档测试时算力（cons@64）下，Grok 3 (Think) 在这项竞赛中取得 93.3%。Grok 3 (Think) 还在研究生级专家推理（GPQA）上取得 84.6%，在衡量代码生成与问题解决的 LiveCodeBench 上取得 79.4%。此外，Grok 3 mini 在不需要太多世界知识的 STEM 任务上达到了高性价比推理的新前沿，在 AIME 2024 上取得 95.8%，在 LiveCodeBench 上取得 80.4%。

### AIME'25

竞赛数学

### AIME'24

竞赛数学

### GPQA

研究生级防搜索问答（Diamond）

### LCB

代码生成：2024/10/1 - 2025/2/1

### MMMU

多模态理解

要使用 Grok 3 的推理能力，只需按下 `Think` 按钮。
Grok 3 (Think) 的思维完全开放，用户不仅可以检查最终答案，还可以检查模型本身的推理过程。
我们发现 Grok 3 (Think) 的表现可以泛化到多样的问题领域。以下是一些 Grok 3 推理示例。

### 研究样本

编码ASCII 艺术谜题数学

---

做一个混合两款经典游戏的游戏。用 pygame 实现，并且要做得好看。

思考了 6 秒

点击阅读我的思维

以下是你所提需求的完整解决方案：一个名为 "Break-Pong" 的 Pygame 游戏，融合了 **Pong** 和 **Breakout** 的元素。在这款游戏中，两名玩家分别控制屏幕两侧的挡板，击打球以打碎中央的砖墙。打碎砖块以及让球穿过对方挡板均可得分。游戏包含流畅的动画、多彩的画面和粒子效果，以提升视觉吸引力。实现如下：

### 代码实现

python

```
import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
BALL_SIZE = 20
BRICK_WIDTH = 40
BRICK_HEIGHT = 20
BRICK_COLUMNS = 5
BRICK_ROWS = 30  # 600 / 20 = 30 rows to span screen height
PADDLE_SPEED = 5
BALL_SPEED = 5
TARGET_SCORE = 50

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 100, 100)
GREEN = (100, 255, 100)
BLUE = (100, 100, 255)

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Break-Pong")
clock = pygame.time.Clock()

# Paddle class
class Paddle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.speed = PADDLE_SPEED

    def move(self, up=True):
        if up:
            self.y -= self.speed
        else:
            self.y += self.speed
        # Keep paddle within screen bounds
        self.y = max(0, min(SCREEN_HEIGHT - self.height, self.y))

    def draw(self):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height))

# Ball class
class Ball:
    def __init__(self):
        self.reset()
        self.size = BALL_SIZE

    def move(self):
        self.x += self.vel_x
        self.y += self.vel_y

    def reset(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.vel_x = random.choice([-1, 1]) * BALL_SPEED
        self.vel_y = random.choice([-1, 1]) * BALL_SPEED
        self.last_hit = None  # Tracks which paddle last hit the ball

    def draw(self):
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.size // 2)

# Brick class
class Brick:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = BRICK_WIDTH
        self.height = BRICK_HEIGHT
        self.color = random.choice([RED, GREEN, BLUE])
        self.intact = True

    def draw(self):
        if self.intact:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

# Particle class for visual effects
class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(2, 5)
        self.vel_x = random.uniform(-2, 2)
        self.vel_y = random.uniform(-2, 2)
        self.life = 30  # Frames until particle disappears
        self.color = random.choice([RED, GREEN, BLUE])

    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.life -= 1

    def draw(self):
        if self.life > 0:
            alpha = int((self.life / 30) * 255)  # Fade out effect
            surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            pygame.draw.circle(surface, (*self.color, alpha), (self.size // 2, self.size // 2), self.size // 2)
            screen.blit(surface, (int(self.x), int(self.y)))

# Collision detection functions
def ball_collides_with_paddle(ball, paddle):
    return (ball.x - ball.size // 2 < paddle.x + paddle.width and
            ball.x + ball.size // 2 > paddle.x and
            ball.y - ball.size // 2 < paddle.y + paddle.height and
            ball.y + ball.size // 2 > paddle.y)

def ball_collides_with_brick(ball, brick):
    if not brick.intact:
        return False
    return (ball.x - ball.size // 2 < brick.x + brick.width and
            ball.x + ball.size // 2 > brick.x and
            ball.y - ball.size // 2 < brick.y + brick.height and
            ball.y + ball.size // 2 > brick.y)

# Initialize game objects
left_paddle = Paddle(50, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
right_paddle = Paddle(SCREEN_WIDTH - 50 - PADDLE_WIDTH, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
ball = Ball()

# Create central brick wall
bricks = []
brick_start_x = SCREEN_WIDTH // 2 - (BRICK_COLUMNS * BRICK_WIDTH) // 2
for col in range(BRICK_COLUMNS):
    for row in range(BRICK_ROWS):
        bricks.append(Brick(brick_start_x + col * BRICK_WIDTH, row * BRICK_HEIGHT))

# Scores and particles
left_score = 0
right_score = 0
particles = []

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Paddle movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        left_paddle.move(up=True)
    if keys[pygame.K_s]:
        left_paddle.move(up=False)
    if keys[pygame.K_UP]:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN]:
        right_paddle.move(up=False)

    # Update ball
    ball.move()

    # Ball collisions with top/bottom walls
    if ball.y - ball.size // 2 <= 0 or ball.y + ball.size // 2 >= SCREEN_HEIGHT:
        ball.vel_y = -ball.vel_y

    # Ball collisions with paddles
    if ball_collides_with_paddle(ball, left_paddle):
        ball.vel_x = abs(ball.vel_x)  # Ensure ball moves right
        ball.last_hit = 'left'
    elif ball_collides_with_paddle(ball, right_paddle):
        ball.vel_x = -abs(ball.vel_x)  # Ensure ball moves left
        ball.last_hit = 'right'

    # Ball collisions with bricks
    for brick in bricks:
        if ball_collides_with_brick(ball, brick):
            brick.intact = False
            ball.vel_x = -ball.vel_x
            # Add particles
            for _ in range(5):
                particles.append(Particle(brick.x + brick.width // 2, brick.y + brick.height // 2))
            # Award points
            if ball.last_hit == 'left':
                left_score += 1
            elif ball.last_hit == 'right':
                right_score += 1

    # Ball off screen
    if ball.x - ball.size // 2 <= 0:
        right_score += 5
        ball.reset()
    elif ball.x + ball.size // 2 >= SCREEN_WIDTH:
        left_score += 5
        ball.reset()

    # Update particles
    for particle in particles[:]:
        particle.update()
        if particle.life <= 0:
            particles.remove(particle)

    # Draw everything
    screen.fill(BLACK)
    for brick in bricks:
        brick.draw()
    left_paddle.draw()
    right_paddle.draw()
    ball.draw()
    for particle in particles:
        particle.draw()

    # Draw scores
    font = pygame.font.Font(None, 36)
    left_text = font.render(f"Left: {left_score}", True, WHITE)
    right_text = font.render(f"Right: {right_score}", True, WHITE)
    screen.blit(left_text, (50, 20))
    screen.blit(right_text, (SCREEN_WIDTH - 150, 20))

    # Check for game over
    if left_score >= TARGET_SCORE or right_score >= TARGET_SCORE:
        winner = "Left" if left_score >= TARGET_SCORE else "Right"
        game_over_text = font.render(f"{winner} Wins!", True, WHITE)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False

    pygame.display.flip()
    clock.tick(60)

# Cleanup
pygame.quit()
sys.exit()
```

---

### 如何运行

1. 确保你已安装 Python 和 Pygame（`pip install pygame`）。
2. 把代码复制到一个 `.py` 文件中（如 `break_pong.py`）。
3. 用 Python 运行该文件（如 `python break_pong.py`）。

---

### 玩法说明

- **操作**：
  - 左侧挡板：`W`（上）、`S`（下）
  - 右侧挡板：`Up Arrow`（上）、`Down Arrow`（下）
- **目标**：打碎中央砖墙上的砖块，并让球穿过对方挡板得分。先得到 50 分者获胜。

---

### 特性

- **Pong 元素**：两块挡板来回击球，球穿过对方挡板时得分。
- **Breakout 元素**：一面砖墙，球撞击即可打碎砖块。
- **视觉吸引力**：
  - 挡板和球的移动流畅。
  - 色彩缤纷的砖块（红、绿、蓝）随机分配。
  - 砖块破碎时的粒子效果，粒子渐隐，画面更有动感。
  - 清晰的分数显示和游戏结束提示。

---

### 可进一步增强

若想让游戏更漂亮、更吸引人，可以考虑：

- 添加音效（如弹跳声、破碎声）。
- 实现道具（如更大的挡板、更快的球），从特殊砖块中掉落。
- 添加背景渐变或图案。
- 加入开始菜单和更平滑的过渡。

这个实现提供了一个有趣、美观的 Pong 与 Breakout 混合游戏，满足你的需求！祝你玩 "Break-Pong" 愉快！

[](https://data.x.ai/game-demo-nobg.mp4)

## 大规模预训练

关闭推理时，Grok 3 可以给出即时、高质量的回答。在非推理模型中，Grok 3 在多项学术基准上取得最先进的结果，包括：研究生级科学知识（GPQA）、通识知识（MMLU-Pro）、数学竞赛题（AIME）。Grok 3 还在图像理解（MMMU）和视频理解（EgoSchema）任务上表现出色。

| 基准 | Grok 3 Beta | Grok 3 mini Beta | Gemini 2.0 | DeepSeek-V3 | GPT 4o | Claude 3.5 Sonnet |
| --- | --- | --- | --- | --- | --- | --- |
| AIME'24 | 52.2% | 39.7% | — | 39.2% | 9.3% | 16.0% |
| GPQA | 75.4% | 66.2% | 64.7% | 59.1% | 53.6% | 65.0% |
| LCB | 57.0% | 41.5% | 36.0% | 33.1% | 32.3% | 40.2% |
| MMLU-pro | 79.9% | 78.9% | 79.1% | 75.9% | 72.6% | 78.0% |
| LOFT (128k) | 83.3% | 83.1% | 75.6% | — | 78.0% | 69.9% |
| SimpleQA | 43.6% | 21.7% | 44.3% | 24.9% | 38.2% | 28.4% |
| MMMU | 73.2% | 69.4% | 72.7% | — | 69.1% | 70.4% |
| EgoSchema | 74.5% | 74.3% | 71.9% | — | 72.2% | — |

凭借 100 万 token 的上下文窗口——比我们之前的模型大 8 倍——Grok 3 可以处理长篇文档、应对复杂提示词，同时保持指令遵循的准确性。
在面向长上下文 RAG 用例的 LOFT (128k) 基准上，Grok 3 取得了最先进的准确率（在 12 项多样任务上取平均），展现了强大的信息检索能力。

Grok 3 还展现了更佳的事实准确性和更强的风格控制。以代号 `chocolate` 测试时，Grok 3 的早期版本登顶 LMArena Chatbot Arena 排行榜，在所有类别的 Elo 分数上全面超越对手。随着规模继续扩大，我们正准备在 200,000 GPU 的集群上训练更大的模型。

![Chatbot Arena 分数](/_next/image?url=%2Fimages%2Fnews%2Farena.webp&w=1200&q=75)Chatbot Arena 分数

## Grok 智能体：推理与工具使用的结合

要理解宇宙，我们必须让 Grok 与世界连接。配备代码解释器和互联网访问能力后，Grok 3 系列模型学会了查询缺失的上下文、动态调整方法，并根据反馈改进推理。

作为迈向这一愿景的第一步，我们正在推出 `DeepSearch`——我们的第一个智能体。它是一个闪电般快速的 AI 智能体，旨在人类知识的全部语料中不懈追寻真相。`DeepSearch` 的设计目标是综合关键信息、对相互矛盾的事实与观点进行推理，并从复杂中提炼清晰。无论你需要获取最新的实时新闻、为自己的社交烦恼寻求建议，还是开展深入的科学研究，`DeepSearch` 都将带你远超一次浏览器搜索。它最终的总结轨迹会形成一份简洁而全面的报告，帮助你跟上这个从不停歇的世界。

### DeepSearch 演示

[](https://data.x.ai/tesla-high-compress.mp4)

[Grok.com](https://grok.com)如果我在 2011 年买了 $TSLA 会怎样？

[](https://data.x.ai/xgrok3-high-compress.mp4)

[𝕏.com](https://x.com/i/grok)X 用户对 Grok 3 发布的反应如何？

[](https://data.x.ai/geometry-high-compress.mp4)

[Grok.com](https://grok.com)给我孩子推荐一些好的在线数学资源。

## Grok 3 API 即将推出

未来几周，我们将通过 API 平台发布 Grok 3 和 Grok 3 mini，提供标准模型和推理模型的访问。`DeepSearch` 也将通过我们的 API 向企业合作伙伴发布。

## Grok 3 的下一步是什么？

Grok 3 的训练仍在进行中，未来几个月计划频繁更新。我们很高兴在[企业 API](https://console.x.ai) 中推出新功能，包括工具使用、代码执行和高级智能体能力。继上周发布 [RMF](https://x.ai/documents/2025.02.20-RMF-Draft.pdf)（风险管理框架）之后，我们尤其有兴趣加速训练期间可扩展监督与对抗鲁棒性方面的进展。

Grok 3 现已向 [𝕏](https://x.com/i/grok) 和 [Grok.com](https://grok.com) 上的 𝕏 Premium 和 Premium+ 用户开放。
𝕏 Premium+ 用户还将立即获得 `Think` 和 `DeepSearch` 的使用权限。
此外，Grok 3 的能力正带着用量限制向所有 Grok 用户推出。
𝕏 Premium+ 用户将拥有更高的限额，并可使用高级能力。

## 加入这段旅程

自 2023 年 11 月发布 Grok 1 以来，xAI 这支小而人才密集的团队推动了历史性的进步，使我们站上了 AI 创新的前沿。借助 Grok 3，我们正在用扩建后的 Colossus 超算集群推进核心推理能力，更多令人兴奋的进展即将到来。如果你热衷于为人类的未来构建 AI，欢迎在 [x.ai/careers](/careers) 申请加入我们的团队。

在以下平台试用 Grok

[网页](https://grok.com)

[iOS](https://apps.apple.com/app/grok/id6670324846)

[Android](https://play.google.com/store/apps/details?id=ai.x.grok&hl=en)

[Grok on X](https://x.com/i/grok)

产品

[Grok](/grok)

[API](/api)

公司

[公司简介](/company)

[招聘](/careers)

[联系我们](/contact)

[新闻](/news)

资源

[状态](https://status.x.ai)

[隐私政策](/privacy-policy)

[安全](/security)

[法律](/legal)
