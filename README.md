# MonsterChecker Bot

MonsterChecker is a web crawler that monitors the Monster Energy rewards page to check the availability of specific products. When a monitored product becomes available, the bot sends a notification via Discord and Telegram. Additionally, the bot performs periodic alive checks to ensure it is still running.

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Features](#features)
- [SQL Database](#sql-database)
- [Security Notice](#security-notice)
- [License](#license)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://https://github.com/Felix-From/Monster-Reward-Checker.git
   cd Monster-Reward-Checker
   ```

2. **Install dependencies**:
   Make sure you have Python and pip installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the database**:
   Create a MySQL database and import the SQL template:
   ```sql
   CREATE DATABASE MonsterChecker;
   USE MonsterChecker;
   SOURCE MonsterChecker.sql;
   ```

4. **Configure the MySQL connection**:
   Update the `DB_HOST`, `DB_USER`, `DB_PSSWRD`, and `DB_NAME` variables in the `MonsterTimer.py` file to match your MySQL configuration.

## Configuration

The bot uses a MySQL database to store settings and the list of products to monitor. These settings include:

- **Discord Webhook URL**: The URL for the Discord webhook to send messages.
- **Discord UserID Mentions**: The user IDs to mention when a product becomes available.
- **Telegram Token**: The API token for the Telegram bot.
- **Telegram Chat IDs**: The IDs of the Telegram chats where notifications should be sent.
- **Products**: The list of products to monitor.
- **Alive Check Interval**: The interval at which alive checks are performed.
- **Sleep Time Between Checks**: The duration between each product availability check.

## Usage

Start the bot with the following command:
```bash
python MonsterTimer.py
```

The bot will monitor the Monster Energy rewards page and send notifications via Discord and Telegram when a specified product is available. Additionally, the bot will perform regular alive checks and post updates to the specified channels.

## Features

- **Product Availability Monitoring**: The bot scans the website for specified products and sends a message when they are available.
- **Notification System**: Sends notifications to predefined Discord and Telegram channels.
- **Alive Check**: The bot regularly checks in to ensure it is still active.

## SQL Database

The SQL database stores all the settings and product lists used by the bot. The structure of the `Settings` table is as follows:

```sql
CREATE TABLE `Settings` (
  `id` int(11) NOT NULL COMMENT '#Used for Updating :D',
  `discord_webhook_url` text NOT NULL COMMENT 'Webhook URL',
  `discord_userID_mention` varchar(1024) NOT NULL COMMENT 'Discord UserID, if more than one then separate with ",".',
  `telegram_token` text NOT NULL COMMENT 'Telegram Token',
  `telegram_chats_id` text NOT NULL COMMENT 'Telegram Chat ID, if more than one then separate with ",".',
  `telegram_owner_id` varchar(64) NOT NULL COMMENT 'Telegram Chat ID Owner (Start Message)',
  `produkte` longtext NOT NULL COMMENT 'Products, if more than one then separate with ",".',
  `time_for_is_alive` int(11) NOT NULL COMMENT 'Amount of Checks till Alive Msg',
  `time_to_sleep` int(11) NOT NULL COMMENT 'Time in Sec. between Checks.'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
```
