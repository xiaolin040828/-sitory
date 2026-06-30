#弄一个工具函数来封装响应类容
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse


def success_response(message : str = "success", data= None):
    content =  {
        "code": 200,
        "message": message,
        "data": data
    }
    #把 content 变成“纯 JSON 数据”: fastapi, ORM, Pydantic对象 编程code, massage, data
    return JSONResponse(content=jsonable_encoder(content))