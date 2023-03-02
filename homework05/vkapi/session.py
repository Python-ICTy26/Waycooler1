import typing as tp

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


class Session:
    """
    Сессия.

    :param base_url: Базовый адрес, на который будут выполняться запросы.
    :param timeout: Максимальное время ожидания ответа от сервера.
    :param max_retries: Максимальное число повторных запросов.
    :param backoff_factor: Коэффициент экспоненциального нарастания задержки.
    """

    def __init__(
        self,
        base_url: str = "https://",
        timeout: float = 5.0,
        max_retries: int = 3,
        backoff_factor: float = 0.3,
    ) -> None:
        self.current_session = requests.session()
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=backoff_factor,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["HEAD", "GET", "OPTIONS"],
        )
        adapter = HTTPAdapter(
            max_retries=retry_strategy
        )  # повторяет попытку соединения в случае неудачи
        self.current_session.mount(
            base_url, adapter=adapter
        )  # регистрируем экземпляр адаптера в префиксе
        self.base_url = base_url
        self.timeout = timeout

    def get(
        self, url: str, *args: tp.Any, **kwargs: tp.Any
    ) -> requests.Response:  # запрос содержимого с определенного ресурса
        return self.current_session.get(
            self.base_url + "/" + url, params=kwargs, timeout=self.timeout
        )

    def post(
        self, url: str, *args: tp.Any, **kwargs: tp.Any
    ) -> requests.Response:  # передача пользовательских данных заданному ресурсу
        return self.current_session.post(self.base_url + "/" + url, data=kwargs)
