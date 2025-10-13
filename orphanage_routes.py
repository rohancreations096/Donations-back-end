from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from services.firebase_service import get_orphanage_by_id, list_orphanages, create_orphanage, update_orphanage
from utils.auth import require_auth_optional

router = APIRouter()

class OrphanageIn(BaseModel):
    name: str
    description: Optional[str] = None
    location: dict  # {"lat": float, "lng": float, "address": str}
    contact: Optional[str] = None
    needs: Optional[List[dict]] = []  # list of needs e.g. {"item": "...", "qty": 2}

class OrphanageOut(OrphanageIn):
    id: str

@router.get("/", response_model=List[OrphanageOut])
async def get_orphanages():
    return await list_orphanages()

@router.get("/{orphanage_id}", response_model=OrphanageOut)
async def get_orphanage(orphanage_id: str):
    doc = await get_orphanage_by_id(orphanage_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Orphanage not found")
    return doc

@router.post("/", response_model=dict)
async def post_orphanage(payload: OrphanageIn, user=Depends(require_auth_optional)):
    # Require organization role ideally - for now just create
    doc = await create_orphanage(payload.dict())
    return {"id": doc}

@router.patch("/{orphanage_id}")
async def patch_orphanage(orphanage_id: str, payload: OrphanageIn, user=Depends(require_auth_optional)):
    updated = await update_orphanage(orphanage_id, payload.dict())
    if not updated:
        raise HTTPException(status_code=404, detail="Orphanage not found")
    return {"status": "ok"}
