import fastapi as fast
app= fast.FastAPI()
from typing import Union
@app.get("/")
def readroot():
	return {'hELLO':'wORDL'}
@app.get("/items/{item_id}")
def read(item_id:int,q:str):
	return {"item_id":item_id,"q":q}
