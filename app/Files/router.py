from fastapi import APIRouter

router = APIRouter()

@router.get("")
async def register() -> dict[str, str]:
    return {"status": "ok"}

@router.post("")
async def login() -> dict[str, str]:
    return {"status": "ok"}

@router.get("/{id}")
async def logout(id: int) -> dict[str, str]:
    print("Id get")
    return {"status": "ok"}

@router.post("/{id}")
async def logout(id: int) -> dict[str, str]:
    print("Id post")
    return {"status": "ok"}

@router.delete("/{id}")
async def logout(id: int) -> dict[str, str]:
    return {"status": "ok"}

@router.post("/merge")
async def logout() -> dict[str, str]:
    print("Merge")
    return {"status": "ok"}