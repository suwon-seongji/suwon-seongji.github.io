# 수원 사이트 발행 규칙

이 규칙은 운영자의 2026-11-04 요청을 구현한다. 매일 실행할 때 최신 버전과 실제 기존 글을 다시 읽는다.

## 범위와 권한
- 게시 대상: suwon-seongji/suwon-seongji.github.io, main. 사이트 https://suwon-seongji.github.io/.
- 한국 시간 하루 신규 글 최대 1개. 예약 시작은 09:13 Asia/Seoul. 공개는 Pages 빌드 완료 후라 시작 시각과 다를 수 있다.
- 본 블로그 htglove/htglove.github.io의 일반 구매·전국 주제와 겹치지 않는 수원 시민용 글을 작성한다.
- 본 블로그의 매일 발행 작업은 별도 운영이다. 해당 예약을 복제·중지하지 않는다.
- 추가 유료 API·이미지·영상 생성·크레딧 구매를 사용하지 않는다.

## 매번 먼저 읽을 자료
1. 두 저장소의 최신 main HEAD와 전체 파일 트리. _posts의 누락 없는 목록을 얻는다. API pagination/truncated 여부를 점검한다.
2. 두 저장소의 모든 기존 글 제목·키워드·요약·소제목·본문. 목록뿐 아니라 본문 문단 중복도 검사한다.
3. 수원 editorial/topics.json, topics.md, local-facts.json, publish-log.json.
4. 본 블로그 GEO_GUIDE.md, topics.md, regions.md. 수원 지역은 본 블로그 발행 대상에서 제외한다.
5. 같은 한국 날짜의 수원 글이 이미 있으면 새 글을 추가하지 않는다. 기존 커밋의 배포를 확인하고 중복 실행으로 종료한다.

## 주제 선택과 증거
- topics.json은 후보 30개 원장이다. status=published는 재사용하지 않는다.
- research 후보는 발행 당일 공식 자료를 조사해 실제 수원 정보가 충분할 때만 선택한다. 존재하지 않는 서비스·중단된 프로그램을 가정하지 않는다.
- needs_data 후보는 운영자가 공개 가능한 실제 자료와 기준일을 제공하기 전에는 발행하지 않는다. 빈 local-facts 값은 '자료 미확인'이다.
- 지역명만 바꿔도 그대로 통하는 글은 탈락시킨다. 동네 이름 나열과 공통 구매 요령만으로는 지역성이 충분하지 않다.
- 이미 다룬 실질 질문·동일 비교 축·유사 문단이면 새 제목을 만드는 대신 다른 질문으로 바꾼다. 본 블로그가 다룰 일반 요금제·초기화·기기변경 비교 등은 반복하지 않는다.
- 수원 실제 자료가 들어오면 그 자료를 우선한다. 한 지역/주제에 변화가 있으면 기존 글 업데이트를 우선하며 하루치 신규 글 수를 채우려고 얇은 글을 만들지 않는다.
- 공개 자료로 쓸 주제가 없으면 발행하지 말고 부족한 자료를 구체적으로 보고한다.

## 허용되는 올댓폰 사실
- 직접 인증한 현금 시세표. 조건은 3개월 이상 입점, 그 기간 문제 건 0건, 인터넷 가입·제휴카드 조건 없음.
- 방문 구매: 시세표 확인 → 카페에서 매장 주소 문의 → 방문.
- 올댓폰 직접 운영 온라인 공동구매: 휴대폰 택배 수령 후 개통.
- 공동구매는 요금제·부가서비스 강제 없음. 요금제·부가서비스 조건을 더해 가격을 비교하려면 방문 조건을 확인하고, 그런 강제 조건 없이 사려면 공동구매.
- 인증 시세표에 요금제·부가서비스 조건도 없다고 확대하지 않는다.
- 회원 수·수원 매장 수·동네·가격·배송비·배송일·재고·최저가·실제 후기·고객 성향은 제공/검증된 근거 없이 쓰지 않는다.

