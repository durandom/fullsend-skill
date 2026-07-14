.DEFAULT_GOAL := help

COMPOSE := $(if $(shell command -v podman 2>/dev/null),podman compose,docker compose)
AGENTSVIEW_HOST ?= $(shell hostname).local
AGENTSVIEW_PORT ?= 8081
XDG_CACHE_HOME ?= $(HOME)/.cache
FULLSEND_AGENTSVIEW_CACHE_DIR ?= $(XDG_CACHE_HOME)/fullsend/agentsview
ARTIFACTS_DIR ?= $(FULLSEND_AGENTSVIEW_CACHE_DIR)/artifacts
RUNS_DIR ?= $(FULLSEND_AGENTSVIEW_CACHE_DIR)/runs
RUNS_LOCAL_DIR ?= $(FULLSEND_AGENTSVIEW_CACHE_DIR)/runs-local
AGENTSVIEW_RUNS ?= $(RUNS_DIR)
export AGENTSVIEW_HOST AGENTSVIEW_PORT FULLSEND_AGENTSVIEW_CACHE_DIR
export ARTIFACTS_DIR RUNS_DIR RUNS_LOCAL_DIR AGENTSVIEW_RUNS

.PHONY: artifacts convert fetch up down local viewer reconvert status paths help

# Auto-recover Podman VM if it died (macOS libkrun drops on sleep)
define ensure-podman
	$(if $(shell command -v podman 2>/dev/null),\
		podman info >/dev/null 2>&1 || podman machine start 2>/dev/null || true)
endef

define start-viewer
	$(ensure-podman)
	AGENTSVIEW_RUNS="$(1)" $(COMPOSE) -f docker-compose.fullsend.yaml up -d
	@echo "AgentsView: http://$${AGENTSVIEW_HOST}:$${AGENTSVIEW_PORT}"
endef

# Download artifact ZIPs from GitHub Actions into the shared cache
artifacts:
	./scripts/fetch-artifacts.sh

# Convert cached artifacts into the remote-run cache
convert:
	./scripts/convert-artifacts.sh

# Download + convert (replaces old fetch-fullsend-runs.sh)
fetch: artifacts convert

# Re-convert all artifacts from scratch (clears RUNS_DIR first)
reconvert:
	./scripts/convert-artifacts.sh --force

# Fetch + start AgentsView container (Podman preferred, Docker fallback)
up: fetch
	$(call start-viewer,$(RUNS_DIR))

# Import local fullsend run(s) + start AgentsView (only local runs shown)
# Usage: make local              (auto-discovers from $TMPDIR/fullsend)
#        make local DIR=/path    (explicit path)
local:
	RUNS_DIR="$(RUNS_LOCAL_DIR)" ./scripts/import-local-run.sh $(if $(DIR),"$(DIR)",)
	$(call start-viewer,$(RUNS_LOCAL_DIR))

# Start AgentsView without fetching (use after manual imports)
viewer:
	$(call start-viewer,$(AGENTSVIEW_RUNS))

status:
	AGENTSVIEW_RUNS="$(AGENTSVIEW_RUNS)" $(COMPOSE) -f docker-compose.fullsend.yaml ps

# Stop AgentsView container
down:
	AGENTSVIEW_RUNS="$(AGENTSVIEW_RUNS)" $(COMPOSE) -f docker-compose.fullsend.yaml down -v

paths:
	@echo "CACHE_DIR=$(FULLSEND_AGENTSVIEW_CACHE_DIR)"
	@echo "ARTIFACTS_DIR=$(ARTIFACTS_DIR)"
	@echo "RUNS_DIR=$(RUNS_DIR)"
	@echo "RUNS_LOCAL_DIR=$(RUNS_LOCAL_DIR)"

help:
	@echo "AgentsView fullsend integration"
	@echo ""
	@echo "  make artifacts      - Download artifact ZIPs into the shared cache"
	@echo "  make convert        - Convert artifacts into AgentsView layout"
	@echo "  make fetch          - Download + convert (artifacts → runs)"
	@echo "  make reconvert      - Re-convert all artifacts (clears remote-run cache first)"
	@echo "  make up             - Fetch + start AgentsView (all remote runs)"
	@echo "  make local          - Import local run(s) + start AgentsView (auto-discovers)"
	@echo "  make viewer         - Start AgentsView without fetching"
	@echo "  make status         - Show the AgentsView container status"
	@echo "  make down           - Stop AgentsView"
	@echo "  make paths          - Print resolved cache and run directories"
	@echo ""
	@echo "Local run examples:"
	@echo "  make local                                                # auto-discover"
	@echo "  make local DIR=/tmp/fullsend                              # explicit --output-dir"
	@echo "  make local DIR=/tmp/fullsend/agent-triage-3705-1234567890 # single run"
	@echo ""
	@echo "Environment variables:"
	@echo "  AGENTSVIEW_PORT           - Host port (default: 8081)"
	@echo "  AGENTSVIEW_HOST           - Public hostname (default: <hostname>.local)"
	@echo "  FULLSEND_AGENTSVIEW_CACHE_DIR - Cache root (default: $(FULLSEND_AGENTSVIEW_CACHE_DIR))"
	@echo "  ARTIFACTS_DIR             - Artifact cache override"
	@echo "  RUNS_DIR                  - Remote-run directory override"
	@echo "  RUNS_LOCAL_DIR            - Local-run directory override"
