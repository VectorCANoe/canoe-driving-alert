#!/usr/bin/env bash
# Hook: Block rm commands — redirect to tmp_rm/
# Exit 2 = block tool call, Exit 0 = allow

input=$(cat)

# Extract the bash command from JSON input
extract_cmd() {
  for py in python python3 "C:/Users/이준영/AppData/Local/Programs/Python/Python311/python.exe"; do
    if cmd=$(echo "$input" | "$py" -c \
      "import sys, json; d=json.load(sys.stdin); print(d.get('command',''))" 2>/dev/null); then
      echo "$cmd"
      return 0
    fi
  done
  return 1
}

cmd=$(extract_cmd) || exit 0

# Block rm if it targets real files (not tmp_rm itself)
if echo "$cmd" | grep -qE '(^|[;&|[:space:]])\s*rm\s' && ! echo "$cmd" | grep -q 'tmp_rm'; then
  echo "=================================="
  echo "rm 사용 금지 — 파일을 tmp_rm/ 에 보존합니다"
  echo ""
  echo "사용법:"
  echo "  mkdir -p tmp_rm && mv <파일경로> tmp_rm/"
  echo ""
  echo "tmp_rm/ 폴더는 사용자가 직접 검토 후 삭제합니다."
  echo "=================================="
  exit 2
fi

exit 0
