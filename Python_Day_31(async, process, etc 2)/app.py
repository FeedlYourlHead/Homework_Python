"""
🚀 Космический шахтёр: Гонка за ресурсами
Главный файл приложения Flask
"""
from flask import Flask, render_template, jsonify, request
import threading
import time
import atexit

from game_engine.state import game_state
from game_engine.async_trader import async_trader
from game_engine.mines import mine_manager
from game_engine.heavy_tasks import heavy_task_manager

app = Flask(__name__)


# Фоновый поток для обработки результатов от процессов
def background_processor():
    """Обрабатывает результаты от multiprocessing"""
    while game_state.game_running:
        # Запрашиваем аналитику каждые 5 секунд
        state = game_state.get_state_snapshot()
        heavy_task_manager.request_analysis(state["planets"])
        heavy_task_manager.request_navigation(
            state["planets"],
            state["ship"]["location"]
        )

        # Обрабатываем пиратские атаки
        for event in game_state.active_events:
            if event["type"] == "pirate_attack":
                threat = event.get("data", {}).get("threat_level", 1)
                heavy_task_manager.request_battle(threat)
                game_state.clear_event("pirate_attack")

        # Получаем результаты
        results = heavy_task_manager.get_results()
        for result in results:
            if result["type"] == "navigation":
                game_state.analytics["best_route"] = result["result"]
            elif result["type"] == "analysis":
                game_state.analytics["price_predictions"] = result["predictions"]
            elif result["type"] == "battle":
                game_state.analytics["battle_result"] = result["result"]
                if result["result"]["victory"]:
                    game_state.add_credits(result["result"]["loot"])
                    game_state.stats["pirates_defeated"] += 1
                    game_state.add_event(
                        "battle_won",
                        f"⚔️ Пираты побеждены! Добыча: {result['result']['loot']} кредитов",
                        result["result"]
                    )
                else:
                    # Потеря ресурсов при поражении
                    loss = 100
                    game_state.remove_credits(loss)
                    game_state.add_event(
                        "battle_lost",
                        f"💀 Пираты победили! Потеряно: {loss} кредитов",
                        result["result"]
                    )

        time.sleep(2)


# ==================== Маршруты ====================

@app.route("/")
def index():
    """Главная страница"""
    return render_template("index.html")


@app.route("/api/state")
def get_state():
    """Получить текущее состояние игры"""
    return jsonify(game_state.get_state_snapshot())


@app.route("/api/fly", methods=["POST"])
def fly():
    """Отправить корабль к планете"""
    data = request.json
    destination = data.get("destination")
    result = async_trader.fly_to(destination)
    return jsonify(result)


@app.route("/api/buy", methods=["POST"])
def buy():
    """Купить ресурс"""
    data = request.json
    resource = data.get("resource")
    amount = int(data.get("amount", 1))
    result = async_trader.buy_resource(resource, amount)
    return jsonify(result)


@app.route("/api/sell", methods=["POST"])
def sell():
    """Продать ресурс"""
    data = request.json
    resource = data.get("resource")
    amount = int(data.get("amount", 1))
    result = async_trader.sell_resource(resource, amount)
    return jsonify(result)


@app.route("/api/load", methods=["POST"])
def load():
    """Загрузить ресурс со станции"""
    data = request.json
    resource = data.get("resource")
    amount = int(data.get("amount", 1))
    result = async_trader.load_from_station(resource, amount)
    return jsonify(result)


@app.route("/api/mine/start", methods=["POST"])
def start_mine():
    """Запустить шахту"""
    data = request.json
    mine_id = data.get("mine_id")
    result = mine_manager.start_mine(mine_id)
    return jsonify(result)


@app.route("/api/mine/stop", methods=["POST"])
def stop_mine():
    """Остановить шахту"""
    data = request.json
    mine_id = data.get("mine_id")
    result = mine_manager.stop_mine(mine_id)
    return jsonify(result)


@app.route("/api/mine/repair", methods=["POST"])
def repair_mine():
    """Отремонтировать шахту"""
    data = request.json
    mine_id = data.get("mine_id")
    result = mine_manager.repair_mine(mine_id)
    return jsonify(result)


@app.route("/api/mine/upgrade", methods=["POST"])
def upgrade_mine():
    """Улучшить шахту"""
    data = request.json
    mine_id = data.get("mine_id")
    result = mine_manager.upgrade_mine(mine_id)
    return jsonify(result)


@app.route("/api/reset", methods=["POST"])
def reset_game():
    """Перезапустить игру"""
    game_state.reset()
    return jsonify({"success": True, "message": "Игра перезапущена!"})


# ==================== Запуск ====================

def start_game_systems():
    """Запустить все игровые системы"""
    print("=" * 50)
    print("🚀 КОСМИЧЕСКИЙ ШАХТЁР: ГОНКА ЗА РЕСУРСАМИ")
    print("=" * 50)

    # Запускаем asyncio трейдер
    async_trader.start()

    # Запускаем потоки шахт
    mine_manager.start_all()

    # Запускаем процессы для тяжёлых задач
    heavy_task_manager.start_all()

    # Запускаем фоновый обработчик
    bg_thread = threading.Thread(target=background_processor, daemon=True)
    bg_thread.start()

    print("✅ Все системы запущены!")
    print("🌐 Откройте http://127.0.0.1:5000")
    print("=" * 50)


def stop_game_systems():
    """Остановить все игровые системы"""
    print("\n🛑 Остановка систем...")
    game_state.game_running = False
    async_trader.stop()
    mine_manager.stop_all()
    heavy_task_manager.stop_all()
    print("✅ Все системы остановлены!")


# Регистрируем очистку при выходе
atexit.register(stop_game_systems)

if __name__ == "__main__":
    start_game_systems()
    app.run(debug=False, threaded=True, port=5000)