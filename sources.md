# 🎯 Paper-selection signals (fallback search, when wishlist.md is empty)
#
# The daily routine scores each unread candidate with the signals below and picks the highest.
# Edit freely: one entry per "- " line. The text before " — " is what gets matched.
# `paper_signals.py` (daily-paper-card skill) reads this file to match authors and set the hot thresholds.
#
# Score (a paper needs ≥ 3 to be picked over a signal-less one):
#   +3  top-venue MAIN-track accept (list below)   · +1 more for oral / spotlight / best paper
#   +1  workshop accept (not a venue tab in the archive)
#   +3  a listed author is on the paper, or a listed lab is an affiliation
#   +3  frontier-lab technical report touching the interest axes
#   +2  hot: over ANY threshold below          · +1 more if "very hot"
# Tie-breaks: axis not covered by the last 2 cards → hotter → newer.
# Recency: prefer ≤ 45 days since first arXiv version; up to 120 days only if score ≥ 5.

## Hot thresholds
- alphaXiv votes — 20
- alphaXiv views — 300
- HF upvotes — 30
- GitHub stars — 500
- very hot: alphaXiv votes — 100
- very hot: HF upvotes — 100
- very hot: GitHub stars — 5000

## Venues (main track)
- NeurIPS
- ICML
- ICLR
- ACL
- EMNLP
- NAACL
- COLM
- CVPR
- ICCV
- ECCV
- AAAI
- KDD
- MLSys
- OSDI
- SOSP
- NSDI
- EuroSys
- ASPLOS
- ISCA
- MICRO
- SIGCOMM

## Authors (first / last / corresponding author, or anywhere on the list)
# Efficient inference · compression · KV cache · quantization · serving
- Song Han — MIT HAN Lab
- Tri Dao — Princeton · Together AI
- Albert Gu — CMU · Cartesia
- Beidi Chen — CMU
- Ion Stoica — UC Berkeley Sky Lab
- Joseph E. Gonzalez — UC Berkeley Sky Lab
- Matei Zaharia — UC Berkeley · Databricks
- Kurt Keutzer — UC Berkeley
- Amir Gholami — UC Berkeley · ICSI
- Christopher Ré — Stanford Hazy Research
- Dan Alistarh — IST Austria · Red Hat AI
- Tim Dettmers — CMU · Ai2
- Hao Zhang — UCSD
- Zhangyang Wang — UT Austin
- Yuandong Tian — Meta FAIR
- Songlin Yang — MIT
- Yoon Kim — MIT
- Guangxuan Xiao — MIT
- Luke Zettlemoyer — UW · Meta
- Ce Zhang — UChicago · Together AI
- Pavlo Molchanov — NVIDIA
- Jan Kautz — NVIDIA
- Woosuk Kwon — vLLM
- Ying Sheng — SGLang
- Lianmin Zheng — SGLang
# Multi-agent · latent communication
- James Zou — Stanford
- Mengdi Wang — Princeton
- Yejin Choi — Stanford · NVIDIA
- Graham Neubig — CMU
- Diyi Yang — Stanford
- Percy Liang — Stanford
- Yilun Du — Harvard
- Igor Mordatch — Google DeepMind
# World models · JEPA
- Yann LeCun — NYU · Meta
- Randall Balestriero — Brown
- Danijar Hafner — Google DeepMind
- Sergey Levine — UC Berkeley
- Pieter Abbeel — UC Berkeley

## Labs (match against the affiliation line alphaXiv shows)
- Google DeepMind
- Google Research
- Meta FAIR
- Meta AI
- OpenAI
- Anthropic
- NVIDIA
- Microsoft Research
- Apple
- Together AI
- MIT HAN Lab
- Hazy Research

## Frontier labs (technical reports count as a signal)
- DeepSeek
- Qwen
- Alibaba
- Moonshot
- Kimi
- Zhipu
- Z.ai
- GLM
- MiniMax
- Gemini
- Gemma
- Llama
- Nemotron
- Mistral
- gpt-oss
- Phi
- MiMo
- ByteDance Seed
- Hunyuan
- StepFun
- Granite
- OLMo
