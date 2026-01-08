/**
 * 🚀 Космический Шахтёр - Клиентский JavaScript
 */

// Глобальное состояние
let gameState = null;
let updateInterval = null;

// Иконки ресурсов
const resourceIcons = {
    iron: '🔩',
    gold: '🥇',
    crystal: '💎',
    uranium: '☢️'
};

// Иконки планет
const planetIcons = {
    Mars: '🔴',
    Venus: '🟡',
    Europa: '🔵',
    Titan: '🟤'
};

// ==================== Инициализация ====================

document.addEventListener('DOMContentLoaded', () => {
    startGame();
});

function startGame() {
    updateGameState();
    updateInterval = setInterval(updateGameState, 500);
}

// ==================== Обновление состояния ====================

async function updateGameState() {
    try {
        const response = await fetch('/api/state');
        gameState = await response.json();
        renderGame();
    } catch (error) {
        console.error('Ошибка получения состояния:', error);
    }
}

function renderGame() {
    if (!gameState) return;

    renderHeader();
    renderStationResources();
    renderMines();
    renderShip();
    renderPlanets();
    renderAnalytics();
    renderEvents();
    renderStats();
}

// ==================== Рендеринг компонентов ====================

function renderHeader() {
    document.getElementById('credits').textContent =
        gameState.credits.toLocaleString();
    document.getElementById('game-time').textContent =
        Math.floor(gameState.game_time);
}

function renderStationResources() {
    const container = document.getElementById('station-resources');
    container.innerHTML = '';

    for (const [resource, amount] of Object.entries(gameState.resources)) {
        const div = document.createElement('div');
        div.className = 'resource-item';
        div.innerHTML = `
            <span class="resource-icon">${resourceIcons[resource] || '📦'}</span>
            <span class="resource-amount">${amount}</span>
            <span class="resource-name">${resource}</span>
        `;

        // Клик для загрузки на корабль
        div.onclick = () => {
            if (gameState.ship.location === 'station' && !gameState.ship.is_flying) {
                showLoadModal(resource, amount);
            }
        };
        div.style.cursor = 'pointer';

        container.appendChild(div);
    }
}

function renderMines() {
    const container = document.getElementById('mines-list');
    container.innerHTML = '';

    for (const [mineId, mine] of Object.entries(gameState.mines)) {
        const div = document.createElement('div');
        div.className = `mine-card ${mine.is_working ? 'working' : ''} ${mine.is_broken ? 'broken' : ''}`;

        let statusClass = 'stopped';
        let statusText = 'Остановлена';
        if (mine.is_broken) {
            statusClass = 'broken';
            statusText = 'Сломана';
        } else if (mine.is_working) {
            statusClass = 'working';
            statusText = 'Работает';
        }

        div.innerHTML = `
            <div class="mine-header">
                <span class="mine-name">⛏️ ${mine.name}</span>
                <span class="mine-status ${statusClass}">${statusText}</span>
            </div>
            <div class="mine-stats">
                Уровень: ${mine.level} | Добыто: ${mine.total_mined}
            </div>
            <div class="mine-actions">
                ${mine.is_broken ?
                    `<button class="btn btn-warning" onclick="repairMine('${mineId}')">🔧 Ремонт</button>` :
                    mine.is_working ?
                        `<button class="btn btn-danger" onclick="stopMine('${mineId}')">⏹️ Стоп</button>` :
                        `<button class="btn btn-success" onclick="startMine('${mineId}')">▶️ Старт</button>`
                }
                ${!mine.is_broken && mine.level < 5 ?
                    `<button class="btn btn-primary" onclick="upgradeMine('${mineId}')">⬆️ Улучшить</button>` :
                    ''}
            </div>
        `;

        container.appendChild(div);
    }
}

function renderShip() {
    const shipInfo = document.getElementById('ship-info');
    const cargoInfo = document.getElementById('cargo-info');
    const ship = gameState.ship;

    let locationText = ship.location === 'station' ?
        '🏭 На станции' :
        `${planetIcons[ship.location] || '🪐'} ${ship.location}`;

    let flightHtml = '';
    if (ship.is_flying) {
        const progress = Math.round(ship.flight_progress * 100);
        flightHtml = `
            <div>✈️ Летим к: ${ship.destination}</div>
            <div class="flight-progress">
                <div class="flight-progress-bar" style="width: ${progress}%"></div>
            </div>
            <div style="text-align: center">${progress}%</div>
        `;
    }

    shipInfo.innerHTML = `
        <div class="ship-location">${locationText}</div>
        ${flightHtml}
    `;

    // Cargo
    const cargoPercent = (ship.cargo_total / ship.cargo_capacity * 100);
    let cargoItems = '';
    for (const [res, amount] of Object.entries(ship.cargo)) {
        cargoItems += `<span>${resourceIcons[res] || '📦'} ${amount}</span> `;
    }

    cargoInfo.innerHTML = `
        <div>📦 Трюм: ${ship.cargo_total}/${ship.cargo_capacity}</div>
        <div class="cargo-bar">
            <div class="cargo-fill" style="width: ${cargoPercent}%"></div>
        </div>
        <div>${cargoItems || 'Пусто'}</div>
    `;
}