## 글 형식
- 새 파일: _posts/YYYY-MM-DD-slug.md. 날짜는 Asia/Seoul 현재 날짜.
- front matter는 JSON 형태의 YAML로 작성한다: --- 줄, JSON 객체, --- 줄.
- 필수: layout=post, title, date, last_modified_at, category, topic_id, primary_keyword, secondary_keyword, keywords, summary, description, faq, sources.
- 제목부터 메인·보조 키워드를 정한다. 공유 앞부분을 가진 키워드를 자연스럽게 담고, 키워드 뒤 8자 내외의 짧은 말을 붙인다. 제목에 연도·월을 넣지 않는다.
- summary와 본문 첫 문단에 결론. 본문 1,500자 이상을 기준으로 충분히 설명하되 불필요하게 늘리지 않는다.
- 본문 ## 소제목 5개 이상, 유용한 비교표 1개 이상. 서로 다른 글에서 공통 섹션을 대량 복제하지 않는다.
- 본문은 실제 로컬 문제 해결 중심. 올댓폰 소개는 필요한 곳에 짧게 쓰고 하단 CTA는 레이아웃이 처리한다.
- FAQ 3~5개(q, a). 실제 상담 기록이 없다면 FAQ를 '수원 고객이 자주 묻는다'는 통계로 표현하지 않는다.
- 레이아웃이 동일 faq 배열로 보이는 FAQ와 JSON-LD를 생성한다. summary는 보이는 요약과 Article abstract에 사용한다.
- sources 배열 원소: title, publisher, url, checked(YYYY-MM-DD), 필요시 published, note. 게시일 미표시는 만들어내지 않는다.
- 본문과 FAQ에 근거 없는 숫자·현재 정책·요금·지원금·법률·뉴스를 넣지 않는다. 이런 정보는 발행 당일 원문을 검색·확인하고 하단 참고 자료에 출처와 게시/확인일을 표기한다.
- 공식 기관·서비스 운영사 자료 우선. 뉴스는 가능하면 원발표와 복수 보도를 확인한다. 기사 문장·구성 복제 금지. 직접 인용은 최대 1회, 15단어 미만.
- 참고 자료는 단순 홈페이지 모음이 아니라 본문 주장을 뒷받침하는 원문이다. 확인하지 않은 링크를 참고 자료에 넣지 않는다.
- '<script', '</script', Liquid 실행문은 글 메타데이터와 본문에 넣지 않는다.
- 기본 레이아웃이 매 글에 본 블로그와 카페 링크, canonical, Organization·BlogPosting·FAQPage를 포함한다. 추가 schema를 중복 삽입하지 않는다.
- AI 추천, 검색 순위, FAQ 리치결과 노출은 보장하지 않는다. llms.txt는 문서 안내다.

## 검증과 게시
1. 두 저장소 전체 기존 글을 reference-posts.json으로 로컬 임시 저장한다.
   형식: {"repositories":[{"name":"htglove/htglove.github.io","head":"최신 SHA","posts":[{"path":"_posts/...md","content":"전체 내용"}]},{"name":"suwon-seongji/suwon-seongji.github.io","head":"최신 SHA","posts":[...]}]}.
   내용이 비어도 repositories에는 두 저장소를 모두 넣는다. 비공개 고객 자료를 저장하지 않는다.
2. 후보와 topics.json 상태·URL·발행일, topics.md 체크, publish-log.json 기록을 함께 준비한다. 후보 선택 이유·전체 기존 글 개수·읽은 HEAD·근거·중복 검토를 기록한다.
3. python scripts/validate.py --reference /path/reference-posts.json 실행. 유사 문단이나 같은 날 글을 발견하면 그대로 게시하지 않는다. 자동 검사는 의미 중복을 완전히 판정하지 못하므로 제목·주제·소제목·문단을 직접 비교한다.
4. 커밋 직전에 두 main HEAD를 다시 읽는다. 바뀌었으면 새 글을 읽고 중복 검사를 다시 한다.
5. 사이트 글·주제 원장·체크리스트·발행 기록을 하나의 커밋으로 반영한다. GitHub create_tree(base_tree는 현재 commit.tree.sha), create_commit(parent는 현재 head), update_ref(expected_sha는 현재 head, force=false) 사용 가능. 강제 덮어쓰기 금지.
6. GitHub Pages 배포 상태를 확인한다. 실패하면 로그를 읽고 이번 변경의 문제를 고친다. 보류 상태를 공개 완료라고 보고하지 않는다.
7. 실제 공개 URL의 제목·본문·FAQ·참고 자료와 JSON-LD를 확인하고 sitemap.xml, rss.xml, llms.txt에 새 URL이 들어갔는지 확인한다.
8. 사용자에게 글 제목·공개 URL·중복 검토 결과를 짧게 보고한다. 미발행이면 이유와 필요한 자료를 보고한다.
9. 같은 글을 재시도할 때 기존 파일·커밋·발행 기록을 확인해 새 파일을 중복 생성하지 않는다.

## 기초 정보 유지
- 기본 운영 문구를 반복해서 새 글을 채우지 않는다.
- 새 글로 sitemap.xml, rss.xml, llms.txt, post-index.json은 Jekyll 빌드 때 자동 갱신된다.
- Naver/Google 소유 확인과 사이트 등록은 별도 작업이다. 등록 완료 근거 없이 완료라고 보고하지 않는다.
- 이 문서와 editorial 디렉터리는 사이트 빌드에서 제외하지만 공개 GitHub 저장소에서는 보인다. 자격 증명과 개인정보를 적지 않는다.
