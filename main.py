"""Главный модуль для построчной обработки файла команд оргтехники."""

import sys
import shlex
from equipment import Mouse, Keyboard, Monitor, Container

sys.stdout.reconfigure(encoding='utf-8') # кодировка вывода


def process_file(filename: str) -> None:
    container = Container()
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    line_no = 0
    for raw_line in lines:
        line_no += 1
        line = raw_line.strip()
        if not line or line.startswith('#'):
            continue
        parts = shlex.split(line)
        cmd = parts[0].upper()
        if cmd == 'ADD':
            if len(parts) < 2:
                raise ValueError(f"Строка {line_no}: ADD требует тип объекта")
            obj_type = parts[1].upper()
            params = {}
            for token in parts[2:]:
                if '=' in token:
                    k, v = token.split('=', 1)
                    params[k.lower()] = v
            price_val = int(params.get('price', -1))
            mfg_val = params.get('manufacturer', '')
            if obj_type == 'MOUSE':
                m_type = params.get('type', '')
                btn_val = int(params.get('buttons', 0))
                container.add(Mouse(m_type, btn_val, price_val, mfg_val))
            elif obj_type == 'KEYBOARD':
                kb_type = params.get('type', '')
                conn_val = params.get('connector', '')
                container.add(Keyboard(kb_type, conn_val, price_val, mfg_val))
            elif obj_type == 'MONITOR':
                w_val = int(params.get('width', 0))
                h_val = int(params.get('height', 0))
                container.add(Monitor(w_val, h_val, price_val, mfg_val))
            else:
                raise ValueError(f"Строка {line_no}: неизвестный вид техники {obj_type}")
        elif cmd == 'PRINT':
            for line_out in container.print_all():
                print(line_out)
        elif cmd == 'REM':
            if len(parts) < 4:
                raise ValueError(f"Строка {line_no}: REM требует условие")
            field = parts[1]
            op = parts[2]
            val = parts[3]
            cond_str = f"{field} {op} {val}"
            removed = container.remove_by_condition(cond_str)
            print(f"REM удалено: {removed}")
        else:
            raise ValueError(f"Строка {line_no}: неизвестная команда {cmd}")


def main():
    if len(sys.argv) < 2:
        print("Использование: python main.py <файл команд>", file=sys.stderr)
        sys.exit(2)
    process_file(sys.argv[1])


if __name__ == '__main__':
    main()
