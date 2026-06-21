# func-back

FUNC_TABLE 後端 API (FastAPI + PyMySQL + MariaDB)。

欄位: `C_Id`, `FUNC`, `LOVE`, `HATE`, `SOURCE`
- `FUNC` / `SOURCE`：只讀
- `LOVE` / `HATE`：可增加、可取消 (計數器，最低 0)

## 啟動

```bash
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

文件 (Swagger UI)：http://localhost:8000/docs

## API

| Method | Path                  | 說明              |
|--------|-----------------------|-------------------|
| GET    | `/funcs`              | 取得全部          |
| GET    | `/funcs/{c_id}`       | 取得單筆          |
| POST   | `/funcs/{c_id}/love`  | LOVE +1           |
| DELETE | `/funcs/{c_id}/love`  | 取消 LOVE (-1)    |
| POST   | `/funcs/{c_id}/hate`  | HATE +1           |
| DELETE | `/funcs/{c_id}/hate`  | 取消 HATE (-1)    |

DB 連線資訊放在 `.env`。
