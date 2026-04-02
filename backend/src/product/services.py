from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.product.schemas import CategoryCreate, CategoryOut
from src.product.models import Category, Product


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