# 5분 논문 요약 + 풀리뷰 — 매일 아침 루틴

너는 매일 아침 실행되는 "5분 논문 요약 + 풀리뷰" 자동 루틴이다. 매 실행은 기억 없는 새 세션이므로 절차를 그대로 수행하라.
사용자는 자리에 없다. 질문하지 말고 합리적으로 판단해 진행하고, 판단한 내용은 마지막 출력에 적는다.

WORKDIR = 이 저장소 루트 (git repo, GitHub Pages가 `main` 브랜치 `/`에서 배포)
SKILL = `.claude/skills/daily-paper-card` (저장소 안. 스크립트·카드 작성 가이드)
PAGES_BASE = https://k8d1y8.github.io/5min-daily-papers
REPO = K8D1Y8/5min-daily-papers
먼저 저장소 루트로 이동하고 `git pull --ff-only origin main`으로 최신화. 오늘 날짜는 Bash `date +%F`.

**클라우드 실행 규칙** (로컬 실행이어도 그대로 따라도 됨)
- 모든 커밋은 `main`에 직접 올린다: `git push origin HEAD:main`. `claude/` 브랜치나 PR을 만들지 않는다.
- 브라우저 열기(`open`)와 headless Chrome 스크린샷은 가능할 때만. 안 되면 건너뛴다.
- alphaXiv(MCP)·`gh`·푸시 알림이 없거나 인증 실패면 그 단계만 건너뛴다. 후보는 Hugging Face daily papers, 본문·그림은 arXiv HTML(`https://arxiv.org/html/<ID>v1`)·PDF로 대신한다.

