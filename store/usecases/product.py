from typing import List, Optional
from uuid import UUID
from datetime import datetime
from fastapi import HTTPException
from store.core.exceptions import NotFoundException, InsertException
from store.models.product import ProductModel
from store.schemas.product import ProductIn, ProductOut, ProductUpdate, ProductUpdateOut
from store.db.mongo import db_client


class ProductUsecase:
    def __init__(self) -> None:
        self.collection = db_client.get_collection("products")

    async def create(self, body: ProductIn, price: float) -> ProductOut:
        try:
            product_model = ProductModel(**body.dict(), price=price)
            await self.collection.insert_one(product_model.dict())
            return ProductOut(**product_model.dict())
        except Exception as e:
            raise InsertException(f"Erro ao inserir Produto: {str(e)}")

    async def get(self, id: UUID) -> ProductOut:
        result = await self.collection.find_one({"id": id})
        if not result:
            raise NotFoundException(message=f"Product not found with filter: {id}")
        return ProductOut(**result)

    async def query(
        self,
        min_price: float = 5000,
        max_price: float = 8000,
        nome: Optional[str] = None,
        cpf: Optional[str] = None,
    ) -> List[ProductOut]:
        query = {"price": {"$gt": min_price, "$lt": max_price}}
        if nome:
            query["nome"] = nome
        if cpf:
            query["cpf"] = cpf
        products = await self.collection.find(query).to_list()
        return [ProductOut(**product) for product in products]

    async def update(self, id: UUID, body: ProductUpdate) -> ProductUpdateOut:
        product = await self.get(id)
        if not product:
            raise NotFoundException("Produto não encontrado")
        body.updated_at = datetime.utcnow()
        update_result = await self.collection.update_one(
            {"id": id}, {"$set": body.dict(exclude_unset=True)}
        )
        if update_result.modified_count == 0:
            raise NotFoundException("Produto não encontrado ou nada  para atualizar")
        updated_product = await self.get(id)
        return ProductUpdateOut(**updated_product)

    async def delete(self, id: UUID) -> bool:
        product = await self.collection.find_one({"id": id})
        if not product:
            raise NotFoundException(message=f"Product not found with filter: {id}")
        result = await self.collection.delete_one({"id": id})
        return True if result.deleted_count > 0 else False
