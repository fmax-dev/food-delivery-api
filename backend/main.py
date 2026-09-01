from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from scalar_fastapi import get_scalar_api_reference

from backend.api.router import api_router
from backend.db.session import create_db_tables


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    await create_db_tables()
    yield

app = FastAPI(lifespan=lifespan_handler)


app.include_router(api_router)


# root
@app.get("/")
def read_root():
    return {"message": "Food Delivery API"}

# Health route
@app.get("/health")
def get_health():
    return {"status": "Ok"}



### Scalar Documentation
@app.get("/scalar", response_class=HTMLResponse, include_in_schema=False)
def get_scalar():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Food Delivery API Doc"
    )
