# 저장소 표면

이 저장소는 공개 OSS 저장소라기보다 `협업 + 제출 + 제품` 저장소입니다.

그래서 표면을 두 층으로 나눠서 봅니다.

## Public-facing surface

- `README.md`
- `product/sdv_operator/README.md`
- `product/sdv_operator/docs-src/*`
- generated docs site

외부 사용자는 이 층만 보면 됩니다.

## Internal working surface

- `canoe/`
- `driving-alert-workproducts/`
- `reference/`
- `scripts/*` 내부 구현
- handoff, mentoring, team board, tmp, reports

이 층은 내부 협업과 제출 추적성을 위한 작업면입니다.

## 운영 원칙

1. public-facing surface는 계속 얇게 유지합니다.
2. internal working surface는 숨기지 말고, 다만 전면 진입점에서는 노출을 줄입니다.
3. repo 전체를 공개 OSS처럼 보이게 만들기보다, public docs entry를 명확하게 유지합니다.
