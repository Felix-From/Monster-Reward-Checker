
# MonsterChecker Bot

MonsterChecker ist ein Webcrawler, der die Rewards-Seite von Monster Energy überwacht, um festzustellen, ob bestimmte Produkte verfügbar sind. Wenn eines der gesuchten Produkte verfügbar ist, sendet der Bot eine Benachrichtigung über Discord und Telegram. Der Bot führt außerdem regelmäßige Alive-Checks durch, um sicherzustellen, dass er weiterhin aktiv ist.

## Inhaltsverzeichnis

- [Installation](#installation)
- [Konfiguration](#konfiguration)
- [Verwendung](#verwendung)
- [Features](#features)
- [SQL Datenbank](#sql-datenbank)
- [Sicherheitshinweis](#sicherheitshinweis)
- [Lizenz](#lizenz)

## Installation

1. **Repository klonen**:
   ```bash
   git clone https://https://github.com/Felix-From/Monster-Reward-Checker.git
   cd Monster-Reward-Checker
   ```

2. **Abhängigkeiten installieren**:
   Stelle sicher, dass Python und pip installiert sind, und führe dann folgendes Kommando aus:
   ```bash
   pip install -r requirements.txt
   ```

3. **Datenbank einrichten**:
   Erstelle eine MySQL-Datenbank und importiere die SQL-Vorlage:
   ```sql
   CREATE DATABASE MonsterChecker;
   USE MonsterChecker;
   SOURCE MonsterChecker.sql;
   ```

4. **Konfiguriere die Verbindung zur MySQL-Datenbank**:
   Aktualisiere die Variablen `DB_HOST`, `DB_USER`, `DB_PSSWRD` und `DB_NAME` in der Datei `MonsterTimer.py` entsprechend deiner MySQL-Konfiguration.

## Konfiguration

Der Bot verwendet eine MySQL-Datenbank, um Einstellungen und zu überwachende Produkte zu speichern. Diese Einstellungen umfassen:

- **Discord Webhook URL**: Die URL für den Discord-Webhook, um Nachrichten zu senden.
- **Discord UserID Mention**: Die Benutzer-IDs, die bei Produktverfügbarkeit erwähnt werden sollen.
- **Telegram Token**: Der API-Token für den Telegram-Bot.
- **Telegram Chats ID**: Die IDs der Telegram-Chats, in denen Benachrichtigungen gesendet werden.
- **Produkte**: Die Liste der zu überwachenden Produkte.
- **Alive Check Interval**: Das Intervall, nach dem Alive-Checks durchgeführt werden. Bemessen an Anzahl der Verfügbarkeitsprüfungen.
- **Schlafzeit zwischen den Checks**: Die Zeitspanne zwischen den einzelnen Verfügbarkeitsprüfungen.

## Verwendung

Starte den Bot mit dem folgenden Befehl:
```bash
python MonsterTimer.py
```

Der Bot wird die Monster Energy Rewards-Seite überwachen und bei Verfügbarkeit der angegebenen Produkte Benachrichtigungen über Discord und Telegram versenden. Zusätzlich wird der Alive-Check regelmäßig durchgeführt und in den angegebenen Kanälen gepostet.

## Features

- **Produktverfügbarkeit prüfen**: Der Bot durchsucht die Webseite nach bestimmten Produkten und sendet eine Nachricht, sobald diese verfügbar sind.
- **Benachrichtigungssystem**: Versendet Benachrichtigungen an vordefinierte Discord- und Telegram-Kanäle.
- **Alive-Check**: Der Bot meldet sich regelmäßig, um sicherzustellen, dass er aktiv ist.

## SQL Datenbank

Die SQL-Datenbank speichert alle Einstellungen und Produktlisten, die der Bot verwendet. Die Struktur der Tabelle `Settings` ist wie folgt:

```sql
CREATE TABLE `Settings` (
  `id` int(11) NOT NULL COMMENT '#Used for Updating :D',
  `discord_webhook_url` text NOT NULL COMMENT 'Webhook URL',
  `discord_userID_mention` varchar(1024) NOT NULL COMMENT 'Discord UserID, if more than one then seperate with "," comma.',
  `telegram_token` text NOT NULL COMMENT 'Telegram Token',
  `telegram_chats_id` text NOT NULL COMMENT 'Telegram ChatID, if more than one then seperate with "," comma.',
  `telegram_owner_id` varchar(64) NOT NULL COMMENT 'Telegram ChatID Owner (Start Message)',
  `produkte` longtext NOT NULL COMMENT 'Products, if more than one then seperate with "," comma.',
  `time_for_is_alive` int(11) NOT NULL COMMENT 'Ammount of Check till Alive Msg',
  `time_to_sleep` int(11) NOT NULL COMMENT 'Time in Sec. between Checks.'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
```