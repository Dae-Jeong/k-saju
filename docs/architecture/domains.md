# 도메인 경계와 의존성 (초안)

Status: 제안 · 2026-09-25

be의 업무 도메인은 다섯 개다: 회원, 결제, 사주, i18n, AI 사용 내역. `ai/`는 도메인이 아니라 LLM 실행
인프라이고, 외부 PG는 `integrations/pg/` 어댑터 뒤에 둔다. 폴더는 현재 구조(역할 폴더 + 도메인 파일)를 유지한다.

## 의존 방향

```mermaid
flowchart TB
    R["routers · HTTP API"]
    W["worker · job 실행"]
    WH["PG 웹훅 router"]

    Saju["사주 saju<br/>readings · chart · interpretations"]

    Calc["domain/saju<br/>명식 계산 (순수 함수)"]
    AI["ai.facade<br/>LLM · Embedding 실행"]
    Pay["결제 payments<br/>주문 · 결제 · 크레딧"]
    I18n["i18n<br/>지원 locale · 용어 번역"]

    Usage["AI 사용 내역 ai_usage<br/>호출 기록 · 한도 · 비용"]
    PG["integrations/pg<br/>외부 PG 어댑터"]

    Member["회원 members<br/>users · 인증 · locale/country<br/>모든 도메인이 user_id로만 참조"]

    R --> Saju
    W --> Saju
    WH --> Pay

    Saju -->|"명식 계산"| Calc
    Saju -->|"해석 생성"| AI
    Saju -->|"크레딧 확인·차감"| Pay
    Saju -->|"locale · 용어"| I18n

    AI -->|"한도 확인 · 기록"| Usage
    Pay -->|"결제 · 서명 검증"| PG

    R -.->|"회원 API"| Member

    classDef domain fill:#e8f1fb,stroke:#4f7fac,color:#1f3b57
    classDef infra fill:#f3f4f6,stroke:#9aa4ac,color:#344451
    classDef entry fill:#ffffff,stroke:#b4bec6,color:#344451
    class Saju,Pay,I18n,Usage,Member domain
    class Calc,AI,PG infra
    class R,W,WH entry
```

- 파란 상자는 도메인, 회색 상자는 인프라·순수 로직이다.
- 실선은 호출 방향이다. 호출은 위에서 아래로만 흐르고 역방향은 금지한다 (예: 결제가 사주를 호출하지 않는다).
- routers는 사주 외에도 회원·결제·i18n의 service를 직접 호출한다 (그림에서는 결제·i18n 화살표를 생략했다).
- 회원은 모든 도메인이 `user_id`로만 참조한다. 회원 도메인의 테이블·repository를 직접 읽지 않는다.
- 도메인끼리는 상대 도메인 service의 공개 함수로만 호출한다.
- `ai.facade`는 사주에서만 호출한다. 호출마다 `ai_usage`로 한도를 확인하고 결과를 기록한다.
- 외부 PG는 `integrations/pg/` 포트 뒤에 둔다. PG를 바꿔도 결제 도메인은 바뀌지 않는다.
