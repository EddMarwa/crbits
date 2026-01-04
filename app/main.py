from fastapi import FastAPI

from app.database import Base, engine
from app.auth.router import router as auth_router
from app.users.router import router as users_router
from app.bots.router import router as bots_router
from app.dashboard.router import router as dashboard_router
from app.ledger.router import router as ledger_router
from app.deposits.router import router as deposits_router
from app.withdrawals.router import router as withdrawals_router
from app.admin.router import router as admin_router

app = FastAPI()

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(bots_router, prefix="/bots", tags=["bots"])
app.include_router(dashboard_router, prefix="/dashboard", tags=["dashboard"])
app.include_router(ledger_router, prefix="/ledger", tags=["ledger"])
app.include_router(deposits_router, prefix="/deposits", tags=["deposits"])
app.include_router(withdrawals_router, prefix="/withdrawals", tags=["withdrawals"])
app.include_router(admin_router, prefix="/admin", tags=["admin"])

