# ================================
# Variables
# ================================

COMPOSE_FILE ?= -f docker-compose.local.yaml
SERVICE      ?= whoami
APP          ?=
FILE         ?= $(error ❌ file 을 지정하세요. 예: make loaddata FILE=dump.json)
NUM          ?= $(error ❌ num 을 지정하세요. 예: make sqlmigrate APP=users NUM=0001)

# ================================
# Help
# ================================

.PHONY: help
help: ## 사용 가능한 명령어 목록
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ================================
# Container Management
# ================================

.PHONY: up
up: ## 컨테이너 실행
	docker compose $(COMPOSE_FILE) up -d

.PHONY: down
down: ## 컨테이너 종료
	docker compose $(COMPOSE_FILE) down

.PHONY: build
build: ## 이미지 빌드 후 실행
	docker compose $(COMPOSE_FILE) up -d --build

.PHONY: restart
restart: ## 컨테이너 재시작 (ex: make restart / make restart SERVICE=db)
	docker compose $(COMPOSE_FILE) restart $(SERVICE)

.PHONY: restart-all
restart-all: ## 컨테이너 재시작 (ex: make restart / make restart SERVICE=db)
	docker compose $(COMPOSE_FILE) restart

.PHONY: stop
stop: ## 컨테이너 중지 (ex: make stop / make stop SERVICE=db)
	docker compose $(COMPOSE_FILE) stop $(SERVICE)

.PHONY: ps
ps: ## 컨테이너 상태 확인
	docker compose $(COMPOSE_FILE) ps

.PHONY: stats
stats: ## 컨테이너 리소스 사용량 확인
	docker stats

# ================================
# Logs
# ================================

.PHONY: logs
logs: ## 로그 확인 (ex: make logs / make logs SERVICE=db)
	docker compose $(COMPOSE_FILE) logs -f $(SERVICE)

.PHONY: logs-all
logs-all: ## 전체 컨테이너 로그 확인
	docker compose $(COMPOSE_FILE) logs -f

# ================================
# Django Management
# ================================

.PHONY: shell
shell: ## Django shell 진입
	docker compose $(COMPOSE_FILE) exec whoami python manage.py shell

.PHONY: bash
bash: ## 컨테이너 bash 진입 (ex: make bash / make bash SERVICE=db)
	docker compose $(COMPOSE_FILE) exec $(SERVICE) bash

.PHONY: migrate
migrate: ## 마이그레이션 실행
	docker compose $(COMPOSE_FILE) exec whoami python manage.py migrate

.PHONY: makemigrations
makemigrations: ## 마이그레이션 파일 생성 (ex: make makemigrations / make makemigrations APP=users)
	docker compose $(COMPOSE_FILE) exec whoami python manage.py makemigrations $(APP)

.PHONY: showmigrations
showmigrations: ## 마이그레이션 상태 확인 (ex: make showmigrations / make showmigrations APP=users)
	docker compose $(COMPOSE_FILE) exec whoami python manage.py showmigrations $(APP)

.PHONY: sqlmigrate
sqlmigrate: ## 마이그레이션 SQL 확인 (ex: make sqlmigrate APP=users NUM=0001)
	docker compose $(COMPOSE_FILE) exec whoami python manage.py sqlmigrate $(APP) $(NUM)

.PHONY: createsuperuser
createsuperuser: ## 슈퍼유저 생성
	docker compose $(COMPOSE_FILE) exec whoami python manage.py createsuperuser

.PHONY: collectstatic
collectstatic: ## 스태틱 파일 수집
	docker compose $(COMPOSE_FILE) exec whoami python manage.py collectstatic --no-input

.PHONY: check
check: ## Django 시스템 체크
	docker compose $(COMPOSE_FILE) exec whoami python manage.py check

# ================================
# Database
# ================================

.PHONY: dbshell
dbshell: ## PostgreSQL shell 진입
	docker compose $(COMPOSE_FILE) exec db psql -U $$DB_USER -d $$DB_NAME

.PHONY: dumpdata
dumpdata: ## DB 데이터 덤프 (ex: make dumpdata / make dumpdata APP=users)
	docker compose $(COMPOSE_FILE) exec whoami python manage.py dumpdata $(app) --indent 2 > dump.json
	@echo "✅ dump.json 으로 저장되었습니다"

.PHONY: loaddata
loaddata: ## DB 데이터 로드 (ex: make loaddata FILE=dump.json)
	docker compose $(COMPOSE_FILE) exec whoami python manage.py loaddata $(FILE)

# ================================
# Cleanup
# ================================

.PHONY: clean
clean: ## 컨테이너 및 이미지 정리 (볼륨 제외)
	docker compose $(COMPOSE_FILE) down --rmi local

.PHONY: clean-all
clean-all: ## 컨테이너, 이미지, 볼륨 전체 정리 (데이터 삭제 주의!)
	docker compose $(COMPOSE_FILE) down -v --rmi local