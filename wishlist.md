# 📚 논문 위시리스트 (Daily 5-min Summary)
#
# 사용법:
#  - 한 줄에 arXiv ID 하나 (예: 2511.20639) 또는 전체 URL.
#  - 위에서부터 우선 처리됩니다. 처리된 항목은 done.log 에 기록되어 다시 안 나옵니다.
#  - 이 줄처럼 '#' 로 시작하면 주석(무시).
#  - 비어 있으면(미처리 항목 0개) 아래 FALLBACK 정책으로 alphaXiv 자동 검색.
#
# === FALLBACK 정책 (위시리스트 소진 시) — 2026-09-26 개정 ===
#  주목도 점수로 고른다: 탑 학회 메인 트랙 · 저명 연구실/저자 · 프런티어 랩 기술 보고서 · 화제성(alphaXiv/HF/GitHub).
#  목록·점수·기준값은 sources.md 에서 직접 고칠 수 있다. 이미 done.log 에 있는 건 제외.
#
# ============================================================
# === ICML 2026 큐 (2026-06-22 큐잉) — ✅ 10/10 전부 처리 완료 (2026-07-21 소진) ===
# ============================================================
#
# ============================================================
# === 2026-08 큐 (2026-08-06 큐잉) ===
#  관심분야 4축 균형: Model Compression 3 / Efficient Sequence Models 3
#  / Multi-Agent & Latent Comm 2 / Shared World Models 2. 위→아래 = 우선순위.
#  선정: alphaXiv discover_papers(4축 개별 검색) · arXiv HTTP 200 실재 검증 완료 · done.log 중복 0.
#  ⚠️ 학회 accept 여부는 미검증 — 아래 주석에 venue를 적지 않았다. 요약 생성 시 [2]단계에서 직접 확인할 것.
# ============================================================
2603.15569   # [Efficient-Seq] Mamba-3: Improved Sequence Modeling using State Space Principles — CMU·Princeton·Together·Cartesia (커뮤니티 반응 최상위)
2608.02901   # [Compression·KV] AnchorKV: Anchor-Residual KV Cache Compression — eviction과 저랭크의 중간 지대
2607.26773   # [Multi-Agent·latent] Do Latent Channels Actually Communicate? A Causal Audit of Latent Multi-Agent LLM — 잠재통신 인과 감사(비판적)
2606.23568   # [Compression·low-rank] SVD-Surgeon: Optimal Singular-Value Surgery for LLM Compression
2606.32026   # [World-Model·latent] AdaJEPA: An Adaptive Latent World Model — 테스트타임 적응(반응 최상위)
2606.15378   # [Efficient-Seq·hybrid] Rethinking the Role of Efficient Attention in Hybrid Architectures — SWA·recurrent mixer 재평가
2607.24331   # [Compression·KV·low-rank] DynaCalKV: KV Cache Compression via Head Grouping and Adaptive Rank Allocation
2606.05711   # [Multi-Agent·latent] Beyond tokens: a unified framework for latent communication in LLM-based MAS — 통합 프레임워크
2608.02032   # [Efficient-Seq] DART: Decoded Attention over Recurrent States for Efficient Long-Context Sequence Modeling
2603.02263   # [World-Model·shared] Social-JEPA: Emergent Geometric Isomorphism — 서로 다른 시점의 에이전트가 공유 world model 획득
#
# ============================================================
# === 2026-09-26 우선 주제 큐 — [P1] 소형–대형 분포 정렬 / [P2] 효율 비디오·월드 모델 생성 ===
#  사용자가 정한 새 우선순위. 루틴은 `paper_signals.py --slot`이 알려주는 오늘 슬롯(P1/P2/legacy)에 맞는
#  태그의 맨 위 항목을 고른다(legacy 날엔 이 큐를 건너뛰고 기존 주제로 대체 검색).
#  선정: alphaXiv 검색 + paper_signals 점수(학회·연구실·화제성·주제) · arXiv id 실재 확인 · done.log 중복 0.
# ============================================================
2407.09141   # [P1] Accuracy is Not All You Need — "flips"·KL: 정확도는 같아도 답이 바뀐다 (Microsoft Research, 이 흐름의 출발점)
2602.02214   # [P2] Causal Forcing — AR 비디오 확산 증류 제대로 하기 (ICML'26, ▲173)
2306.13649   # [P1] GKD — On-Policy Distillation of LMs (Google DeepMind, ICLR'24, OPD의 원조)
2602.01801   # [P2] Fast AR Video Diffusion & World Models — 시간 캐시 압축 + 희소 어텐션 (ICML'26, NVIDIA)
2604.13016   # [P1] Rethinking On-Policy Distillation — 현상·메커니즘·레시피 (Tsinghua, ▲309)
2609.20744   # [P2] Video DeltaNet — 라이브스트림용 비디오 하이브리드 선형 어텐션 (Berkeley·Keutzer, 9월)
2606.25519   # [P1] Quantization Inflates Reasoning — 정답은 유지, 추론 토큰은 증가 (UIUC·Microsoft)
2608.13391   # [P2] Context-Matched Distillation — AR 비디오 증류의 교사 인과성 맞추기 (NVIDIA, P1과 다리)
2606.01476   # [P1] OmniOPD — 추측 검증(speculative verification)으로 logit 없는 OPD (Meta AI, ▲96)
2608.22364   # [P1] WAM-OPD — 월드 액션 모델을 위한 OPD (UCL, P1·P2 교차점)
