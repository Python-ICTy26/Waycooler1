import textwrap
import time
import typing as tp
from string import Template

import pandas as pd
from pandas import json_normalize
from vkapi import config, session
from vkapi.exceptions import APIError


def get_posts_2500(
        owner_id: str = "",
        domain: str = "",
        offset: int = 0,
        count: int = 10,
        max_count: int = 2500,
        filter: str = "owner",
        extended: int = 0,
        fields: tp.Optional[tp.List[str]] = None,
) -> tp.Dict[str, tp.Any]:
    pass


def get_wall_execute(
        owner_id: str = "",
        domain: str = "",
        offset: int = 0,
        count: int = 10,
        max_count: int = 2500,
        filter: str = "owner",
        extended: int = 0,
        fields: tp.Optional[tp.List[str]] = None,
        progress=None,
) -> pd.DataFrame:
    """
    Возвращает список записей со стены пользователя или сообщества.

    @see: https://vk.com/dev/wall.get

    :param owner_id: Идентификатор пользователя или сообщества, со стены которого необходимо получить записи.
    :param domain: Короткий адрес пользователя или сообщества.
    :param offset: Смещение, необходимое для выборки определенного подмножества записей.
    :param count: Количество записей, которое необходимо получить (0 - все записи).
    :param max_count: Максимальное число записей, которое может быть получено за один запрос.
    :param filter: Определяет, какие типы записей на стене необходимо получить.
    :param extended: 1 — в ответе будут возвращены дополнительные поля profiles и groups, содержащие информацию о пользователях и сообществах.
    :param fields: Список дополнительных полей для профилей и сообществ, которые необходимо вернуть.
    :param progress: Callback для отображения прогресса.
    """
    code = f"""
        if({count} < 100):
            retVal = API.wall.get(
                {{
                    "owner_id":{owner_id},
                    "domain":{domain},
                    "offset":{offset},
                    "count":"{count}",
                    "filter":{filter},
                    "extended":{extended},
                    "fields": {fields}
                    "v":{config.VK_CONFIG["version"]}
                }}
            )
        else :
            retVal =[]
            for i in range(0, Math.floor({count} / 100) - 1, 100):
                answer=API.wall.get({{
                    "owner_id": str = {owner_id},
                    "domain": str = {domain},
                    "offset": int = {offset} + i * 100,
                    "count": int = 100,
                    "filter": str = {filter},
                    "extended": str = {extended},
                    "fields": str = {fields},
                    "v":{config.VK_CONFIG["version"]}
                }})
                retVal.push(...answer)
        return retVal
        """
    time.sleep(2)
    response = session.post(
        "execute",
        code=code,
        access_token=config.VK_CONFIG["access_token"],
        version=config.VK_CONFIG["version"],
    ).json()["response"]["items"]

    return json_normalize(response)
