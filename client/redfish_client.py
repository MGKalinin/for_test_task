import requests
from typing import Dict, Any

class RedfishClient:
    """ Класс клиента для работы с Redfish API."""

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/') # на случай двойного слеша при конкатенации?

    def get(self,path: str) -> Dict[str, Any]:
        """Метод выполняет GET запрос."""

        url = f"{self.base_url}{path}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе к {url}: {e}")
            return None
        except ValueError:
            print(f"Ответ от {url} не является JSON.")
            return None

