from typing import Annotated
from fastapi import APIRouter, Depends, UploadFile, File, Form
from src.account.models import User
from src.db.config import SessionDep
from src.product.schemas import ProductCreate, ProductOut
from src.account.deps import require_admin
from src.product.services import create_product
router = APIRouter()

@router.post("", response_model=ProductOut)
async def product_create(
  session: SessionDep,
  title: str = Form(...),
  description: str | None = Form(None),
  price: float = Form(...), 
  stock_quantity: int = Form(...), 
  category_ids: Annotated[list[int], Form()] = [],
  image_url: UploadFile | None = File(None), 
  admin_user: User = Depends(require_admin)
  ):
  data = ProductCreate(
    title=title,
    description=description,
    price=price,
    stock_quantity=stock_quantity,
    category_ids=category_ids
  )
  return await create_product(session, data, image_url)
