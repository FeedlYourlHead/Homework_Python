from functools import wraps
import time
from datetime import datetime

def log_transaction(func):
    def wrapper(account_id, amount, transaction_type,   *args, **kwargs):
        result = func(account_id, amount,transaction_type, *args, **kwargs)
        print(f"[{datetime.now()}] Счет: {account_id}, Операция: {transaction_type}, Сумма: {amount}, Результат: {result['status']}, Сообщение: {result['message']}")
        return result
    return wrapper

def require_role(role):
    def decorator(func):
        def wrapper(account_id, amount, transaction_type, *args, **kwargs):
            if role == "client" and transaction_type == 'withdraw' and amount > 50000:
                return {
                    'status': 'error',
                    'message': 'Клиенты не могут снимать более 50000'
                }
            return func(account_id, amount, transaction_type, *args, **kwargs)
        return wrapper
    return decorator

operation_counts = {}
def limit(rate, period):
    def decorator(func):
        def wrapper(account_id, amount, transaction_type, *args, **kwargs):
            key = account_id
            current_time = time.time()
            
            if key not in operation_counts:
                operation_counts[key] = []


            operation_counts[key] = [t for t in operation_counts[key] if current_time - t < period]
            
            if len(operation_counts[key]) >= rate:
                return {'status': 'error', 'message': f'Лимит операций: не более {rate} за {period} сек.'}

            operation_counts[key].append(current_time)
            return func(account_id, amount, transaction_type)
        return wrapper
    return decorator

balance_cache = {}
def cache_balance(ttl):
    def decorator(func):
        def wrapper(account_id, amount, transaction_type, *args, **kwargs):
            key = account_id
            current_time = time.time()

            if key in balance_cache:
                cache_time, cached_result = balance_cache[key]
                if current_time - cache_time < ttl:
                    cached_result['from_cache'] = True
                    return cached_result

            result = func(account_id, amount, transaction_type, *args, **kwargs)
            balance_cache[key] = (current_time, result)
            return result
        return wrapper
    return decorator



@log_transaction
@require_role('client')
@limit(rate=3, period=10)
@cache_balance(ttl=5)
def process_transaction(account_id:int, amount:float, transaction_type:str):
    return {
        'status': "success", 
        'message': f'Операция {transaction_type} на сумму {amount} выполнена',
        'account_id': account_id,
        'amount': amount,
        'type': transaction_type
    }

def main():
    result1 = process_transaction(1993, 500000.0, 'withdraw')
    result2 = process_transaction(1992, 10000.0, 'withdraw')
    result3 = process_transaction(1992, 500000.0, 'deposit')
    print(f"Результат: {result3}")

if __name__ == "__main__":
    main()
