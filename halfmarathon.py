import math


class Phase2:
    """
    Расчитывает параметры тренировок по 2 фазе при подготовке 
    к полумарафону плана Джека Дениелса
    'От 800 метров до марафона' второе издание 
    """
    def __init__(self, week_distance):
        """
        Параметри:
        week_distance: Загальний об'єм за тиждень, км
        
        """
        self.week_distance = week_distance # недельный километраж
        self.easy_week_distance = week_distance * 0.25 # max дистанция длительной тренировки
        self.repeats_week_distance = week_distance * 0.05 # max объем дистанций повторов в неделю
        self.threshold_week_distance = week_distance * 0.1 # max объем дистанций в пороговом темпе в неделю
        self.marathon_week_distance = week_distance * 0.1 # max объем дистанций в марафонском темпе в неделю
        
    def calculate_distance_long(self, time_long: int, pace_long: str) -> float:
        """
        Расчитывает дистанцию длительной тренировки 25% от
        недельного километража или дистанцмю по заплонированному времени.
        Выводит меньшую дистанцию
        
        Параметры:
        time_long: Время длительного забега по плану в минутах
        pace_long: Темп мин/км. Например '6:45'
        
        Возвращаемое значение:
        float: Дистанцию на длительную тренировку
        """
        # Разделяем темп на минуты и секунды
        pace_minutes, pace_seconds = map(int, pace_long.split(':'))

        # Переводим темп в секунды
        pace_total_seconds = pace_minutes * 60 + pace_seconds

        # Переводим общее время в секунды
        total_time_seconds = time_long * 60

        # Вычисляем расстояние в километрах
        distance_km = total_time_seconds / pace_total_seconds
        result_distance = round(min(distance_km, self.easy_week_distance), 2)

        return result_distance
    
    
    def number_episodes_threshold(self, distance_interval: float, pace: str) -> tuple:
        """
        Метод расчитывает количество серий повторов в П-темпе
        
        Параметры:
        distance_interval (float): дистанция интервала в км (1.6, 3.2) по плану
        pace (str): темп '5:45'
        
        Возвращаемое значение:
        tuple: Первое значение это количество интервалов (int), второе значение это
        общее расстояние в П-темпе в км (float), третье (str)- план тренировки
        """
        if self.threshold_week_distance > 6.4:
            distance_threshold = 6.4
        else:
            distance_threshold = self.threshold_week_distance
            
        nm = distance_threshold / distance_interval # количество повторов сесии
        nm = math.floor(nm) # количество повторов сесии округлить до целого в меньшую сторону
        
        # общее расстояние в П-темпе 
        distance = distance_interval * nm

        # расчет времени на преодоление дистанции 
        minutes, seconds = map(int, pace.split(":"))# Преобразуем темп в минуты (десятичный формат)
        pace_decimal = minutes + seconds / 60  # Темп переводится в десятичный формат для удобства вычислений.
        time = distance_interval * pace_decimal # в десятичном формате
        cool_down = time / 5 # для расчета времени восстановления на каждые 5 минут (по 1 минуте на каждые 5)
        
        # Перевод cool_down в формат минуты : секунды
        minutes = int(cool_down) # Выделяем целые минуты
        seconds = round((cool_down - minutes) * 60)# Переводим дробную часть в секунды
        
        # Сборка строки плана вида 3 х (1,6 км П + 1:50 отдых)
        cool_down_time = f"{minutes}:{seconds:02}"
        plan = f"{nm} x ({distance_interval} км П + {cool_down_time} отдых)"

        # Расчет общей дистанции пробегаемой в восстановительном темпе
        total_cool_down = cool_down * nm # общее время в восстановительном темпе
        distance_cool_down = total_cool_down / (pace_decimal + 1.5) # увеличиваем пороговый темп на 1:30
        
        distance = round(distance + distance_cool_down, 2)

        return (nm, distance, plan)   
         
    
    
    def number_episodes_repeats(self, plan_repeats: tuple, portion: float) -> tuple:
        """
        Метод расчитывает количество серий повторов в Пв-темпе
        
        Параметры:
        plan_repeats (tuple): Список повторов в тренировоке. Например ((200, 200), (200, 400))
                             первый элемент в кортеже дистанция в метрах Пв, второй - трусца
        portion (float): Доля от недельного объема в Пв-темпе в данной тренировке от 0.1 до 1

        Возвращаемое значение: tuple
        int: Количество серий повторов в Пв-темпе.
        float: Общая дистанция тренировки
        str: План тренировки
        
        """
        wd = self.repeats_week_distance * portion # дистанция в темпе Пв
          
        total_repeats = sum(pair[0] for pair in plan_repeats) / 1000
        total_recovery = sum(pair[1] for pair in plan_repeats) / 1000
        nm = wd / total_repeats
        nm = math.floor(nm) # округлить до целого в меньшую сторону

        distance = round(nm * (total_repeats + total_recovery), 2) # общая дистанция тренировки

        # Сборка строки плана тренировки
        plan = ""
        for i in plan_repeats:
            plan = f"{plan} + {i[0]} Пв/{i[1]} трусцой"

        plan = f"{nm} х ({plan[3:]})"    
        
        return (nm, distance, plan) 


    def calculate_distance_marathon(self, min_distance: float) -> tuple:
        """
        Метод разраховує дистанцію в тренуванні з М-темпом

        Параметри:
        min_distance (float): Мінімальна дістанція в М-темпі в одному тренуванні (по плану 6.4 км)

        Повертає: tuple
        distance_marathon (float): Дистанція в тренуванні з М-темпом
        plan (str): План тренування з М-темпом
        
        """
        if self.marathon_week_distance > min_distance:
            distance_marathon = self.marathon_week_distance
        else:
            distance_marathon = min_distance

        plan = f"{self.week_distance * 0.2 - distance_marathon} км в Л-темпе + {distance_marathon} км в М-темпе"    
           
        return (distance_marathon, plan)    
         

if __name__ == "__main__":
    p_m = Phase2(60)
    result = p_m.calculate_distance_marathon(6.4)
    print(result[1])
