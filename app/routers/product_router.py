from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.models.engine import get_db
from app.models.database import Product, StockMovement
from app.schemas.product import ProductCreate, ProductResponse

product_router = APIRouter(prefix="/products", tags=["Products"])


def get_current_stock(db: Session, product_id: int) -> int:
    movements = db.exec(
        select(StockMovement).where(StockMovement.product_id == product_id)
    ).all()
    
    total = 0
    for mov in movements:
        if mov.type == "in":
            total += mov.quantity
        else:
            total -= mov.quantity
    return total


@product_router.get("/", response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    query = select(Product)
    products = db.exec(query).all()
    
    result = []
    for product in products:
        product_data = ProductResponse(
            id=product.id,
            name=product.name,
            description=product.description,
            category_id=product.category_id
        )
        result.append(product_data)
    return result


@product_router.get("/{id}", response_model=ProductResponse)
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    product = db.get(Product, id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return ProductResponse(
        id=product.id,
        name=product.name,
        description=product.description,
        category_id=product.category_id
    )


@product_router.post("/", response_model=ProductResponse, status_code=201)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    
    return ProductResponse(
        id=db_product.id,
        name=db_product.name,
        description=db_product.description,
        category_id=db_product.category_id
    )
