from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.models.engine import get_db
from app.models.database import Category
from app.schemas.category import CategoryCreate, CategoryResponse

category_router = APIRouter(prefix="/categories", tags=["Categories"])


@category_router.get("/", response_model=list[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    query = select(Category)
    categories = db.exec(query).all()
    return categories


@category_router.get("/{id}", response_model=CategoryResponse)
def get_category_by_id(id: int, db: Session = Depends(get_db)):
    category = db.get(Category, id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@category_router.post("/", response_model=CategoryResponse, status_code=201)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    # Cek duplicate
    existing = db.exec(select(Category).where(Category.name == category.name)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Category already exists")
    
    db_category = Category(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category
