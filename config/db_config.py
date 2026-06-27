#配置数据库引擎连接数据库

#导入异步sqlachemy包，创建数据库连接引擎， 创建会话，操作数据库
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine

#创建连接引擎
async_ad_url = 'mysql+aiomysql://root:00000000@localhost:3306/news_app?charset=utf8'
engine = create_async_engine(
    url = async_ad_url,
    echo=True,
    pool_size = 10,
    max_overflow = 20,
)

#创建会话工厂
async_session = async_sessionmaker(
    bind= engine,
    class_= AsyncSession,   #返回的session对象是async的
    expire_on_commit = False,
)

#依赖项，用来获取session对话操作数据库
async def get_db():
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except:
            await session.rollback()
            raise
        finally:
            await session.close()














