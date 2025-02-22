from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.cahce import init_redis_cache
from app.midlewares import DBSessionMiddleware, setup_error_middleware
from app.routers import (
    order_product_router,
    order_router,
    product_router,
    report_router,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager.
    Initializes Redis cache on application startup.
    """
    await init_redis_cache()
    yield


# Create FastAPI application instance with lifespan context.
app = FastAPI(lifespan=lifespan)

# Add CORS middleware to allow cross-origin requests.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any origin.
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods.
    allow_headers=["*"],  # Allow all headers.
)

# Include routers for different resources.
app.include_router(order_router, tags=["Orders"])
app.include_router(order_product_router, tags=["OrdersProducts"])
app.include_router(product_router, tags=["Products"])
app.include_router(report_router, tags=["Reports"])

# Setup custom error handling middleware.
setup_error_middleware(app)

# Add database session middleware.
app.add_middleware(DBSessionMiddleware)


@app.get("/")
async def hello_world():
    """
    Root endpoint for health check.
    """
    return {"message": "Hello, World!"}