function renderPlanets() {
    const container = document.getElementById('planets-grid');
    container.innerHTML = '';

    for (const [name, planet] of Object.entries(gameState.planets)) {
        const priceChange = planet.current_price - planet.base_price;
        const priceClass = priceChange > 0 ? 'price-up' : priceChange < 0 ? 'price-down' : '';
        const priceSign = priceChange > 0 ? '+' : '';

        const isCurrent = gameState.ship.location === name;

        const div = document.createElement('div');
        div.className = `planet-card ${isCurrent ? 'current' : ''}`;
        div.innerHTML = `
            <div class="planet-name">${planetIcons[name] || '🪐'} ${name}</div>
            <div class="planet-resource">${resourceIcons[planet.resource] || '📦'} ${planet.resource}</div>
            <div class="planet-price ${priceClass}">
                💰 ${planet.current_price.toFixed(1)}
                <small>(${priceSign}${((priceChange/planet.base_price)*100).toFixed(0)}%)</small>
            </div>
            <div class="planet-distance">🚀 ${planet.distance}с полёта</div>
        `;

        div.onclick = () => handlePlanetClick(name, planet);

        container.appendChild(div);
    }
}

function renderAnalytics() {
    // Навигация
    const navInfo = document.getElementById('navigation-info');
    const route = gameState.analytics.best_route;
    if (route && route.route) {
        navInfo.innerHTML = route.route.map(r => `
            <div class="route-item">
                ${planetIcons[r.planet] || '🪐'} ${r.planet}:
                <strong>${r.action === 'buy' ? '🛒 Покупать' : '💰 Продавать'}</strong>
            </div>
        `).join('') + `<div>💵 Потенциал: ~${Math.round(route.estimated_profit)}</div>`;
    } else {
        navInfo.innerHTML = '⏳ Расчёт маршрута...';
    }

    // Предсказания
    const predInfo = document.getElementById('predictions-info');
    const predictions = gameState.analytics.price_predictions;
    if (predictions && Object.keys(predictions).length > 0) {
        predInfo.innerHTML = Object.entries(predictions).map(([planet, pred]) => {
            const trendIcon = pred.trend === 'up' ? '📈' : pred.trend === 'down' ? '📉' : '➡️';
            const trendClass = `trend-${pred.trend}`;
            return `
                <div class="prediction-item">
                    <span>${planetIcons[planet] || '🪐'} ${planet}</span>
                    <span class="${trendClass}">${trendIcon} ${pred.recommendation}</span>
                </div>
            `;
        }).join('');
    } else {
        predInfo.innerHTML = '⏳ Анализ данных...';
    }

    // Бой
    const battleInfo = document.getElementById('battle-info');
    const battle = gameState.analytics.battle_result;
    if (battle) {
        battleInfo.innerHTML = `
            <div>${battle.victory ? '🎉 Победа!' : '💀 Поражение'}</div>
            <div>Раундов: ${battle.rounds?.length || 0}</div>
            <div>HP: ${battle.final_player_hp}</div>
            ${battle.victory ? `<div>Добыча: ${battle.loot} 💰</div>` : ''}
        `;
    } else {
        battleInfo.innerHTML = '⚔️ Нет данных о бое';
    }
}

function renderEvents() {
    const container = document.getElementById('events-log');
    const events = gameState.event_log.slice().reverse();

    container.innerHTML = events.map(event => {
        let eventClass = '';
        if (event.type.includes('attack') || event.type.includes('broken')) {
            eventClass = 'danger';
        } else if (event.type.includes('warning') || event.type.includes('meteor') || event.type.includes('flare')) {
            eventClass = 'warning';
        } else if (event.type.includes('bonus') || event.type.includes('won') || event.type.includes('repaired')) {
            eventClass = 'success';
        }

        return `<div class="event-item ${eventClass}">${event.message}</div>`;
    }).join('');
}

function renderStats() {
    const container = document.getElementById('stats');
    const stats = gameState.stats;

    container.innerHTML = `
        <div class="stat-item">
            <div class="stat-value">${stats.total_trades}</div>
            <div class="stat-label">Сделок</div>
        </div>
        <div class="stat-item">
            <div class="stat-value">${stats.total_mined}</div>
            <div class="stat-label">Добыто</div>
        </div>
        <div class="stat-item">
            <div class="stat-value">${stats.pirates_defeated}</div>
            <div class="stat-label">Пиратов</div>
        </div>
        <div class="stat-item">
            <div class="stat-value">${stats.events_survived}</div>
            <div class="stat-label">Событий</div>
        </div>
    `;
}

// ==================== Действия ====================

async function handlePlanetClick(planetName, planet) {
    const ship = gameState.ship;

    if (ship.is_flying) {
        showNotification('Корабль в полёте!', 'warning');
        return;
    }

    if (ship.location === planetName) {
        // Уже на планете - показать торговлю
        showTradeModal(planetName, planet);
    } else {
        // Лететь к планете
        await flyTo(planetName);
    }
}

