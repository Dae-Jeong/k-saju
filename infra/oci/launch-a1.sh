#!/usr/bin/env bash
# A1 인스턴스를 자리가 날 때까지 재시도하며 만든다 ("Out of host capacity" 대응).
# 사용: SUBNET_ID=ocid1.subnet... ./infra/oci/launch-a1.sh   (SSH 키 기본값 ~/.ssh/oci_server.pub)
set -euo pipefail
: "${SUBNET_ID:?SUBNET_ID 필요 (network.sh 출력)}"
SSH_PUBKEY=${SSH_PUBKEY:-$HOME/.ssh/oci_server.pub}
OCPUS=${OCPUS:-2}; MEM=${MEM:-12}; BOOT_GB=${BOOT_GB:-100}; INTERVAL=${INTERVAL:-60}
NAME=${NAME:-app-a1}
TENANCY=$(awk -F= '/^tenancy/{print $2; exit}' ~/.oci/config | tr -d ' ')
C=${COMPARTMENT_ID:-$TENANCY}

IMAGE=$(oci compute image list --compartment-id "$C" --operating-system "Canonical Ubuntu" --operating-system-version "22.04" \
  --shape VM.Standard.A1.Flex --sort-by TIMECREATED --sort-order DESC --query 'data[0].id' --raw-output)
ADS=()
while IFS= read -r ad; do [ -n "$ad" ] && ADS+=("$ad"); done < <(oci iam availability-domain list --compartment-id "$C" --query 'data[].name' --raw-output | tr -d '[]", ')
echo "image=$IMAGE  ads=${ADS[*]}  shape=${OCPUS}ocpu/${MEM}GB boot=${BOOT_GB}GB"

attempt=0
while true; do
  for AD in "${ADS[@]}"; do
    attempt=$((attempt+1))
    echo "[$(date '+%F %T')] 시도 #$attempt ($AD)"
    if out=$(oci compute instance launch --compartment-id "$C" --availability-domain "$AD" \
        --shape VM.Standard.A1.Flex --shape-config "{\"ocpus\":$OCPUS,\"memoryInGBs\":$MEM}" \
        --image-id "$IMAGE" --subnet-id "$SUBNET_ID" --assign-public-ip true \
        --boot-volume-size-in-gbs "$BOOT_GB" --display-name "$NAME" \
        --ssh-authorized-keys-file "$SSH_PUBKEY" --query 'data.id' --raw-output 2>&1); then
      echo "성공: $out"; exit 0
    fi
    if echo "$out" | grep -qiE 'out of (host )?capacity|InternalError|TooManyRequests'; then
      echo "  자리 없음 → ${INTERVAL}s 후 재시도"
    else
      echo "  재시도할 수 없는 오류:"; echo "$out"; exit 1
    fi
  done
  sleep "$INTERVAL"
done
