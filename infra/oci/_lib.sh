# 공통: 새 API 키가 퍼지는 동안 가끔 나는 401(NotAuthenticated)을 짧게 재시도한다.
export SUPPRESS_LABEL_WARNING=True
oci() {
  local out rc i
  for i in 1 2 3 4 5; do
    out=$(command oci "$@" 2>&1); rc=$?
    if [ $rc -eq 0 ] || ! echo "$out" | grep -q NotAuthenticated; then echo "$out"; return $rc; fi
    sleep 3
  done
  echo "$out"; return $rc
}
