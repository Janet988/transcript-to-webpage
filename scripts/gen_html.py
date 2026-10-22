#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把三个版本的 markdown 打包成自包含的 tab 切换 HTML。

用法:
  python3 gen_html.py --title "标题" --meta "副标题行" --dir "./输出目录" --out "./输出目录/演讲稿.html"

默认读取 --dir 下的 01_框架版.md / 02_金句实例版.md / 03_完整逐字稿.md。
依赖: pip install markdown
"""
import argparse
import os
import markdown


DEFAULT_FILES = [
    ("01_框架版.md", "框架版", "快速掌握讲座整体结构"),
    ("02_金句实例版.md", "金句+实例版", "可复用的金句与案例弹药"),
    ("03_完整逐字稿.md", "完整逐字稿", "清理后的完整干净讲稿"),
]

CSS = """
:root{
  --navy:#0f2a4a; --navy2:#14355c; --gold:#c9a227; --gold2:#e0bd5a;
  --bg:#f5f6f8; --card:#ffffff; --ink:#22293a; --muted:#6b7280; --line:#e6e8ec;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei","Segoe UI",Roboto,sans-serif;background:var(--bg);color:var(--ink);line-height:1.75;-webkit-font-smoothing:antialiased}
header{background:linear-gradient(135deg,var(--navy) 0%,var(--navy2) 60%,#1d4e8f 100%);color:#fff;padding:40px 20px 0;position:sticky;top:0;z-index:20;box-shadow:0 4px 20px rgba(15,42,74,.18)}
header .wrap{max-width:960px;margin:0 auto}
header h1{font-size:24px;margin:0 0 6px;font-weight:700;letter-spacing:.5px}
header .meta{font-size:13px;color:#c8d6ea;margin:0 0 20px}
.tabs{display:flex;gap:6px;max-width:960px;margin:0 auto;flex-wrap:wrap}
.tab{appearance:none;border:none;cursor:pointer;padding:12px 20px;font-size:15px;font-weight:600;color:#c8d6ea;background:transparent;border-radius:10px 10px 0 0;transition:.2s}
.tab:hover{color:#fff;background:rgba(255,255,255,.08)}
.tab.active{color:var(--navy);background:var(--bg);font-weight:700}
main{max-width:960px;margin:24px auto 80px;padding:0 20px}
.panel{display:none}
.panel.active{display:block;animation:fade .25s ease}
@keyframes fade{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
.subtitle{color:var(--muted);font-size:14px;margin:4px 0 20px}
.card{background:var(--card);border-radius:14px;padding:30px 34px;box-shadow:0 2px 14px rgba(15,42,74,.06)}
.panel h1{font-size:22px;color:var(--navy);border-bottom:3px solid var(--gold);padding-bottom:10px;margin:26px 0 16px}
.panel h2{font-size:19px;color:var(--navy2);margin:28px 0 12px;padding-left:12px;border-left:4px solid var(--gold)}
.panel h3{font-size:16px;color:#20314f;margin:20px 0 8px}
.panel h4{font-size:15px;color:#33415e;margin:16px 0 6px}
.panel p{margin:10px 0}
.panel ul,.panel ol{margin:10px 0;padding-left:26px}
.panel li{margin:6px 0}
.panel strong{color:var(--navy);font-weight:700}
.panel em{color:#8a6d1a;font-style:normal;background:#fbf6e8;padding:1px 6px;border-radius:5px}
.panel blockquote{margin:14px 0;padding:12px 18px;background:#f0f5fc;border-left:4px solid var(--gold);border-radius:0 10px 10px 0;color:#3a4a66}
.panel blockquote p{margin:4px 0}
.panel hr{border:none;border-top:1px solid var(--line);margin:28px 0}
.panel table{border-collapse:collapse;width:100%;margin:14px 0;font-size:14px}
.panel th,.panel td{border:1px solid var(--line);padding:8px 12px;text-align:left}
.panel th{background:#f0f5fc;color:var(--navy)}
.panel code{background:#eef2f7;padding:1px 6px;border-radius:5px;font-size:13px;color:#14355c}
.panel a{color:#1d4e8f}
@media(max-width:640px){
  header{padding-top:26px}
  header h1{font-size:20px}
  .tab{padding:10px 14px;font-size:14px}
}
"""

TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>__TITLE__</title>
<style>__CSS__</style>
</head>
<body>
<header>
  <div class="wrap">
    <h1>__TITLE__</h1>
    <p class="meta">__META__</p>
  </div>
  <div class="tabs">__TABS__</div>
</header>
<main>
  <div class="card">__PANELS__</div>
</main>
<script>
function switchTab(i){
  document.querySelectorAll('.tab').forEach(function(t){t.classList.toggle('active', +t.dataset.i===i)});
  document.querySelectorAll('.panel').forEach(function(p,j){p.classList.toggle('active', j===i)});
  window.scrollTo({top:0,behavior:'smooth'});
}
</script>
</body>
</html>"""


def build(title, meta, directory, out):
    md = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists"])
    tabs, panels = [], []
    for i, (fn, tab_name, subtitle) in enumerate(DEFAULT_FILES):
        path = os.path.join(directory, fn)
        if not os.path.exists(path):
            print(f"[skip] 缺少 {fn}，跳过该 tab")
            continue
        with open(path, encoding="utf-8") as f:
            body = md.convert(f.read())
        md.reset()
        active = " active" if i == 0 else ""
        tabs.append(
            f'<button class="tab{active}" data-i="{i}" onclick="switchTab({i})">{tab_name}</button>'
        )
        panels.append(
            f'<section class="panel{active}" id="panel-{i}"><p class="subtitle">{subtitle}</p>{body}</section>'
        )

    doc = (
        TEMPLATE.replace("__TITLE__", title)
        .replace("__META__", meta)
        .replace("__CSS__", CSS.strip())
        .replace("__TABS__", "".join(tabs))
        .replace("__PANELS__", "".join(panels))
    )
    with open(out, "w", encoding="utf-8") as f:
        f.write(doc)
    print(f"OK -> {out} ({len(doc)} bytes, {len(tabs)} tabs)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--title", required=True)
    ap.add_argument("--meta", default="")
    ap.add_argument("--dir", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    build(args.title, args.meta, args.dir, args.out)
