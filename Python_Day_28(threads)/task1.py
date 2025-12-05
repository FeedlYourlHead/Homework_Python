import time
import threading

def send_notification(user, delay):
    print(f"Начинаю отправку уведомления для {user}...")
    time.sleep(delay)
    print(f'Уведомление для {user} отправлено!')

if __name__ == '__main__':
    users = [('Alice', 2), ('Bob', 3), ('Charlie', 1), ('Diana', 4)]
    threads = []
    for user in users:
        t = threading.Thread(target=send_notification, args=user)
        threads.append(t)
        t.start()
    for t in threads:
        t.join()


