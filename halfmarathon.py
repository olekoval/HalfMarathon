import math


class Phase2:
    """
    Расчитывает параметры тренировок по 2 фазе при подготовке 
    к полумарафону плана Джека Дениелса
    'От 800 метров до марафона' второе издание 
    """
    def __init__(self, week_distance):
        self.week_distance = week_distance # недельный километраж
        self.easy_week_distance = week_distance * 0.25 # max дистанция длительной тренировки
        self.repeats_week_distance = week_distance * 0.05 # max объем дистанций повторов в неделю
        self.threshold_week_distance = week_distance * 0.1 # max объем дистанций в пороговом темпе в неделю
        
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
    
    
    def number_episodes__threshold(self, distance_interval: float) -> tuple:
        """
        Метод расчитывает количество серий повторов в П-темпе
        
        Параметры:
        distance_interval (float): дистанция интервала в км (1.6, 3.2)
        
        Возвращаемое значение:
        int: Количество серий повторов в П-темпе.
        """
        if self.threshold_week_distance > 6.4:
            distance_threshold = 6.4
        else:
            distance_threshold = self.threshold_week_distance
            
        nm = distance_threshold / distance_interval
        nm = math.floor(nm) # округлить до целого в меньшую сторону    
            
        return (nm, distance_interval * nm)   
         
    
    
    def number_episodes_repeats(self, plan_repeats: tuple, number_training: int) -> tuple:
        """
        Метод расчитывает количество серий повторов в Пв-темпе
        
        Параметры:
        plan_repeats (tuple): Список повторов в тренировоке. Например ((200, 200), (200, 400))
                             первый элемент в кортеже дистанция в метрах Пв, второй - трусца
        number_training (int): Номер К тренировки.

        Возвращаемое значение:
        int: Количество серий повторов в Пв-темпе.
        
        """
        wd = self.repeats_week_distance
        if number_training == 1:
            wd = wd * .75 # оставить 25% дистанции для второй тренировки
            
        total_repeats = sum(pair[0] for pair in plan_repeats) / 1000
        nm = wd / total_repeats
        nm = math.floor(nm) # округлить до целого в меньшую сторону
        if number_training == 1:
            self.repeats_week_distance = self.repeats_week_distance - total_repeats * nm
        
        return (nm, total_repeats) 
    
    
