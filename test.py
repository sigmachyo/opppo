"""Модуль базовых тестов для оргтехники и контейнера."""

import sys
from equipment import Mouse, Keyboard, Monitor, Container

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')


def test_equipment():
    """Тестирование создания и свойств объектов оргтехники."""
    m = Mouse("laser", 6, 2500, "Logitech")
    assert m.kind() == "mouse"
    assert m.price == 2500
    assert m.buttons == 6

    k = Keyboard("membrane", "USB", 3500, "A4Tech")
    assert k.kind() == "keyboard"
    assert k.connector == "USB"

    mon = Monitor(1920, 1080, 15000, "LG")
    assert mon.kind() == "monitor"
    assert mon.width == 1920


def test_container():
    """Тестирование добавления и фильтрации объектов в контейнере."""
    c = Container()
    c.add(Mouse("laser", 6, 2500, "Logitech"))
    c.add(Keyboard("membrane", "USB", 3500, "A4Tech"))
    c.add(Monitor(1920, 1080, 15000, "LG"))
    assert len(c.items) == 3

    removed = c.remove_by_condition("price > 5000")
    assert removed == 1
    assert len(c.items) == 2


def run_tests():
    """Запуск тестовых сценариев."""
    test_equipment()
    test_container()
    print("All tests passed!")


if __name__ == '__main__':
    run_tests()
