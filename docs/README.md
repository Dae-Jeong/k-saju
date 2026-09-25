# 문서 안내

문서는 성격별로 세 폴더에 둔다. 같은 내용은 한 문서만 소유하고, 다른 문서는 링크로 가리킨다.

| 폴더 | 소유하는 것 | 문서 |
| --- | --- | --- |
| `policies/` | **무엇을 어떻게 운영하는가** (정책 SSOT, 버전 `plan-vX.Y.Z`) | [README](policies/README.md) · [회원](policies/members.md) · [결제](policies/payments.md) · [AI 사용 내역](policies/ai-usage.md) · [i18n](policies/i18n.md) · [사주 (계산 방법론 포함)](policies/saju.md) |
| `planning/` | **사용자가 무엇을 겪는가** (기획) | [경쟁 서비스 분석](planning/competitive-analysis.md) · [유저 저니](planning/user-journey.md) · [사이트맵](planning/sitemap.md) · [와이어프레임](planning/wireframes.html) · [FAQ·푸터](planning/content.md) |
| `architecture/` | **어떻게 만드는가** (기술 설계) | [도메인 경계](architecture/domains.md) · [AI 모듈](architecture/ai-module.md) · [i18n 흐름·데이터](architecture/i18n.md) · [환경변수](architecture/env.md) · [배포 인프라](architecture/infra.md) |

## 읽는 순서

1. 정책 버전과 합의 현황: [policies/README.md](policies/README.md)
2. 사용자 흐름: [planning/user-journey.md](planning/user-journey.md) → [planning/sitemap.md](planning/sitemap.md)
3. 구현 설계: [architecture/domains.md](architecture/domains.md)부터

## 규칙

- 결정은 `policies/`에 정책 ID(`MEM-`, `PAY-`, `AIU-`, `I18N-`, `SAJU-`)로 남긴다. 기획·설계 문서는 결정을 다시 쓰지 않고 ID로 가리킨다.
- 구조도는 mermaid로 그리고 렌더링을 확인한다. 서버 구성도는 `architecture/server-architecture.html` + `images/`의 PNG로 관리한다.
