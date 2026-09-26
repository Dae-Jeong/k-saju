# 공통: 새 API 키가 퍼지는 동안 가끔 나는 401(NotAuthenticated)을 짧게 재시도한다.
# stdout(결과값)과 stderr(진행 메시지·오류)를 섞지 않는다.
export SUPPRESS_LABEL_WARNING=True
export PYTHONWARNINGS=ignore
oci() {
  local out rc i err
  err=$(mktemp)
  for i in 1 2 3 4 5; do
    out=$(command oci "$@" 2>"$err"); rc=$?
    if [ $rc -eq 0 ] || ! grep -q NotAuthenticated "$err"; then
      [ -n "$out" ] && printf '%s\n' "$out"
      [ $rc -ne 0 ] && cat "$err" >&2
      rm -f "$err"; return $rc
    fi
    sleep 3
  done
  cat "$err" >&2; rm -f "$err"; return $rc
}
