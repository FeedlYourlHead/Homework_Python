from abc import ABC, abstractmethod

#Adaptees =================================================
class OldFileLogger:
    def log_to_file(self, message:str, level:str) -> None:
        print(f'{level}:{message}')

class ConsolePrinter:
    def print_message(self, data:dict) -> None:
        print(f'{data["level"]}: {data["message"]}')
# =================================================

#Target =================================================
class LoggerInterface(ABC):
    @abstractmethod
    def log(self, message:str, level:str):
        pass
# =================================================

#Adapters =================================================
class FileLoggerAdapter(LoggerInterface):
    def __init__(self, old_file_logger: OldFileLogger) -> None:
        self.old_file_logger = old_file_logger

    def log(self, message, level):
        return self.old_file_logger.log_to_file(message, level)

class ConsoleAdapter(LoggerInterface):
    def __init__(self, console_printer: ConsolePrinter) -> None:
        self.console_printer = console_printer

    def log(self, message, level):
        data = {
            "message": message,
            "level": level
        }
        return self.console_printer.print_message(data)
# =================================================

#main =================================================
def run_application_code(logger: LoggerInterface):
    logger.log('info message', 'INFO')
    logger.log('warning message', 'WARNING')
    logger.log('error message', 'ERROR')

# =================================================
if __name__ == "__main__":
    old_file = OldFileLogger()
    old_console = ConsolePrinter()
    file_adapter = FileLoggerAdapter(old_file)
    console_adapter = ConsoleAdapter(old_console)
    print('Тестирование file adapter')
    run_application_code(file_adapter)
    print()
    print('Тестирование console adapter')
    run_application_code(console_adapter)
