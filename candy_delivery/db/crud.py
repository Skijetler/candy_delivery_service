from sqlalchemy.orm import Session

from candy_delivery.api.schema import Order as Order_schema, Courier as Courier_schema
from candy_delivery.db.models import Order as Order_db, Courier as Courier_db

def get_courier(db: Session, courier_id: int):
    return db.query(Courier_db).filter(Courier_db.id == courier_id).first()

def get_order(db: Session, order_id: int):
    return db.query(Order_db).filter(Order_db.id == order_id).first()

def create_courier(db: Session, courier: Courier_schema):
    db_courier = Courier_db(courier_type=courier.courier_type,
                            regions=courier.regions,
                            working_hours=courier.working_hours
                            )
    db.add(db_courier)
    db.commit()
    db.refresh(db_courier)
    return db_courier

def create_order(db: Session, order: Order_schema):
    db_order = Order_db(weight=order.weight,
                        region=order.region,
                        delivery_hours=order.delivery_hours,
                        )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order