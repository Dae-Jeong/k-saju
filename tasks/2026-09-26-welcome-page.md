# Task 1. Welcome 페이지 구현·배포

상태: 검증 완료 — 배경 분리 변경과 작업 기록의 origin 반영·배포 확인 예정.

목표:
서비스 준비 중임을 알리는 welcome 페이지를 구성하고, PC에서도 모바일처럼 좁은 세로 화면으로 제공한다.

예상 결과:
- 브랜드 A의 색상·글꼴·단청 장식과 예시 카드가 있는 welcome 페이지.
- PC에서도 최대 폭 448px로 가운데 정렬되고, 소개와 카드가 세로로 이어지는 화면.
- PC의 바깥 회색 배경과 서비스 내부 한지색이 구분되는 화면.
- lint·테스트 결과와 검증하지 못한 범위가 기록되고, origin 반영 및 Vercel 배포가 확인된 상태.

## 구현과 선택 이유

| 내용 | 방식·이유 | 근거 |
| --- | --- | --- |
| 브랜드 표현 | 한지·먹·오행 색상을 공통 토큰으로 관리하고, 제목은 Noto Serif KR, 본문은 Noto Sans KR 사용 | [브랜드 시안](../docs/design/brand-a.html), [tokens.css](../fe/src/common/styles/tokens.css), [layout.tsx](../fe/src/app/layout.tsx) |
| 세로 화면 | `w-full max-w-md mx-auto`로 폭과 중앙 정렬, `flex-col`로 소개와 카드의 세로 배치. 사용자가 웹에서도 세로 화면을 요청 | [page.tsx](../fe/src/app/page.tsx) |
| 바깥·안쪽 배경 | 바깥은 `canvas`(`#e9e7e2`), 서비스 내부는 한지색(`#f6f1e7`). `shadow-sm`으로 경계를 보완. 같은 배경색으로 화면 경계가 흐려진다는 사용자 피드백 반영 | [globals.css](../fe/src/app/globals.css), [tokens.css](../fe/src/common/styles/tokens.css), [PC 화면](images/welcome-desktop.png) |
| 단청 재사용 | 휘 띠를 `HwiBand` SVG 컴포넌트로 분리해 헤더와 카드에 사용 | [hwi-band.tsx](../fe/src/common/components/dancheong/hwi-band.tsx) |
| 준비 중 안내 | 아직 실행할 기능이 없어 준비 중 문구로 표시. 가짜 사업자·연락처 정보는 제거 | [page.tsx](../fe/src/app/page.tsx) |

## 검증 근거와 한계

- `make lint`: 백엔드 ruff·ty, 프론트엔드 ESLint·타입 검사 통과.
- `make test`: 로컬에서 15 passed, 2 skipped. 프론트엔드 자동 테스트 suite는 아직 없으며, 타입 검사와 실제 화면으로 검증.
- skip 항목: `test_pgvector_extension_is_installed`, `test_readiness_returns_ok_when_database_reachable`. 로컬 `localhost:5433` DB 연결 불가 시 skip하도록 작성되어 있어, 이번 로컬 실행에서는 두 DB 연동 항목을 검증하지 못함.
- PC 1920×1080: 실제 렌더링에서 가운데 세로 화면, 바깥 회색·내부 한지색, 제목·카드·푸터 배치를 확인. [캡처](images/welcome-desktop.png).
- 모바일 390px: 서비스 화면 폭 390px, 한지색 배경, 가로 넘침 없음 확인.
- 실행: `PORT=3002 make dev-fe`. `http://localhost:3002/`에서 HTTP 200 및 welcome 제목 확인.
- 캡처 도구: Orca 브라우저의 화면 캡처가 탭 표시 상태 때문에 timeout되어, 별도 임시 프로필의 Chrome Headless로 PC 캡처. 모바일은 Orca 브라우저에서 DOM 크기·색상 확인.

## 2026-09-26 작업 기록

1. 사용량 제한으로 멈춘 기존 작업을 확인하고, 남아 있던 welcome 변경을 이어서 검증.
2. 준비 중 안내와 예시 카드를 정리하고 `feca8d6`으로 구현 반영.
3. 사용자의 웹·모바일 세로 배치 요청을 반영하고 `1082be0`으로 origin/main에 push. 해당 CI와 Vercel 배포 성공, 운영 도메인에서 세로 배치 확인.
4. 사용자 화면 피드백에 따라 바깥 배경과 서비스 내부 배경을 분리. 로컬 검증 완료.

## 2026-09-27 작업 기록

1. 이번 task 문서·목록과 PC 캡처를 추가. 배경 분리 변경과 함께 origin에 반영 후 배포 확인 예정.

## 배포 확인

- 대상: `origin/main`, FE Vercel 자동 배포.
- 운영 페이지: <https://saju.marinkim.xyz>.
- 이번 배경 분리 변경의 CI·운영 반영: push 후 확인 예정.

## 후속 작업

이번 요청 범위의 구현은 완료했으며, 원격 반영·배포 확인이 남아 있다.

다음 실제 화면 구현 시 공통 폭·여백·글자 계층·버튼·카드 규칙을 정하고, 세로 화면 배치를 공통 레이아웃으로 옮기는 작업을 별도 task로 다룬다. 현재 448px 배치는 welcome 페이지에만 적용되어 있다.
