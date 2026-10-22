# transcript-to-webpage

把一场讲座/课程/分享的逐字稿（docx / pdf / txt），清洗后产出三个版本——①框架版 ②金句+实例版 ③完整逐字稿——再打包成一个带 tab 切换的自包含 HTML，可选部署到飞书妙搭生成外部链接。

## 安装（Claude Code）

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/Janet988/transcript-to-webpage.git ~/.claude/skills/transcript-to-webpage
```

安装后，把一份逐字稿丢给 Claude，说「整理成网页 / 可视化 / 三版本」即可触发。

## 结构

- `SKILL.md` — 6 步完整流程（提取文本 → 清洗 → 三版本 → 生成 HTML → 妙搭部署 → 交付自检）
- `scripts/gen_html.py` — 把三个 md 打包成自包含 HTML

## 依赖

```bash
pip install markdown
```
