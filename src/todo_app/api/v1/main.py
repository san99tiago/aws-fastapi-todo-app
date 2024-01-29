###############################################################################
# Entrypoint for the API that uses "Mangum" as a wrapper for API-GW integration
###############################################################################

# External imports
from mangum import Mangum
from fastapi import FastAPI

# Own imports
from todo_app.api.v1.routers import (
    todos,
)

app = FastAPI()

app.include_router(todos.router, prefix="/api/v1")

# This is the Lambda Function's entrypoint (handler)
handler = Mangum(app)
