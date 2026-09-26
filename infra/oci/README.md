# OCI (Oracle Cloud) 무료 서버

Always Free Ampere A1 서버 1대를 만들기 위한 스크립트. 실행은 루트 Makefile 타겟으로 한다.

## 준비 (최초 1회)

1. OCI CLI 설치: `brew install oci-cli`
2. API 키: `~/.oci/oci_api_key.pem` (개인키, 커밋 금지) · `~/.oci/oci_api_key_public.pem`
3. 콘솔 → 우측 상단 프로필 → **My profile → API keys → Add API key → Paste a public key** 에 공개키를 붙여넣는다.
4. 등록 후 콘솔이 보여주는 **Configuration file preview**를 `~/.oci/config`에 저장하고 `key_file=~/.oci/oci_api_key.pem`로 맞춘다.
5. 서버 접속용 SSH 키: `~/.ssh/oci_server` (개인키) · `~/.ssh/oci_server.pub`

## 실행

```sh
make oci-check                      # 홈 리전 · 가용 영역 · A1 한도 · A1 제공 여부
make oci-network MY_IP=<내 공인 IP>  # VCN · IGW · 라우트 · 보안 목록(22 내 IP, 80/443) · 퍼블릭 서브넷
make oci-launch SUBNET_ID=<ocid>    # A1 (2 OCPU · 12GB · 부트 100GB) 자리 날 때까지 재시도
```

## 주의

- Always Free 자원은 **홈 리전**에서만 무료다. 이 계정의 홈 리전은 춘천(ap-chuncheon-1).
- 공식 문서는 A1을 "South Korea North(춘천)를 제외한" 가용 영역에서 만들 수 있다고 적고 있다. `make oci-check`의 A1 한도·shape 결과로 실제 가능 여부를 확인한다.
- 무료 유지: 추가 블록 볼륨·로드밸런서·NAT·관리형 DB·AMD/Intel shape를 만들지 않는다. 부트 볼륨 합계 200GB 이내.
- Ubuntu 이미지는 iptables가 80/443을 막고 있으므로 서버 안에서도 열어야 한다.
