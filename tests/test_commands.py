"""Модульные тесты для парсеров команд и обработки входного файла."""

import pytest
from equipment import Container
from main import (
    parse_mouse, parse_keyboard, parse_monitor,
    handle_add, handle_rem, process_file
)


class TestParseMouse:
    """Тесты функции parse_mouse."""

    def test_valid_mouse(self):
        """Корректные параметры создают объект Mouse."""
        params = {"type": "laser", "buttons": "6", "price": "2500", "manufacturer": "Logitech"}
        m = parse_mouse(params)
        assert m.type == "laser"
        assert m.buttons == 6
        assert m.price == 2500

    def test_bad_buttons_raises(self):
        """Нечисловое значение кнопок вызывает ValueError."""
        params = {"type": "laser", "buttons": "abc", "price": "2500", "manufacturer": "Logitech"}
        with pytest.raises(ValueError):
            parse_mouse(params)


class TestParseKeyboard:
    """Тесты функции parse_keyboard."""

    def test_valid_keyboard(self):
        """Корректные параметры создают объект Keyboard."""
        params = {"type": "membrane", "connector": "USB", "price": "3500", "manufacturer": "A4Tech"}
        kb = parse_keyboard(params)
        assert kb.type == "membrane"
        assert kb.connector == "USB"

    def test_bad_type_raises(self):
        """Недопустимый тип клавиатуры вызывает ValueError."""
        params = {"type": "unknown_type", "connector": "USB", "price": "3500", "manufacturer": "A4Tech"}
        with pytest.raises(ValueError, match="Неизвестный тип клавиатуры"):
            parse_keyboard(params)


class TestParseMonitor:
    """Тесты функции parse_monitor."""

    def test_valid_monitor(self):
        """Корректные параметры создают объект Monitor."""
        params = {"width": "1920", "height": "1080", "price": "15000", "manufacturer": "LG"}
        mon = parse_monitor(params)
        assert mon.width == 1920
        assert mon.height == 1080

    def test_bad_dimensions_raises(self):
        """Нечисловые размеры вызывают ValueError."""
        params = {"width": "wide", "height": "1080", "price": "15000", "manufacturer": "LG"}
        with pytest.raises(ValueError):
            parse_monitor(params)


class TestHandleAdd:
    """Тесты диспетчера команды ADD."""

    def test_add_mouse(self):
        """Успешное добавление мыши в контейнер."""
        c = Container()
        parts = ["ADD", "MOUSE", "type=laser", "buttons=6", "price=2500", 'manufacturer="Logitech"']
        handle_add(parts, 1, c)
        assert len(c.items) == 1
        assert c.items[0].kind() == "mouse"

    def test_add_keyboard(self):
        """Успешное добавление клавиатуры в контейнер."""
        c = Container()
        parts = ["ADD", "KEYBOARD", "type=membrane", "connector=USB", "price=3500", 'manufacturer="A4Tech"']
        handle_add(parts, 2, c)
        assert len(c.items) == 1
        assert c.items[0].kind() == "keyboard"

    def test_add_monitor(self):
        """Успешное добавление монитора в контейнер."""
        c = Container()
        parts = ["ADD", "MONITOR", "width=1920", "height=1080", "price=15000", 'manufacturer="LG"']
        handle_add(parts, 3, c)
        assert len(c.items) == 1
        assert c.items[0].kind() == "monitor"

    def test_unknown_type_raises(self):
        """Неизвестный вид оргтехники вызывает ValueError."""
        c = Container()
        parts = ["ADD", "PRINTER", "price=5000", 'manufacturer="HP"']
        with pytest.raises(ValueError, match="неизвестный вид техники"):
            handle_add(parts, 4, c)

    def test_missing_params_raises(self):
        """Команда ADD без типа вызывает ValueError."""
        c = Container()
        parts = ["ADD"]
        with pytest.raises(ValueError, match="ADD требует тип объекта"):
            handle_add(parts, 5, c)

    def test_negative_price_raises(self):
        """Отрицательная цена вызывает ValueError."""
        c = Container()
        parts = ["ADD", "MOUSE", "type=laser", "buttons=3", "price=-100", 'manufacturer="Logitech"']
        with pytest.raises(ValueError, match="Цена не может быть отрицательной"):
            handle_add(parts, 6, c)


class TestHandleRem:
    """Тесты диспетчера команды REM."""

    def test_handle_rem_valid(self):
        """Успешное удаление по условию через handle_rem."""
        c = Container()
        c.add(parse_mouse({"type": "laser", "buttons": "6", "price": "2500", "manufacturer": "Logitech"}))
        parts = ["REM", "price", ">", "2000"]
        handle_rem(parts, 1, c)
        assert len(c.items) == 0

    def test_handle_rem_short_parts_raises(self):
        """Неполные параметры REM вызывают ValueError."""
        c = Container()
        with pytest.raises(ValueError, match="REM требует условие"):
            handle_rem(["REM", "price"], 2, c)


class TestProcessFile:
    """Тесты сквозной обработки файла команд."""

    def test_file_not_found(self):
        """Несуществующий файл не приводит к сбою программы."""
        c = process_file("non_existent_file.txt")
        assert len(c.items) == 0

    def test_valid_file(self):
        """Корректный файл sample.txt полностью обрабатывается."""
        c = process_file("data/sample.txt")
        assert len(c.items) == 1
        assert c.items[0].kind() == "keyboard"
        assert c.items[0].manufacturer == "A4Tech"
