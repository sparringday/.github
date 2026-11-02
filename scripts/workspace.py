#!/usr/bin/env python3
"""Helpers for the intentionally small, dependency-free repos.yaml format."""
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'repos.yaml'

def read_repos():
    items = []
    current = None
    for raw in MANIFEST.read_text(encoding='utf-8').splitlines():
        line = raw.strip()
        if not line or line.startswith('#') or line == 'repositories:':
            continue
        if line.startswith('- name:'):
            if current:
                items.append(current)
            current = {'name': line.split(':', 1)[1].strip()}
            continue
        if current and ':' in line:
            key, value = line.split(':', 1)
            current[key.strip()] = value.strip().strip('"').strip("'")
    if current:
        items.append(current)
    required = {'name', 'path', 'type', 'owner', 'url'}
    for item in items:
        if not required.issubset(item):
            raise ValueError(f"Entrada incompleta em repos.yaml: {item}")
    return items

def run(args, cwd=None):
    return subprocess.run(args, cwd=cwd, check=False).returncode

def clone(items):
    failures = 0
    for item in items:
        if item['path'] == '.':
            print(f"SKIP    {item['name']} (workspace atual)")
            continue
        target = ROOT / item['path']
        if (target / '.git').exists():
            print(f"SKIP    {item['name']} (Git já inicializado)")
            continue
        if target.exists() and any(target.iterdir()):
            print(f"ERRO    {item['name']}: {target} não está vazio e não é um repositório")
            failures += 1
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        if run(['git', 'clone', item['url'], str(target)]) != 0:
            failures += 1
    return 1 if failures else 0

def sync(items):
    failures = 0
    for item in items:
        target = ROOT / item['path']
        if not (target / '.git').exists():
            print(f"PENDENTE {item['name']}: ainda não clonado")
            failures += 1
            continue
        print(f"FETCH   {item['name']}")
        if run(['git', 'fetch', '--all', '--prune'], cwd=target) != 0:
            failures += 1
    return 1 if failures else 0

def check_all(items):
    pending = 0
    for item in items:
        target = ROOT / item['path']
        workflow = target / '.github' / 'workflows' / 'ci.yml'
        if not workflow.exists():
            if item['type'] not in {'workspace', 'docs'}:
                print(f"PENDENTE {item['name']}: ci.yml ausente")
                pending += 1
            continue
        content = workflow.read_text(encoding='utf-8').lower()
        if 'todo' in content or 'mockup' in content:
            print(f"PENDENTE {item['name']}: workflow ainda é mockup; CI não executada")
            pending += 1
        else:
            print(f"CONFIGURADO {item['name']}: workflow sem marcador TODO (execução não solicitada)")
    if pending:
        print(f"\n{pending} repositórios ainda têm pipeline pendente; nenhum teste foi executado.")
        return 2
    return 0

if __name__ == '__main__':
    if len(sys.argv) != 2 or sys.argv[1] not in {'clone', 'sync', 'check-all'}:
        print('Uso: workspace.py {clone|sync|check-all}', file=sys.stderr)
        raise SystemExit(2)
    repos = read_repos()
    command = sys.argv[1]
    raise SystemExit({'clone': clone, 'sync': sync, 'check-all': check_all}[command](repos))
