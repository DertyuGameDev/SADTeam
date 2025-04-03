WORK WITH WEATHER

import pandas as pd

# Загрузка данных (замени 'data.csv' на имя своего файла)
df = pd.read_csv('/weather.csv')

# Вывод общей информации о таблице
df.info()

# Вывод количества строк в каждом столбце (не пустых значений)
print(df.count())

# Удаление строк, где колонка 'Datetime' пуста
df = df.dropna(subset=['Datetime'])

# Проверяем, что пустые строки удалены
print(df.info())

"""'''Всего записей: 3673.Теперь записей 3672.'''"""

df['Datetime'] = pd.to_datetime(df['Datetime'], errors='coerce')

# Удаление строк с некорректными датами
df = df.dropna(subset=['Datetime'])

# Создание отдельных колонок для года, месяца и дня
df['Year'] = df['Datetime'].dt.year
df['Month'] = df['Datetime'].dt.month
df['Day'] = df['Datetime'].dt.day


print(df.head())
print(df.info())

"""'''Удаляет строки с NaT в Datetime.Создаю три колонки:Year, Month, Day.Теперь можно анализировать данные с учетом сезонности, выходных, месяцев и т. д.'''"""

import pandas as pd

# Загрузка данных
df_weather = pd.read_csv('/weather.csv')

# Преобразование 'Datetime' в тип данных datetime
df_weather['Datetime'] = pd.to_datetime(df_weather['Datetime'], errors='coerce')

# Преобразование 'Temperature' в числовой формат (если данные не могут быть преобразованы, они будут заменены на NaN)
df_weather['Temperature'] = pd.to_numeric(df_weather['Temperature'], errors='coerce')

# Проверим, есть ли пропущенные значения в 'Temperature'
print(f"Пропущенные значения в 'Temperature': {df_weather['Temperature'].isna().sum()}")

# Извлечение информации из 'Datetime'
df_weather['Year'] = df_weather['Datetime'].dt.year
df_weather['Month'] = df_weather['Datetime'].dt.month
df_weather['Day'] = df_weather['Datetime'].dt.day
df_weather['Day of Week'] = df_weather['Datetime'].dt.day_name()
df_weather['Hour'] = df_weather['Datetime'].dt.hour
df_weather['Minute'] = df_weather['Datetime'].dt.minute
df_weather['Second'] = df_weather['Datetime'].dt.second

# Пример: Вывод первых строк с новыми колонками
print(df_weather[['Datetime', 'Year', 'Month', 'Day', 'Day of Week', 'Hour', 'Minute', 'Second']].head())

# Дополнительный анализ:
# 1. Количество записей по годам
year_counts = df_weather['Year'].value_counts().sort_index()
print("Количество записей по годам:")
print(year_counts)

# 2. Количество записей по месяцам
month_counts = df_weather['Month'].value_counts().sort_index()
print("Количество записей по месяцам:")
print(month_counts)

# 3. Количество записей по дням недели
day_of_week_counts = df_weather['Day of Week'].value_counts()
print("Количество записей по дням недели:")
print(day_of_week_counts)

# 4. Среднее значение температуры по месяцам (с обработкой NaN значений)
average_month_temperature = df_weather.groupby('Month')['Temperature'].mean()
print("Средняя температура по месяцам:")
print(average_month_temperature)

def get_season(month):
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    else:
        return 'Autumn'


df['Season'] = df['Month'].apply(get_season)


print(df.head())
print(df.info())

"""'''данные дополнены колонкой "Season", которая определяет сезон по месяцу:

Winter (декабрь, январь, февраль)

Spring (март, апрель, май)

Summer (июнь, июль, август)

Autumn (сентябрь, октябрь, ноябрь)

Теперь можно анализировать спрос по сезонам!'''


+ Зимой поездки могут быть короче из-за холодов, летом – длиннее.
"""

#Сколько поездок приходится на каждое время года?
print(df['Season'].value_counts())

"""###WORK WITH RIDES.CSV"""

import pandas as pd

# Загрузка данных (замени 'data.csv' на имя своего файла)
df = pd.read_csv('/rides.csv')

# Вывод общей информации о таблице
df.info()

# Вывод количества строк в каждом столбце (не пустых значений)
print(df.count())

Работаем с StartDate -  дата и время начала поездки и End Date - дата и время окончания поездки

"""Поездки по дням: воскресенье и суббота - выходные, у людей больше времени
Поездки по часам:с 16-21, люди едут с учебы, работы

Визуализация количества поездок по сезонам и месяцам
"""

import pandas as pd
import matplotlib.pyplot as plt

# Загрузка данных (замени 'rides.csv' на имя своего файла)
df = pd.read_csv('/rides.csv')

# Вывод первых строк для проверки структуры данных
print(df[['Start Date', 'End Date']].head())

# Преобразование 'Start Date' и 'End Date' в формат datetime64 с обработкой ошибок
df['Start Date'] = pd.to_datetime(df['Start Date'], errors='coerce')
df['End Date'] = pd.to_datetime(df['End Date'], errors='coerce')

# Удаление строк с некорректными датами
df.dropna(subset=['Start Date', 'End Date'], inplace=True)

