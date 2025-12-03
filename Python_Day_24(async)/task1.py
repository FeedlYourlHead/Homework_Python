import asyncio

async def send_email(recipient, delay):
    print(f'Начинаю отправлять письмо получателю {recipient}')
    await asyncio.sleep(delay)
    print(f'Письмо получателю {recipient} отправлено')

async def main():
    users = [('Alice', 2), ('Bob', 3), ('Charlie', 1), ('Diana', 4)]
    tasks = [asyncio.create_task(send_email(*user)) for user in users]

    await asyncio.gather(*tasks)
    
if __name__ == '__main__':
    asyncio.run(main())
