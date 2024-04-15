from fastapi import APIRouter, Depends, Body
from fastapi.responses import Response, JSONResponse
from typing import Annotated

from src.dependencies.oauth2 import get_current_user_api
from src.db.banners_manager import *
from src.configuration import BANNER_USER, BANNER_NAME
from src.client.json_data import *

router = APIRouter(
    tags=["client"],
    dependencies=[Depends(get_current_user_api)]
)
banners = BannerManager(BANNER_USER, BANNER_NAME)


@router.get("/user_banner", summary="Получение баннера для пользователя")
async def user_banner(response: Response,
                      tag_id: int,
                      feature_id: int,
                      token: Annotated[dict, Depends(get_current_user_api)],
                      use_last_revision: bool = False):
    try:
        response.status_code = 200
        resp = await banners.find_banners(tag_id, feature_id, use_last_revision)
        if resp is None:
            response.status_code = 404
            return JSONResponse(content={"description": "Баннер не найдены"})
        if len(resp) == 0:
            response.status_code = 404
            return JSONResponse(content={"description": "Баннер не найдены"})
        return JSONResponse(content=resp[0]["content"])
    except:
        response.status_code = 500
        return JSONResponse(content={"description": "Внутренняя ошибка сервера"})


@router.get("/banner", summary="Получение всех баннеров c фильтрацией по фиче и/или тегу")
async def banner(response: Response,
                 tag_id: int,
                 feature_id: int,
                 limit: int,
                 token: Annotated[dict, Depends(get_current_user_api)]):
    try:
        response.status_code = 200
        if token["role"] != "admin":
            response.status_code = 403
            return JSONResponse(content={"description": "Пользователь не имеет доступа"})
        resp = await banners.find_banners_by_tag_or_feature(tag_id, feature_id, limit)
        if resp is not None and len(resp) == 0:
            response.status_code = 404
            return JSONResponse(content={"description": "Баннеры не найдены"})
        return JSONResponse(content=resp)
    except:
        response.status_code = 500
        return JSONResponse(content={"description": "Внутренняя ошибка сервера"})


@router.post("/banner", summary="Создание нового баннера")
async def banner(response: Response,
                 token: Annotated[dict, Depends(get_current_user_api)],
                 banner: BannerModel = Body(...)):
    try:
        response.status_code = 201
        if token["role"] != "admin":
            response.status_code = 403
            return JSONResponse(content={"description": "Пользователь не имеет доступа"})
        resp = banners.create_banner(banner.tag_ids,
                                     banner.feature_id,
                                     banner.content)
        return JSONResponse(content={"banner_id": resp})
    except:
        response.status_code = 500
        return JSONResponse(content={"description": "Внутренняя ошибка сервера"})


@router.patch("/banner/{id}", summary="Обновление содержимого баннера")
async def patch_banner(response: Response,
                       id: int,
                       token: Annotated[dict, Depends(get_current_user_api)],
                       banner: BannerModel = Body(...)):
    try:
        response.status_code = 200
        if token["role"] != "admin":
            response.status_code = 403
            return JSONResponse(content={"description": "Пользователь не имеет доступа"})
        resp = banners.update_banner(id,
                                         banner.tag_ids,
                                         banner.feature_id,
                                         banner.content,
                                         banner.is_active)
        return JSONResponse(content={"description": "OK"})
    except:
        response.status_code = 500
        return JSONResponse(content={"description": "Внутренняя ошибка сервера"})


@router.delete("/banner/{id}", summary="Удаление баннера по идентификатору")
async def delete_banner(response: Response,
                        id: int,
                        token: Annotated[dict, Depends(get_current_user_api)]):
    try:
        response.status_code = 204
        if token["role"] != "admin":
            response.status_code = 403
            return JSONResponse(content={"description": "Пользователь не имеет доступа"})
        await banners.delete_banner(id)
        return JSONResponse(content={"description": "Баннер успешно удален"})
    except:
        response.status_code = 500
        return JSONResponse(content={"description": "Внутренняя ошибка сервера"})
