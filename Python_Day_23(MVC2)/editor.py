import os
import json
from datetime import datetime
from typing import Optional, List, Dict


class EditorModel:
    
    def __init__(self, history_dir: str = ".versions"):
        self.current_file: Optional[str] = None
        self.content: str = ""
        self.history_dir = history_dir
        self.is_modified: bool = False
        
        if not os.path.exists(history_dir):
            os.makedirs(history_dir)
    
    def create_file(self, filename: str) -> bool:
        if os.path.exists(filename):
            return False
        self.current_file = filename
        self.content = ""
        self.is_modified = True
        return True
    
    def open_file(self, filename: str) -> bool:
        if not os.path.exists(filename):
            return False
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                self.content = f.read()
            self.current_file = filename
            self.is_modified = False
            return True
        except Exception:
            return False
    
    def set_content(self, content: str) -> None:
        self.content = content
        self.is_modified = True
    
    def get_content(self) -> str:
        return self.content
    
    def save_file(self) -> bool:
        if not self.current_file:
            return False
        try:
            if os.path.exists(self.current_file):
                self._save_version()
            
            with open(self.current_file, 'w', encoding='utf-8') as f:
                f.write(self.content)
            self.is_modified = False
            return True
        except Exception:
            return False
    
    def _get_history_file(self) -> str:
        safe_name = self.current_file.replace('/', '_').replace('\\', '_')
        return os.path.join(self.history_dir, f"{safe_name}.history.json")
    
    def _save_version(self) -> None:
        history_file = self._get_history_file()
        
        history = self._load_history()
        
        try:
            with open(self.current_file, 'r', encoding='utf-8') as f:
                old_content = f.read()
        except:
            old_content = ""
        
        version = {
            'version': len(history) + 1,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'content': old_content
        }
        history.append(version)
        
        history = history[-10:]
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    
    def _load_history(self) -> List[Dict]:
        history_file = self._get_history_file()
        if os.path.exists(history_file):
            try:
                with open(history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def get_versions(self) -> List[Dict]:
        if not self.current_file:
            return []
        return self._load_history()
    
    def restore_version(self, version_num: int) -> bool:
        history = self._load_history()
        for version in history:
            if version['version'] == version_num:
                self.content = version['content']
                self.is_modified = True
                return True
        return False
    
    def get_stats(self) -> Dict:
        chars = len(self.content)
        words = len(self.content.split()) if self.content.strip() else 0
        lines = len(self.content.splitlines()) if self.content else 0
        return {'chars': chars, 'words': words, 'lines': lines}


class EditorView:
    SEPARATOR = "=" * 50
    
    def clear_screen(self) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def show_header(self, filename: Optional[str], modified: bool) -> None:
        print(self.SEPARATOR)
        print("ТЕКСТОВЫЙ РЕДАКТОР MVC")
        print(self.SEPARATOR)
        if filename:
            status = " [изменён]" if modified else ""
            print(f" Файл: {filename}{status}")
        else:
            print(" Файл не открыт")
        print(self.SEPARATOR)
    
    def show_main_menu(self) -> None:
        """Показать главное меню."""
        print("\n ГЛАВНОЕ МЕНЮ:")
        print("  1. Создать новый файл")
        print("  2. Открыть файл")
        print("  3. Редактировать")
        print("  4. Сохранить")
        print("  5. Просмотреть содержимое")
        print("  6. История версий")
        print("  7. Восстановить версию")
        print("  8. Статистика")
        print("  0. Выход")
        print()
    
    def get_input(self, prompt: str) -> str:
        """Получить ввод пользователя."""
        return input(f"➤ {prompt}: ").strip()
    
    def get_menu_choice(self) -> str:
        """Получить выбор меню."""
        return input("➤ Выберите действие: ").strip()
    
    def show_message(self, message: str, msg_type: str = "info") -> None:
        """Показать сообщение."""
        icons = {
            "success": "✅",
            "error": "❌",
            "info": "ℹ️",
            "warning": "⚠️"
        }
        icon = icons.get(msg_type, "ℹ️")
        print(f"\n{icon} {message}")
    
    def show_content(self, content: str) -> None:
        """Показать содержимое файла."""
        print("\n" + "-" * 50)
        print(" СОДЕРЖИМОЕ ФАЙЛА:")
        print("-" * 50)
        if content:
            lines = content.splitlines()
            for i, line in enumerate(lines, 1):
                print(f"{i:3} │ {line}")
        else:
            print("(файл пуст)")
        print("-" * 50)
    
    def show_versions(self, versions: List[Dict]) -> None:
        """Показать историю версий."""
        print("\n" + "-" * 50)
        print(" ИСТОРИЯ ВЕРСИЙ:")
        print("-" * 50)
        if not versions:
            print("История пуста")
        else:
            for v in versions:
                preview = v['content'][:50].replace('\n', ' ')
                if len(v['content']) > 50:
                    preview += "..."
                print(f"  v{v['version']} | {v['timestamp']} | {preview}")
        print("-" * 50)
    
    def show_stats(self, stats: Dict) -> None:
        """Показать статистику."""
        print("\n" + "-" * 50)
        print(" СТАТИСТИКА:")
        print("-" * 50)
        print(f"  Символов: {stats['chars']}")
        print(f"  Слов:     {stats['words']}")
        print(f"  Строк:    {stats['lines']}")
        print("-" * 50)
    
    def get_multiline_input(self) -> str:
        """Получить многострочный ввод."""
        print("\n Режим редактирования")
        print("   (введите :save для сохранения, :cancel для отмены)")
        print("-" * 50)
        
        lines = []
        line_num = 1
        while True:
            try:
                line = input(f"{line_num:3} │ ")
                if line == ':save':
                    break
                elif line == ':cancel':
                    return None
                lines.append(line)
                line_num += 1
            except EOFError:
                break
        return '\n'.join(lines)
    
    def confirm(self, message: str) -> bool:
        """Запросить подтверждение."""
        response = input(f" {message} (д/н): ").strip().lower()
        return response in ('д', 'да', 'y', 'yes')
    
    def pause(self) -> None:
        """Пауза перед продолжением."""
        input("\n⏎ Нажмите Enter для продолжения...")


class EditorController:
    
    def __init__(self):
        self.model = EditorModel()
        self.view = EditorView()
        self.running = True
    
    def run(self) -> None:
        while self.running:
            self.view.clear_screen()
            self.view.show_header(
                self.model.current_file, 
                self.model.is_modified
            )
            self.view.show_main_menu()
            
            choice = self.view.get_menu_choice()
            self._handle_choice(choice)
    
    def _handle_choice(self, choice: str) -> None:
        actions = {
            '1': self._create_file,
            '2': self._open_file,
            '3': self._edit_file,
            '4': self._save_file,
            '5': self._view_content,
            '6': self._view_history,
            '7': self._restore_version,
            '8': self._show_stats,
            '0': self._exit,
        }
        
        action = actions.get(choice)
        if action:
            action()
        else:
            self.view.show_message("Неверный выбор", "error")
            self.view.pause()
    
    def _create_file(self) -> None:
        filename = self.view.get_input("Имя нового файла")
        if not filename:
            return
        
        if '.' not in filename:
            filename += '.txt'
        
        if self.model.create_file(filename):
            self.view.show_message(f"Файл '{filename}' создан", "success")
        else:
            self.view.show_message("Файл уже существует", "error")
        self.view.pause()
    
    def _open_file(self) -> None:
        txt_files = [f for f in os.listdir('.') if f.endswith('.txt')]
        if txt_files:
            print("\n Доступные файлы:")
            for f in txt_files:
                print(f"   • {f}")
        
        filename = self.view.get_input("Имя файла для открытия")
        if not filename:
            return
        
        if self.model.open_file(filename):
            self.view.show_message(f"Файл '{filename}' открыт", "success")
        else:
            self.view.show_message("Файл не найден", "error")
        self.view.pause()
    
    def _edit_file(self) -> None:
        if not self.model.current_file:
            self.view.show_message("Сначала создайте или откройте файл", "warning")
            self.view.pause()
            return
        
        current = self.model.get_content()
        if current:
            self.view.show_content(current)
            if not self.view.confirm("Заменить содержимое?"):
                print("\n📝 Добавление текста:")
                new_content = self.view.get_multiline_input()
                if new_content is not None:
                    self.model.set_content(current + '\n' + new_content)
                    self.view.show_message("Текст добавлен", "success")
                self.view.pause()
                return
        
        new_content = self.view.get_multiline_input()
        if new_content is not None:
            self.model.set_content(new_content)
            self.view.show_message("Содержимое обновлено", "success")
        else:
            self.view.show_message("Редактирование отменено", "info")
        self.view.pause()
    
    def _save_file(self) -> None:
        if not self.model.current_file:
            self.view.show_message("Нет файла для сохранения", "warning")
            self.view.pause()
            return
        
        if self.model.save_file():
            self.view.show_message("Файл сохранён (версия создана)", "success")
        else:
            self.view.show_message("Ошибка сохранения", "error")
        self.view.pause()
    
    def _view_content(self) -> None:
        if not self.model.current_file:
            self.view.show_message("Файл не открыт", "warning")
            self.view.pause()
            return
        
        self.view.show_content(self.model.get_content())
        self.view.pause()
    
    def _view_history(self) -> None:
        if not self.model.current_file:
            self.view.show_message("Файл не открыт", "warning")
            self.view.pause()
            return
        
        versions = self.model.get_versions()
        self.view.show_versions(versions)
        
        if versions:
            ver_num = self.view.get_input("Номер версии для просмотра (Enter - пропустить)")
            if ver_num.isdigit():
                for v in versions:
                    if v['version'] == int(ver_num):
                        self.view.show_content(v['content'])
                        break
        self.view.pause()
    
    def _restore_version(self) -> None:
        if not self.model.current_file:
            self.view.show_message("Файл не открыт", "warning")
            self.view.pause()
            return
        
        versions = self.model.get_versions()
        self.view.show_versions(versions)
        
        if not versions:
            self.view.pause()
            return
        
        ver_num = self.view.get_input("Номер версии для восстановления")
        if ver_num.isdigit():
            if self.model.restore_version(int(ver_num)):
                self.view.show_message(f"Версия {ver_num} восстановлена", "success")
                self.view.show_content(self.model.get_content())
            else:
                self.view.show_message("Версия не найдена", "error")
        self.view.pause()
    
    def _show_stats(self) -> None:
        if not self.model.current_file:
            self.view.show_message("Файл не открыт", "warning")
            self.view.pause()
            return
        
        self.view.show_stats(self.model.get_stats())
        self.view.pause()
    
    def _exit(self) -> None:
        if self.model.is_modified:
            if self.view.confirm("Есть несохранённые изменения. Сохранить?"):
                self.model.save_file()
                self.view.show_message("Сохранено", "success")
        
        self.view.show_message("До свидания!", "info")
        self.running = False


def main():
    controller = EditorController()
    controller.run()


if __name__ == "__main__":
    main()
