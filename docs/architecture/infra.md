# 배포 아키텍처 (클라우드 중립)

Status: 운영 중 (2026-09-26) · 아래 "현재 운영 구성"이 실제 상태다. 그 뒤의 논리 구조·클라우드별 대응은 초기 설계안으로 남겨 둔다.

클라우드와 무관한 논리 구조를 먼저 정한다. 각 구성요소는 아래 대응표로 클라우드별 서비스에
매핑한다. 이 규모에서는 클라우드마다 구조 차이가 거의 없다.

## 현재 운영 구성

```mermaid
flowchart LR
    User(["사용자"])
    GH["GitHub · Dae-Jeong/k-saju"]
    CI["GitHub Actions CI<br/>be lint·migrate·test · fe lint·build"]

    subgraph Vercel["Vercel (Hobby)"]
        Web["fe · Next.js<br/>saju.marinkim.xyz"]
    end

    subgraph OCI["OCI 춘천 · A1 2 OCPU / 12GB (Always Free)"]
        Nginx["nginx + certbot<br/>saju-api.marinkim.xyz · HTTPS<br/>(MarinInfra 소유)"]
        Api["saju-api · FastAPI :8000<br/>edge + internal 네트워크"]
        Pg[("saju-postgres<br/>PostgreSQL 18 + pgvector<br/>internal 네트워크만")]
        Backup["cron 03:30 백업<br/>14일 보관"]
    end

    User -->|"HTTPS"| Web
    User -->|"HTTPS · API 호출 (CORS)"| Nginx
    Nginx --> Api --> Pg
    Backup -.-> Pg
    GH --> CI
    GH -->|"push → 자동 배포"| Web
    GH -.->|"make deploy-be (pull · 서버 빌드)"| Api
```

| 항목 | 내용 |
| --- | --- |
| fe | Vercel 프로젝트 `k-saju` (Root `fe`, Node 24). `main` push 시 자동 배포. 환경변수는 `NEXT_PUBLIC_API_BASE_URL`만 |
| be | OCI A1 서버. 앱 compose는 이 레포 `infra/docker/compose.prod.yaml`, 배포는 `make deploy-be` (서버에서 `git pull` 후 arm64 빌드·교체, 컨테이너 시작 시 마이그레이션) |
| 서버·프록시 | 초기 세팅, 방화벽, nginx, 인증서, 도메인은 private 레포 `Dae-Jeong/MarinInfra`가 소유 |
| DB | 같은 서버의 `saju-postgres` 컨테이너. 외부 노출 없음. 매일 03:30 `pg_dump` 백업 14일 보관 |
| 비밀값 | 서버의 `infra/docker/.env.prod`(권한 600)에만. 레포·Vercel에 없음 |
| DNS (가비아) | `saju` A → 76.76.21.21 (Vercel) · `saju-api` A → 168.110.100.93 (OCI) |
| 비용 감시 | OCI 예산 `free-tier-guard` $1/월 알림 |

### 후속 과제

- be 자동 배포 (지금은 `make deploy-be` 수동)
- 운영에서 API 문서(`/docs`) 노출 여부 결정
- uvicorn이 nginx 전달 헤더(X-Forwarded-*)를 신뢰하도록 설정
- Vercel Hobby는 비상업용 — 결제 시작 전에 Pro로 전환

## 전제

- 환경: `prod` 하나
- fe: Vercel
- be: 관리형 컨테이너 서비스 (VM·Kubernetes 아님)
- DB: 관리형 PostgreSQL + pgvector. 컨테이너 안에 DB를 두지 않는다 (컨테이너 디스크는 휘발성)
- 비용: 가능한 한 무료 한도 안에서 운영
- 도메인: fe `saju.marinkim.xyz` (Vercel), api `saju-api.marinkim.xyz` (OCI 서버 nginx). 서비스명은 미정

## 논리 구조

