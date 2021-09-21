from typing import Optional, Any, List
from sqlmodel import Field, Session, SQLModel, create_engine


class ContractBase(SQLModel):
    address: str
    name: str
    country: str
    city: str
    email: str
    website: str
    details: str
    p2p_endpoint: str
    node_address: str


class ContractCreate(ContractBase):
    pass


class Contract(ContractBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # def get(self, db: Session, address: Any) -> Optional[ContractBase]:
    #     return db.query(self.model).filter(self.model.address == address).first()
    #
    # def get_multi(
    #         self, db: Session, *, skip: int = 0, limit: int = 100
    # ) -> List[Contract]:
    #     return db.query(self.model).offset(skip).limit(limit).all()
    #
    # def create(self, db: Session, *, obj_in: CreateSchemaType) -> Contract:
    #     obj_in_data = jsonable_encoder(obj_in)
    #     db_obj = self.model(**obj_in_data)
    #     db.add(db_obj)
    #     db.commit()
    #     db.refresh(db_obj)
    #     return db_obj
    #
    # def remove(self, db: Session, *, address: Any) -> Contract:
    #     obj = db.query(self.model).get(address)
    #     db.delete(obj)
    #     db.commit()
    #     return obj
