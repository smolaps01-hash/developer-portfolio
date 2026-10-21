# Telegram Lead Bot

Демонстрационный бот собирает имя, телефон и комментарий, нормализует номер и сохраняет заявку в SQLite.

## Запуск

Из корня репозитория:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
pip install -r telegram_lead_bot/requirements.txt
$env:BOT_TOKEN="token-from-botfather"
python -m telegram_lead_bot.bot
```

Linux/macOS:

```bash
source .venv/bin/activate
pip install -r telegram_lead_bot/requirements.txt
export BOT_TOKEN="token-from-botfather"
python -m telegram_lead_bot.bot
```

## Важно

- Токен запрещено сохранять в коде, скриншотах или коммитах.
- Файл `leads.db` содержит персональные данные: не публикуйте его.
- Для непрерывной работы нужен отдельный сервер или хостинг; локальный запуск прекращается вместе с компьютером.
- Перед реальной эксплуатацией нужно определить срок хранения заявок и круг людей с доступом к базе.

