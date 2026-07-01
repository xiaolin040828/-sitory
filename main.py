from fastapi import FastAPI
from routers import news, users, favorite
#解决跨域问题
from fastapi.middleware.cors import CORSMiddleware
from utils.exception_response import register_exception_handlers

app = FastAPI()

#注册异常处理器
register_exception_handlers(app)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"],
                   allow_headers=["*"])

@app.get("/")
async def root():
    return {"message": "Hello World"}

#挂载路由
app.include_router(news.news_router)
app.include_router(users.user_router)
app.include_router(favorite.router)