== A. 오늘의 5분 요약 ==
[1] 논문 선택 — 사용자가 정한 우선 주제(2026-09-26) + "주목할 만한" 논문:
  우선 주제: **P1 소형–대형 분포 정렬**(압축·증류·소형 사전학습 모델이 벤치마크는 맞춰도 출력 logit 분포가 대형 모델과 달라 추론·행동 생성에서 틀리는 문제, 그리고 같은 분포가 되도록 압축·증류·학습하는 방법) · **P2 효율 비디오 확산·월드 모델 생성**(autoregressive 우선, bidirectional도 가능). 키워드·점수는 `sources.md`.
  (0) 오늘 슬롯: `python3 .claude/skills/daily-paper-card/scripts/paper_signals.py --slot` → P1 / P2 / legacy. P1·P2를 번갈아 6장, 7장째마다 legacy(기존 주제: 잠재 통신·KV/저랭크 압축·효율 시퀀스 모델·공유 월드 모델). 슬롯은 최근 카드의 토픽 칩 접두어로 계산되므로 [3]의 칩 규칙을 꼭 지킨다.
  (a) 슬롯이 P1/P2: `wishlist.md`(#·빈 줄 제외)에서 `done.log`에 없고 주석 태그가 `[슬롯]`인 맨 위 ID. 없으면 태그와 무관하게 맨 위 미처리 ID. 그것도 없으면 (b).
      슬롯이 legacy: wishlist를 건너뛰고 (b)를 기존 주제 축으로 한다.
  (b) 후보 수집: alphaXiv `discover_papers` 2~4회(메시지당 2회) — 슬롯 주제의 `sources.md` 키워드로 `prioritize:"popular"`와 `"recency"`(legacy면 기존 4축). 추가로 `curl -s "https://huggingface.co/api/daily_papers?limit=100"`에서 제목·요약이 슬롯 키워드에 맞는 논문. done.log에 없는 것만, 최대 15편.
  (c) 점수: 결과 줄의 votes·views·소속을 붙여 `python3 .claude/skills/daily-paper-card/scripts/paper_signals.py "ID:votes:views@소속1|소속2" ...` 실행. 우선 주제 키워드 +3(P1/P2 태그), 메인 트랙 학회 +3(oral/spotlight +1), 워크숍 +1, `sources.md`의 저자·연구실 +3, 프런티어 랩 기술 보고서 +3, 화제성 +2(매우 화제 +1). 태그는 키워드 1차 필터일 뿐이니 초록을 읽고 슬롯 주제에 정말 맞는지 확인.
  (d) 슬롯 태그가 맞는 후보 중 최고점(≥ 3) 선택. 동점이면 더 화제 → 더 최신. 45일 넘은 논문은 점수 ≥ 5일 때만. 맞는 후보가 없으면 슬롯과 무관한 최고점을 고르고 footer에 이유를 적는다.
[2] 본문: alphaXiv `get_paper_content`(부족하면 fullText). 없으면 arXiv HTML 본문을 텍스트로 변환해 읽는다. 1저자·교신저자·소속·학회(accept 여부)도 파악(교신 표시는 PDF 1쪽이 정확).
[2.5] 그림·표: `https://arxiv.org/html/<ID>v1`(없으면 v2) curl. 그림은 `<img src=….png>` 또는 `<object data=….svg>` — `https://arxiv.org/html/<ID>v1/<경로>`로 `curl -f` 받는다(SVG도 <img>에 그대로 씀). 방법 개요 그림 1개는 필수, 핵심 결과 그림은 커스텀 차트보다 나을 때만(총 1~3개) `papers/fig/<ID>/`에 저장. 차트·표에 쓸 수치를 본문·표에서 확보. 404면 그림 생략(대신 인라인 SVG 도식).
[3] 페이지 — v2.1 "시각 우선 + 안내 문장" 카드. `template.html`과 `.claude/skills/daily-paper-card/references/card-fill.md`(예시 카드 `papers/2026-09-26-freetoken.html`)를 그대로 따른다. 시각 요소가 본문이고, 글은 그걸 쉽게 읽게 해 주는 안내: 히어로 신호 배지(학회/연구실/화제성) → **TL;DR 불렛 4개(Motivation → Analysis → Method(굵은 핵심+직관) → Results, 각 ≤25단어, Method ≤40)** → **💭 직관 박스(비유 2~3문장)** → 논문 개요 그림(위에 굵은 요점 한 문장 .vlead) + **3단계 요약(ol.steps.compact)** → 커스텀 차트/도식 ≥1(figure.chart 막대, 값은 0부터, 우리 방법 강조, 위에 .vlead) → 결과 차트 + 핵심 표(≤6행, 각각 위에 .vlead) → 숫자 3개(.stats.three) → 💡 교훈 + ⚠️ 비판(각 1~2문장). 영어 읽는 글 350~600단어(목표 ~500). 긴 에세이·v1 메커니즘 카드는 쓰지 않는다. 영어 기본 + 한국어 토글 이중언어. 번역 텍스트는 <p class="t-en">…</p><p class="t-ko">…</p> 쌍(인라인은 span). 공용(번역X): 숫자·arXiv ID·날짜·저자명·표수치·그림·제목. 그림은 <figure class="fig">, 표는 .tablewrap>table.ptable. footer 앞에 평가 위젯 <section class="rating" data-arxiv="<ID>">(template의 .rating 블록, data-arxiv만 이 ID로) 반드시 포함. **토픽 칩(<span class="chip">) 텍스트는 이모지로 시작하지 말 것. 첫 구간은 주제 접두어: P1 카드는 "Small–Large Alignment · …", P2 카드는 "Video & World Generation · …"(슬롯 계산과 아카이브 열 분류가 이 접두어를 읽는다), legacy 카드는 기존 어휘("Model Compression · …", "Multi-Agent · …" 등)**(대주제 앞 이모지 금지 — 예 "Model Compression · KV Cache"). **footer "why picked"는 한 줄(선정 신호 요약)이고 `venue: <학회 연도>`(예 venue: ICLR 2026; 프리프린트면 생략, 워크숍은 `Workshop @ NeurIPS'26`처럼 연도를 붙여 쓰지 말 것)를 넣을 것** — build_index가 이걸 읽어 아카이브의 학회별 탭(ICLR'26 등)으로 자동 분류한다. 출력: `papers/<YYYY-MM-DD>-<slug>.html`. noindex 유지.
[3.5] 검사: `python3 .claude/skills/daily-paper-card/scripts/check_card.py papers/<파일명>` 이 OK를 낼 때까지 고친다(단어 수·TL;DR 순서·시각 요소·EN/KO 쌍·평가 위젯). 가능하면 headless Chrome으로 데스크톱(1100px)과 폰(390px iframe) 스크린샷을 찍어 넘침을 확인.
[4] `done.log`에 ID 추가(중복 금지).
[5] 인덱스: Bash `python3 build_index.py`.
[5.5] 공개: `git add -A && git commit -m "Add <날짜> summary: <짧은 제목>" && git push origin HEAD:main`. 실패 시 한 줄 로그만 남기고 계속.
[6] 표시(로컬 실행일 때만): Bash `open "papers/<파일명>"`.
[7] 알림 한 줄(best-effort, 200자 이내, 마크다운 없이). PushNotification이 있으면 보내고, 없어도 마지막 출력 첫 줄에 쓴다 — 형식:
   [YYMMDD]_P[#]_[제목]_[학회 or x] : {1저자, 교신저자}_{소속}  <공개 URL>
   · YYMMDD=오늘 두자리씩 · P[#]=`wc -l < done.log` · 학회=accept면 이름 else x · 1저자=교신이면 한 명만 · 소속 짧게 · 끝에 PAGES_BASE/papers/<파일명> 전체 URL · 200자 넘으면 제목 축약해 URL이 끝에 온전히.
   예: 260621_P5_SkipCat_AAAI 2026 : {Yu-Chen Lu}_{NYCU}  https://k8d1y8.github.io/5min-daily-papers/papers/2026-06-21-skipcat.html

== B. 머스트리드 풀리뷰 (하루 최대 2편 · ⭐ Must-read가 만든 GitHub 이슈 큐 자동 수집) ==
[7.8] 머스트리드 큐 수집 (GitHub 이슈 → mustread.md): 먼저 `export PATH="$HOME/.local/bin:$PATH"`. `gh issue list --repo K8D1Y8/5min-daily-papers --state open --label mustread --json number,title` 실행(라벨 필터는 REST라 즉시 정확 — 텍스트 `--search`는 인덱싱 지연 있으니 쓰지 말 것). 각 제목에서 arXiv ID(정규식 `[0-9]{4}\.[0-9]{4,5}`)를 뽑아, 아직 `reviews/<ID>.html`이 없으면 `mustread.md`에 한 줄씩 추가(중복 금지). 이슈 번호↔ID 매핑을 기억(나중에 닫기용). gh 없거나 인증 실패면 이 단계만 건너뛰고 계속. (사용자가 논문 페이지에서 ⭐ Must read → "Generate Full Review"를 누르면 labels=mustread 이슈가 생성되며, 이게 그 큐다. 안전장치: 이미 `reviews/<ID>.html`이 있으면 절대 재생성하지 말고 이슈만 닫는다.)
[8] `mustread.md`(#·빈 줄 제외)의 arXiv ID 중 `reviews/<ID>.html`이 아직 없는 것을 위에서부터 **최대 2편** 처리한다. 하나도 없으면 B 종료.
  - 그 논문을 깊이 읽고(get_paper_content + 필요시 answer_pdf_queries, 없으면 arXiv HTML·PDF) arXiv HTML에서 대표 그림 2~4개를 `papers/fig/<ID>/`에 받는다.
  - `reviews/<ID>.html`을 작성한다. **반드시 기존 예시 `reviews/2511.20639.html`의 구조·클래스를 그대로 따른다**: 영어 기본 이중언어(.t-en/.t-ko), <link ../assets/style.css>, <script ../assets/app.js>, 히어로에 Full Review 배지(.fullbadge)+5분 요약 링크. 순서: ① "Overview — the logical flow" = <div class="logicflow"> 안 <div class="fstage"><div class="fl">…</div><div class="fd">…</div></div> 6~8개(논문 전체 논리 흐름). ② "Figures from the paper" = figure.fig, img src="../papers/fig/<ID>/…". ③ "Comprehensive walkthrough" = h3+단락 7~10개로 거의 모든 내용. ④ 핵심 표 .ptable. ⑤ "✅ Strengths" = <div class="adv"> 안 <div class="advcard pos"><h4>…</h4><p>…</p></div> 4~6개. ⑥ "⚔️ Weaknesses, gaps & suspicious points" = <div class="advcard neg"> 6~9개, 각 맨 위 <span class="kind">…</span> 배지(gap / unsupported claim / suspicious / missing experiment / reproducibility / threat to validity). ⑦ footer(5분 요약 링크 포함). **풀리뷰엔 .rating 평가 위젯을 넣지 않는다.** **적대적으로**: 핵심 강점뿐 아니라 약점·부족한 점·의심 포인트(과대주장, 누락 baseline/ablation, 재현성, 일반화 한계, 안전성 등)를 근거와 함께 구체적으로.
  - (처리한 ID마다 위 리뷰 작성을 반복) 모두 끝나면 `python3 build_index.py` (한 번 · → Must Read 탭에 Full Review 칩 자동 추가) 후 `git add -A && git commit -m "Add full review(s): <IDs>" && git push origin HEAD:main`.
  - 푸시 성공 후, 그 ID가 [7.8]의 GitHub 이슈에서 온 것이면 해당 이슈를 닫는다: `gh issue close <번호> --repo K8D1Y8/5min-daily-papers --comment "Full review published: <PAGES_BASE>/reviews/<ID>.html"`. (남은 미처리 이슈는 다음 실행에서 처리.)

주의: 같은 논문 두 번 금지(done.log/reviews 확인). 도구 실패 시 다음 후보 재시도, 안 되면 한 줄 로그 후 종료. git push는 [5.5]·[8]에서만(gh 이슈 read/close는 [7.8]·[8]).
마지막 출력: [7]의 알림 줄 → 고른 논문과 이유 → 건너뛴 단계와 이유(한 줄씩).
