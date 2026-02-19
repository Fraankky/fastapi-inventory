from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.models.engine import get_db
from app.models.database import StockMovement, Product
from app.schemas.stock_movement import MovementCreate, MovementResponse

movement_router = APIRouter(prefix="/movements", tags=["Stock Movements"])


def get_current_stock(db: Session, product_id: int) -> int:
    """Helper: Calculate real-time stock"""
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


@movement_router.get("/", response_model=list[MovementResponse])
def get_movements(product_id: int | None = None, db: Session = Depends(get_db)):
    query = select(StockMovement)
    if product_id:
        query = query.where(StockMovement.product_id == product_id)
    
    movements = db.exec(query.order_by(StockMovement.created_at.desc())).all()
    
    result = []
    for mov in movements:
        movement_data = MovementResponse(
            id=mov.id,
            product_id=mov.product_id,
            movement_type=mov.type,
            quantity=mov.quantity,
            note=mov.note,
            created_at=mov.created_at
        )
        result.append(movement_data)
    return result


@movement_router.get("/{id}", response_model=MovementResponse)
def get_movement_by_id(id: int, db: Session = Depends(get_db)):
    movement = db.get(StockMovement, id)
    if not movement:
        raise HTTPException(status_code=404, detail="Movement not found")
    
    return MovementResponse(
        id=movement.id,
        product_id=movement.product_id,
        movement_type=movement.type,
        quantity=movement.quantity,
        note=movement.note,
        created_at=movement.created_at
    )


@movement_router.post("/", response_model=MovementResponse, status_code=201)
def create_movement(movement: MovementCreate, db: Session = Depends(get_db)):
    product = db.get(Product, movement.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if movement.movement_type == "out":
        current = get_current_stock(db, movement.product_id)
        if movement.quantity > current:
            raise HTTPException(
                status_code=400, 
                detail=f"Insufficient stock! Available: {current}, Requested: {movement.quantity}"
            )
    
    db_movement = StockMovement(
        product_id=movement.product_id,
        type=movement.movement_type,    
        quantity=movement.quantity,
        note=movement.note
    )
    db.add(db_movement)
    db.commit()
    db.refresh(db_movement)
    
    return MovementResponse(
        id=db_movement.id,
        product_id=db_movement.product_id,
        movement_type=db_movement.type,
        quantity=db_movement.quantity,
        note=db_movement.note,
        created_at=db_movement.created_at
    )

    movement = db.get(StockMovement, id)
    if not movement:
        raise HTTPException(status_code=404, detail="Movement not found")
    db.delete(movement)
    db.commit()
    return None