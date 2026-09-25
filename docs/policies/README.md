# 정책 (Policies)

Version: **v0.1.0** · 회원·결제·AI 사용 내역·i18n 합의, 사주는 "보고서"로 추상화한 상태.
사주 심층 설계까지 끝나면 **v1.0.0**으로 올리고 git 태그 `plan-v1.0.0`을 붙인다. 버전마다 git 태그 `plan-vX.Y.Z`를 남긴다.

도메인 경계는 [../domains.md](../domains.md), 단계별 흐름은 [../user-journey.md](../user-journey.md)를 따른다.

## 원칙

- 정책은 도메인 → 하위 모듈 → 정책 항목 순으로 나눈다. 하위 모듈은 자기 데이터와 불변 규칙을 가진다.
- 정책 항목 하나는 **규칙**(거의 안 바뀜, 코드의 순수 함수)과 **파라미터**(운영 중 바뀜, 설정값)로 나눈다.
- 돈과 크레딧에 관한 기록은 지우지 않는다. 정정도 새 기록으로 남긴다.
- 모든 항목은 하나씩 논의해서 합의한 뒤 `합의`로 표시한다.
- **운영 기준은 한국법**이다 (약관 준거법·관할 한국). 해외 규정은 지켜야 할 최소선으로 챙긴다: 개인정보(GDPR), 디지털 상품 세금, 청약 철회 고지.

## 문서

| 도메인 | 문서 | ID 접두사 | 상태 |
| --- | --- | --- | --- |
| 회원 | [members.md](members.md) | `MEM-` | 합의 |
| 결제 | [payments.md](payments.md) | `PAY-` | 합의 (확인 필요 항목 있음) |
| 사주 | saju.md | `SAJU-` | 보류 (보고서로 추상화, 별도 심층 설계) |
| AI 사용 내역 | [ai-usage.md](ai-usage.md) | `AIU-` | 합의 |
| i18n | [i18n.md](i18n.md) | `I18N-` | 합의 |

## 정책 항목 템플릿

```text
### PAY-000 제목
- 상태: 초안 | 합의
- 규칙: 무엇이 언제 어떻게 되는가
- 파라미터: 운영 중 바뀔 수 있는 값 (아래 파라미터 목록에도 등록)
- 적용 지점: 어느 모듈의 어느 공개 함수에서 실행되는가
- 사용자 고지: 화면·약관 문구 요지
```

## 파라미터 목록

운영 중에 바꿀 수 있는 값을 한곳에 모은다. 처음에는 코드 상수로 두고, 자주 바뀌면 DB·관리 화면으로 옮긴다.

| 키 | 값 | 정책 |
| --- | --- | --- |
| `credit.unit_price_usd` | 0.99 | PAY-001 |
| `credit.packs` | 1: $0.99 · 3: $2.97 · 10: $9.90 (+1) · 100: $99.00 (+20) | PAY-002 |
| `credit.large_pack_requires_prior_purchase` | true (100크레딧 묶음) | PAY-002 |
| `order.expire_minutes` | 30 | PAY-010 |
| `member.min_age` | 16 | MEM-007 |
| `member.session_days` | 30 | MEM-010 |
| `member.retention.payment_years` | 5 | MEM-011 |
| `member.retention.dispute_years` | 3 | MEM-011 |
| `credit.expiry.paid_years` | 5 | PAY-021 |
| `credit.expiry.bonus_years` | 1 | PAY-021 |
| `credit.expiry.notice_days` | 30 | PAY-023 |
| `payment.sync_after_minutes` | 5 | PAY-033 |
| `payment.reconcile_cron` | 매일 1회 | PAY-033 |
| `refund.withdrawal_days` | 7 | PAY-040 |
| `ai.model_prices` | 모델별 단가표 | AIU-002 |
| `ai.max_retries` | 2 | AIU-005 |
| `i18n.locales` | ko, en | I18N-005 |
| `i18n.default_locale` | ko | I18N-005 |
| `i18n.fallback_locale` | en | I18N-006 |
| `refund.balance_fee_rate` | 0.10 | PAY-041 |
| `credit.first_purchase_bonus` | 1 | PAY-003 |
| `product.detailed_report.credits` | 3 | PAY-005 |

## 변경 이력

| 버전 | 날짜 | 내용 |
| --- | --- | --- |
| v0.1.0 | 2026-09-25 | 정책 모듈 구조 도입. 회원·결제·AI 사용 내역·i18n 합의. 사주는 보고서로 추상화(심층 설계 보류) |
