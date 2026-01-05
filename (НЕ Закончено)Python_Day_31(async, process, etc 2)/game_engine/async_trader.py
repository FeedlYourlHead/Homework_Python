import asyncio
import random
import threading
import time
from typing import Optional
from .state import game_state, EventType

class AsyncTrader:
    def __init__(self):
        self.loop: Optional[asyncio.AbstractEventLoop] = None
        self.thread: Optional[threading.Thread] = None
        self.running = False
        self._tasks = []

    def start(self):
        if self.running:
            return

        self.running = True
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()
        print("AsyncTrader запущен")

    def stop(self):
        self.running = False
        if self.loop:
            self.loop.call_soon_threadsafe(self.loop.stop)

    def _run_loop(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        try:
            self.loop.run_until_complete(self._main())
        except Exception as e:
            print(f'AsyncTrader ошибка: {e}')
        finally:
            self.loop.close()

    async def _main(self):

        tasks = [
            asyncio.create_task(self._price_updater()),
            asyncio.create_task(self._event_generator()),
            asyncio.create_task(self._flight_manager())
        ]
        self._tasks = tasks

        while self.running and game_state.game_running:
            await asyncio.sleep(0.1)

        for task in tasks:
            task.cancel()

    async def _price_updater(self):
        while self.running:
            await asyncio.sleep(3)

            for planet in game_state.planets.values():
                variation = random.uniform(-0.3, 0.3)
                planet.current_price = planet.base_price * (1 + variation)

            game_state.add_event(
                'price_update',
                'Цены на рынках обновились!',
                {'time': time.time()}
            )

    async def _event_generator(self):
        while self.running:
            await asyncio.sleep(random.uniform(10, 20))

            event = random.choice([
                EventType.METEOR_SHOWER,
                EventType.SOLAR_FLARE,
                EventType.PIRATE_ATTACK,
                EventType.TRADE_BONUS
            ])

            await self._handle_event(event)

    async def _handle_event(self, event: EventType):

        if event == EventType.METEOR_SHOWER:
            damage = random.randint(1, 3)
            for mine in list(game_state.mines.values())[:damage]:
                if random.random() < 0.3:
                    mine.is_broken = True
            game_state.add_event(
                'meteor_shower',
                'Метеоритный дождь! Проверьте шахты',
                {'damage_chance': damage}
            )
            game_state.stats['events_survived'] += 1

        elif event == EventType.SOLAR_FLARE:
            game_state.add_event(
                'solar_flare',
                "Солнечная вспышка! Связь нестабильна!",
                {'duration': 5}
            )
            await asyncio.sleep(5)
            game_state.clear_event('solar_flare')
            game_state.stats['events_survived'] += 1

        elif event == EventType.PIRATE_ATTACK:
            game_state.add_event(
                'pirate_attack',
                'Пиратская атака! Активирована защита',
                {'threat_level': random.randint(1, 5)}
            )

        elif event == EventType.TRADE_BONUS:
            bonus = random.randint(50, 200)
            game_state.add_credits(bonus)
            game_state.add_event(
                'trade_bonus',
                f'Торговый бонус! Получено {bonus} кредитов!',
                {'bonus': bonus}
            )

    async def _flight_manager(self):
        while self.running:
            await asyncio.sleep(0.1)

            ship = game_state.ship
            if ship.is_flying and ship.destination:
                ship.flight_progress += 0.1 / ship.flight_duration









