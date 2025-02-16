from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.cahce import init_redis_cache
from app.midlewares import DBSessionMiddleware, setup_error_middleware
from app.routers import order_product_router, order_router, product_router, report_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_redis_cache()
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(order_router, tags=["Orders"])
app.include_router(order_product_router, tags=["OrdersProducts"])
app.include_router(product_router, tags=["Products"])
app.include_router(report_router, tags=["Reports"])
setup_error_middleware(app)

app.add_middleware(DBSessionMiddleware)


@app.get("/")
async def hello_world():
    return {"message": "Hello, World!"}
