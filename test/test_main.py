import pytest
from src.main import Product, Category, Smartphone, LawnGrass


@pytest.fixture
def product_sample():
    return Product("Чайник", "Электрический чайник", 1500.0, 5)


@pytest.fixture
def category_sample():
    Category.category_count = 0
    Category.product_count = 0
    products = [
        Product("Сковорода", "Сковорода с антипригарным покрытием", 1200.0, 10),
        Product("Кастрюля", "Кастрюля 3 литра", 1800.0, 7),
    ]
    return Category("Кухня", "Товары для кухни", products)


@pytest.fixture
def smartphone():
    return Smartphone(
        "iPhone", "Смартфон Apple", 50000.0, 3, 2.5, "14 Pro", 256, "Black"
    )


@pytest.fixture
def lawngrass1():
    return LawnGrass("Газон", "Трава для газона", 300.0, 10, "Россия", 14, "Зеленый")


def test_product_init(product_sample):
    assert product_sample.name == "Чайник"
    assert product_sample.description == "Электрический чайник"
    assert product_sample.price == 1500.0
    assert product_sample.quantity == 5


def test_category_init(category_sample):
    assert category_sample.name == "Кухня"
    assert category_sample.description == "Товары для кухни"
    assert isinstance(category_sample.products, str)
    assert len(category_sample.products.split("\n")) == 2
    assert "Сковорода, 1200.0 руб. Остаток: 10 шт." in category_sample.products
    assert "Кастрюля, 1800.0 руб. Остаток: 7 шт." in category_sample.products


def test_category_counter():
    Category.category_count = 0
    Category("Одежда", "Товары для взрослых")
    Category("Обувь", "Обувь для всех сезонов")
    assert Category.category_count == 2


def test_product_counter(category_sample, product_sample):
    assert Category.product_count == 2
    Category(
        "Книги",
        "Художественная литература",
        [Product("Роман", "Книга в твёрдой обложке", 500.0, 15)],
    )
    assert Category.product_count == 3


def test_add_product(category_sample, product_sample):
    initial = Category.product_count
    category_sample.add_product(product_sample)
    assert "Чайник, 1500.0 руб. Остаток: 5 шт." in category_sample.products
    assert Category.product_count == initial + 1


def test_empty_category():
    Category.product_count = 0
    Category.category_count = 0
    empty = Category("Пустая", "Без товаров")
    assert empty.products == "Категория пуста"
    assert Category.category_count == 1
    assert Category.product_count == 0


def test_product_price_setter(product_sample, capsys):
    product_sample.price = 0
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert product_sample.price == 1500.0
    product_sample.price = 2000.0
    assert product_sample.price == 2000.0


def test_new_product_no_duplicates():
    product_data = {
        "name": "Тостер",
        "description": "Тостер для хлеба",
        "price": 2500.0,
        "quantity": 3,
    }
    new_product = Product.new_product(product_data)
    assert new_product.name == "Тостер"
    assert new_product.description == "Тостер для хлеба"
    assert new_product.price == 2500.0
    assert new_product.quantity == 3


def test_new_product_with_duplicates():
    existing_products = [Product("Тостер", "Тостер для хлеба", 2000.0, 3)]
    product_data = {
        "name": "Тостер",
        "description": "Тостер для хлеба",
        "price": 2500.0,
        "quantity": 2,
    }
    updated_product = Product.new_product(product_data, existing_products)
    assert updated_product.quantity == 5  # 3 + 2
    assert updated_product.price == 2500.0


def test_add_product_subclass(category_sample):
    class SubProduct(Product):
        pass

    sub_product = SubProduct("Тостер", "Тостер для хлеба", 2000.0, 3)
    category_sample.add_product(sub_product)
    assert "Тостер, 2000.0 руб. Остаток: 3 шт." in category_sample.products


def test_product_str(product_sample):
    assert str(product_sample) == "Чайник, 1500.0 руб. Остаток: 5 шт."


def test_category_str(category_sample):
    assert str(category_sample) == "Кухня, количество продуктов: 17 шт."


def test_product_add():
    product1 = Product("Блендер", "Кухонный блендер", 150.0, 8)
    product2 = Product("Тостер", "Тостер для хлеба", 250.0, 4)
    assert product1 + product2 == 2200.0


def test_product_add_type_error(smartphone, lawngrass1):
    with pytest.raises(TypeError):
        smartphone + lawngrass1


def test_smartphone_init(smartphone):
    assert smartphone.name == "iPhone"
    assert smartphone.description == "Смартфон Apple"
    assert smartphone.price == 50000.0
    assert smartphone.quantity == 3
    assert smartphone.efficiency == 2.5
    assert smartphone.model == "14 Pro"
    assert smartphone.memory == 256
    assert smartphone.color == "Black"


def test_lawngrass_init(lawngrass1):
    assert lawngrass1.name == "Газон"
    assert lawngrass1.description == "Трава для газона"
    assert lawngrass1.price == 300.0
    assert lawngrass1.quantity == 10
    assert lawngrass1.country == "Россия"
    assert lawngrass1.germination_period == 14
    assert lawngrass1.color == "Зеленый"


def test_smartphone_inheritance(smartphone):
    from src.main import Product

    assert isinstance(smartphone, Product)


def test_lawngrass_inheritance(lawngrass1):
    from src.main import Product

    assert isinstance(lawngrass1, Product)


def test_smartphone_attributes_types(smartphone):
    assert isinstance(smartphone.efficiency, float)
    assert isinstance(smartphone.model, str)
    assert isinstance(smartphone.memory, int)
    assert isinstance(smartphone.color, str)


def test_lawngrass_attributes_types(lawngrass1):
    assert isinstance(lawngrass1.country, str)
    assert isinstance(lawngrass1.germination_period, int)
    assert isinstance(lawngrass1.color, str)
