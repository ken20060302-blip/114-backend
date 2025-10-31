#python -m venv .venv
#Set-ExecutionPolicy -ExecutionPolicy bypass -Scope Process
#.\.venv\Scripts\activate
#pip freeze > requirements.txt
#pip install -r requirements.txt
from typing import Annotated , List , Union
from fastapi import Body, FastAPI, Path, Cookie ,Form
from pydantic import BaseModel ,Field


# Pydantic Model
class Item(BaseModel):
    name: str
    description: str | None = Field(
        default=None,title="The description of the item",max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: Union[float | None] = None
    tag: List[str] = []

app = FastAPI()
@app.post("/login")
async def login(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    ):
        return {"username": username}
# 根目錄
@app.get("/")
async def root():
    return {"message": "Hello world"}
'''
# 根據 item_id 取得項目
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

# 假資料放最上面供使用
fake_items_db = [
    {"item_name": "Foo"},
    {"item_name": "Bar"},
    {"item_name": "Baz"}
]

# 支援跳過與限制筆數的查詢參數
@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]
'''

@app.get("/items/")
async def read_items(ads_id: Annotated[str | None, Cookie()]) -> list[Item]:
    return {"ads_id":ads_id}

'''
# 建立新的項目
@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.model_dump()#dict() 將.jason存成py好處理的格式
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax":price_with_tax})
    return item_dict  # 回傳接收到的 item 資料
'''

@app.post("/items/")
async def create_item(item: Item) -> Item:
    return item 

"""
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q : str | None = None):
    item_id = Annotated[int, Path(title = "This ID of the item to get", ge=0,le=1000)],
    q: str | None =  None,
    item: Item | None = None,
);
    results = {"item_id":item_id, **item.model_dump()}
    if q:
        results.update({"q":q})
    if item:
        results.update({"item":item})
    return results
"""
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body(embed = True)]):
    results = {"item_id":item_id,"item":item}
    return results
