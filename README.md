# 수원 휴대폰 성지

올댓폰이 운영하는 수원 시민용 구매·통신 생활 가이드.

- 사이트: https://suwon-seongji.github.io/
- 본 블로그: https://htglove.github.io/
- 카페: https://cafe.naver.com/cutebell

## 발행

GitHub Pages: main / (root), Jekyll. 2026-11-04 사용자 요청으로 첫 글 게시와 예약 발행을 취소했습니다. 현재 게시글과 예약 작업은 없으며 사이트 기본 틀만 유지합니다. 사용자가 발행 재개를 명시적으로 요청하기 전에는 글을 게시하거나 예약을 만들지 않습니다.

작업 규칙: [editorial/PUBLISHING.md](editorial/PUBLISHING.md)
주제 원장: [editorial/topics.json](editorial/topics.json)
주제 체크리스트: [editorial/topics.md](editorial/topics.md)
현지 자료: [editorial/local-facts.json](editorial/local-facts.json)

글 front matter는 JSON 형태의 유효한 YAML을 사용합니다. 레이아웃이 요약·FAQ 본문과 JSON-LD, 참고 자료, 본 블로그·카페 링크를 렌더링합니다. sitemap.xml은 jekyll-sitemap이 생성하고 RSS·llms·글 색인은 글 목록에서 자동 갱신됩니다.

검사: python scripts/validate.py --reference ../reference-posts.json
(참조 파일은 매번 두 저장소 최신 전체 글로 다시 생성. 경로는 실행 환경에 맞게 지정.)
로컬 미리보기: bundle install && bundle exec jekyll build

Naver/Google 소유 확인 값은 이 호스트에 대해 새로 발급받아 _config.yml의 naver_verification/google_verification에 넣습니다. 본 블로그의 값을 복사하지 않습니다.
