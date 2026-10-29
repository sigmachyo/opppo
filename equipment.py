from abc import ABC, abstractmethod
from typing import List, Any


class OfficeEquipment(ABC):
    def __init__(self, price: int, manufacturer: str):
        if price < 0:
            raise ValueError("Цена не может быть отрицательной")
        if not manufacturer:
            raise ValueError("Производитель не может быть пустым")
        self.price = price
        self.manufacturer = manufacturer

    @abstractmethod
    def kind(self) -> str:
        pass

    @abstractmethod
    def description(self) -> str:
        pass

    def matches(self, field: str, op: str, value: Any) -> bool:
        actual = getattr(self, field, None)
        if actual is None:
            return False
        if isinstance(actual, (int, float)):
            try:
                num = float(value)
                if op == "==":
                    return actual == num
                if op == "!=":
                    return actual != num
                if op == "<":
                    return actual < num
                if op == "<=":
                    return actual <= num
                if op == ">":
                    return actual > num
                if op == ">=":
                    return actual >= num
            except (ValueError, TypeError):
                return False
        elif isinstance(actual, str):
            val_str = str(value)
            if op == "==":
                return actual.lower() == val_str.lower()
            if op == "!=":
                return actual.lower() != val_str.lower()
        return False


class Mouse(OfficeEquipment):
    def __init__(self, mouse_type: str, buttons: int, price: int, manufacturer: str):
        super().__init__(price, manufacturer)
        if mouse_type.lower() not in ("ball", "laser"):
            raise ValueError("Неизвестный тип мыши")
        if buttons < 1:
            raise ValueError("Число кнопок должно быть положительным")
        self.type = mouse_type.lower()
        self.buttons = buttons

    def kind(self) -> str:
        return "mouse"

    def description(self) -> str:
        return (
            f'MOUSE type="{self.type}" buttons={self.buttons} '
            f'price={self.price} manufacturer="{self.manufacturer}"'
        )


class Keyboard(OfficeEquipment):
    def __init__(self, keyboard_type: str, connector: str, price: int, manufacturer: str):
        super().__init__(price, manufacturer)
        self.type = keyboard_type.lower()
        self.connector = connector

    def kind(self) -> str:
        return "keyboard"

    def description(self) -> str:
        return (
            f'KEYBOARD type="{self.type}" connector="{self.connector}" '
            f'price={self.price} manufacturer="{self.manufacturer}"'
        )


class Monitor(OfficeEquipment):
    def __init__(self, width: int, height: int, price: int, manufacturer: str):
        super().__init__(price, manufacturer)
        self.width = width
        self.height = height

    def kind(self) -> str:
        return "monitor"

    def description(self) -> str:
        return (
            f'MONITOR width={self.width} height={self.height} '
            f'price={self.price} manufacturer="{self.manufacturer}"'
        )


class Container:
    def __init__(self):
        self.items: List[OfficeEquipment] = []

    def add(self, item: OfficeEquipment) -> None:
        self.items.append(item)

    def print_all(self) -> List[str]:
        return [item.description() for item in self.items]

    def remove_by_condition(self, condition: str) -> int:
        initial_len = len(self.items)
        remaining = []
        for item in self.items:
            context = {
                "price": item.price,
                "manufacturer": item.manufacturer,
                "type": getattr(item, "type", ""),
                "buttons": getattr(item, "buttons", 0),
                "connector": getattr(item, "connector", ""),
                "width": getattr(item, "width", 0),
                "height": getattr(item, "height", 0)
            }
            try:
                if not eval(condition, {}, context):
                    remaining.append(item)
            except Exception:
                remaining.append(item)
        self.items = remaining
        return initial_len - len(self.items)
