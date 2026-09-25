# Agent Entry

이 파일은 이 저장소 고유의 라우팅과 사실만 소유한다. 머신 공통 규칙(git 제한, 로컬
포트 규약, 커밋 정책 등)은 이 파일에 복제하지 않는다 — `/Users/marin/AGENTS.md`와
그것이 가리키는 글로벌 agent wiki를 먼저 따른다.

## 프로젝트 이름

디렉터리명 `k-saju`는 임시 작업 폴더명일 뿐, 최종 프로젝트 이름이 아니다. 코드,
설정, 패키지명, 컨테이너 이름 등 어디에도 `k-saju`/`ksaju`를 쓰지 않는다. compose
프로젝트 기본값 `saju`(`COMPOSE_PROJECT_NAME`)만 예외로 승인되어 있다.

## 레이아웃

| 경로 | 역할 |
| --- | --- |
| `be/` | FastAPI 백엔드. 상세는 `be/README.md`, `be/AGENTS.md`(있다면) |
| `fe/` | Next.js 프론트엔드. 상세는 `fe/README.md`, `fe/AGENTS.md` |
| `infra/terraform/` | 인프라 as code. 아직 비어 있음(후순위, 아래 참고) |
| `docs/` | 저장소 문서 |
| `tasks/` | 작업 기록 |
| `compose.yaml`, `Makefile`, `.env.example` | 루트 오케스트레이션 |

## 스택

- 백엔드: FastAPI + uv + SQLAlchemy(async) + Alembic + PostgreSQL
- 프론트엔드: Next.js 16 + pnpm + Tailwind + shadcn/radix + TanStack Query
- DB: PostgreSQL (compose의 `postgres` 서비스, 컨테이너 `saju-postgres`)

## 참고 소스

새 코드를 작성하기 전에 아래 기존 구현을 참고한다. 아이디어·패턴만 가져오고
그대로 복사하지 않는다.

- 백엔드 패턴: `/Users/marin/personal-workspace/backend-template/python/fastapi`
- 프론트엔드 패턴: `/Users/marin/workspace/ceramique-fe`

## 설정은 라이브러리 CLI로

설정 파일을 손으로 새로 쓰지 않는다. 해당 라이브러리의 CLI로 생성하고 필요한
부분만 고친다.

- 백엔드 의존성/가상환경: `uv`
- 마이그레이션: `alembic`
- 프론트엔드 패키지: `pnpm`
- UI 컴포넌트: `shadcn`

## 로컬 포트

| 용도 | 포트 |
| --- | --- |
| PostgreSQL (compose `postgres`) | 5433 |
| 메인 백엔드 | 8000 |
| 메인 프론트엔드 | 3000 |
| 격리 작업 백엔드 | 8001 이상 |
| 격리 작업 프론트엔드 | 3001 이상 |

3000/8000은 사용자 실사용 표면이다. 파괴적 실험은 격리 포트에서 한다. 자세한
DB/앱 격리 규약은 글로벌 agent wiki의 로컬 개발 환경 규약을 따른다.

## Make 타겟 (작업 기준)

사람과 agent 모두 실행·검증을 아래 make 타겟으로 한다. 같은 일을 하는 임의 명령
(`docker compose ...`, `uv run ...`, `pnpm ...` 직접 호출)을 새로 만들지 않는다. 타겟이
부족하면 Makefile에 추가하고 이 목록을 갱신한다. 변경 완료 전 `make lint`와
`make test`를 통과시킨다. 루트에서 `make help`로 전체 목록을 본다.

- `make db` / `make db-down` — postgres만 기동/중지 (볼륨 유지)
- `make dev-be` / `make dev-fe` — 로컬 프로세스로 개별 실행
- `make migrate` — alembic 마이그레이션
- `make up` / `make down` — `api`+`web`+`postgres` 전체를 컨테이너로 기동 (profile `app`) / `down`은 api·web만 내리고 postgres는 유지
- `make lint` / `make test` / `make fmt` — be+fe 전체

## infra

`infra/terraform/`은 아직 비어 있다. OCI(Oracle Cloud Infrastructure)를 배포 대상
후보로 검토 중이며, 실제 구성은 후순위 작업이다.

## 프론트엔드 세부 규칙

Next.js가 자동 생성/갱신하는 `fe/AGENTS.md`는 그대로 둔다. `fe/` 안에서 작업할
때는 그 파일도 함께 읽는다. `CLAUDE.md`는 두지 않는다 — Claude Code도 `AGENTS.md`를
읽는다. (`fe/AGENTS.md`가 있으면 `next dev`는 `CLAUDE.md`를 재생성하지 않는다.)
