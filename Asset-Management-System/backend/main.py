from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text

from database import engine, Base, get_db
from routers import assets, inventory, maintenance, staff, dashboard, categories


app = FastAPI(
    title="資產管理系統 API",
    description="固定資產管理系統後端服務",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 註冊路由
app.include_router(assets.router, prefix="/api/assets", tags=["資產台帳"])
app.include_router(inventory.router, prefix="/api/inventory", tags=["盤點管理"])
app.include_router(maintenance.router, prefix="/api/maintenance", tags=["維修保養"])
app.include_router(staff.router, prefix="/api/staff", tags=["人員管理"])
app.include_router(dashboard.router, prefix="/api", tags=["儀表板"])
app.include_router(categories.router, prefix="/api/categories", tags=["資產類別"])


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "資產管理系統 API 運行中", "status": "ok"}


@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    return {"status": "healthy", "database": db_status}
