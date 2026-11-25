# Awesome Extracting Asset Skill

[English](./README.md)

**别再让 AI 盲扫你的旧项目仓库把上下文撑爆了。**

`extracting-asset-skill` 是一个面向 AI 编程助手（Claude Code、Antigravity、Cursor、Codex 等）的开源 **元技能（Meta-Skill）**。它能把任意做完的游戏或创意项目里的可复用资产（程序化 3D/2D 模型、Shader、UI 交互骨架、音效引擎、特效库），标准化抽成**可精准检索、底座与皮肤解耦、带零图片实时陈列室**的 Agent Skill。

---

## 解决什么痛点？

用 AI 连做多款游戏或创意项目时，复用旧代码通常会踩中三个坑：

1. **上下文瞬间爆炸**：直接让 AI 读旧仓库，它还没写一行新代码，Token 先烧掉一半、开始健忘降智。
2. **画风与业务强耦合**：配色、比例、i18n 和旧游戏状态全粘在组件里，直接拷贝要么编译报错，要么新游戏长出一张旧游戏的脸。
3. **人眼看不见、图库装不下**：隔几个月自己都忘了某个模型/组件长什么样，但往 Skill 目录塞几十张 `.png` 截图又会撑爆包体与上下文。

## 核心设计（4 大支柱）

1. **动手前静默扫描与对齐门控（`Step 0`）**
   - 先扫描旧项目，自动区分**高价值可复用资产**与**项目业务胶水**；
   - 动手前必问 4 个问题：**抽取范围、新建还是增量合并进老库、长期维护路径（中央资产库）、交付物清单**，确认后再写文件。
2. **通用底座 + 可插拔风格包（Universal Base + Style Pack）**
   - 剥离旧项目的业务 `import`，将纯逻辑/几何骨架抽进 `templates/`（标记 `"style": "universal"`）；
   - 将色板、比例、光照、CSS 变量独立放进 `styles/<style-id>/`，同一领域 Skill（如 UI 或 3D）可跨游戏一键换肤、增量滚雪球。
3. **行号级 CLI 检索（`assets-catalog.json` + `search_assets.py`）**
   - AI 先跑检索脚本拿到精确的 `文件#L行号`，只读命中的几十行代码，彻底告别盲扫；
   - `--sync-lines` 支持 JS/TS 导出、CSS 选择器与 Python 定义的自动行号校验，保证 0 失效路径。
4. **零 PNG 实时交互陈列室（`showroom/gallery.html`）**
   - Skill 目录内不留一张 `.png` 截图；
   - 人类打开浏览器直接运行真实源码查看 3D 旋转 / 试按 UI 按钮 / 一键切皮肤，AI 永远只查 JSON 索引，互不打扰。

---

## 安装方式

### 方式一：直接让 AI Agent 安装
把下面这句话发给支持 `SKILL.md` 的 AI Agent：

```text
请帮我安装这个仓库里的 Skill：https://github.com/elysianx138/awesome-extracting-asset-skill
```

### 方式二：手动安装
将 `skills/extracting-asset-skill/` 复制到你的 Agent Skills 目录：
- **工作区级（Antigravity / Codex / 通用）**：`.agents/skills/extracting-asset-skill/`
- **Claude Code 全局**：`~/.claude/skills/extracting-asset-skill/`

### 方式三：同步到个人中央资产库
```bash
python skills/extracting-asset-skill/scripts/pack_and_sync_skill.py \
  skills/extracting-asset-skill \
  --target "~/game-asset-vault"
```

---

## 使用示例

提取旧项目的可复用资产：
```text
用 extracting-asset-skill 帮我把 ./my-previous-game 里的可复用 UI 交互骨架和视觉皮肤抽成一个 Skill
```

将第二款游戏的风格增量合并进已有资产库：
```text
用 extracting-asset-skill 把 ./game-2 的奶油磨砂风皮肤和抽屉工具栏，增量合并进现有的 building-web-game-ui 资产库
```

## 目录结构

```text
skills/extracting-asset-skill/
├── SKILL.md                           # 核心流程与 Step 0 对齐门控
├── references/
│   ├── style-pack-pattern.md          # 底座+皮肤分离与零 PNG 陈列室架构说明
│   └── skill-spec-checklist.md        # Token 经济性与 SKILL.md 规范清单
├── scripts/
│   └── pack_and_sync_skill.py         # 多路径同步（--target）与 POSIX ZIP 打包工具
└── templates/
    ├── search_assets.py               # 领域无关的资产检索与 --sync-lines 校验 CLI
    └── style.json                     # 风格包元数据起始模板
```

## 开源协议

MIT License — 详见 [LICENSE](./LICENSE)。
