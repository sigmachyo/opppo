"""Главный модуль для построчной обработки файла команд оргтехники."""

import sys
import shlex
from typing import Dict, List
from equipment import Mouse, Keyboard, Monitor, Container

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')  # кодировка вывода


def parse_params(tokens: List[str]) -> Dict[str, str]:
    """Извлекает словарь параметров key=value из токенов команды."""
    params = {}
    for token in tokens:
        if '=' in token:
            k, v = token.split('=', 1)
            params[k.lower()] = v
    return params


def parse_mouse(params: Dict[str, str]) -> Mouse:
    """Создаёт объект Mouse из словаря параметров."""
    m_type = params.get('type', '')
    btn_val = int(params.get('buttons', 0))
    price_val = int(params.get('price', -1))
    mfg_val = params.get('manufacturer', '')
    return Mouse(m_type, btn_val, price_val, mfg_val)


def parse_keyboard(params: Dict[str, str]) -> Keyboard:
    """Создаёт объект Keyboard из словаря параметров."""
    kb_type = params.get('type', '')
    conn_val = params.get('connector', '')
    price_val = int(params.get('price', -1))
    mfg_val = params.get('manufacturer', '')
    return Keyboard(kb_type, conn_val, price_val, mfg_val)


def parse_monitor(params: Dict[str, str]) -> Monitor:
    """Создаёт объект Monitor из словаря параметров."""
    w_val = int(params.get('width', 0))
    h_val = int(params.get('height', 0))
    price_val = int(params.get('price', -1))
    mfg_val = params.get('manufacturer', '')
    return Monitor(w_val, h_val, price_val, mfg_val)


def handle_add(parts: List[str], line_no: int, container: Container) -> None:
    """Обрабатывает команду ADD и добавляет созданный объект в контейнер."""
    if len(parts) < 2:
        raise ValueError(f"Строка {line_no}: ADD требует тип объекта")
    obj_type = parts[1].upper()
    params = parse_params(parts[2:])

    if obj_type == 'MOUSE':
        container.add(parse_mouse(params))
    elif obj_type == 'KEYBOARD':
        container.add(parse_keyboard(params))
    elif obj_type == 'MONITOR':
        container.add(parse_monitor(params))
    else:
        err = f"Строка {line_no}: неизвестный вид техники {obj_type}"
        raise ValueError(err)


def handle_rem(parts: List[str], line_no: int, container: Container) -> None:
    """Обрабатывает команду REM и удаляет подходящие объекты."""
    if len(parts) < 4:
        raise ValueError(f"Строка {line_no}: REM требует условие")
    cond_str = f"{parts[1]} {parts[2]} {parts[3]}"
    removed = container.remove_by_condition(cond_str)
    print(f"REM удалено: {removed}")


def process_file(filename: str) -> None:
    """Построчно считывает файл команд и управляет объектами в контейнере."""
    container = Container()
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line_no, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()
        if not line or line.startswith('#'):
            continue
        parts = shlex.split(line)
        cmd = parts[0].upper()
        if cmd == 'ADD':
            handle_add(parts, line_no, container)
        elif cmd == 'PRINT':
            for line_out in container.print_all():
                print(line_out)
        elif cmd == 'REM':
            handle_rem(parts, line_no, container)
        else:
            raise ValueError(f"Строка {line_no}: неизвестная команда {cmd}")


def main():
    """Точка входа программы."""
    if len(sys.argv) < 2:
        print("Использование: python main.py <файл команд>", file=sys.stderr)
        sys.exit(2)
    process_file(sys.argv[1])


if __name__ == '__main__':
    main()