# Создание отдельных колонок для анализа
# Длительность поездки в минутах
df.loc[:, 'Duration'] = (df['End Date'] - df['Start Date']).dt.total_seconds() / 60

# Фильтрация аномалий (убираем 0 и экстремально большие значения)
df = df[(df['Duration'] > 1) & (df['Duration'] < 120)]

# Часы и дни недели для анализа пиковых часов
df.loc[:, 'Start Hour'] = df['Start Date'].dt.hour
df.loc[:, 'Day of Week'] = df['Start Date'].dt.day_name()

# Функция для определения сезона
def get_season(month):
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    else:
        return 'Autumn'

# Добавление колонки с сезонами
df.loc[:, 'Season'] = df['Start Date'].dt.month.apply(get_season)
df.loc[:, 'Month'] = df['Start Date'].dt.month

# Проверяем результат
print(df[['Start Date', 'End Date', 'Duration', 'Start Hour', 'Day of Week', 'Season', 'Month']].head())

# Анализ факторов, влияющих на спрос
# 1. Средняя длительность поездки по сезонам
season_duration = df.groupby('Season')['Duration'].mean()
print(season_duration)

# 2. Количество поездок по дням недели
day_counts = df['Day of Week'].value_counts()
print(day_counts)

# 3. Количество поездок по часам
hour_counts = df['Start Hour'].value_counts().sort_index()
print(hour_counts)

# 4. Количество поездок по сезонам
season_counts = df['Season'].value_counts()

# 5. Количество поездок по месяцам
month_counts = df['Month'].value_counts().sort_index()

# Визуализация данных с аннотациями
plt.figure(figsize=(10, 5))
day_counts.plot(kind='bar', color='skyblue')
plt.xlabel('День недели')
plt.ylabel('Количество поездок')
plt.title('Распределение поездок по дням недели')
for i, v in enumerate(day_counts):
    plt.text(i, v + 100, str(v), ha='center', fontsize=10)
plt.show()

plt.figure(figsize=(10, 5))
hour_counts.plot(kind='bar', color='salmon')
plt.xlabel('Час начала поездки')
plt.ylabel('Количество поездок')
plt.title('Распределение поездок по часам')
for i, v in enumerate(hour_counts):
    plt.text(i, v + 100, str(v), ha='center', fontsize=8, rotation=90)
plt.show()

plt.figure(figsize=(8, 5))
season_counts.plot(kind='bar', color='green')
plt.xlabel('Сезон')
plt.ylabel('Количество поездок')
plt.title('Распределение поездок по сезонам')
plt.show()

plt.figure(figsize=(10, 5))
month_counts.plot(kind='bar', color='purple')
plt.xlabel('Месяц')
plt.ylabel('Количество поездок')
plt.title('Распределение поездок по месяцам')
plt.xticks(range(1, 13))
plt.show()

print(df['Season'].unique())

print(df['Month'].unique())

print(df['Season'].value_counts())

"""Additionally WORK!!!"""

df.dropna(subset=['Distance'], inplace=True)
df = df[(df['Duration'] > 1) & (df['Duration'] < 120)]
print("Пропущенные значения в колонке Distance:", df['Distance'].isna().sum())

import pandas as pd
import matplotlib.pyplot as plt

# Загрузка данных
df_weather = pd.read_csv('/weather.csv')

# Преобразование данных в числовой формат
df_weather['Wind Gust'] = pd.to_numeric(df_weather['Wind Gust'], errors='coerce')
df_weather['Wind Speed'] = pd.to_numeric(df_weather['Wind Speed'], errors='coerce')

# Проверка наличия пропусков в этих колонках
print(f"Пропущенные значения в 'Wind Gust': {df_weather['Wind Gust'].isna().sum()}")
print(f"Пропущенные значения в 'Wind Speed': {df_weather['Wind Speed'].isna().sum()}")

# Заполнение пропусков (если необходимо, можно использовать медиану или среднее значение)
df_weather['Wind Gust'].fillna(df_weather['Wind Gust'].median(), inplace=True)
df_weather['Wind Speed'].fillna(df_weather['Wind Speed'].median(), inplace=True)

# Статистика по данным
print("Статистика по 'Wind Gust':")
print(df_weather['Wind Gust'].describe())

print("Статистика по 'Wind Speed':")
print(df_weather['Wind Speed'].describe())

# Визуализация распределения данных
plt.figure(figsize=(12, 6))

# График для Wind Gust
plt.subplot(1, 2, 1)
plt.hist(df_weather['Wind Gust'], bins=30, color='skyblue', edgecolor='black')
plt.title('Распределение Wind Gust')
plt.xlabel('Wind Gust (км/ч)')
plt.ylabel('Частота')

# График для Wind Speed
plt.subplot(1, 2, 2)
plt.hist(df_weather['Wind Speed'], bins=30, color='salmon', edgecolor='black')
plt.title('Распределение Wind Speed')
plt.xlabel('Wind Speed (км/ч)')
plt.ylabel('Частота')

plt.tight_layout()
plt.show()

# Корреляция между Wind Gust и Wind Speed
correlation = df_weather[['Wind Gust', 'Wind Speed']].corr()
print("Корреляция между Wind Gust и Wind Speed:")
print(correlation)