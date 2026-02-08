from fastapi import Query


def pagination(limit: int | None = Query(default=10), offset: int | None = Query(default=0)) -> dict:
  return {"limit": limit, "offset": offset} 