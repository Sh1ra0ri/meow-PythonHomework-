# Категории и товары

В этом проекте реализованы классы для работы с товарами и категориями в магазине.

## Классы

- `Product` — класс для описания товара (название, описание, цена, количество).
- `Category` — класс для описания категории товаров (название, описание, список товаров).
- `Smartphone` — класс-наследник `Product`, описывающий смартфоны (дополнительные атрибуты: производительность, модель, память, цвет).
- `LawnGrass` — класс-наследник `Product`, описывающий газонную траву (дополнительные атрибуты: страна, период прорастания, цвет).
- `BaseProduct` — абстрактный базовый класс, определяющий общий интерфейс для всех продуктов.
- `PrintInitMixin` — миксин, который выводит информацию о создании объекта.

## Основной функционал

- Автоматический подсчёт количества категорий и товаров.
- Возможность добавления товаров в категорию с проверкой типа через `isinstance` или `issubclass`.
- Создание и обновление продуктов через классовый метод `new_product`.
- Сложение общей стоимости товаров (`price * quantity`) с ограничением на типы (вызывает `TypeError` для разных классов).
- Вывод информации о товарах и категориях через метод `__str__`.
- Абстрактный класс `BaseProduct` задаёт общий интерфейс для всех продуктов.
- Миксин `PrintInitMixin` выводит в консоль информацию о классе и параметрах при создании объекта.

## Тестирование

Проект содержит тесты, которые проверяют:
- Создание объектов классов `Product`, `Category`, `Smartphone`, `LawnGrass`.
- Подсчёт количества категорий и товаров.
- Добавление товаров в категории, включая подклассы.
- Корректность работы метода `__add__` и вызова `TypeError` при неверных типах.
- Корректность работы метода `new_product` для новых и существующих продуктов.
- Корректность установки цены через сеттер `price`.
- Невозможность инстанцирования абстрактного класса `BaseProduct`.
- Наследование `Product` от `BaseProduct` и `PrintInitMixin`.
- Вывод информации о создании объекта через `PrintInitMixin`.

Покрытие тестами — более 75% 