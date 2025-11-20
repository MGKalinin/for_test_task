# Инструкция по запуску проекта
### Пропущены команды установки Docker- выполнить самостоятельно согласно ОС. Отображённые ниже консольные команды для ОС Linux/Mac

## A.Установка проекта   
1. Клонировать проект
```
git clone https://github.com/MGKalinin/for_test_task.git
```   
2. Рекомендуется использовать виртуальное окружение   
```
python -m venv .venv
source .venv/bin/activate 
```
3. Установить зависимости   
```
pip install -r requirements.txt
```

## B.Запуск Redfish-Mockup-Server    
1. Установить Docker   
2. Скачать образ Redfish Mockup Server   
```
docker pull dmtf/redfish-mockup-server:latest
```   
3. Запустить контейнер   
```
docker run -d --rm -p 8000:8000 --name redfish-mockup dmtf/redfish-mockup-server:latest
```    
 
4. Проверить что контейнер запущен   
```
docker ps
```   

5. Остановить контейнер по окончанию использования   
```
docker stop redfish-mockup
```  


## C. Запуск тестов 
1. Перейти в директорию с проектом   
2. Запустить тесты
```
pytest tests/ -v
```   
## Структура проекта   
```
for_test_task/
├── client/
│   ├── __init__.py
│   └── redfish_client.py           
├── models/
│   ├── __init__.py
│   └── cpu.py                       
├── tests/
│   ├── __init__.py
│   └── test_cpu.py                  
├── requirements.txt                 
└── README.md                        
```