```mermaid
flowchart TB
    User(["User"])
    DNS["DNS · marinkim.xyz (가비아)"]

    subgraph Vercel["Vercel"]
        Web["web · Next.js (SSR)<br/>saju.marinkim.xyz"]
    end

    subgraph Cloud["Cloud (prod)"]
        direction TB
        subgraph Run["관리형 컨테이너 서비스"]
            Api["api · FastAPI<br/>saju-api.marinkim.xyz<br/>HTTPS"]
            Worker["worker<br/>같은 be 이미지 · 다른 command<br/>외부 ingress 없음"]
        end
        Migrate["migrate job<br/>alembic upgrade head<br/>배포마다 1회"]
        DB[("PostgreSQL + pgvector<br/>관리형 · 자동 백업")]
        Secrets["Secret store<br/>→ 컨테이너 환경변수"]
        Registry["Container Registry"]
        Storage["Object Storage<br/>RAG 원문"]
        Logs["Logs · Metrics"]
    end

    LLM["외부 LLM · Embedding API"]
    GH["GitHub Actions"]

    User --> DNS
    DNS --> Web
    DNS --> Api
    Web -->|"SSR · 브라우저 API 호출 (CORS)"| Api
    Api -->|"reading · job 생성"| DB
    Worker -->|"job 선점 · 결과 저장"| DB
    Worker --> LLM
    Worker --> Storage
    Migrate --> DB
    Secrets -.->|"env 주입"| Api
    Secrets -.-> Worker
    Secrets -.-> Migrate
    Registry -.->|"image pull"| Run
    Api -.-> Logs
    Worker -.-> Logs
    GH -->|"build · push"| Registry
    GH -->|"배포: migrate → 롤링 교체"| Migrate
```

### 구성요소 책임

| 구성요소 | 책임 | 비고 |
| --- | --- | --- |
| web | 화면·SSR. Vercel이 빌드·배포 | `NEXT_PUBLIC_API_BASE_URL`은 Vercel 빌드 환경변수 |
| api | HTTP API. LLM을 직접 호출하지 않음 | 최소 1개 인스턴스 (콜드스타트 허용 여부는 비용과 함께 결정) |
| worker | job 실행 (RAG · LLM 호출) | ingress 없음. 폴링 방식이라 상시 1개 필요 |
| migrate job | 스키마 마이그레이션 | 앱 기동과 분리. 배포 파이프라인에서 api 교체 전에 실행 |
| DB | 원장 + 벡터 검색 | pgvector 지원 필수. 컨테이너에 두지 않음 |
| Secret store | DB 비밀번호, LLM API 키 | 앱은 환경변수만 읽음 ([env.md](env.md)) |
| Object Storage | RAG 원문 문서 | 임베딩 결과는 DB에 저장 |

## 네트워크

![Server architecture](images/server-architecture.png)

> 설계안 · 미구현. 클라우드 미정이라 아이콘은 모두 일반화된 심볼이며 특정 클라우드 제품을
> 가리키지 않는다. 전체 배치도(HTML/SVG 원본): [server-architecture.html](server-architecture.html)

| 서브넷 | 구성요소 | 인바운드 | 아웃바운드 |
| --- | --- | --- | --- |
| Public subnet | Load Balancer / Ingress, NAT Gateway | 인터넷 → 443(TLS) | LB → private·app; NAT → 인터넷(egress 중계) |
| Private subnet · app | api, worker, migrate job | LB에서만(api) · 외부 ingress 없음(worker·migrate) | DB로 SQL, NAT 경유 외부 LLM API 호출 |
| Private subnet · data | PostgreSQL + pgvector | api·worker·migrate에서만(같은 VPC 내부) | 없음 (public 없음) |

- private 서브넷은 LB를 통해서만 외부에서 도달 가능하다. api·worker·migrate에는 직접 ingress가 없다.
- DB는 public endpoint를 두지 않는다. private endpoint로만 연결한다.
- private 앱 서브넷의 아웃바운드(LLM API 호출 등)는 NAT를 통해서만 나간다.
- 배치도에서는 Load Balancer(ingress)와 NAT(egress)를 이해를 돕기 위해 별도 박스로 그렸다. 위
  표처럼 실제로는 하나의 public subnet일 수 있다(클라우드 확정 시 결정).
