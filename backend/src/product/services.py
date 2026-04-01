from sqlalchemy.ext.asyncio import AsyncSession
from src.product.schemas import CategoryCreate, CategoryOut
from src.product.models import Category, Product


async def create_category(session: AsyncSession, category: CategoryCreate)->CategoryOut:
    category = Category(name=category.name)
    session.add(category)
    await session.commit()
    await session.refresh(category)
    return category