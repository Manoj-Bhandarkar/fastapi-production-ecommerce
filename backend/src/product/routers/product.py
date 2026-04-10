from typing import Annotated
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    UploadFile,
    File,
    Form,
    status,
)
from src.account.models import User
from src.db.config import SessionDep
from src.product.schemas import ProductCreate, ProductOut, PaginatedProductOut
from src.account.deps import require_admin
from src.product.services import (
    create_product,
    delete_product,
    get_all_products,
    get_product_by_slug,
    search_products,
)

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
    admin_user: User = Depends(require_admin),
):
    data = ProductCreate(
        title=title,
        description=description,
        price=price,
        stock_quantity=stock_quantity,
        category_ids=category_ids,
    )
    return await create_product(session, data, image_url)


@router.get("", response_model=PaginatedProductOut)
async def list_products(
    session: SessionDep,
    categories: list[str] | None = Query(default=None),
    limit: int = Query(default=5, ge=1, le=100),
    page: int = Query(default=1, ge=1),
):
    return await get_all_products(session, categories, limit, page)


@router.get("/{slug}", response_model=ProductOut)
async def product_get_by_slug(session: SessionDep, slug: str):
    product = await get_product_by_slug(session, slug)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return product


@router.get("/search", response_model=PaginatedProductOut)
async def products_search(
    session: SessionDep,
    categories: list[str] | None = Query(default=None),
    title: str | None = Query(None),
    description: str | None = Query(None),
    min_price: float | None = Query(None),
    max_price: float | None = Query(None),
    limit: int = Query(default=5, ge=1, le=100),
    page: int = Query(default=1, ge=1),
):
    return await search_products(
        session=session,
        category_names=categories,
        title=title,
        description=description,
        min_price=min_price,
        max_price=max_price,
        limit=limit,
        page=page,
    )


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def product_delete(
    session: SessionDep, product_id: int, admin_user: User = Depends(require_admin)
):
    success = await delete_product(session, product_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
