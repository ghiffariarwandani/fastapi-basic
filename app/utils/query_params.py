from fastapi import Query


def pagination(limit: int = Query(default=10, ge=1), offset: int = Query(default=0, ge=0)) -> dict[str, int]:
    return {"limit": limit, "offset": offset}
