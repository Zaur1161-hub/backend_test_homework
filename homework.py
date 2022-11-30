class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type, duration,
                 distance, speed, calories):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60
    LEN_STEP: float = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = ((self.action * self.LEN_STEP
                       / self.M_IN_KM) / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: int = 1.79
    LEN_STEP: float = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return super().get_distance()

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return super().get_mean_speed()

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                     * (self.get_mean_speed())
                     + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight
                    / self.M_IN_KM
                    * (self.duration * self.MIN_IN_H))
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    first_coefficient: float = 1.1
    second_coefficient: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return super().get_distance()

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = (self.length_pool
                      * self.count_pool / self.M_IN_KM / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        """(средняя_скорость + 1.1) * 2 * вес * время_тренировки """
        calories = ((self.get_mean_speed() + self.first_coefficient)
                    * self.second_coefficient * self.weight * self.duration)
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_MULTIPLIER = 0.035
    KMH_IN_MSEC: float = 0.278
    CALORIES_SPEED_HEIGHT_MULTIPLIER = 0.029
    CM_IN_M: int = 100
    LEN_STEP: float = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.height = height

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return super().get_distance()

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return super().get_mean_speed()

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        height_in_m = self.height / self.CM_IN_M
        speed_in_ms = self.get_mean_speed() * self.KMH_IN_MSEC
        duration_in_m = self.duration * self.MIN_IN_H
        calories = ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                     + (speed_in_ms**2 / height_in_m)
                     * self.CALORIES_SPEED_HEIGHT_MULTIPLIER * self.weight)
                    * duration_in_m)
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    slovar = {'SWM': Swimming, 'RUN': Running,
              'WLK': SportsWalking}
    return slovar[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = (training.show_training_info())
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]
# .get_message()
    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
