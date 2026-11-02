#!/usr/bin/env bash
set -uo pipefail
missing=0
check() {
  if command -v "$1" >/dev/null 2>&1; then
    printf 'OK      %s\n' "$1"
  else
    printf 'FALTA   %s\n' "$1"
    missing=1
  fi
}
check git
check python3
check node
check sam
check aws
check gh
check cfn-lint
check checkov
if command -v node >/dev/null 2>&1; then
  major="$(node -p 'Number(process.versions.node.split(".")[0])')"
  if (( major >= 22 )); then printf 'OK      Node.js %s\n' "$major"; else printf 'FALTA   Node.js 22+ (encontrado %s)\n' "$major"; missing=1; fi
fi
if (( missing )); then
  printf '%s\n' 'Instale os itens ausentes antes de executar verificações locais.'
  exit 1
fi
