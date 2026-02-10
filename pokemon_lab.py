import requests   #для работы с интернет-запросами
import matplotlib.pyplot as plt  #для рисования графиков
import pandas as pd  #работы с таблицами
import time

print("=== Лабораторная работа 1: Работа с данными по внешнему API ===\n")

# 1. Получение данных по API
print("1. Получаем список покемонов из API...")
base_url = "https://pokeapi.co/api/v2/pokemon?limit=20"  # Берем 20 покемонов для начала
response = requests.get(base_url)  #переменная ответ на запрос

if response.status_code != 200:    # если 200 то все ок если нет то ошибка
    print(f"Ошибка при получении данных: {response.status_code}")
    exit()   #выход

pokemon_list = response.json()['results']   #Из ответа сервера взять список покемонов и положить в pokemon_list"
print(f"Получен список из {len(pokemon_list)} покемонов\n")  #посчитать сколько элементов, Вывести сколько покемонов получили

# 2. Парсинг JSON и создание списка data
print("2. Собираем детальную информацию о каждом покемоне...")
data = []   # хранение информации о покемонах

for i, pokemon in enumerate(pokemon_list):  #функция которая нумерует элементы списка
    print(f"  Обрабатываю покемона {i + 1}/{len(pokemon_list)}: {pokemon['name']}")

    # Запрос детальной информации
    detail_response = requests.get(pokemon['url'])  #ящик для детального ответа
    detail_data = detail_response.json()  #Преобразовать ответ в формат Python и положить в detail_data"

    # Извлекаем нужные характеристики
    pokemon_info = {        #создаем переменную для информации о покемоне
        'id': detail_data['id'],
        'name': detail_data['name'].capitalize(),  # С большой буквы
        'height': detail_data['height'],
        'weight': detail_data['weight'],
        'hp': detail_data['stats'][0]['base_stat'],  # HP
        'attack': detail_data['stats'][1]['base_stat'],  # Attack
        'defense': detail_data['stats'][2]['base_stat'],  # Defense
        'speed': detail_data['stats'][5]['base_stat'],  # Speed
        'type': detail_data['types'][0]['type']['name'].capitalize()  # Основной тип
    }

    data.append(pokemon_info)  #метод списка: "добавить в конец"
    time.sleep(0.1)  # Небольшая задержка

print(f"\nДанные успешно собраны для {len(data)} покемонов!\n")

# 3. Создаем DataFrame для удобства
df = pd.DataFrame(data)  #Создать таблицу из списка data и назвать ее df
print("Первые 5 покемонов в данных:")
print(df[['name', 'type', 'hp', 'attack', 'defense']].head())
print()

# Сохраняем данные в CSV файл
df.to_csv('pokemon_data.csv', index=False, encoding='utf-8')
print("Данные сохранены в файл 'pokemon_data.csv'\n")

# 4. Визуализация данных
print("3. Строим графики... (закрывайте каждый график чтобы увидеть следующий)\n")

# График 1: Топ-10 по атаке
plt.figure(figsize=(12, 6))
top_10_attack = df.nlargest(10, 'attack')
bars = plt.bar(top_10_attack['name'], top_10_attack['attack'], color='#FF6B6B')
plt.title('Топ-10 покемонов по силе атаки', fontsize=16)
plt.xlabel('Имя покемона')
plt.ylabel('Сила атаки')
plt.xticks(rotation=45, ha='right')

# Добавляем значения на столбцы
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2., height + 0.5,
             f'{int(height)}', ha='center', va='bottom')

plt.tight_layout()
plt.show()

# График 2: Атака vs Защита - ПОДПИСЫВАЕМ ВСЕ ТОЧКИ
plt.figure(figsize=(12, 8))  # Увеличили размер для подписей
plt.scatter(df['attack'], df['defense'], alpha=0.7, c='green', s=80, edgecolors='black', linewidth=0.5)
plt.title('Соотношение атаки и защиты с именами покемонов', fontsize=14)
plt.xlabel('Атака', fontsize=12)
plt.ylabel('Защита', fontsize=12)
plt.grid(True, alpha=0.3)

# Подписываем ВСЕ точки (каждого покемона)
for i, row in df.iterrows():
    # Подписываем каждую точку с небольшим смещением
    plt.annotate(row['name'],
                 (row['attack'], row['defense']),
                 xytext=(5, 5),  # смещение текста от точки
                 textcoords='offset points',
                 fontsize=8,  # уменьшаем шрифт чтобы не перекрывались
                 alpha=0.7)   # делаем подписи полупрозрачными

plt.tight_layout()
plt.show()

# График 3: Распределение здоровья
plt.figure(figsize=(10, 6))
plt.hist(df['hp'], bins=10, color='skyblue', edgecolor='black', alpha=0.8)
plt.title('Распределение здоровья (HP) покемонов', fontsize=14)
plt.xlabel('Здоровье (HP)')
plt.ylabel('Количество покемонов')
plt.grid(axis='y', alpha=0.5)
plt.tight_layout()
plt.show()

# График 4: Распределение по типам
plt.figure(figsize=(8, 8))
type_counts = df['type'].value_counts()
plt.pie(type_counts.values, labels=type_counts.index, autopct='%1.1f%%',
        startangle=90, colors=['#FF9999', '#66B2FF', '#99FF99'])
plt.title('Распределение покемонов по типам', fontsize=14)
plt.tight_layout()
plt.show()

# График 5: Горизонтальная столбчатая диаграмма средних значений
plt.figure(figsize=(10, 6))  # Меняем пропорции для горизонтального графика
stats = ['hp', 'attack', 'defense', 'speed']
avg_stats = [df[stat].mean() for stat in stats]

# Создаем Горизонтальные столбцы - используем barh вместо bar
bars = plt.barh(stats, avg_stats, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'], height=0.6)
plt.title('Средние значения характеристик покемонов', fontsize=14)
plt.xlabel('Среднее значение')  # Теперь это ось X (горизонтальная)
# plt.ylabel не нужна - подписи уже слева

# Устанавливаем пределы по оси X (горизонтальной)
plt.xlim(0, max(avg_stats) * 1.15)  # Увеличиваем на 15% для подписей справа

# Добавляем значения на концы столбцов (справа)
for bar in bars:
    width = bar.get_width()  # Для горизонтальных столбцов - ширина, а не высота
    # Размещаем текст справа от столбца
    plt.text(width + max(avg_stats)*0.02,  # X: ширина + небольшой отступ
             bar.get_y() + bar.get_height()/2,  # Y: середина столбца
             f'{width:.1f}',  # Значение с одним знаком после запятой
             va='center',  # Выравнивание по вертикали: по центру
             fontsize=11)

plt.tight_layout()
plt.show()

print("\n=== Лабораторная работа выполнена! ===")
print("Построено 5 графиков:")
print("1. Топ-10 покемонов по атаке (вертикальные столбцы)")
print("2. Соотношение атаки и защиты (все точки подписаны)")
print("3. Распределение здоровья (гистограмма)")
print("4. Распределение по типам (круговая диаграмма)")
print("5. Средние значения характеристик (ГОРИЗОНТАЛЬНЫЕ столбцы)")
print("\nДанные сохранены в 'pokemon_data.csv'")
print("Графики показываются по очереди - закрывайте каждый чтобы увидеть следующий.")