from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from database import engine, Base
from auth.router import router as auth_router
from ai.router import router as ai_router
from dotenv import load_dotenv
import traceback

# Load environment variables
load_dotenv()

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Workout Program Generator")

# ============================================
# CORS Configuration - Maximum Permissiveness
# ============================================
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "*",  # Allow all origins for testing
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,  # Set to False when using "*" in origins
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================
# Exception Handlers with CORS
# ============================================
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    response = JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    response = JSONResponse(
        status_code=422,
        content={"detail": exc.errors()}
    )
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    print(f"Unhandled exception: {exc}")
    print(traceback.format_exc())
    response = JSONResponse(
        status_code=500,
        content={"detail": str(exc)}
    )
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

# ============================================
# Manual CORS Handler (Backup)
# ============================================
@app.middleware("http")
async def add_cors_headers(request: Request, call_next):
    # Handle preflight OPTIONS requests
    if request.method == "OPTIONS":
        response = JSONResponse(content={"message": "OK"})
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "*"
        return response

    # Process the request
    try:
        response = await call_next(request)
    except Exception as e:
        print(f"Middleware caught exception: {e}")
        print(traceback.format_exc())
        response = JSONResponse(
            status_code=500,
            content={"detail": str(e)}
        )

    # Add CORS headers to all responses
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"

    return response


# Include routers
app.include_router(auth_router)
app.include_router(ai_router)


@app.get("/")
def root():
    return {"message": "Workout API running"}


# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy", "cors": "enabled"}