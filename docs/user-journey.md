# 유저 저니 (초안)

Status: 제안 · 2026-09-25

근거: [경쟁 서비스 분석](research/competitive-analysis.md). 비회원 무료 짧은 리포트 → 1회 결제 상세 리포트, 구독 없음,
대화형이 아니라 입력하면 결과가 나오는 형태.

```mermaid
flowchart TB
    Search(["① 검색"])
    Card(["① 공유된 아키타입 카드"])
    Invite(["① 친구 비교 링크"])

    Landing["랜딩<br/>locale 자동 · 영어 기본"]

    subgraph Input["② 입력 · 가입 없음"]
        Form["이름 · 생년월일 · 성별 · 태어난 시각 · 출생 도시<br/>시각 모르면 정오 기준 (추정 표시)"]
        Calc["명식 계산<br/>출생지 시간대 · 진태양시 보정"]
    end

    subgraph Free["③ 무료 결과 · AI 비용 0"]
        Identity["아키타입 카드<br/>일간 10종 · K-감성"]
        Chart["명식표 · 오행 균형"]
        Summary["짧은 요약"]
        Locked["잠긴 섹션 미리보기<br/>제목 + 첫 줄"]
    end

    subgraph Viral["④ 공유 루프"]
        Share["카드 공유 · OG 이미지"]
        Compare["친구와 비교하기 링크"]
        NewVisitor(["새 방문자 → ① 유입"])
    end

    subgraph Pay["⑤ 결제 · 1회"]
        Signup["가벼운 가입<br/>이메일 링크 · 소셜"]
        Checkout["외부 PG 결제"]
        Webhook["PG 웹훅 확정 · 이용권 지급"]
    end

    subgraph Paid["⑥ 상세 리포트 · AI"]
        Generating["생성 중 · 이용권 예약"]
        Report["상세 리포트<br/>성격 · 연애 · 직업/재물 · 건강 · 대운 · 올해"]
        Retry["실패: 과금 없이 재시도<br/>이용권 복구"]
        PDF["PDF 다운로드"]
    end

    subgraph After["⑦ 재방문 · 사후"]
        MyReports["내 리포트 목록"]
        Refund["7일 환불 요청"]
        Delete["탈퇴 · 데이터 삭제"]
    end

    Search --> Landing
    Card --> Landing
    Invite -->|"친구가 입력하면 궁합 미리보기"| Landing
    Landing --> Form --> Calc --> Identity --> Chart --> Summary --> Locked

    Identity -.-> Share
    Identity -.-> Compare
    Share -.-> NewVisitor
    Compare -.-> NewVisitor

    Locked -->|"더 보기"| Signup --> Checkout --> Webhook --> Generating
    Generating -->|"성공 · 이용권 차감"| Report
    Generating -->|"실패"| Retry
    Report --> PDF
    Report --> MyReports
    MyReports --> Refund
    MyReports --> Delete
```

## 단계별 도메인

| 단계 | 주 도메인 | 핵심 정책 |
| --- | --- | --- |
| ① 유입 · 랜딩 | i18n | 영어 기본, 지원하지 않는 locale은 en |
| ② 입력 | 사주 · 회원 | 동양 사주 기준만 사용. 이름·생년월일·성별 입력, 시각과 도시는 최대한 받되 시각을 모르면 정오로 계산하고 시주를 추정으로 표시. 출생지 시간대 → UTC 저장. 이름은 표시용이며 LLM에 보내지 않음 |
| ③ 무료 결과 | 사주 · i18n | AI 호출 없음, 미리 써둔 콘텐츠, 같은 입력이면 같은 결과 |
| ④ 공유 루프 | 사주 | 카드·요약만 공개, 상세 리포트는 비공개. 점선은 선택 흐름 |
| ⑤ 결제 | 회원 · 결제 | 결제 시점 가입, 결제 확정은 웹훅 기준, 멱등 처리 |
| ⑥ 상세 리포트 | 사주 · AI 사용 내역 · 결제 | 이용권 예약 → 성공 시 차감 / 실패 시 복구, 호출마다 비용 기록·한도 확인 |
| ⑦ 재방문 · 사후 | 회원 · 결제 | 리포트 재열람 보장, 7일 환불, 탈퇴 시 개인정보 삭제·결제 기록은 분리 보관 |

## 상세 흐름 — 방문부터 가입·결제·리포트까지

회원 정책([members.md](policies/members.md))과 결제 정책([payments.md](policies/payments.md))을 반영한 흐름이다.

```mermaid
sequenceDiagram
    autonumber
    actor U as 사용자
    participant B as 브라우저 저장소
    participant FE as fe
    participant BE as be
    participant T as Toss Payments
    participant GA as GA4

    Note over U,GA: ① 비회원 체험 — 서버 저장 없음 (MEM-003)
    U->>FE: 방문 (검색 · 공유 카드 · 친구 링크)
    FE->>GA: page_view (EU는 쿠키 동의 후)
    U->>FE: 이름 · 생년월일 · 성별 · 시각 · 출생 도시 입력
    FE->>B: 입력값 보관
    FE->>BE: 명식 계산 요청
    BE-->>FE: 명식 · 무료 결과 (저장하지 않음)
    FE-->>U: 아키타입 카드 · 명식표 · 오행 · 요약 · 잠긴 섹션
    opt 공유
        U->>FE: 카드 공유
        FE-->>U: 명식 코드만 담긴 공유 링크 (개인정보 없음)
    end

    Note over U,GA: ② 가입 — 결제 직전에만 (MEM-002, MEM-004)
    U->>FE: 상세 리포트 보기
    FE-->>U: 가입 요청 (Google · Apple · 이메일 매직 링크)
    U->>FE: 가입 · 약관 동의 · 16세 이상 확인
    FE->>BE: 계정 생성 + 브라우저의 입력값 전송
    BE-->>FE: 명식을 계정에 처음 저장

    Note over U,GA: ③ 크레딧 구매 (PAY-001~034)
    FE-->>U: 판매 페이지 Free · 1 · 3 · 10★ · 100
    U->>FE: 묶음 선택
    FE->>BE: 주문 생성 (가격 고정 · 30분 만료)
    FE-->>U: 주문 요약 + Toss 결제 위젯
    U->>T: 결제 (해외 카드 · PayPal, USD)
    T-->>FE: successUrl (인증 완료)
    FE->>BE: 승인 요청
    BE->>T: 금액 검증 후 결제 승인 API
    T-->>BE: 승인 완료
    BE->>BE: 크레딧 로트 지급 (결제 5년 · 보너스 1년) + 첫 구매 보너스
    FE->>GA: purchase (금액 · 묶음만)

    Note over U,GA: ④ 상세 리포트 (PAY-020~023)
    U->>FE: 상세 리포트 생성
    FE->>BE: 생성 요청
    BE->>BE: 3크레딧 예약 (보너스 → 만료 빠른 순)
    BE-->>FE: 생성 중
    alt 성공
        BE->>BE: 예약 확정
        FE-->>U: 상세 리포트 · PDF
    else 실패
        BE->>BE: 예약 해제 (크레딧 복구)
        FE-->>U: 다시 시도 안내
    end

    Note over U,GA: ⑤ 재방문 · 사후 (MEM-008, PAY-040~045)
    U->>FE: 로그인 (세션 유지)
    FE-->>U: 내 리포트 · 크레딧 잔액 · 유효기간 · 구매 내역
    opt 환불 버튼
        U->>BE: 환불 요청
        BE->>T: 청약 철회 전액 또는 잔액 환불 (10% 공제)
        BE->>BE: 크레딧 회수 기록
    end
```
