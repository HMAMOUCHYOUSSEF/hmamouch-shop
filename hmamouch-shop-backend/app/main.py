from fastapi import FastAPI
from .db import engine # to get the taxi vahicle 
from .models import Base
from .routers import users, products, auth_router


app = FastAPI(title="Hmamouch Shop Backend") # <- this creates the API or we can say the restaurant system that has all what we need to start the work.

# here we create all planned tables structures
Base.metadata.create_all(bind=engine)
#base has our disered structure
#metadata has all the planned tables design to mache to our diserd structure
#create_all based on these plans it build these tables
#and put it on the engine (the taxi vahicule) to be created at the end on the database 
app.include_router(users.router)
# we included the router on the main.py.
app.include_router(products.router)
# the same with products endpoints.
app.include_router(auth_router.router)


@app.get("/") # is an endpoint for test only.
async def root():
    return {"ok": True, "message": "Hmamouch Shop backend is running"}