- NAT Gateway는 대체로 무료가 아니다(시간당 과금 + 처리 데이터 과금). 클라우드를 확정할 때 비용을
  다시 확인한다. 무료 한도를 우선한다면 대안으로 api·worker를 public subnet에 두고
  보안 그룹(inbound 제한)으로 격리하는 방식을 검토한다 — NAT 비용은 없지만 서브넷 격리 수준이 낮아진다.

## 배포 흐름

```mermaid
sequenceDiagram
    autonumber
    participant Dev as main push
    participant GH as GitHub Actions
    participant Reg as Container Registry
    participant Mig as migrate job
    participant Svc as api · worker
    participant V as Vercel

    Dev->>GH: push (be/**)
    GH->>GH: make lint · make test
    GH->>Reg: be 이미지 build · push (tag = git sha)
    GH->>Mig: 새 이미지로 alembic upgrade head
    Mig-->>GH: 성공
    GH->>Svc: 새 이미지로 롤링 교체
    Svc-->>GH: /health/ready 통과
    Dev->>V: push (fe/**) → Vercel Git 연동으로 자동 배포
```

- 클라우드 인증은 GitHub OIDC로 한다. 장기 액세스 키를 GitHub Secrets에 두지 않는다.
- 서버·nginx·인증서는 `Dae-Jeong/MarinInfra`(private)가, 앱의 운영 compose·배포 스크립트는 이 레포 `infra/`가 관리한다.

## 클라우드별 대응

| 논리 구성요소 | AWS | Azure | GCP | OCI |
| --- | --- | --- | --- | --- |
| api (컨테이너 서비스) | ECS Fargate + ALB | App Service (Linux 컨테이너) | Cloud Run service | Container Instances + LB |
| worker (상시 컨테이너) | ECS Fargate service | App Service (별도 앱) 또는 WebJob | Cloud Run (min-instances 1) 또는 worker pool | Container Instances |
| migrate job | ECS RunTask | App Service 배포 슬롯 전 단계 / Container Apps Job | Cloud Run job | Container Instances (1회 실행) |
| PostgreSQL + pgvector | RDS for PostgreSQL | Azure Database for PostgreSQL Flexible Server | Cloud SQL for PostgreSQL | OCI Database with PostgreSQL |
| Secret store | Secrets Manager | Key Vault | Secret Manager | Vault |
| Container Registry | ECR | ACR | Artifact Registry | OCIR |
| Object Storage | S3 | Blob Storage | Cloud Storage | Object Storage |
| Logs · Metrics | CloudWatch | Azure Monitor | Cloud Logging · Monitoring | Logging · Monitoring |
| TLS · 도메인 | ACM + ALB | App Service 관리형 인증서 | Cloud Run 도메인 매핑 | LB 인증서 |
| Terraform state | S3 | Storage Account | GCS | Object Storage |
| VPC / VNet | VPC | VNet | VPC | VCN |
| NAT | NAT Gateway | NAT Gateway | Cloud NAT | NAT Gateway |
| Load Balancer | ALB | App Service 내장 or Application Gateway | Cloud Run 내장 or HTTPS LB | Load Balancer |

> 관리형 DB의 pgvector 지원·무료 한도·가격은 자주 바뀐다. 클라우드를 확정할 때 공식 문서로 다시
> 확인하고 출처와 확인 날짜를 남긴다. 무료 한도 안에서 DB 비용이 부담되면 외부 관리형
> Postgres(예: Neon)를 대안으로 검토한다.

## 도메인

| 호스트 | 대상 |
| --- | --- |
| `saju.marinkim.xyz` | Vercel (web) · 가비아 CNAME |
| `saju-api.marinkim.xyz` | OCI 서버 nginx → api · 가비아 A 168.110.100.93 |

## 미정

- 클라우드 선택 (AWS / Azure / GCP / OCI)
- NAT·서브넷 구성 (비용)
- api 최소 인스턴스 수 (콜드스타트 허용 여부)
- worker 트리거: 상시 폴링 유지 vs 큐 push 방식 (scale-to-zero 플랫폼이면 push가 유리)
- DB: 클라우드 관리형 vs 외부 관리형 (무료 한도 비교 후 결정)
- 모니터링·알림 수준
