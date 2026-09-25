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
