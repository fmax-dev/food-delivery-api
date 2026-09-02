from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from scalar_fastapi import get_scalar_api_reference

from backend.api.router import api_router
from backend.db.session import create_db_tables
from backend.web.template import BASE_DIR


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    await create_db_tables()
    yield

app = FastAPI(lifespan=lifespan_handler)


app.include_router(api_router)


app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")



# Health route
@app.get("/health")
def get_health():
    return {"status": "Ok"}


# root
@app.get("/")
def read_root():
    return {"message": "Food Delivery API"}

### Scalar Documentation
@app.get("/scalar", response_class=HTMLResponse, include_in_schema=False)
def get_scalar():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Food Delivery API Doc"
    )
