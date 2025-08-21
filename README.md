# Securin Recipes Assessment — Complete Solution

This repo contains:
- PostgreSQL database (via Docker)
- FastAPI backend with pagination, sorting, and search
- Static frontend (Tailwind) calling the REST API and meeting all UI requirements

## Quick Start (Docker)

```bash
# 1) Clone/unzip this folder
# 2) Copy env example
cp backend/.env.example backend/.env

# 3) (Optional) Replace data/recipes.json with the provided JSON
#    Keep the array-of-objects structure.

# 4) Start services
docker compose up --build -d

# 5) Seed the database once
docker compose exec api python -m app.seed

# 6) Open the app
open http://localhost:8000
```

The API is served at `http://localhost:8000/api/...` and the frontend is served from the same host.

## API

### 1) Get All Recipes (sorted by rating desc, paginated)
`GET /api/recipes?page=1&limit=10`

Response:
```json
{
  "page": 1,
  "limit": 10,
  "total": 50,
  "data": [ { "id": 1, "title": "...", "cuisine": "...", "rating": 4.8, ... } ]
}
```

### 2) Search Recipes (supports operators)
`GET /api/recipes/search?calories=<=400&title=pie&rating=>=4.5&total_time=<60&page=1&limit=20`

- `title` and `cuisine`: partial (case-insensitive) match
- `rating`, `total_time`, `calories`: support `>=`, `<=`, `>`, `<`, `=`, `==`

Calories are parsed from the JSONB field by stripping non-digits (e.g., `"389 kcal"` → `389`) inside PostgreSQL.

## Data Handling

- Numeric fields (`rating`, `prep_time`, `cook_time`, `total_time`) are converted; `"NaN"` or invalid values become `NULL` before insert.
- Schema (PostgreSQL):

```sql
CREATE TABLE recipes (
    id SERIAL PRIMARY KEY,
    cuisine VARCHAR(255),
    title VARCHAR(255),
    rating FLOAT,
    prep_time INT,
    cook_time INT,
    total_time INT,
    description TEXT,
    nutrients JSONB,
    serves VARCHAR(50)
);
```

The table is auto-created on API startup and by the seeder.

## Frontend Requirements Coverage

- Table columns: Title (truncated), Cuisine, Rating (stars), Total Time, Serves ✅
- Row click opens a right-side drawer showing:
  - Header: Title + Cuisine ✅
  - Description key/value ✅
  - Total Time with "Expand" to show Cook/Prep ✅
  - Nutrition table: calories, carbohydrateContent, cholesterolContent, fiberContent, proteinContent, saturatedFatContent, sodiumContent, sugarContent, fatContent ✅
- Field-level filters that call `/api/recipes/search` ✅
- Pagination + results-per-page 15–50 ✅
- Fallback when no results ✅

## Development (without Docker)

Requirements: Python 3.11+, PostgreSQL 16+

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Set env
cp .env.example .env
# If running locally, change DATABASE_URL in .env to:
# postgresql+psycopg2://postgres:postgres@localhost:5432/recipes

# Create DB (once): create a database named 'recipes'
# Seed:
python -m app.seed

# Run:
uvicorn app.main:app --reload
```

Open http://localhost:8000

## Testing

- Health check: visit `/` to see the UI.
- Try: `/api/recipes?page=1&limit=10`
- Try search: `/api/recipes/search?title=pie&rating=>=4.5&calories=<=400`

## Notes

- Replace `data/recipes.json` with your provided file before seeding.
- The seeder is idempotent per-run only if you reset the table; for repeated seeds, truncate the table first.
- For production, consider Alembic migrations and better error handling.
