class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type: str, duration: float, distance: float, speed: float, calories: float):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return f"""Тип тренировки: {self.training_type}; Длительность: {self.duration:.3f} ч.; Дистанция: {self.distance:.3f} км; Ср. скорость: {self.speed:.3f} км/ч; Потрачено ккал: {self.calories:.3f}."""


class Training:
    """Базовый класс тренировки."""
    M_IN_KM = 1000
    HOURS_TO_MIN = 60
    LEN_STEP = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    @property
    def training_type(self):
        return None

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.training_type, self.duration, self.get_distance(), self.get_mean_speed(), self.get_spent_calories())

class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def __init__(self, action: int, duration: float, weight: float):
        super().__init__(action, duration, weight)

    @property
    def training_type(self):
        return 'Running'

    def get_spent_calories(self) -> float:
        return (self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight / self.M_IN_KM * (self.duration * self.HOURS_TO_MIN)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_MULTIPLIER1 = 0.035
    CALORIES_WEIGHT_MULTIPLIER2 = 0.029
    KMH_TO_MH_COEFF = 0.278
    CM_TO_M_COEFF = 100

    def __init__(self, action: int, duration: float, weight: float, height: float):
        super().__init__(action, duration, weight)
        self.height = height

    @property
    def training_type(self):
        return 'SportsWalking'

    def get_spent_calories(self) -> float:
        return (
                (self.CALORIES_WEIGHT_MULTIPLIER1 * self.weight +
                ((self.get_mean_speed() * self.KMH_TO_MH_COEFF)**2 / (self.height / self.CM_TO_M_COEFF)) *
                 self.CALORIES_WEIGHT_MULTIPLIER2 * self.weight) * (self.duration * self.HOURS_TO_MIN)
                )


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    CALORIES_SPEED_SHIFT = 1.1
    CALORIES_MULTIPLIER = 2

    def __init__(self, action: int, duration: float, weight: float, length_pool: float, count_pool: int):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    @property
    def training_type(self):
        return 'Swimming'

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.length_pool * self.count_pool / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.CALORIES_SPEED_SHIFT)
                * self.CALORIES_MULTIPLIER * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    try:
        type2class = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
        return type2class[workout_type](*data)
    except Exception:
        return None

def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
