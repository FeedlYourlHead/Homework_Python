import jinja2
import sys
import os
from collections import Counter, deque
from utils import LogEntry, log_parser, timing,HEAVY_REQUEST

class LogAnalyzer:
    # для хранения времени анализа (устанавливается @timing)
    analysis_time = 0.0

    def __init__(self, file_path):
        self.file_path = file_path
        # контейнеры для сбора статистики
        self.url_counts = Counter() #по URL
        self.status_counts = Counter()#по HTTP статусу
        self.method_counts = Counter()#по методу

        self.total_requests = 0 #общее количество запросов
        self.total_bytes = 0 #общий объем данных

        self.heavy_requests = [] # ТОП 10 по размеру
        self.MAX_HEAVY_REQUESTS = 10 #макс кол-во тяжелых запросов

    @timing
    def analyze(self):
        print(f'Start analyzing')
        for entry in log_parser(self.file_path):
            self.total_requests += 1
            self.total_bytes += entry.size

            # обновляем счетчики
            self.url_counts[entry.url] += 1
            if entry.status_code != 0:
                self.status_counts[entry.status_code] += 1
            self.method_counts[entry.method] += 1

            # логика проверки для топ10 тяжелых запросов
            if entry.size > HEAVY_REQUEST:
                heavy_data={
                    'size': entry.size,
                    'request': entry.full_request,
                    'ip': entry.ip,
                    'status': entry.status_code
                }
                if len(self.heavy_requests) < self.MAX_HEAVY_REQUESTS:
                    self.heavy_requests.append(heavy_data)
                else:
                    min_size = min(req['size'] for req in self.heavy_requests)
                    if heavy_data['size'] > min_size:
                        min_index = next(i for i, req in enumerate(self.heavy_requests) if req['size'] == min_size)
                        self.heavy_requests[min_index] = heavy_data
        self.heavy_requests.sort(key=lambda x: x['size'], reverse=True)
        print('Finish analyzing')

    def generate_report(self, template_path, output_path='report.html'):
        template_dir = os.path.dirname(template_path)
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir or '.'))
        template = env.get_template(os.path.basename(template_path)) #загрузка шаблона

        #сводка по кодам статуса
        # status_counts = {'200': 100, '201': 130, '404': 500}
        status_summary = {
            '2xx': sum(c for status, c in self.status_counts.items() if 200<=status<=299),
            '3xx': sum(c for status, c in self.status_counts.items() if 300<=status<=399),
            '4xx': sum(c for status, c in self.status_counts.items() if 400<=status<=499),
            '5xx': sum(c for status, c in self.status_counts.items() if 500<=status<=599),
            'other': sum(c for status, c in self.status_counts.items() if status<200 or status > 599),
        }

        def format_bytes(bytes_value):
            if bytes_value < 1024:
                return f'{bytes_value} B'
            elif bytes_value < 1024*1024:
                return f'{bytes_value / 1024:.2f} KB'
            elif bytes_value < 1024*1024*1024:
                return f'{bytes_value / (1024*1024):.2f} MB'
            else:
                return f'{bytes_value / (1024*1024*1024):.2f} GB'

        template_data = {
            'analysis_time': f'{self.analysis_time:.4f} сек.',
            'total_requests': self.total_requests,
            'total_data': format_bytes(self.total_bytes),
            'top_10_urls': self.url_counts.most_common(10),
            'status_summary': status_summary,
            'heavy_list': self.heavy_requests,
            'format_bytes': format_bytes,
            'analyzer': self,
            'method_stats': self.method_counts.most_common()
        }
        rendered_template = template.render(template_data)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(rendered_template)

        print('Saved report')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('используется: python main.py <путь к access.log>')
        sys.exit(1)
    log_file_path = sys.argv[1]
    template_file_path = 'report_template.html'
    output_file_path = 'report.html'

    analyzer = LogAnalyzer(log_file_path)
    analyzer.analyze()

    if not os.path.exists(template_file_path):
        print('не найден файл шаблона')
        sys.exit(1)
    analyzer.generate_report(template_file_path, output_file_path)