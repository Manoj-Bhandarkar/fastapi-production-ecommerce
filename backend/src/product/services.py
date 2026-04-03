from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.product.schemas import CategoryCreate, CategoryOut
from src.product.models import Category, Product

################# Category ###################
async def create_category(session: AsyncSession, category: CategoryCreate)->CategoryOut:
    category = Category(name=category.name)
    session.add(category)
    await session.commit()
    await session.refresh(category)
    return category

async def get_all_category(session:AsyncSession) -> list[CategoryOut]:
    stmt = select(Category).order_by(Category.id)
    result = await session.scalars(stmt)
    return result.all()

async def delete_category(session:AsyncSession, category_id:int)-> bool:
    category = await session.get(Category, category_id)
    if not category:
        return False
    await session.delete(category)
    await session.commit()
    return True
