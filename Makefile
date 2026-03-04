.PHONY: dev-backend dev-web dev-mobile test-backend docker-up docker-down seed

dev-backend:
	cd backend && pip install -e ".[dev]" && alembic upgrade head && uvicorn app.main:app --reload

dev-web:
	cd web && npm install && npm run dev

dev-mobile:
	cd mobile && npm install && npx expo start

test-backend:
	cd backend && pytest -v

docker-up:
	docker compose up -d

docker-down:
	docker compose down

seed:
	cd backend && python -m app.utils.seed
