# 🎯 Paper-selection signals (fallback search, when wishlist.md is empty)
#
# The daily routine scores each unread candidate with the signals below and picks the highest.
# Edit freely: one entry per "- " line. The text before " — " is what gets matched.
# `paper_signals.py` (daily-paper-card skill) reads this file to match authors and set the hot thresholds.
#
# Score (a paper needs ≥ 3 to be picked over a signal-less one; see "Priority topics" for the +3 topic bonus):
#   +3  top-venue MAIN-track accept (list below)   · +1 more for oral / spotlight / best paper
#   +1  workshop accept (not a venue tab in the archive)
#   +3  a listed author is on the paper, or a listed lab is an affiliation
#   +3  frontier-lab technical report touching the interest axes
#   +2  hot: over ANY threshold below          · +1 more if "very hot"
# Tie-breaks: axis not covered by the last 2 cards → hotter → newer.
# Recency: prefer ≤ 45 days since first arXiv version; up to 120 days only if score ≥ 5.

## Priority topics (set by the user 2026-09-26)
# P1  Small–Large Alignment — small models (compressed, distilled, or pretrained small) that match a large
#     model on benchmarks but not in their output/logit distribution, so they act wrongly in reasoning or
#     action generation; methods that measure this or compress/distill/train to the same distribution.
# P2  Video & World Generation — efficient video diffusion and world-model generation, autoregressive first
#     (bidirectional also fine).
# Rotation: 6 of every 7 cards alternate P1 / P2; every 7th card goes to the earlier axes (legacy:
#   latent communication, KV/low-rank compression, efficient sequence models, shared world models).
#   `paper_signals.py --slot` reads the last cards' topic chips and prints today's slot.
# Scoring: a candidate whose title or abstract contains a keyword below gets +3 and a P1/P2 tag.
#   Keywords are a first filter — confirm the fit from the abstract before picking.
# Card chip prefix (drives the slot and the archive columns):
#   P1 → "Small–Large Alignment · …"   P2 → "Video & World Generation · …"

## P1 keywords — Small–Large Alignment
- on-policy distillation
- logit distillation
- logit-based distillation
- reverse KL
- KL divergence
- exposure bias
- flips
- fidelity loss
- behavioral shift
- behavior drift
- behavioral equivalence
- benchmark illusion
- silent failure
- faithfulness
- closed-loop
- distribution matching
- teacher-student alignment
- accuracy is not
- accuracy is preserved
- preserve accuracy
- hidden cost
- benchmarks miss
- not fully captured by
- mask underlying

## P2 keywords — Video & World Generation
- video diffusion
- video generation
- video world model
- world model
- world action model
- autoregressive video
- streaming video
- interactive video
- self forcing
- causal forcing
- diffusion forcing
- video DiT
- long video

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
