# tests/test_cpu.py
import pytest
from client.redfish_client import RedfishClient
from models.cpu import CPU

# Базовый URL для запущенного mockup-сервера
BASE_URL = "http://127.0.0.1:8000"


@pytest.fixture
def redfish_client():
    """Фикстура для создания клиента Redfish."""

    return RedfishClient(BASE_URL)


@pytest.fixture
def system_data(redfish_client):
    """Фикстура для получения данных системы."""

    systems_data = redfish_client.get("/redfish/v1/Systems")
    if not systems_data or not systems_data.get("Members"):
        pytest.skip("Нет доступных систем для тестирования.")

    first_system_summary = systems_data["Members"][0]
    # URL системы из '@odata.id'
    system_url = first_system_summary.get("@odata.id")
    if not system_url:
        pytest.skip("Не удалось получить URL системы.")

    # Данные системы по URL
    full_system_data = redfish_client.get(system_url)
    if not full_system_data:
        pytest.skip(f"Не удалось получить данные системы по URL: {system_url}")

    return full_system_data # Возврат данных


def test_get_systems_data(redfish_client):
    """Тест проверяет, что можно получить список систем."""

    data = redfish_client.get("/redfish/v1/Systems")
    # Проверка, что ответ не None и содержит ключ Members
    assert data is not None
    assert "Members" in data
    assert len(data["Members"]) > 0


def test_cpu_fields_not_empty(redfish_client, system_data):
    """Тест проверяет, что основные строковые поля CPU не пусты,
    а числовые, если не None, то положительные."""
    cpus = CPU.fetch_from_system(redfish_client, system_data)

    # Проверка, что список CPU не пуст
    assert len(cpus) > 0, "Список CPU не должен быть пустым."

    for cpu in cpus:
        # Проверка, что строковые поля не пусты
        assert cpu.id != "", f"Id процессора {cpu.id} не должен быть пустым."
        assert cpu.name != "", f"Name процессора {cpu.id} не должно быть пустым."
        assert cpu.model != "", f"Model процессора {cpu.id} не должна быть пустой."
        assert cpu.manufacturer != "", f"Manufacturer процессора {cpu.id} не должен быть пустым."
        assert cpu.socket != "", f"Socket процессора {cpu.id} не должен быть пустым."
        assert cpu.processor_type != "", f"ProcessorType процессора {cpu.id} не должен быть пустым."

        # Проверка числовых атрибутов
        # Проверка TotalCores
        if cpu.total_cores is not None:
            assert isinstance(cpu.total_cores, int), f"TotalCores процессора {cpu.id} должно быть целым числом или None."
            assert cpu.total_cores > 0, f"TotalCores процессора {cpu.id} должно быть положительным, если задано."

        # Проверка TotalThreads
        if cpu.total_threads is not None:
            assert isinstance(cpu.total_threads, int), f"TotalThreads процессора {cpu.id} должно быть целым числом или None."
            assert cpu.total_threads > 0, f"TotalThreads процессора {cpu.id} должно быть положительным, если задано."

        # Проверка MaxSpeedMHz
        if cpu.max_speed_mhz is not None:
            assert isinstance(cpu.max_speed_mhz, int), f"MaxSpeedMHz процессора {cpu.id} должно быть целым числом или None."
            assert cpu.max_speed_mhz > 0, f"MaxSpeedMHz процессора {cpu.id} должно быть положительным, если задано."

        # Проверка структуры статуса
        assert isinstance(cpu.status, dict), f"Status процессора {cpu.id} должен быть словарем."
        assert "State" in cpu.status, f"Status процессора {cpu.id} должен содержать ключ 'State'."
        assert "Health" in cpu.status, f"Status процессора {cpu.id} должен содержать ключ 'Health'."


def test_cpu_object_attributes_types(redfish_client, system_data):
    """Тест проверяет типы атрибутов объектов CPU."""

    cpus = CPU.fetch_from_system(redfish_client, system_data)
    assert len(cpus) > 0

    for cpu in cpus:
        # Проверка типов строковых атрибутов
        assert isinstance(cpu.id, str), f"Id {cpu.id} должен быть строкой."
        assert isinstance(cpu.name, str), f"Name {cpu.id} должно быть строкой."
        assert isinstance(cpu.model, str), f"Model {cpu.id} должна быть строкой."
        assert isinstance(cpu.manufacturer, str), f"Manufacturer {cpu.id} должен быть строкой."
        assert isinstance(cpu.socket, str), f"Socket {cpu.id} должен быть строкой."
        assert isinstance(cpu.processor_type, str), f"ProcessorType {cpu.id} должен быть строкой."

        # Проверка, что типы числовых атрибутов могут быть None
        assert isinstance(cpu.total_cores, (int, type(None))), f"TotalCores {cpu.id} должно быть целым числом или None."
        assert isinstance(cpu.total_threads, (int, type(None))), f"TotalThreads {cpu.id} должно быть целым числом или None."
        assert isinstance(cpu.max_speed_mhz, (int, type(None))), f"MaxSpeedMHz {cpu.id} должно быть целым числом или None."

        # Проверка типа атрибута статуса
        assert isinstance(cpu.status, dict), f"Status {cpu.id} должен быть словарем."


