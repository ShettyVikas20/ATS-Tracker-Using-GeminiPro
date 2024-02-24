from fastapi import FastAPI
from routers.home import home_api_router







try:

    app = FastAPI()

    @app.get("/",tags=["root"])
    async def root():
        return{"data":"https://www.youtube.com/watch?v=dQw4w9WgXcQ"}

    app.include_router(home_api_router)
    

except Exception as e:
        print(f"[-]Error during routing at main.py : {str(e)}")
        














