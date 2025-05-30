from abc import ABC, abstractmethod


class BaseProduct(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @property
    @abstractmethod
    def price(self) -> float:
        pass

    @price.setter
    @abstractmethod
    def price(self, value: float):
        pass

    @classmethod
    @abstractmethod
    def new_product(cls, product_data: dict, existing_products: list = None):
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def __add__(self, other):
        pass


class PrintInitMixin:
    def __init__(
        self, name: str, description: str, price: float, quantity: int, *args, **kwargs
    ):
        print(
            f"Создан объект класса {self.__class__.__name__} с параметрами: {(name, description, price, quantity)}"
        )
        self.name = name
        self.description = description
        self._price = price
        self.quantity = quantity
        super().__init__(*args, **kwargs)


class Product(PrintInitMixin, BaseProduct):
    name: str
    description: str
    __price: float
    quantity: int

    def __init__(self, name: str, description: str, price: float, quantity: int):
        if quantity == 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")
        super().__init__(name, description, price, quantity)
        self.__price = price

    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, value: float):
        if value <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            self.__price = value

    @classmethod
    def new_product(
        cls, product_data: dict, existing_products: list = None
    ) -> "Product":
        name = product_data.get("name")
        description = product_data.get("description", "")
        price = product_data.get("price", 0.0)
        quantity = product_data.get("quantity", 0)
        if quantity == 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")

        if existing_products:
            for product in existing_products:
                if product.name == name:
                    product.quantity += quantity
                    if price > product.price:
                        product.price = price
                    return product

        return cls(name, description, price, quantity)

    def __str__(self) -> str:
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        if type(self) is not type(other):
            raise TypeError
        return (self.price * self.quantity) + (other.price * other.quantity)


class Category:
    category_count: int = 0
    product_count: int = 0

    name: str
    description: str

    def __init__(self, name: str, description: str, products: list = None):
        self.name = name
        self.description = description
        self.__products = products if products is not None else []
        Category.category_count += 1
        Category.product_count += len(self.__products)

    def add_product(self, product):
        if not isinstance(product, Product):
            raise ValueError(
                "Продукт должен быть экземпляром класса Product или его подкласса"
            )
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        if not self.__products:
            return "Категория пуста"
        return "\n".join(
            f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт."
            for product in self.__products
        )

    def __str__(self) -> str:
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def average_price(self) -> float:
        try:
            total_price = sum(product.price for product in self.__products)
            return total_price / len(self.__products)
        except ZeroDivisionError:
            return 0.0


class Smartphone(Product):
    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        efficiency: float,
        model: str,
        memory: int,
        color: str,
    ):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: int,
        color: str,
    ):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color
