# Food Delivery API

This is my practice project for managing restaurants and food delivery orders. It has an async JSON API backed by PostgreSQL, plus a small read-only web interface rendered with Jinja2.

I built it to get hands-on with FastAPI, async database work, and a layered app structure. API routes pass work to service classes, which use SQLModel and an async database session. Pydantic schemas handle request and response data. The bulk-order endpoint is a chance to practice running async database lookups concurrently.

## Features

- Create, view, update, and delete restaurants and orders through the JSON API.
- Filter restaurants by cuisine, whether they’re open, or a case-insensitive name search.
- Filter orders by status, restaurant, or price range.
- Paginate collection endpoints.
- View a restaurant’s orders through a nested endpoint.
- Validate restaurant ratings, order prices, and item summaries.
- Apply a few business rules, like preventing deletion of restaurants with orders.
- Fetch multiple orders concurrently with `asyncio.TaskGroup`.
- Browse read-only restaurant and order pages rendered with Jinja2.
- Explore the API with FastAPI’s docs or Scalar.

## Technology

- Python 3.12+
- FastAPI
- SQLModel and SQLAlchemy's asyncio support
- PostgreSQL with `asyncpg`
- Pydantic Settings
- Jinja2
- `uv` for dependency and virtual-environment management

## Get started

### What you’ll need

- Python 3.12 or newer
- [`uv`](https://docs.astral.sh/uv/)
- A running PostgreSQL server and a database for this application

### Install the dependencies

Clone the repo, move into its folder, and install the dependencies:

```bash
uv sync
```

### Set up PostgreSQL

Create a `.env` file in the project root and fill in your PostgreSQL connection details. `POSTGRES_URL` has to build manually using your database user and password.

```dotenv
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_USER=your_database_user
POSTGRES_PASSWORD=your_database_password
POSTGRES_DB=fooddelivery
POSTGRES_URL=postgresql+asyncpg://your_database_user:your_database_password@localhost:5432/fooddelivery
```

Replace the example values with your own. If your password contains characters that have a special meaning in a URL, encode them in `POSTGRES_URL`. Keep your real credentials in `.env` and out of Git.

### Run the application

```bash
uv run fastapi dev backend/main.py
```

When the app starts, it creates the SQLModel tables if they don’t exist. That’s handy while developing. For a production app, I’d use a migration tool like Alembic to manage database changes.

## Using the application

Once the server is running, you can visit:

- Interactive OpenAPI documentation: <http://127.0.0.1:8000/docs>
- Scalar API reference: <http://127.0.0.1:8000/scalar>
- Health check: <http://127.0.0.1:8000/health>
- Restaurant pages: <http://127.0.0.1:8000/restaurants>
- Orders page: <http://127.0.0.1:8000/orders>

The JSON API lives under `/api`. The HTML pages have their own paths and call the services directly, without making an HTTP request back to the API.

## API overview

The endpoints below use the local server address, `http://127.0.0.1:8000`.

### Restaurants

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/api/restaurant` | List restaurants; optionally filter by `cuisine_type`, `is_open`, or `name_search`, with `limit` and `offset` pagination. |
| `GET` | `/api/restaurant/{id}` | Retrieve a restaurant by ID. |
| `POST` | `/api/restaurant` | Create a restaurant. |
| `PATCH` | `/api/restaurant/{id}` | Partially update a restaurant. |
| `DELETE` | `/api/restaurant/{id}` | Delete a restaurant that has no orders. |
| `GET` | `/api/restaurant/{id}/orders` | List a restaurant's orders; optionally filter by `status`, `min_price`, or `max_price`, with pagination. |

### Orders

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/api/order` | List orders; optionally filter by `status`, `restaurant_id`, `min_price`, or `max_price`, with `limit` and `offset` pagination. |
| `GET` | `/api/order/latest` | Retrieve the most recently created order. |
| `GET` | `/api/order/{id}` | Retrieve an order by ID. |
| `GET` | `/api/order/bulk?ids=1&ids=2&ids=3` | Retrieve existing orders for repeated `ids` query parameters. Lookups run concurrently and use separate database sessions. |
| `POST` | `/api/order` | Create an order for an existing restaurant. |
| `PATCH` | `/api/order/{id}` | Update an order's status or delivery address. |
| `DELETE` | `/api/order/{id}` | Delete an order, subject to its delivery status. |

The `/latest` and `/bulk` routes come before `/{id}` in the router so FastAPI doesn’t mistake those words for order IDs.

## Architecture

```text
backend/
├── api/        # JSON API endpoints and dependency wiring
├── core/       # Application configuration
├── db/         # Async engine, sessions, and table initialization
├── models/     # SQLModel database models and relationships
├── schemas/    # API request and response schemas
├── services/   # Database operations and application rules
├── web/        # Jinja2 page routes and template setup
└── main.py     # FastAPI app, lifespan, and router registration

templates/      # Jinja2 HTML templates
static/         # CSS and other static assets
```

The API and web routes share the same service dependencies. The web pages are read-only for now, and the API is kept separate so the page layer can be replaced later without reworking the core application.

## Scope and next steps

This is a learning project, not a production-ready ordering system. There’s no authentication, authorization, HTML form submissions, automated test suite, or database migration setup yet. Orders store their items as a summary string rather than as separate menu items or order lines.

Things I’d like to explore next include adding automated tests and migrations, building out authentication, and giving orders proper line items.
