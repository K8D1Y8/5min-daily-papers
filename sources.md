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

## Priority topics (P2 set 2026-09-26, P1 redefined by the user 2026-10-16)
# P1  Compressed Reasoning — how compressed models (quantized, pruned, sparsified, low-rank, KV-cache
#     compressed, distilled small models) behave in reasoning and long-horizon / agentic tasks (longer or
#     looping outputs, errors that compound over steps, accuracy that holds on short benchmarks but breaks
#     over long horizons), and compression methods that are aware of reasoning or long-horizon use.
#     On-policy distillation (OPD) is OUT of scope from 2026-10-16: papers whose title is about OPD get no
#     priority tag (see "Priority exclude").
# P2  Video & World Generation — efficient video diffusion and world-model generation, autoregressive first
#     (bidirectional also fine).
# Rotation: 6 of every 7 cards alternate P1 / P2; every 7th card goes to the earlier axes (legacy:
#   latent communication, KV/low-rank compression, efficient sequence models, shared world models).
#   `paper_signals.py --slot` reads the last cards' topic chips and prints today's slot.
# Scoring: +3 and a P1/P2 tag when the title or abstract matches the topic.
#   P1 matches when it contains a "P1 keywords" phrase, OR a "P1 compression terms" entry together
#   with a "P1 context terms" entry. P2 matches on any "P2 keywords" phrase.
#   Keywords are a first filter — confirm the fit from the abstract before picking.
# Card chip prefix (drives the slot and the archive columns):
#   P1 → "Compressed Reasoning · …"   P2 → "Video & World Generation · …"
#   (cards before 2026-10-16 used "Small–Large Alignment · …"; the slot still counts them as P1)

## P1 keywords — Compressed Reasoning (any one phrase is enough)
- quantized reasoning
- compressed reasoning model
- reasoning-aware quantization
- reasoning-aware pruning
- reasoning-aware compression
- reasoning-aware kv
- long-horizon-aware
- quantization inflates
- pruning-recovery
- compressed llms fail
- compressed models fail

## P1 compression terms — paired with a context term
- quantiz
- low-bit
- 2-bit
- 4-bit
- prun
- sparsif
- sparsity
- low-rank
- model compression
- compressed model
- kv cache compression
- kv-cache compression
- kv cache eviction
- kv cache quantization
- kv-cache quantization
- token eviction
- small language model

## P1 context terms — paired with a compression term
- reasoning
- chain-of-thought
- long-horizon
- long horizon
- multi-step
- multi-turn
- agentic
- agent
- long-output
- long generation
- test-time scaling
- thinking

## Priority exclude — a title containing any of these gets no P1/P2 tag
- on-policy distillation
- on-policy self-distillation
- OPD

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
