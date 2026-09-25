# Service (이름 미정)

FastAPI backend (`be/`) + Next.js frontend (`fe/`) + PostgreSQL, orchestrated
with Docker Compose. See `AGENTS.md` for project conventions and routing.

## Local architecture

```mermaid
flowchart LR
    Browser["Browser"]

    subgraph Host["Host (make dev-be / make dev-fe)"]
        direction TB
        Web["web · Next.js<br/>localhost:3000"]
        Api["api · FastAPI<br/>localhost:8000"]
    end

    subgraph Docker["Docker · infra/docker/compose.local.yaml (project saju)"]
        direction TB
        WebC["saju-web<br/>127.0.0.1:3000"]
        ApiC["saju-api<br/>127.0.0.1:8000<br/>start.sh: alembic → uvicorn"]
        Pg[("saju-postgres<br/>PostgreSQL 18 + pgvector<br/>127.0.0.1:5433 → 5432")]
        Vol[["volume<br/>saju_postgres-data"]]
    end

    Browser -->|"pages (SSR)"| Web
    Browser -->|"API calls · CORS<br/>NEXT_PUBLIC_API_BASE_URL"| Api
    Api -->|"asyncpg · localhost:5433"| Pg

    Browser -.->|"make up (profile app)"| WebC
    Browser -.-> ApiC
    ApiC -.->|"asyncpg · postgres:5432"| Pg
    Pg --- Vol
```

- 실선: 평소 개발 — `make db` 로 postgres만 컨테이너, api·web은 호스트 프로세스.
- 점선: 통합 확인 — `make up` 으로 api·web도 컨테이너(profile `app`). 같은 3000/8000 포트를 쓰므로 둘 중 하나만 띄운다.
- `make down` 은 api·web만 내리고 postgres는 유지한다.

## Deployment architecture (설계안)

![Server architecture](docs/images/server-architecture.png)

prod 단일 · fe는 Vercel · be(api·worker·migrate)는 관리형 컨테이너 · 관리형 PostgreSQL + pgvector · 서비스명·도메인·클라우드 미정.
네트워크 규칙, 클라우드별 대응, 배포 흐름은 [`docs/infra-architecture.md`](docs/infra-architecture.md)를 본다.

## Environment variables

```mermaid
flowchart TB
    Spec["<b>.env.example</b> (git 커밋)<br/>변수 명세 · required / optional"]
    Env["<b>.env</b> (gitignore)<br/>로컬 값의 유일한 원천"]
    Spec -->|"make env<br/>(최초 1회, 덮어쓰지 않음)"| Env

    subgraph Local["로컬"]
        direction LR
        Host["호스트 프로세스<br/>make dev-be · dev-fe · migrate · test"]
        Ctr["컨테이너 (make up)<br/>saju-api · saju-web"]
    end

    Env -->|"Makefile export<br/>set -a; . ./.env"| Host
    Env -->|"compose --env-file .env<br/>environment: ${VAR:?}"| Ctr

    subgraph Deploy["배포 (OCI, 추후)"]
        Srv["서버 · 컨테이너 런타임 환경변수<br/>비밀값: Vault → 환경변수<br/>서버에 .env 파일 없음"]
    end

    Validate{"앱 시작 시 검증<br/>be: Settings() · pydantic<br/>fe: env-config.ts · zod"}
    Host -->|"OS 환경변수"| Validate
    Ctr -->|"OS 환경변수"| Validate
    Srv -->|"OS 환경변수"| Validate

    Validate -->|"통과"| Run["기동"]
    Validate -->|"누락 · 형식 오류"| Fail["누락 키 전부 출력<br/>exit 1"]
```

> fe 예외: `NEXT_PUBLIC_*`는 빌드 시 JS 번들에 박힌다 → docker build arg로 전달하고 빌드 단계에서 검증한다.

- 변수 추가·변경은 `.env.example`에 먼저 적는다 (`# required` / `# optional (default: X)`).
- 앱은 `.env`를 직접 읽지 않는다. 필수 값이 없으면 기동하지 않는다.
- 자세한 규칙과 검증 지점: [`docs/env.md`](docs/env.md)

## Quick start

```sh
make env         # create .env from .env.example (see docs/env.md)

make db          # start postgres only (127.0.0.1:5433)
make migrate     # apply backend migrations
make dev-be      # run the backend locally (127.0.0.1:8000)
make dev-fe      # run the frontend locally (127.0.0.1:3000), in another shell
```

Or run everything in containers:

```sh
make up          # build + start api, web, postgres
make down        # stop api+web (postgres keeps running)
```

## Checks

```sh
make lint
make test
make fmt
```

See `be/README.md` and `fe/README.md` for per-app details.
