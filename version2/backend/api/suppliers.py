from fastapi import APIRouter

router = APIRouter()

@router.get("/suppliers")
async def get_suppliers():
    """
    Step 18+ placeholder: This will eventually return parsed supplier data.
    """
    return {
        "status": "not_implemented",
        "suppliers": []
    }