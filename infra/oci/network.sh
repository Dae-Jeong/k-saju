#!/usr/bin/env bash
# 무료 범위의 네트워크를 만든다: VCN · 인터넷 게이트웨이 · 라우트 · 보안 목록(22 내 IP, 80/443 전체) · 퍼블릭 서브넷.
# 이미 같은 이름이 있으면 새로 만들지 않고 그대로 쓴다.
# 사용: MY_IP=1.2.3.4 ./infra/oci/network.sh
set -euo pipefail
: "${MY_IP:?MY_IP (SSH 허용할 내 공인 IP) 필요}"
NAME=${NAME:-app}
TENANCY=$(awk -F= '/^tenancy/{print $2; exit}' ~/.oci/config | tr -d ' ')
C=${COMPARTMENT_ID:-$TENANCY}

find_one() { oci "$@" --compartment-id "$C" --all --query "data[?\"lifecycle-state\"=='AVAILABLE'] | [0].id" --raw-output 2>/dev/null || true; }

VCN=$(find_one network vcn list --display-name "$NAME-vcn")
[ -z "$VCN" ] || [ "$VCN" = "null" ] && VCN=$(oci network vcn create --compartment-id "$C" --display-name "$NAME-vcn" --cidr-blocks '["10.0.0.0/16"]' --wait-for-state AVAILABLE --query 'data.id' --raw-output)
echo "VCN $VCN"

IGW=$(oci network internet-gateway list --compartment-id "$C" --vcn-id "$VCN" --query "data[0].id" --raw-output 2>/dev/null || true)
[ -z "$IGW" ] || [ "$IGW" = "null" ] && IGW=$(oci network internet-gateway create --compartment-id "$C" --vcn-id "$VCN" --is-enabled true --display-name "$NAME-igw" --wait-for-state AVAILABLE --query 'data.id' --raw-output)
echo "IGW $IGW"

RT=$(oci network vcn get --vcn-id "$VCN" --query 'data."default-route-table-id"' --raw-output)
oci network route-table update --rt-id "$RT" --force \
  --route-rules "[{\"destination\":\"0.0.0.0/0\",\"destinationType\":\"CIDR_BLOCK\",\"networkEntityId\":\"$IGW\"}]" >/dev/null
echo "Route 0.0.0.0/0 -> IGW"

SL=$(oci network vcn get --vcn-id "$VCN" --query 'data."default-security-list-id"' --raw-output)
oci network security-list update --security-list-id "$SL" --force \
  --egress-security-rules '[{"destination":"0.0.0.0/0","protocol":"all"}]' \
  --ingress-security-rules "[
    {\"source\":\"$MY_IP/32\",\"protocol\":\"6\",\"tcpOptions\":{\"destinationPortRange\":{\"min\":22,\"max\":22}}},
    {\"source\":\"0.0.0.0/0\",\"protocol\":\"6\",\"tcpOptions\":{\"destinationPortRange\":{\"min\":80,\"max\":80}}},
    {\"source\":\"0.0.0.0/0\",\"protocol\":\"6\",\"tcpOptions\":{\"destinationPortRange\":{\"min\":443,\"max\":443}}}
  ]" >/dev/null
echo "Security list: 22 <- $MY_IP, 80/443 <- all"

SUBNET=$(oci network subnet list --compartment-id "$C" --vcn-id "$VCN" --query "data[0].id" --raw-output 2>/dev/null || true)
[ -z "$SUBNET" ] || [ "$SUBNET" = "null" ] && SUBNET=$(oci network subnet create --compartment-id "$C" --vcn-id "$VCN" --display-name "$NAME-public" --cidr-block 10.0.1.0/24 --prohibit-public-ip-on-vnic false --wait-for-state AVAILABLE --query 'data.id' --raw-output)
echo "SUBNET $SUBNET"
