---
title: "如何为 Claude 创建 Skills：步骤与示例"
title_en: "How to create Skills for Claude: steps and examples"
source: https://claude.com/blog/how-to-create-skills-key-steps-limitations-and-examples/
crawled: 2026-09-14
translated: 2026-09-14
---

# 如何为 Claude 创建 Skills：步骤与示例

> 原文：[How to create Skills for Claude: steps and examples](https://claude.com/blog/how-to-create-skills-key-steps-limitations-and-examples/) · Claude 博客

[Skills](https://www.claude.com/blog/skills) 是扩展 Claude 在特定任务或领域上能力的自定义指令。

当你通过一个 [SKILL.md](http://skill.md) 文件创建技能（skill）时，你是在教 Claude 如何更有效地处理特定场景。技能的力量在于：它们能够编码机构知识、标准化输出，并处理复杂的多步骤工作流——否则，这些工作流要么需要反复解释，要么需要投入构建一个自定义智能体。

了解如何创建技能，把 Claude 从通用助手变成针对你特定工作流的专家——可以使用我们的 [skill creator](https://github.com/anthropics/skills/tree/main/skill-creator) 模板，也可以手动创建。（Pro tip：为了省事，我们推荐先用这个模板搭建你的 [SKILL.md](http://skill.md) 文件，再在其基础上裁剪。）

## **用 5 个步骤创建技能**

遵循这套结构化方法，构建触发更可靠的技能。

### **1. 理解核心要求**

在动笔之前，先弄清楚你的技能解决什么问题。好的技能以可度量的结果应对具体的需求。"从 PDF 中提取财务数据并格式化为 CSV"胜过"帮我处理财务上的事"，因为它明确了输入格式、操作和预期输出。

先问自己：这个技能完成什么具体任务？什么触发条件应当激活它？成功是什么样子？有哪些边缘情况或限制？

### **2. 写名称**

你的技能需要三个核心组件：**name**（清晰的标识符）、**description**（何时激活）和 **instructions**（如何执行）。实际上，name 和 description 是 [SKILL.md](http://skill.md) 文件中仅有的影响触发的部分——所谓触发，就是 Claude 能够调用一个技能来获取专业知识或工作流。

名称应当直白且具有描述性。使用小写加连字符（例如 pdf-editor、brand-guidelines）。保持简短清晰。

### **3. 写 description 字段**

description 决定你的技能何时激活，因此它是最关键的组件。从 Claude 的视角来写，聚焦于触发条件、能力和使用场景。

一个好的 description 需要平衡几个要素：具体的能力、清晰的触发条件、相关的上下文，以及边界。

**弱的 description**：

```
This skill helps with PDFs and documents.
```

**强的 description**：

```
Comprehensive PDF manipulation toolkit for extracting text and tables, creating new PDFs, merging/splitting documents, and handling forms. When Claude needs to fill in a PDF form or programmatically process, generate, or analyze PDF documents at scale. Use for document workflows and batch operations. Not for simple PDF viewing or basic conversions.
```

更强的版本给了 Claude 多个数据点：具体的动词（extract、create、merge）、具体的使用场景（表单填写、批量操作），以及清晰的边界（不用于简单查看）。

### **4. 写主要指令**

你的指令应当结构化、易于浏览、可执行。使用 markdown 标题、用要点列出选项、用代码块给出示例。

用清晰的层级组织结构：概述、前置条件、执行步骤、示例、错误处理和限制。把复杂的工作流拆成具有明确输入输出的独立阶段。

包含展示正确用法的具体示例。明确说明技能做不到什么，以防误用并管理预期。你的 [SKILL.md](http://skill.md) 文件还可以包含额外的参考文件和资源，为技能触发时你要求智能体做的事情提供更清晰的指导。

### **5. 上传你的技能**

根据你构建所用的 Claude 产品形态，按以下方式上传你的技能：

- [Claude.ai](http://claude.ai)（Claude 应用）：进入 **Settings** 并在其中添加你的自定义技能。自定义技能需要启用代码执行的 Pro、Max、Team 或 Enterprise 计划。在这里上传的技能是个人的——不在全组织范围共享，也无法由管理员集中管理。
- [Claude Code](https://www.claude.com/product/claude-code)：在你的插件或项目根目录下创建 skills/ 目录，添加包含 SKILL.md 文件的技能文件夹。插件安装后，Claude 会自动发现并使用它们。示例结构：

```
my-project/
├── skills/
│   └── my-skill/
│       └── SKILL.md
```

- [Claude Developer Platform](https://www.claude.com/platform/api)：通过 Skills API（/v1/skills 端点）上传技能。使用带有必需 beta 头的 POST 请求：

```
curl -X POST "https://api.anthropic.com/v1/skills" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: skills-2025-10-02" \
  -F "display_title=My Skill Name" \
  -F "files[]=@my-skill/SKILL.md;filename=my-skill/SKILL.md"
```

### **4. 测试与验证**

在部署之前，用真实场景测试你的技能。系统化的测试能暴露指令中的缺口、description 中的歧义，以及只有在实际使用中才会浮现的意外边缘情况。

创建一个覆盖三类场景的测试矩阵：

- **正常操作**：用技能理应完美处理的典型请求来测试。如果你构建了一个财务分析技能，试试"分析微软最新财报"或"为这份 10-K 文件构建一个 datapack"。这些基线测试确认你的指令按预期工作。
- **边缘情况**：用不完整或异常的输入测试。数据缺失时会怎样？文件格式出乎意料时会怎样？用户给出模糊指令时会怎样？你的技能应当优雅地处理这些情况——要么产出降级但仍有用的输出，要么说明继续进行需要什么。
- **超出范围的请求**：用看起来相关、但不应该触发你技能的任务来测试。如果你构建了一个 NDA 审查技能，试试请求"审查这份雇佣协议"或"分析这份租约"。技能应保持休眠，让其他技能或 Claude 的通用能力来处理请求。

考虑实施以下测试，进行更深入的验证：

- **触发测试**：技能是否在预期时激活？同时用显式请求（"用财务 datapack 技能分析这家公司"）和自然请求（"帮我理解这家公司的财务状况"）来测试。无关时它是否保持不激活？一个范围划定良好的技能知道何时不该激活。用相似但有区别的请求来验证边界。
- **功能测试**：包括输出一致性（相似输入的多次运行是否产生可比的结果？）、可用性（不熟悉该领域的人能否成功使用？）和文档准确性（你的示例与实际行为是否一致？）。

### **5. 根据使用情况迭代**

监控你的技能在真实使用中的表现。如果触发不稳定，就打磨 description。如果输出出现意外的不一致，就澄清 instructions。与提示词一样，最好的技能是在实际应用中演化出来的。

## **创建技能的通用最佳实践**

这些原则帮助你创建可维护、可复用、真正有用（而非纸上谈兵）的技能。

### **从使用场景出发**

不要凭空猜想地写技能。在有真实的、重复的任务时才构建它们。最好的技能解决你经常遇到的问题。

创建技能之前先问：这个任务我至少做过五次吗？以后还会至少再做十次吗？如果是，技能就值得做。

### **定义成功标准——并把它写进技能**

告诉 Claude 好的产出是什么样子。如果你在创建财务报告技能，就明确必需的章节、格式标准、校验检查和质量阈值。把这些标准写进你的 instructions，让 Claude 可以自查。

### **使用 Skill-Creator 技能**

[skill-creator 技能](https://github.com/anthropics/skills/tree/main/skill-creator)会引导你创建结构良好的技能。它会提出澄清问题、建议改进 description，并帮助正确排版 instructions。它可以在 [GitHub 上的 Skills 仓库](https://github.com/anthropics/skills)中找到，也可以直接通过 [Claude.ai](http://claude.ai) 使用；对你最初的几个技能尤其有价值。

## **技能的限制与注意事项**

理解技能的工作方式——以及它们的边界——有助于你设计更有效的技能并设定合理的预期。

### **技能触发**

Claude 会把技能 description 与你的请求进行比对来判断相关性。这不是关键词匹配——Claude 理解语义关系。不过，模糊的 description 会降低触发的准确性。

多个技能可以同时激活，只要它们处理的是复杂任务的不同方面。过于宽泛的 description 会导致不恰当的激活，而遗漏使用场景则会导致该触发时没有触发。

### **合适的文件大小**

编写技能时，避免用不必要的内容撑大上下文窗口。考虑每条信息是需要每次都加载，还是只需按条件加载。

使用"菜单"式做法：如果你的技能涵盖多个不同的流程或选项，SKILL.md 应当描述有哪些可用内容，并用相对路径引用每个流程各自的独立文件。Claude 随后只读取与用户任务相关的文件，在本次对话中不碰其他文件。

这些独立文件不必代表互斥的路径。关键原则是把内容拆成合理的小块，让 Claude 根据手头任务选择需要的内容。

## **真实的技能示例**

### **技能示例 #1：**[**docx 创建技能**](https://github.com/anthropics/skills/tree/main/document-skills/docx)

```
#---
name: docx
description: "Comprehensive document creation, editing, and analysis with support for tracked changes, comments, formatting preservation, and text extraction. When Claude needs to work with professional documents (.docx files) for: (1) Creating new documents, (2) Modifying or editing content, (3) Working with tracked changes, (4) Adding comments, or any other document tasks"
license: Proprietary. LICENSE.txt has complete terms
---

# DOCX creation, editing, and analysis

## Overview

A user may ask you to create, edit, or analyze the contents of a .docx file. A .docx file is essentially a ZIP archive containing XML files and other resources that you can read or edit. You have different tools and workflows available for different tasks.

## Workflow Decision Tree

### Reading/Analyzing Content
Use "Text extraction" or "Raw XML access" sections below

### Creating New Document
Use "Creating a new Word document" workflow

### Editing Existing Document
- **Your own document + simple changes**
  Use "Basic OOXML editing" workflow

- **Someone else's document**
  Use **"Redlining workflow"** (recommended default)

- **Legal, academic, business, or government docs**
  Use **"Redlining workflow"** (required)

## Reading and analyzing content

### Text extraction
If you just need to read the text contents of a document, you should convert the document to markdown using pandoc. Pandoc provides excellent support for preserving document structure and can show tracked changes:

```bash
# Convert document to markdown with tracked changes
pandoc --track-changes=all path-to-file.docx -o output.md
# Options: --track-changes=accept/reject/all
```

### Raw XML access
You need raw XML access for: comments, complex formatting, document structure, embedded media, and metadata. For any of these features, you'll need to unpack a document and read its raw XML contents.

#### Unpacking a file
`python ooxml/scripts/unpack.py <office_file> <output_directory>`

#### Key file structures
* `word/document.xml` - Main document contents
* `word/comments.xml` - Comments referenced in document.xml
* `word/media/` - Embedded images and media files
* Tracked changes use `<w:ins>` (insertions) and `<w:del>` (deletions) tags

## Creating a new Word document

When creating a new Word document from scratch, use **docx-js**, which allows you to create Word documents using JavaScript/TypeScript.

### Workflow
1. **MANDATORY - READ ENTIRE FILE**: Read [`docx-js.md`](docx-js.md) (~500 lines) completely from start to finish. **NEVER set any range limits when reading this file.** Read the full file content for detailed syntax, critical formatting rules, and best practices before proceeding with document creation.
2. Create a JavaScript/TypeScript file using Document, Paragraph, TextRun components (You can assume all dependencies are installed, but if not, refer to the dependencies section below)
3. Export as .docx using Packer.toBuffer()

## Editing an existing Word document

When editing an existing Word document, use the **Document library** (a Python library for OOXML manipulation). The library automatically handles infrastructure setup and provides methods for document manipulation. For complex scenarios, you can access the underlying DOM directly through the library.

### Workflow
1. **MANDATORY - READ ENTIRE FILE**: Read [`ooxml.md`](ooxml.md) (~600 lines) completely from start to finish. **NEVER set any range limits when reading this file.** Read the full file content for the Document library API and XML patterns for directly editing document files.
2. Unpack the document: `python ooxml/scripts/unpack.py <office_file> <output_directory>`
3. Create and run a Python script using the Document library (see "Document Library" section in ooxml.md)
4. Pack the final document: `python ooxml/scripts/pack.py <input_directory> <office_file>`

The Document library provides both high-level methods for common operations and direct DOM access for complex scenarios.

## Redlining workflow for document review

This workflow allows you to plan comprehensive tracked changes using markdown before implementing them in OOXML. **CRITICAL**: For complete tracked changes, you must implement ALL changes systematically.

**Batching Strategy**: Group related changes into batches of 3-10 changes. This makes debugging manageable while maintaining efficiency. Test each batch before moving to the next.

**Principle: Minimal, Precise Edits**
When implementing tracked changes, only mark text that actually changes. Repeating unchanged text makes edits harder to review and appears unprofessional. Break replacements into: [unchanged text] + [deletion] + [insertion] + [unchanged text]. Preserve the original run's RSID for unchanged text by extracting the `<w:r>` element from the original and reusing it.

Example - Changing "30 days" to "60 days" in a sentence:
```python
# BAD - Replaces entire sentence
'<w:del><w:r><w:delText>The term is 30 days.</w:delText></w:r></w:del><w:ins><w:r><w:t>The term is 60 days.</w:t></w:r></w:ins>'

# GOOD - Only marks what changed, preserves original <w:r> for unchanged text
'<w:r w:rsidR="00AB12CD"><w:t>The term is </w:t></w:r><w:del><w:r><w:delText>30</w:delText></w:r></w:del><w:ins><w:r><w:t>60</w:t></w:r></w:ins><w:r w:rsidR="00AB12CD"><w:t> days.</w:t></w:r>'
```

### Tracked changes workflow

1. **Get markdown representation**: Convert document to markdown with tracked changes preserved:
   ```bash
   pandoc --track-changes=all path-to-file.docx -o current.md
   ```

2. **Identify and group changes**: Review the document and identify ALL changes needed, organizing them into logical batches:

   **Location methods** (for finding changes in XML):
   - Section/heading numbers (e.g., "Section 3.2", "Article IV")
   - Paragraph identifiers if numbered
   - Grep patterns with unique surrounding text
   - Document structure (e.g., "first paragraph", "signature block")
   - **DO NOT use markdown line numbers** - they don't map to XML structure

   **Batch organization** (group 3-10 related changes per batch):
   - By section: "Batch 1: Section 2 amendments", "Batch 2: Section 5 updates"
   - By type: "Batch 1: Date corrections", "Batch 2: Party name changes"
   - By complexity: Start with simple text replacements, then tackle complex structural changes
   - Sequential: "Batch 1: Pages 1-3", "Batch 2: Pages 4-6"

3. **Read documentation and unpack**:
   - **MANDATORY - READ ENTIRE FILE**: Read [`ooxml.md`](ooxml.md) (~600 lines) completely from start to finish. **NEVER set any range limits when reading this file.** Pay special attention to the "Document Library" and "Tracked Change Patterns" sections.
   - **Unpack the document**: `python ooxml/scripts/unpack.py <file.docx> <dir>`
   - **Note the suggested RSID**: The unpack script will suggest an RSID to use for your tracked changes. Copy this RSID for use in step 4b.

4. **Implement changes in batches**: Group changes logically (by section, by type, or by proximity) and implement them together in a single script. This approach:
   - Makes debugging easier (smaller batch = easier to isolate errors)
   - Allows incremental progress
   - Maintains efficiency (batch size of 3-10 changes works well)

   **Suggested batch groupings:**
   - By document section (e.g., "Section 3 changes", "Definitions", "Termination clause")
   - By change type (e.g., "Date changes", "Party name updates", "Legal term replacements")
   - By proximity (e.g., "Changes on pages 1-3", "Changes in first half of document")

   For each batch of related changes:

   **a. Map text to XML**: Grep for text in `word/document.xml` to verify how text is split across `<w:r>` elements.

   **b. Create and run script**: Use `get_node` to find nodes, implement changes, then `doc.save()`. See **"Document Library"** section in ooxml.md for patterns.

   **Note**: Always grep `word/document.xml` immediately before writing a script to get current line numbers and verify text content. Line numbers change after each script run.

5. **Pack the document**: After all batches are complete, convert the unpacked directory back to .docx:
   ```bash
   python ooxml/scripts/pack.py unpacked reviewed-document.docx
   ```

6. **Final verification**: Do a comprehensive check of the complete document:
   - Convert final document to markdown:
     ```bash
     pandoc --track-changes=all reviewed-document.docx -o verification.md
     ```
   - Verify ALL changes were applied correctly:
     ```bash
     grep "original phrase" verification.md  # Should NOT find it
     grep "replacement phrase" verification.md  # Should find it
     ```
   - Check that no unintended changes were introduced


## Converting Documents to Images

To visually analyze Word documents, convert them to images using a two-step process:

1. **Convert DOCX to PDF**:
   ```bash
   soffice --headless --convert-to pdf document.docx
   ```

2. **Convert PDF pages to JPEG images**:
   ```bash
   pdftoppm -jpeg -r 150 document.pdf page
   ```
   This creates files like `page-1.jpg`, `page-2.jpg`, etc.

Options:
- `-r 150`: Sets resolution to 150 DPI (adjust for quality/size balance)
- `-jpeg`: Output JPEG format (use `-png` for PNG if preferred)
- `-f N`: First page to convert (e.g., `-f 2` starts from page 2)
- `-l N`: Last page to convert (e.g., `-l 5` stops at page 5)
- `page`: Prefix for output files

Example for specific range:
```bash
pdftoppm -jpeg -r 150 -f 2 -l 5 document.pdf page  # Converts only pages 2-5
```

## Code Style Guidelines
**IMPORTANT**: When generating code for DOCX operations:
- Write concise code
- Avoid verbose variable names and redundant operations
- Avoid unnecessary print statements

## Dependencies

Required dependencies (install if not available):

- **pandoc**: `sudo apt-get install pandoc` (for text extraction)
- **docx**: `npm install -g docx` (for creating new documents)
- **LibreOffice**: `sudo apt-get install libreoffice` (for PDF conversion)
- **Poppler**: `sudo apt-get install poppler-utils` (for pdftoppm to convert PDF to images)
- **defusedxml**: `pip install defusedxml` (for secure XML parsing)
```

**它的亮点**：提供了清晰的决策树，根据任务类型把 Claude 路由到正确的工作流；使用渐进式披露（progressive disclosure）让主文件保持精简，只在需要时才引用详细的实现文件；并包含具体的正/反示例，清楚展示了如何实现修订记录（tracked changes）这类复杂模式。

### **技能示例 #2：**[**Brand guidelines**](https://github.com/anthropics/skills/blob/main/brand-guidelines/SKILL.md?plain=1)

```
#name: brand-guidelines
description: Applies Anthropic's official brand colors and typography to any sort of artifact that may benefit from having Anthropic's look-and-feel. Use it when brand colors or style guidelines, visual formatting, or company design standards apply.
license: Complete terms in LICENSE.txt
---

# Anthropic Brand Styling

## Overview

To access Anthropic's official brand identity and style resources, use this skill.

**Keywords**: branding, corporate identity, visual identity, post-processing, styling, brand colors, typography, Anthropic brand, visual formatting, visual design

## Brand Guidelines

### Colors

**Main Colors:**

- Dark: `#141413` - Primary text and dark backgrounds
- Light: `#faf9f5` - Light backgrounds and text on dark
- Mid Gray: `#b0aea5` - Secondary elements
- Light Gray: `#e8e6dc` - Subtle backgrounds

**Accent Colors:**

- Orange: `#d97757` - Primary accent
- Blue: `#6a9bcc` - Secondary accent
- Green: `#788c5d` - Tertiary accent

### Typography

- **Headings**: Poppins (with Arial fallback)
- **Body Text**: Lora (with Georgia fallback)
- **Note**: Fonts should be pre-installed in your environment for best results

## Features

### Smart Font Application

- Applies Poppins font to headings (24pt and larger)
- Applies Lora font to body text
- Automatically falls back to Arial/Georgia if custom fonts unavailable
- Preserves readability across all systems

### Text Styling

- Headings (24pt+): Poppins font
- Body text: Lora font
- Smart color selection based on background
- Preserves text hierarchy and formatting

### Shape and Accent Colors

- Non-text shapes use accent colors
- Cycles through orange, blue, and green accents
- Maintains visual interest while staying on-brand

## Technical Details

### Font Management

- Uses system-installed Poppins and Lora fonts when available
- Provides automatic fallback to Arial (headings) and Georgia (body)
- No font installation required - works with existing system fonts
- For best results, pre-install Poppins and Lora fonts in your environment

### Color Application

- Uses RGB color values for precise brand matching
- Applied via python-pptx's RGBColor class
- Maintains color fidelity across different systems
```

**它的亮点**：提供了 Claude 本身并不具备的精确、可执行的信息（确切的十六进制色值、字体名称、字号阈值），以及一个清晰的 description，既告诉 Claude 它做什么，也告诉它何时触发。

**它的亮点**：有清晰边界的创作能力、内置的版权保护、面向非音乐人的技术脚手架、质量标准。

### **技能示例 #3：**[**frontend design 技能**](https://www.claude.com/blog/improving-frontend-design-through-skills)

```
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, or applications. Generates creative, polished code that avoids generic AI aesthetics.
license: Complete terms in LICENSE.txt
---

This skill guides creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details and creative choices.

The user provides frontend requirements: a component, page, application, or interface to build. They may include context about the purpose, audience, or technical constraints.

## Design Thinking

Before coding, understand the context and commit to a BOLD aesthetic direction:
- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian, etc. There are so many flavors to choose from. Use these for inspiration but design one that is true to the aesthetic direction.
- **Constraints**: Technical requirements (framework, performance, accessibility).
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work - the key is intentionality, not intensity.

Then implement working code (HTML/CSS/JS, React, Vue, etc.) that is:
- Production-grade and functional
- Visually striking and memorable
- Cohesive with a clear aesthetic point-of-view
- Meticulously refined in every detail

## Frontend Aesthetics Guidelines

Focus on:
- **Typography**: Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial and Inter; opt instead for distinctive choices that elevate the frontend's aesthetics; unexpected, characterful font choices. Pair a distinctive display font with a refined body font.
- **Color & Theme**: Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes.
- **Motion**: Use animations for effects and micro-interactions. Prioritize CSS-only solutions for HTML. Use Motion library for React when available. Focus on high-impact moments: one well-orchestrated page load with staggered reveals (animation-delay) creates more delight than scattered micro-interactions. Use scroll-triggering and hover states that surprise.
- **Spatial Composition**: Unexpected layouts. Asymmetry. Overlap. Diagonal flow. Grid-breaking elements. Generous negative space OR controlled density.
- **Backgrounds & Visual Details**: Create atmosphere and depth rather than defaulting to solid colors. Add contextual effects and textures that match the overall aesthetic. Apply creative forms like gradient meshes, noise textures, geometric patterns, layered transparencies, dramatic shadows, decorative borders, custom cursors, and grain overlays.

NEVER use generic AI-generated aesthetics like overused font families (Inter, Roboto, Arial, system fonts), cliched color schemes (particularly purple gradients on white backgrounds), predictable layouts and component patterns, and cookie-cutter design that lacks context-specific character.

Interpret creatively and make unexpected choices that feel genuinely designed for the context. No design should be the same. Vary between light and dark themes, different fonts, different aesthetics. NEVER converge on common choices (Space Grotesk, for example) across generations.

**IMPORTANT**: Match implementation complexity to the aesthetic vision. Maximalist designs need elaborate code with extensive animations and effects. Minimalist or refined designs need restraint, precision, and careful attention to spacing, typography, and subtle details. Elegance comes from executing the vision well.

Remember: Claude is capable of extraordinary creative work. Don't hold back, show what can truly be created when thinking outside the box and committing fully to a distinctive vision.
```

## **常见问题**

### **如何写出真正能触发的 description？**

聚焦于能力和场景，而不是泛泛的关键词。包含动作动词、具体的文件类型和清晰的使用场景。与其写"文档处理技能"，不如写"从 PDF 中提取表格并转换为 CSV 格式，用于数据分析工作流"。

### **Claude 如何决定调用哪些技能？**

Claude 使用语义理解，把你的请求与技能 description 进行比对。这不是关键词匹配——Claude 判断的是上下文相关性。多个技能可以同时激活，只要它们处理的是你请求的不同方面。

### **我的 description 粒度多粗才合适？**

以单一用途的技能为目标。"面向博客文章的 SEO 优化"足够聚焦、可以写出具体的指令，又足够宽泛、可以复用。太宽泛："内容营销助手"。太狭窄："添加 meta description"。

### **如何在组织内共享 Skills？**

无论团队规模大小，我们建议创建一个包含技能规格说明的共享文档仓库。

**对小团队**，使用包含 name、description、instructions 和版本信息的模板格式。

**对中大型团队**，建立一套技能治理流程：

- 为每个领域（财务、法务、市场）指定技能负责人
- 维护一个中央 wiki 或共享网盘作为你的技能库
- 为每个技能附上使用示例和常见故障排查方法
- 为技能做版本管理，并在 changelog 中记录变更
- 安排季度评审，更新或淘汰过时的技能

**适用于所有团队规模的最佳实践**：

- 记录每个技能的业务目的
- 为维护和更新指定明确的负责人
- 制作入职材料，向新成员展示如何使用共享技能
- 追踪哪些技能创造的价值最大，以此排定维护工作的优先级
- 使用一致的命名约定，让技能易于查找

Enterprise 客户可以与 Anthropic 的客户成功团队合作，探索更多部署选项和治理框架。

### **如何调试技能？**

把触发和执行分开测试。如果技能没有激活，就拓宽你的 description 并添加使用场景。如果结果不一致，就让 instructions 更具体，并加入校验步骤。创建一个覆盖正常使用、边缘情况和超范围请求的测试用例库。

在 [Claude.ai](http://claude.ai/) 中，Skills 目前是每个用户独立的，不过面向全组织的管理与共享能力即将推出。在此之前，无论团队规模大小，我们建议创建一个包含技能规格说明的共享文档仓库。这既能让你的组织为即将推出的功能做好准备，也能在今天建立起良好的治理实践。

## **开始使用**

准备好用 Skills 构建了吗？以下是上手方法：

[Claude.ai](https://claude.ai/) 用户：

- 在 Settings → Features 中启用 Skills
- 在 claude.ai/projects 创建你的第一个项目
- 试试在你的下一个分析任务中，把项目知识与 Skills 结合起来

API 开发者：

- 在[文档](https://docs.anthropic.com/)中探索 Skills 端点
- 查看我们的 [skills cookbook](https://platform.claude.com/cookbook/skills-notebooks-01-skills-introduction)

Claude Code 用户：

- 通过[插件市场](https://code.claude.com/docs/en/plugin-marketplaces)安装 Skills
- 查看我们的 [skills cookbook](https://platform.claude.com/cookbook/skills-notebooks-01-skills-introduction)

## Agent Skills

今天就开始用 Skills 与 Claude 一起构建更强大的应用。

FAQ（常见问题）
