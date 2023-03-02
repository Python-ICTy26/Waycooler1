import datetime as dt
import statistics
import typing as tp

from vkapi.friends import get_friends


def age_predict(user_id: int) -> tp.Optional[float]:
    """
    Наивный прогноз возраста пользователя по возрасту его друзей.

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: Идентификатор пользователя.
    :return: Медианный возраст пользователя.
    """
    list_friends = get_friends(user_id=user_id, fields=["bdate"])
    ret = []
    year = dt.datetime.now().year
    month = dt.datetime.now().month
    day = dt.datetime.now().day
    for i in list_friends.items:
        if "bdate" in i:  # type: ignore
            date = list(map(int, i["bdate"].split(".")))  # type: ignore
            if len(date) != 3:
                continue
            age = (
                -date[2]
                + year
                - (1 if (date[1] < month or (date[1] == month and day < date[0])) else 0)
            )
            ret.append(age)
    if not len(ret):
        return None

    return statistics.median(ret)
