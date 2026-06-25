from fastapi import FastAPI
from routers import news
#解决跨域问题
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"],
                   allow_headers=["*"], )

@app.get("/")
async def root():
    return {"message": "Hello World"}

#挂载路由
app.include_router(news.news_router)
