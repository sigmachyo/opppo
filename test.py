import sys
import pytest
from equipment import Mouse, Keyboard, Monitor, Container

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')


class TestMouse:
    """Тестирование создания и валидации класса Mouse."""

    def test_properties(self):
        """Проверка корректной инициализации свойств мыши."""
        m = Mouse("laser", 6, 2500, "Logitech")
        assert m.kind() == "mouse"
        assert m.price == 2500
        assert m.buttons == 6
        assert m.type == "laser"
        assert "MOUSE" in str(m)

    def test_invalid_type_raises(self):
        """Проверка исключения при недопустимом типе мыши."""
        with pytest.raises(ValueError, match="Неизвестный тип мыши"):
            Mouse("optical", 3, 900, "Test")

    def test_zero_buttons_raises(self):
        """Проверка исключения при неположительном числе кнопок."""
        msg = "Число кнопок должно быть положительным"
        with pytest.raises(ValueError, match=msg):
            Mouse("laser", 0, 1000, "Test")


class TestKeyboard:
    """Тестирование создания и валидации класса Keyboard."""

    def test_properties(self):
        """Проверка корректной инициализации свойств клавиатуры."""
        k = Keyboard("membrane", "USB", 3500, "A4Tech")
        assert k.kind() == "keyboard"
        assert k.connector == "USB"
        assert k.price == 3500
        assert "KEYBOARD" in str(k)

    def test_invalid_type_raises(self):
        """Проверка исключения при недопустимом типе клавиатуры."""
        with pytest.raises(ValueError, match="Неизвестный тип клавиатуры"):
            Keyboard("mechanical", "USB", 5000, "Test")

    def test_empty_connector_raises(self):
        """Проверка исключения при пустом разъёме."""
        with pytest.raises(ValueError, match="Разъем не может быть пустым"):
            Keyboard("membrane", "", 3000, "Test")


class TestMonitor:
    """Тестирование создания и валидации класса Monitor."""

    def test_properties(self):
        """Проверка корректной инициализации свойств монитора."""
        mon = Monitor(1920, 1080, 15000, "LG")
        assert mon.kind() == "monitor"
        assert mon.width == 1920
        assert mon.height == 1080
        assert "MONITOR" in str(mon)

    def test_zero_dimensions_raises(self):
        """Проверка исключения при неположительных размерах монитора."""
        msg = "Размеры монитора должны быть положительными"
        with pytest.raises(ValueError, match=msg):
            Monitor(0, 1080, 10000, "Test")


class TestContainer:
    """Тестирование методов контейнера."""

    def test_add_and_print(self):
        """Проверка добавления элементов и их строкового вывода."""
        c = Container()
        c.add(Mouse("laser", 6, 2500, "Logitech"))
        c.add(Keyboard("membrane", "USB", 3500, "A4Tech"))
        c.add(Monitor(1920, 1080, 15000, "LG"))
        assert len(c.items) == 3
        descriptions = c.print_all()
        assert len(descriptions) == 3
        assert "MOUSE" in descriptions[0]

    def test_remove_by_price(self):
        """Проверка удаления объектов по числовому условию."""
        c = Container()
        c.add(Mouse("laser", 6, 2500, "Logitech"))
        c.add(Monitor(1920, 1080, 15000, "LG"))
        removed = c.remove_by_condition("price > 5000")
        assert removed == 1
        assert len(c.items) == 1
        assert c.items[0].kind() == "mouse"

    def test_remove_by_manufacturer(self):
        """Проверка удаления объектов по строковому условию."""
        c = Container()
        c.add(Mouse("laser", 6, 2500, "Logitech"))
        c.add(Monitor(1920, 1080, 15000, "LG"))
        removed = c.remove_by_condition('manufacturer == "Logitech"')
        assert removed == 1
        assert len(c.items) == 1
        assert c.items[0].kind() == "monitor"
