from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from bll.exceptions import EntityNotFoundError
from presentation.routers.alerts_router import router as alerts_router
from presentation.routers.auth import router as auth_router
from presentation.routers.devices_router import router as devices_router
from presentation.routers.organizations_router import router as organizations_router
from presentation.routers.readings_router import router as readings_router
from presentation.routers.sensors_router import router as sensors_router
from presentation.routers.users_router import router as users_router

app = FastAPI(title="IoT Device Management API", version="1.0")


@app.exception_handler(EntityNotFoundError)
async def entity_not_found_handler(request: Request, exc: EntityNotFoundError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})


app.include_router(organizations_router)
app.include_router(devices_router)
app.include_router(sensors_router)
app.include_router(alerts_router)
app.include_router(readings_router)
app.include_router(auth_router)
app.include_router(users_router)