async function flyTo(destination) {
    try {
        const response = await fetch('/api/fly', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ destination })
        });
        const result = await response.json();
        showNotification(result.message, result.success ? 'success' : 'error');
    } catch (error) {
        showNotification('Ошибка полёта!', 'error');
    }
}

async function flyToStation() {
    await flyTo('station');
}

// Шахты
async function startMine(mineId) {
    await mineAction('start', mineId);
}

async function stopMine(mineId) {
    await mineAction('stop', mineId);
}

async function repairMine(mineId) {
    await mineAction('repair', mineId);
}

async function upgradeMine(mineId) {
    await mineAction('upgrade', mineId);
}

async function mineAction(action, mineId) {
    try {
        const response = await fetch(`/api/mine/${action}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ mine_id: mineId })
        });
        const result = await response.json();
        showNotification(result.message, result.success ? 'success' : 'error');
    } catch (error) {
        showNotification('Ошибка!', 'error');
    }
}

// Торговля
function showTradeModal(planetName, planet) {
    const modal = document.getElementById('trade-modal');
    const title = document.getElementById('modal-title');
    const body = document.getElementById('modal-body');

    title.textContent = `🪐 ${planetName} - ${planet.resource}`;

    body.innerHTML = `
        <div class="trade-form">
            <div>
                <strong>Текущая цена:</strong> ${planet.current_price.toFixed(2)} кредитов
            </div>
            <div class="trade-input">
                <label>Количество:</label>
                <input type="number" id="trade-amount" value="10" min="1" max="100">
            </div>
            <div class="trade-buttons">
                <button class="btn btn-success" onclick="buyResource('${planet.resource}')">
                    🛒 Купить
                </button>
                <button class="btn btn-warning" onclick="sellResource('${planet.resource}')">
                    💰 Продать
                </button>
            </div>
            <div style="margin-top: 15px;">
                <strong>В трюме:</strong>
                ${Object.entries(gameState.ship.cargo).map(([r, a]) =>
                    `${resourceIcons[r]} ${a}`
                ).join(', ') || 'Пусто'}
            </div>
        </div>
    `;

    modal.classList.remove('hidden');
}

function showLoadModal(resource, available) {
    const modal = document.getElementById('trade-modal');
    const title = document.getElementById('modal-title');
    const body = document.getElementById('modal-body');

    title.textContent = `📦 Загрузить ${resource}`;

    body.innerHTML = `
        <div class="trade-form">
            <div>
                <strong>На складе:</strong> ${available}
            </div>
            <div class="trade-input">
                <label>Количество:</label>
                <input type="number" id="trade-amount" value="${Math.min(10, available)}" min="1" max="${available}">
            </div>
            <div class="trade-buttons">
                <button class="btn btn-primary" onclick="loadResource('${resource}')">
                    📦 Загрузить в трюм
                </button>
            </div>
        </div>
    `;

    modal.classList.remove('hidden');
}

async function buyResource(resource) {
    const amount = parseInt(document.getElementById('trade-amount').value);
    try {
        const response = await fetch('/api/buy', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ resource, amount })
        });
        const result = await response.json();
        showNotification(result.message, result.success ? 'success' : 'error');
        if (result.success) closeModal();
    } catch (error) {
        showNotification('Ошибка покупки!', 'error');
    }
}

async function sellResource(resource) {
    const amount = parseInt(document.getElementById('trade-amount').value);
    try {
        const response = await fetch('/api/sell', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ resource, amount })
        });
        const result = await response.json();
        showNotification(result.message, result.success ? 'success' : 'error');
        if (result.success) closeModal();
    } catch (error) {
        showNotification('Ошибка продажи!', 'error');
    }
}

async function loadResource(resource) {
    const amount = parseInt(document.getElementById('trade-amount').value);
    try {
        const response = await fetch('/api/load', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ resource, amount })
        });
        const result = await response.json();
        showNotification(result.message, result.success ? 'success' : 'error');
        if (result.success) closeModal();
    } catch (error) {
        showNotification('Ошибка загрузки!', 'error');
    }
}

function closeModal() {
    document.getElementById('trade-modal').classList.add('hidden');
}

async function resetGame() {
    if (confirm('Начать новую игру?')) {
        try {
            await fetch('/api/reset', { method: 'POST' });
            showNotification('Игра перезапущена!', 'success');
        } catch (error) {
            showNotification('Ошибка!', 'error');
        }
    }
}

// ==================== Утилиты ====================

function showNotification(message, type = 'info') {
    // Простое уведомление через alert (можно заменить на toast)
    console.log(`[${type}] ${message}`);

    // Добавляем в лог событий визуально
    const eventsLog = document.getElementById('events-log');
    const div = document.createElement('div');
    div.className = `event-item ${type === 'error' ? 'danger' : type === 'warning' ? 'warning' : 'success'}`;
    div.textContent = message;
    eventsLog.insertBefore(div, eventsLog.firstChild);
}

// Закрытие модального окна по клику вне его
document.getElementById('trade-modal').addEventListener('click', (e) => {
    if (e.target.id === 'trade-modal') {
        closeModal();
    }
});