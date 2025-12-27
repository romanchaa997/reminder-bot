# reminder-bot

Telegram reminder bot with aiogram and SQLite. Create, manage and receive notifications for scheduled reminders.

## Features

- Create reminders via Telegram command
- List active reminders anytime
- Automatic notifications at scheduled time
- SQLite database for persistence
- Fast & lightweight with minimal dependencies
- Easy to customize and extend

## Quick Start

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Clone the repository:
```bash
git clone https://github.com/romanchaa997/reminder-bot.git
cd reminder-bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Get your Telegram bot token from BotFather (@BotFather on Telegram)

4. Update config.py:
```python
BOT_TOKEN = "your_token_here"
```

5. Run the bot:
```bash
python main.py
```

## Usage

### Commands

**/start** - Get help and instructions

**/add YYYY-MM-DD HH:MM reminder text** - Create a new reminder

Example:
```
/add 2025-12-28 15:00 call client
/add 2025-12-28 09:30 send report
```

**/list** - Show all active reminders

## Tech Stack

- aiogram 3 - Async Telegram Bot API framework
- apscheduler - Task scheduler for reminders
- SQLite3 - Lightweight database
