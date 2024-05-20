from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException, Path, status, Query
from pydantic import UUID4
from store.core.exceptions import NotFoundException, InsertException
from store.schemas.product import ProductIn, ProductOut, ProductUpdate, ProductUpdateOut
from store.usecases.product import ProductUsecase
from datetime import datetime

router = APIRouter(tags=["products"])


@router.patch(path="/{id}", status_code=status.HTTP_200_OK)
async def patch(
    id: UUID4 = Path(alias="id"),
    body: ProductUpdate = Body(...),
    usecase: ProductUsecase = Depends(),
) -> ProductUpdateOut:
    try:
        return await usecase.update(id=id, body=body)
    except NotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado ou nada para atualizar.",
        )


@router.post(path="/", status_code=status.HTTP_201_CREATED)
async def post(
    body: ProductIn = Body(...),
    price: float = Body(...),
    usecase: ProductUsecase = Depends(),
) -> ProductOut:
    try:
        return await usecase.create(body=body, price=price)
    except InsertException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=exc.message)


@router.get(path="/", status_code=status.HTTP_200_OK)
async def query(
    min_price: float = Query(5000, alias="minPrice"),
    max_price: float = Query(8000, alias="maxPrice"),
    usecase: ProductUsecase = Depends(),
) -> List[ProductOut]:
    return await usecase.query(min_price=min_price, max_price=max_price)


@router.delete(path="/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    id: UUID4 = Path(alias="id"), usecase: ProductUsecase = Depends()
) -> None:
    try:
        await usecase.delete(id=id)
    except NotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)


@router.get(path="/{id}", status_code=status.HTTP_200_OK)
async def get(
    id: UUID4 = Path(alias="id"), usecase: ProductUsecase = Depends()
) -> ProductOut:
    try:
        return await usecase.get(id=id)
    except NotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)
