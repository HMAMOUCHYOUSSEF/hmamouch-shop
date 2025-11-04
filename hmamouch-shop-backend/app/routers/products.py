from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import Product

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/")
def create_product(
    name: str,
    description: str,
    price: float,
    stock: int,
    owner_id: int,
    db: Session = Depends(get_db)
):
    product = Product(
        name=name,
        description=description,
        price=price,
        stock=stock,
        owner_id=owner_id
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@router.get("/")
def list_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

@router.get("/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}")
def update_product(product_id: int, name: str, price: float, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.name = name
    product.price = price
    db.commit()
    db.refresh(product)
    return product

@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}
