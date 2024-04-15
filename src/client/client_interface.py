from fastapi import APIRouter, Depends
from fastapi.responses import Response, JSONResponse
from typing import List, Dict, Annotated

from src.dependencies.oauth2 import get_current_user_api
from src.db.banners_manager import *
from src.configuration import BANNER_USER, BANNER_NAME

router = APIRouter(
    tags=["client"]
)
banners = BannerManager(BANNER_USER, BANNER_NAME)


@router.get("/user_banner")
async def user_banner(response: Response,
                      tag_id: int,
                      feature_id: int,
                      token: Annotated[dict, Depends(get_current_user_api)],
                      use_last_revision: bool = False):
    '''
    Получение баннера для пользователя
    :param response:
    :param tag_id:
    :param feature_id:
    :param use_last_revision:
    :param token:
    :return:
    '''
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


@router.get("/banner")
async def banner(response: Response,
                 tag_id: int,
                 feature_id: int,
                 limit: int,
                 token: Annotated[dict, Depends(get_current_user_api)]):
    '''
    Получение всех баннеров c фильтрацией по фиче и/или тегу
    :param response:
    :param data:
    :param token:
    :return:
    '''
    try:
        response.status_code = 200
        if token["role"] != "admin":
            response.status_code = 403
            return JSONResponse(content={"description": "Пользователь не имеет доступа"})
        resp = await banners.find_banners_by_tag_or_feature(tag_id, feature_id, limit)
        if resp is not None and len(resp) == 0:
            response.status_code = 404
            return JSONResponse(content={"description": "Баннеры не найдены"})

    except:
        response.status_code = 500
        return JSONResponse(content={"description": "Внутренняя ошибка сервера"})


@router.post("/banner")
async def banner(response: Response,
                 tag_ids: List[int],
                 feature_id: int,
                 content: Dict[str, str],
                 is_active: bool,
                 token: Annotated[dict, Depends(get_current_user_api)]):
    '''
    Создание нового баннера
    :param response:
    :param tag_ids:
    :param feature_id:
    :param content:
    :param is_active:
    :param token:
    :return:
    '''
    try:
        pass
    except:
        response.status_code = 500
        return JSONResponse(content={"description": "Внутренняя ошибка сервера"})


@router.patch("/banner/{id}")
async def patch_banner(response: Response,
                       id: int,
                       data,
                       token: Annotated[dict, Depends(get_current_user_api)]):
    '''
    Обновление содержимого баннера
    :param response:
    :param id:
    :param data:
    :param token:
    :return:
    '''
    try:
        pass
    except:
        response.status_code = 500
        return JSONResponse(content={"description": "Внутренняя ошибка сервера"})


@router.delete("/banner/{id}")
async def delete_banner(response: Response,
                        id: int,
                        token: Annotated[dict, Depends(get_current_user_api)]):
    '''
    Удаление баннера по идентификатору
    :param response:
    :param id:
    :param token:
    :return:
    '''
    try:
        pass
    except:
        response.status_code = 500
        return JSONResponse(content={"description": "Внутренняя ошибка сервера"})
