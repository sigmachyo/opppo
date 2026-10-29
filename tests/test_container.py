"""Модульные тесты для контейнера и функции вычисления условий."""

import pytest
from equipment import Mouse, Keyboard, Monitor, Container, _evaluate_condition


class TestContainerAdd:
    """Тесты добавления элементов в контейнер."""

    def test_add_single(self):
        """Добавление одного объекта оргтехники."""
        c = Container()
        c.add(Mouse("laser", 6, 2500, "Logitech"))
        assert len(c.items) == 1

    def test_add_multiple(self):
        """Добавление нескольких объектов различных типов."""
        c = Container()
        c.add(Mouse("laser", 6, 2500, "Logitech"))
        c.add(Keyboard("membrane", "USB", 3500, "A4Tech"))
        c.add(Monitor(1920, 1080, 15000, "LG"))
        assert len(c.items) == 3

    def test_added_figure_is_same_object(self):
        """Объект в контейнере идентичен переданному."""
        c = Container()
        m = Mouse("laser", 6, 2500, "Logitech")
        c.add(m)
        assert c.items[0] is m


class TestContainerRemove:
    """Тесты удаления элементов по условию."""

    def test_remove_by_price(self):
        """Удаление по числовой цене (price > 5000)."""
        c = Container()
        c.add(Mouse("laser", 6, 2500, "Logitech"))
        c.add(Monitor(1920, 1080, 15000, "LG"))
        removed = c.remove_by_condition("price > 5000")
        assert removed == 1
        assert len(c.items) == 1
        assert c.items[0].price == 2500

    def test_remove_by_manufacturer(self):
        """Удаление по строковому производителю."""
        c = Container()
        c.add(Mouse("laser", 6, 2500, "Logitech"))
        c.add(Keyboard("membrane", "USB", 3500, "A4Tech"))
        removed = c.remove_by_condition('manufacturer == "Logitech"')
        assert removed == 1
        assert len(c.items) == 1
        assert c.items[0].manufacturer == "A4Tech"

    def test_remove_nothing_when_no_match(self):
        """Условие не совпало — ни один элемент не удалён."""
        c = Container()
        c.add(Mouse("laser", 6, 2500, "Logitech"))
        removed = c.remove_by_condition("price > 50000")
        assert removed == 0
        assert len(c.items) == 1

    def test_remove_all_by_broad_condition(self):
        """Широкое условие удаляет все элементы."""
        c = Container()
        c.add(Mouse("laser", 6, 2500, "Logitech"))
        c.add(Keyboard("membrane", "USB", 3500, "A4Tech"))
        removed = c.remove_by_condition("price >= 0")
        assert removed == 2
        assert len(c.items) == 0

    def test_remove_invalid_condition_keeps_all(self):
        """Некорректное условие не ломает контейнер, элементы остаются."""
        c = Container()
        c.add(Mouse("laser", 6, 2500, "Logitech"))
        removed = c.remove_by_condition("bad_syntax")
        assert removed == 0
        assert len(c.items) == 1


class TestContainerPrint:
    """Тесты вывода содержимого контейнера."""

    def test_print_empty(self):
        """Вывод пустого контейнера возвращает информационную строку."""
        c = Container()
        res = c.print_all()
        assert res == ["Контейнер пуст."]

    def test_print_notempty(self):
        """Вывод непустого контейнера возвращает описания объектов."""
        c = Container()
        c.add(Mouse("laser", 6, 2500, "Logitech"))
        res = c.print_all()
        assert len(res) == 1
        assert "MOUSE" in res[0]


class TestEvaluateCondition:
    """Тесты функции _evaluate_condition."""

    def test_equals_string_true(self):
        """Равенство строк совпадает (True)."""
        ctx = {"manufacturer": "Logitech"}
        assert _evaluate_condition('manufacturer == "Logitech"', ctx) is True

    def test_equals_string_false(self):
        """Равенство строк не совпадает (False)."""
        ctx = {"manufacturer": "Logitech"}
        assert _evaluate_condition('manufacturer == "LG"', ctx) is False

    def test_not_equals(self):
        """Оператор неравенства !=."""
        ctx = {"type": "laser"}
        assert _evaluate_condition('type != "ball"', ctx) is True

    def test_greater_true(self):
        """Оператор > истинен."""
        ctx = {"price": 15000}
        assert _evaluate_condition("price > 5000", ctx) is True

    def test_greater_false(self):
        """Оператор > ложен."""
        ctx = {"price": 2500}
        assert _evaluate_condition("price > 5000", ctx) is False

    def test_less(self):
        """Оператор <."""
        ctx = {"price": 2500}
        assert _evaluate_condition("price < 5000", ctx) is True

    def test_greater_equal(self):
        """Оператор >=."""
        ctx = {"buttons": 6}
        assert _evaluate_condition("buttons >= 6", ctx) is True

    def test_less_equal(self):
        """Оператор <=."""
        ctx = {"buttons": 6}
        assert _evaluate_condition("buttons <= 6", ctx) is True

    def test_equals_number(self):
        """Оператор == для чисел."""
        ctx = {"width": 1920}
        assert _evaluate_condition("width == 1920", ctx) is True

    def test_unknown_field_raises_key_error(self):
        """Обращение к неизвестному полю вызывает KeyError."""
        ctx = {"price": 1000}
        with pytest.raises(KeyError, match="Неизвестное поле"):
            _evaluate_condition("color == red", ctx)

    def test_no_operator_raises_value_error(self):
        """Строка без трёх токенов вызывает ValueError."""
        ctx = {"price": 1000}
        with pytest.raises(ValueError, match="Нет оператора"):
            _evaluate_condition("price", ctx)

