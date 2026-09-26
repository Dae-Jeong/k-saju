#!/usr/bin/env bash
# Always Free A1을 받을 수 있는지 확인한다: 홈 리전, 가용 영역, A1 한도, A1 shape 제공 여부.
# 사용: ./infra/oci/check.sh   (~/.oci/config 필요)
set -euo pipefail

TENANCY=$(oci iam compartment list --query 'data[0]."compartment-id"' --raw-output 2>/dev/null || true)
TENANCY=${TENANCY:-$(awk -F= '/^tenancy/{print $2; exit}' ~/.oci/config | tr -d ' ')}

echo "== 구독 리전 (IS-HOME-REGION=true 가 홈 리전)"
oci iam region-subscription list --tenancy-id "$TENANCY" --output table

echo "== 현재 설정 리전의 가용 영역"
oci iam availability-domain list --compartment-id "$TENANCY" --query 'data[].name' --output table

echo "== A1 한도 (0이면 이 리전에서 A1을 만들 수 없음)"
oci limits value list --compartment-id "$TENANCY" --service-name compute --all \
  --query "data[?contains(name, 'standard-a1')].{name:name, ad:\"availability-domain\", value:value}" --output table

echo "== A1 shape 제공 여부"
oci compute shape list --compartment-id "$TENANCY" --all \
  --query "data[?shape=='VM.Standard.A1.Flex'].{shape:shape, ocpus:\"ocpu-options\".max, memory:\"memory-options\".\"max-in-g-bs\"}" --output table

echo "== AMD Micro (대안) 제공 여부"
oci compute shape list --compartment-id "$TENANCY" --all \
  --query "data[?shape=='VM.Standard.E2.1.Micro'].shape" --output table
