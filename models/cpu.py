from typing import Dict, Any, List, Optional

class CPU:
    """ Модель для представления CPU из Redfish API."""
    def __init__(self,  data:Dict[str, Any]):
        """Инициализирует объект CPU из словаря данных, полученного из API."""

        self.id = data.get("Id", "")
        self.name = data.get("Name", "")
        self.socket = data.get("Socket", "")
        self.processor_type = data.get("ProcessorType", "")
        self.manufacturer = data.get("Manufacturer", "")
        self.model = data.get("Model", "")
        self.total_cores = data.get("TotalCores")
        self.total_threads = data.get("TotalThreads")
        self.max_speed_mhz = data.get("MaxSpeedMHz")
        self.status = data.get("Status", {})

    @classmethod
    def fetch_from_system(cls, client, system_data:Dict[str, Any]) -> List['CPU']:
        """Метод получает список CPU системы."""

        # Ссылка на коллекцию процессоров
        processors_link = system_data.get("Processors", {}).get("@odata.id")
        if not processors_link:
            print("Ссылка на процессоры не найдена .")
            return []

        # Список процессоров по ссылке
        processors_data = client.get(processors_link)
        if not processors_data:
            print(f"Не удалось получить данные процессоров по ссылке: {processors_link}")
            return []

        members = processors_data.get("Members", [])
        cpus = []
        for member in members:
            # Ссылка на конкретный процессор
            cpu_link = member.get("@odata.id")
            if cpu_link:
                # Детали процессора
                cpu_details = client.get(cpu_link)
                if cpu_details:
                    # Создать и добавить объект CPU в список
                    cpus.append(cls(cpu_details))
        return cpus

# curl -X GET http://127.0.0.1:8000/redfish/v1/Systems/
