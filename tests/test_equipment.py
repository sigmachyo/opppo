"""Модульные тесты для классов иерархии оргтехники."""

import pytest
from equipment import OfficeEquipment, Mouse, Keyboard, Monitor


class DummyEquipment(OfficeEquipment):
    """Тестовый класс для проверки методов базового класса."""

    def kind(self) -> str:
        return "dummy"

    def description(self) -> str:
        return f"DUMMY price={self.price} manufacturer={self.manufacturer}"


class TestOfficeEquipmentBase:
    """Тесты базового класса OfficeEquipment."""

    def test_base_stores_price_and_manufacturer(self):
        """Проверка сохранения цены и производителя."""
        obj = DummyEquipment(1000, "Sony")
        assert obj.price == 1000
        assert obj.manufacturer == "Sony"
        assert obj.kind() == "dummy"

    def test_base_negative_price_raises(self):
        """Отрицательная цена вызывает ValueError."""
        with pytest.raises(ValueError, match="Цена не может быть отрицательной"):
            DummyEquipment(-10, "Sony")

    def test_base_empty_manufacturer_raises(self):
        """Пустой производитель вызывает ValueError."""
        with pytest.raises(ValueError, match="Производитель не может быть пустым"):
            DummyEquipment(1000, "")

    def test_base_matches_numeric(self):
        """Проверка метода matches для числовых полей."""
        obj = DummyEquipment(1000, "Sony")
        assert obj.matches("price", "==", "1000") is True
        assert obj.matches("price", "!=", "2000") is True
        assert obj.matches("price", ">", "500") is True
        assert obj.matches("price", "<", "1500") is True
        assert obj.matches("price", ">=", "1000") is True
        assert obj.matches("price", "<=", "1000") is True
        assert obj.matches("price", "==", "not_a_number") is False

    def test_base_matches_string(self):
        """Проверка метода matches для строковых полей."""
        obj = DummyEquipment(1000, "Sony")
        assert obj.matches("manufacturer", "==", "sony") is True
        assert obj.matches("manufacturer", "!=", "lg") is True
        assert obj.matches("unknown_field", "==", "any") is False
        assert obj.matches("manufacturer", ">", "any") is False

    def test_base_str_calls_description(self):
        """Метод __str__ возвращает строку description."""
        obj = DummyEquipment(500, "Dell")
        assert str(obj) == obj.description()
        assert "DUMMY" in str(obj)


class TestMouse:
    """Тесты класса Mouse."""

    def test_mouse_laser_properties(self):
        """Корректная инициализация лазерной мыши."""
        m = Mouse("laser", 6, 2500, "Logitech")
        assert m.type == "laser"
        assert m.buttons == 6
        assert m.price == 2500
        assert m.manufacturer == "Logitech"

    def test_mouse_ball_properties(self):
        """Корректная инициализация шариковой мыши."""
        m = Mouse("ball", 3, 900, "OldTech")
        assert m.type == "ball"
        assert m.buttons == 3

    def test_mouse_kind(self):
        """Метод kind возвращает 'mouse'."""
        m = Mouse("laser", 5, 1200, "A4Tech")
        assert m.kind() == "mouse"

    def test_mouse_str_contains_mouse(self):
        """__str__ содержит ключевое слово MOUSE."""
        m = Mouse("laser", 6, 2500, "Logitech")
        assert "MOUSE" in str(m)
        assert 'type="laser"' in str(m)

    def test_mouse_zero_buttons_raises(self):
        """Кнопки <= 0 вызывают ValueError."""
        with pytest.raises(ValueError, match="Число кнопок должно быть положительным"):
            Mouse("laser", 0, 1500, "Genius")

    def test_mouse_invalid_type_raises(self):
        """Неизвестный тип мыши вызывает ValueError."""
        with pytest.raises(ValueError, match="Неизвестный тип мыши"):
            Mouse("optical", 3, 1000, "Genius")


class TestKeyboard:
    """Тесты класса Keyboard."""

    def test_keyboard_membrane_properties(self):
        """Инициализация мембранной клавиатуры."""
        kb = Keyboard("membrane", "USB", 3500, "A4Tech")
        assert kb.type == "membrane"
        assert kb.connector == "USB"
        assert kb.price == 3500

    def test_keyboard_dome_properties(self):
        """Инициализация купольной клавиатуры."""
        kb = Keyboard("dome", "PS/2", 1500, "Mitsumi")
        assert kb.type == "dome"
        assert kb.connector == "PS/2"

    def test_keyboard_capacitive_properties(self):
        """Инициализация емкостной клавиатуры."""
        kb = Keyboard("capacitive", "USB Type-C", 8000, "HHKB")
        assert kb.type == "capacitive"
        assert kb.connector == "USB Type-C"

    def test_keyboard_kind(self):
        """Метод kind возвращает 'keyboard'."""
        kb = Keyboard("membrane", "USB", 2000, "HP")
        assert kb.kind() == "keyboard"

    def test_keyboard_str_contains_keyboard(self):
        """__str__ содержит ключевое слово KEYBOARD."""
        kb = Keyboard("membrane", "USB", 3500, "A4Tech")
        assert "KEYBOARD" in str(kb)
        assert 'connector="USB"' in str(kb)

    def test_keyboard_invalid_type_raises(self):
        """Неизвестный тип клавиатуры вызывает ValueError."""
        with pytest.raises(ValueError, match="Неизвестный тип клавиатуры"):
            Keyboard("mechanical", "USB", 5000, "Razer")


class TestMonitor:
    """Тесты класса Monitor."""

    def test_monitor_properties(self):
        """Инициализация параметров монитора."""
        mon = Monitor(1920, 1080, 15000, "LG")
        assert mon.width == 1920
        assert mon.height == 1080
        assert mon.price == 15000
        assert mon.manufacturer == "LG"

    def test_monitor_kind(self):
        """Метод kind возвращает 'monitor'."""
        mon = Monitor(2560, 1440, 25000, "Dell")
        assert mon.kind() == "monitor"

    def test_monitor_str_contains_monitor(self):
        """__str__ содержит ключевое слово MONITOR."""
        mon = Monitor(1920, 1080, 15000, "LG")
        assert "MONITOR" in str(mon)
        assert "width=1920" in str(mon)

    def test_monitor_zero_width_raises(self):
        """Ширина <= 0 вызывает ValueError."""
        with pytest.raises(ValueError, match="Размеры монитора должны быть положительными"):
            Monitor(0, 1080, 10000, "Samsung")

    def test_monitor_zero_height_raises(self):
        """Высота <= 0 вызывает ValueError."""
        with pytest.raises(ValueError, match="Размеры монитора должны быть положительными"):
            Monitor(1920, 0, 10000, "Samsung")
