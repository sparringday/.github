SHELL := /usr/bin/env bash
PYTHON ?= python3

.PHONY: help bootstrap clone sync check-all

help:
	@printf '%s\n' 'bootstrap  Verifica ferramentas locais' 'clone      Clona repos.yaml' 'sync       Executa git fetch nos repositórios' 'check-all  Lista pipelines ainda pendentes'

bootstrap:
	@bash scripts/bootstrap.sh

clone:
	@$(PYTHON) scripts/workspace.py clone

sync:
	@$(PYTHON) scripts/workspace.py sync

check-all:
	@$(PYTHON) scripts/workspace.py check-all
