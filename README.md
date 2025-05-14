# Helldivers 2 Data Pipeline

**Automated, production-ready backend pipeline for fetching, transforming, and storing Helldivers 2 game data from the public API into a local MySQL database.**

![Helldivers 2](https://helldiverstrainingmanual.com/images/logo.png)

---

## 🚀 Overview

This project provides a robust, testable, and schedulable data pipeline for the [Helldivers 2 API](https://helldiverstrainingmanual.com/api). It fetches live game data (planets, war status, news, campaigns, major orders, and planet history), transforms it, and stores it in a normalized MySQL database for analytics, dashboards, or archival.

- **Automated daily updates** (or custom interval)
- **Modular, testable architecture**
- **Configurable via environment or file**
- **Comprehensive logging**
- **Easy to extend for new data types**
- **Production-ready: lockfile, error handling, and CLI/daemon modes**

---

## 📦 Features

- **API Client:** Robust Python client for all Helldivers 2 API endpoints, with error handling and retries.
- **Database Layer:** Efficient MySQL access with connection pooling and upsert logic.
- **Transformers:** Modular data normalization for each entity.
- **Fetchers:** Pluggable fetch/store logic for each data type.
- **Orchestrator:** End-to-end update runner with error handling and summary logging.
- **CLI & Scheduler:** Flexible command-line interface with daemon mode and lockfile safety.
- **Config & Logging:** Centralized, environment-driven, with rotating logs.
- **Testing:** Comprehensive test scripts for all major modules.

---

## 🏗️ Architecture

```
+-------------------+      +-------------------+      +-------------------+
| Helldivers 2 API  | ---> |   Transformers    | ---> |    MySQL DB       |
+-------------------+      +-------------------+      +-------------------+
         |                        |                           ^
         v                        v                           |
+-------------------+      +-------------------+      +-------------------+
|   API Client      | ---> |    Fetchers       | ---> |  Database Manager |
+-------------------+      +-------------------+      +-------------------+
         |                        |                           ^
         v                        v                           |
+------------------------------------------------------------+
|                  Update Orchestrator & CLI                 |
+------------------------------------------------------------+
```

---

## ⚡ Quickstart

### 1. Clone & Install

```bash
git clone https://github.com/YOUR_USERNAME/helldivers2-pipeline.git
cd helldivers2-pipeline
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Set Up MySQL

- Install MySQL (e.g., via Homebrew: `brew install mysql`)
- Start MySQL: `brew services start mysql`
- Create a database and user (see below)
- Run the migration:

```bash
mysql -u root -p < migrations/001_create_schema.sql
```

### 3. Configure

Create a `.env` file or edit `config.yaml` (see `src/config.py` for options):

```env
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=youruser
MYSQL_PASSWORD=yourpassword
MYSQL_DATABASE=helldivers2
LOG_LEVEL=INFO
UPDATE_INTERVAL_HOURS=24
```

### 4. Run a Full Update

```bash
python src/main.py --update
```

### 5. Run as a Daemon (Daily Updates)

```bash
python src/main.py --daemon --interval 24
```

### 6. Run Individual Fetchers

```bash
python src/main.py --update-planets
python src/main.py --update-war-status
# ...etc
```

---

## 🛠️ Project Structure

```
src/
  helldivers_api_client.py      # API client for all endpoints
  database_manager.py           # MySQL access layer
  config.py                     # Config and logging
  transformers/                 # Data transformers (one per entity)
  war_status_fetcher.py         # Fetch/store logic for war status
  planet_fetcher.py             # Fetch/store logic for planets
  news_fetcher.py               # Fetch/store logic for news
  campaign_fetcher.py           # Fetch/store logic for campaigns
  major_orders_fetcher.py       # Fetch/store logic for major orders
  planet_history_fetcher.py     # Fetch/store logic for planet history
  update_orchestrator.py        # Orchestrates full update
  main.py                       # CLI entrypoint
migrations/
  001_create_schema.sql         # MySQL schema
  002_update_news_table.sql     # News table migration
  003_rebuild_war_status_and_planet_status.sql  # Migration for war_status and planet_status tables
scripts/
  prd.txt                       # Product Requirements Document
  wipe_db.py                    # Script to wipe the database for a fresh pull
tests/
  test_*.py                     # Test scripts for all major modules
```

---

## 🧪 Testing

Run all tests:

```bash
pytest tests/
```

Or run individual test scripts:

```bash
python tests/test_helldivers_api_client.py
python tests/test_database_manager.py
# ...etc
```

### ⚠️ Test Database Safety & Cleanup

- **All tests must use a dedicated test database** (e.g., `helldivers2_test`).
- **Never run tests with production credentials or against the production database.**
- **Safety check:** All test scripts will abort if the database name does not end with `_test`.
- **Automatic cleanup:** Test scripts automatically clean up all test data before and after each run using a shared utility (`test_utils.py`).
- This ensures no sample or mock data ever pollutes production, and test runs are always isolated and repeatable.

---

## 📝 Configuration

- **Environment variables**: `.env` file in project root (recommended for secrets)
- **Config file**: `config.yaml` (optional, for non-secret settings)
- **Logging**: Rotating file and console logging, level set via config

---

## 🔒 Safety & Reliability

- **Lockfile**: Prevents overlapping runs (`/tmp/helldivers2_pipeline.lock`)
- **Error Handling**: All fetchers and orchestrator log and handle errors gracefully
- **Retry Logic**: API client retries on transient failures
- **Daemon Mode**: Safe, interval-based scheduling

---

## 📈 Extending

- Add new data types: Create a new transformer and fetcher, register in the orchestrator.
- Add new endpoints: Extend the API client and corresponding fetcher/transformer.
- Add analytics: Query the MySQL database directly or build a dashboard.

---

## 🤝 Contributing

Pull requests are welcome! Please open an issue to discuss major changes.  
All code should be tested and follow project conventions.

---

## 📚 References

- [Helldivers 2 API Docs](https://helldiverstrainingmanual.com/api)
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [Python Requests](https://docs.python-requests.org/)
- [Task Master AI](https://github.com/your-org/task-master-ai) (for project management)

---

## 🏅 Credits

- **Project Lead:** [Your Name](https://github.com/YOUR_USERNAME)
- **Contributors:** See [GitHub contributors](https://github.com/YOUR_USERNAME/helldivers2-pipeline/graphs/contributors)
- **Inspired by:** The Helldivers 2 community

---

## 🛡️ License

MIT License. See [LICENSE](LICENSE) for details.

---

## 🧹 Wiping the Database for a Fresh Pull

To completely remove all data (but keep the schema) from your database, use the provided wipe script:

```bash
python scripts/wipe_db.py --force
```

- **Purpose:** Truncates all tables, leaving the schema intact so you can perform a fresh pull from the Helldivers 2 API.
- **Safety:** By default, the script will not run unless you provide the `--force` flag. Running without it will print a warning and exit.
- **Config:** Uses the same environment variables or config as the rest of the project to determine which database to wipe.
- **Warning:** This operation is irreversible! Make sure you are targeting the correct database (test or production) before running with `--force`.

Example:

```bash
# Dry run (shows warning, does nothing)
python scripts/wipe_db.py

# Actually wipe all data
python scripts/wipe_db.py --force
```

---

## 🛠️ CLI Usage

Run the CLI tool:

```bash
python src/main.py [OPTIONS]
```

### Common Options

- `--config <file>`: Path to config file
- `--update`: Run a full data update
- `--update-war-status`: Update war status only
- `--update-planets`: Update planets only
- `--update-news`: Update news only
- `--update-campaign`: Update campaign only
- `--update-major-orders`: Update major orders only
- `--update-planet-history`: Update planet history only
- `--daemon`: Run as a daemon with scheduled updates
- `--interval <hours>`: Update interval in hours (default: 24, used with `--daemon`)
- `--wipe-db`: WIPE ALL DATA from the database (schema preserved, requires --force)
- `--force`: Required with `--wipe-db` to actually wipe the database

### Examples

**Full update (all data):**
```bash
python src/main.py --update
```

**Wipe the database (all data, schema preserved):**
```bash
python src/main.py --wipe-db           # Shows warning, does nothing
python src/main.py --wipe-db --force   # Actually wipes all data
```

**Update only planets:**
```bash
python src/main.py --update-planets
```

**Run as a daemon (every 24 hours):**
```bash
python src/main.py --daemon --interval 24
```

**Show help:**
```bash
python src/main.py --help
```

---

**Ready to join the fight for Super Earth? Deploy your own Helldivers 2 data pipeline today!**

### News Table Schema (as of migration 002)

| Column     | Type         | Description                        |
|------------|--------------|------------------------------------|
| id         | INT (PK)     | News item ID from API              |
| published  | DATETIME     | When the news was published        |
| type       | VARCHAR(100) | News type/category                 |
| tagIds     | JSON         | List of tag IDs (as JSON array)    |
| message    | TEXT         | News message/content               |
| created_at | TIMESTAMP    | Row creation time                  |

**Migration Note:**
- The news table was updated in `migrations/002_update_news_table.sql` to match the live API fields. Old columns (`title`, `content`, `publish_date`) were removed. The API's `id` is now the primary key. 

### War Status Table Schema (as of migration 003)

| Column             | Type         | Description                                 |
|--------------------|--------------|---------------------------------------------|
| war_id             | INT (PK)     | War ID from API                             |
| time               | DATETIME     | War status timestamp (converted from int)   |
| impact_multiplier  | FLOAT        | Impact multiplier from API                  |
| story_beat_id32    | INT          | Story beat ID from API                      |
| created_at         | TIMESTAMP    | Row creation time                           |

### Planet Status Table Schema (as of migration 003)

| Column           | Type         | Description                                 |
|------------------|--------------|---------------------------------------------|
| war_id           | INT (FK)     | War ID, references war_status(war_id)       |
| planet_index     | INT          | Planet index in the war                     |
| owner            | INT          | Owner ID                                    |
| health           | BIGINT       | Planet health                               |
| regen_per_second | FLOAT        | Health regeneration per second              |
| players          | INT          | Number of players on the planet             |
| position_x       | FLOAT        | X coordinate of planet position             |
| position_y       | FLOAT        | Y coordinate of planet position             |
| PRIMARY KEY      | (war_id, planet_index) | Composite PK for uniqueness         |

**Migration Note:**
- The war_status and planet_status tables were rebuilt in `migrations/003_rebuild_war_status_and_planet_status.sql` to match the live API fields. `war_id` is the primary key for war_status and a foreign key in planet_status. The planet_status table uses a composite primary key (`war_id`, `planet_index`). 