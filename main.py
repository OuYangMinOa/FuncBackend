"""FUNC_TABLE 後端 API。

欄位: C_Id, FUNC, LOVE, HATE, SOURCE
- FUNC / SOURCE: 只提供讀取
- LOVE / HATE: 可以「增加」與「取消」(計數器，不會低於 0)
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from db import DB_TABLE, get_conn

app = FastAPI(title="FUNC API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def _fetch_one(c_id: int):
    sql = f"SELECT C_Id, FUNC, LOVE, HATE, SOURCE FROM `{DB_TABLE}` WHERE C_Id = %s"
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(sql, (c_id,))
        row = cur.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail=f"C_Id {c_id} 不存在")
    return row


def _adjust(c_id: int, column: str, delta: int):
    """調整 LOVE 或 HATE 計數，取消(delta=-1)時不會低於 0。"""
    # GREATEST 確保計數不會變成負數
    sql = (
        f"UPDATE `{DB_TABLE}` "
        f"SET `{column}` = GREATEST(COALESCE(`{column}`, 0) + %s, 0) "
        f"WHERE C_Id = %s"
    )
    with get_conn() as conn, conn.cursor() as cur:
        affected = cur.execute(sql, (delta, c_id))
    if affected == 0:
        raise HTTPException(status_code=404, detail=f"C_Id {c_id} 不存在")
    return _fetch_one(c_id)


@app.get("/funcs")
def list_funcs():
    """取得所有資料。"""
    sql = f"SELECT C_Id, FUNC, LOVE, HATE, SOURCE FROM `{DB_TABLE}` ORDER BY C_Id"
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(sql)
        return cur.fetchall()


@app.get("/funcs/{c_id}")
def get_func(c_id: int):
    """取得單筆資料。"""
    return _fetch_one(c_id)


@app.post("/funcs/{c_id}/love")
def add_love(c_id: int):
    """LOVE +1。"""
    return _adjust(c_id, "LOVE", 1)


@app.delete("/funcs/{c_id}/love")
def cancel_love(c_id: int):
    """取消 LOVE (LOVE -1，最低 0)。"""
    return _adjust(c_id, "LOVE", -1)


@app.post("/funcs/{c_id}/hate")
def add_hate(c_id: int):
    """HATE +1。"""
    return _adjust(c_id, "HATE", 1)


@app.delete("/funcs/{c_id}/hate")
def cancel_hate(c_id: int):
    """取消 HATE (HATE -1，最低 0)。"""
    return _adjust(c_id, "HATE", -1)
