from fastapi import APIRouter, Depends
from fastapi.responses import Response, JSONResponse
from typing import List, Dict, Annotated

from src.dependencies.oauth2 import get_current_user_api

router = APIRouter(
    tags=["client"]
)


@router.get("/user_banner")
async def user_banner(response: Response,
                      tag_id: int,
                      feature_id: int,
                      use_last_revision: bool,
                      token: Annotated[dict, Depends(get_current_user_api)]):
    '''
    Получение баннера для пользователя
    :param response:
    :param tag_id:
    :param feature_id:
    :param use_last_revision:
    :param token:
    :return:
    '''
    pass


@router.get("/banner")
async def banner(response: Response,
                 data,
                 token):
    '''
    Получение всех баннеров c фильтрацией по фиче и/или тегу
    :param response:
    :param data:
    :param token:
    :return:
    '''
    pass


@router.post("/banner")
async def banner(response: Response,
                 tag_ids: List[int],
                 feature_id: int,
                 content: Dict[str, str],
                 is_active: bool,
                 token):
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
    pass


@router.patch("/banner/{id}")
async def patch_banner(response: Response,
                       id: int,
                       data,
                       token):
    '''
    Обновление содержимого баннера
    :param response:
    :param id:
    :param data:
    :param token:
    :return:
    '''
    pass


@router.delete("/banner/{id}")
async def delete_banner(response: Response,
                        id: int,
                        token):
    '''
    Удаление баннера по идентификатору
    :param response:
    :param id:
    :param token:
    :return:
    '''
    pass
