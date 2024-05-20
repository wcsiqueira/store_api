from typing import List
from uuid import UUID
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import pymongo
from store.db.mongo import db_client
from store.models.product import ProductModel
from store.schemas.product import ProductIn, ProductOut, ProductUpdate, ProductUpdateOut
from store.core.exceptions import NotFoundException
from store.core.exceptions import InsertException
from datetime import datetime


class ProductUsecase:
    def __init__(self) -> None:
        self.client: AsyncIOMotorClient = db_client.get()
        self.database: AsyncIOMotorDatabase = self.client.get_database()
        self.collection = self.database.get_collection("products")

    async def create(self, body: ProductIn) -> ProductOut:
        product_model = ProductModel(**body.model_dump())
        await self.collection.insert_one(product_model.model_dump())

        return ProductOut(**product_model.model_dump())

    async def get(self, id: UUID) -> ProductOut:
        result = await self.collection.find_one({"id": id})

        if not result:
            raise NotFoundException(message=f"Product not found with filter: {id}")

        return ProductOut(**result)

    async def query(self) -> List[ProductOut]:
        return [ProductOut(**item) async for item in self.collection.find()]

    async def update(self, id: UUID, body: ProductUpdate) -> ProductUpdateOut:
        result = await self.collection.find_one_and_update(
            filter={"id": id},
            update={"$set": body.model_dump(exclude_none=True)},
            return_document=pymongo.ReturnDocument.AFTER,
        )

        return ProductUpdateOut(**result)

    async def delete(self, id: UUID) -> bool:
        product = await self.collection.find_one({"id": id})
        if not product:
            raise NotFoundException(message=f"Product not found with filter: {id}")

        result = await self.collection.delete_one({"id": id})

        return True if result.deleted_count > 0 else False


product_usecase = ProductUsecase()



async def query(self, price_min: float, price_max: float) -> List[ProductOut]:
    query = {"price": {"$gt": Decimal(price_min), "$lt": Decimal(price_max)}}
    products = await self.db.find_products(query)  # Método simulado
    return products




class ProductUsecase:
    async def create(self, body: ProductIn) -> ProductOut:
        try:
            # código de inserção aqui
        except SomeInsertError:  # substitua com o erro específico
            raise InsertException()



class ProductUsecase:
    async def update(self, id: UUID4, body: ProductUpdate) -> ProductUpdateOut:
        product = await self.get(id)  # Supondo que este método levanta NotFoundException se não encontrar o produto
        if not product:
            raise NotFoundException()
        
        body.updated_at = datetime.utcnow()
        # código de atualização aqui
class ProductUsecase:
    async def query(self, min_price: float, max_price: float) -> List[ProductOut]:
        # código de consulta com filtro de preço aqui
        products = await self.collection.find({
            "price": {"$gt": min_price, "$lt": max_price}
        }).to_list()
        return products
