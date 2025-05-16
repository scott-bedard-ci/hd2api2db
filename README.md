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

## 🏗️ Architecture & Data Integrity

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

> **Note:**
> The update process always fetches and upserts planets before war_info and planet_infos to ensure all foreign key constraints are satisfied. This prevents errors when inserting planet_infos that reference planets.

- **Factions:**
  - All factions referenced in campaigns are created with their real names during campaign ingestion.
  - Any additional factions referenced only by ID in war_info (e.g., in planet_infos or home_worlds) are upserted with a placeholder name (e.g., 'Unknown (id)').
  - This ensures all foreign key references to factions succeed, even if the name is not yet known.

- **Planets:**
  - All planet IDs, including 0 (Super Earth), are now present in the API and imported directly.
  - The planets table uses the API's id as the primary key (not auto-increment), so planet_id 0 is supported natively.

- **Ingestion Order:**
  1. Planets
  2. Campaigns (creates most factions)
  3. war_info (ensures all referenced factions exist)
  4. war_status
  5. news
  6. major_orders
  7. planet_history

- **Robustness:**
  - The pipeline is robust to new/unknown factions from the API. Placeholder entries are created as needed and can be updated later when real data is available.

## ❓ FAQ / Troubleshooting

- **Why do I see 'Unknown' factions or planets in the database?**
  - The pipeline creates placeholder entries for any referenced faction or planet that does not yet exist in the database. This is necessary to satisfy foreign key constraints and ensure ingestion does not fail when the API references new or unknown entities. These entries can be updated later when more information becomes available.

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
- Run the schema setup:

```bash
mysql -u root -p < migrations/schema.sql
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
  schema.sql                    # Full MySQL schema (single source of truth)
scripts/
  prd.txt                       # Product Requirements Document
  wipe_db.py                    # Script to wipe the database for a fresh pull
  war_info_api_sample.txt       # Sample API response for War Info
tests/
  test_*.py                     # Test scripts for all major modules
```

---

## 🧪 Testing

This project uses `pytest` for all automated testing. The test suite is fully migrated to pytest and uses shared fixtures for database setup and cleanup, located in `src/conftest.py`. This ensures all tests use the correct test database credentials and are isolated and repeatable.

### Test Categories
- **fast**: Unit and functional tests that run quickly and do not require full integration (default for most tests).
- **complete**: Full integration/orchestration tests (e.g., end-to-end pipeline tests). Only run when explicitly selected.

### Running Tests
- **Only fast tests:**
  ```sh
  pytest -m "not complete"
  ```
- **Only complete (integration) tests:**
  ```sh
  pytest -m complete
  ```
- **All tests:**
  ```sh
  pytest
  ```

### Test Infrastructure
- All test DB credentials and environment variables are managed via shared fixtures in `src/conftest.py`.
- Test data is cleaned up before and after each test, ensuring a clean environment.
- Tests marked with `@pytest.mark.no_db` skip DB setup/teardown (for config/env tests).
- The orchestration/integration test is marked with `@pytest.mark.complete` and excluded from fast runs.

### DRY Principle
- All DB setup/teardown logic is centralized in `conftest.py`.
- No duplicate fixture code in individual test files.

### Additional Notes
- See `pytest.ini` for marker definitions and usage.
- The test suite is robust, maintainable, and safe for iterative development.

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

- **Project Lead:** [Scott Bedard](https://github.com/scott-bedard-ci)
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

### Planet History Table Schema (as of migration 007)

| Column         | Type         | Description                                 |
|---------------|--------------|---------------------------------------------|
| id            | INT (PK)     | Auto-incremented row ID                     |
| planet_id     | INT (FK)     | Planet ID, references planets(id)           |
| timestamp     | DATETIME     | Event timestamp                             |
| status        | VARCHAR(100) | Status of the planet at this time           |
| current_health| BIGINT       | Current health of the planet                |
| max_health    | BIGINT       | Maximum health of the planet                |
| player_count  | INT          | Number of players present                   |
| created_at    | TIMESTAMP    | Row creation time                           |

**Migration Note:**
- The planet_history table was updated in `migrations/007_update_planet_history.sql` to add the fields `current_health`, `max_health`, and `player_count` to match the live API response. If you encounter foreign key errors during ingestion, ensure the referenced planet IDs exist in the `planets` table or perform a full DB rebuild. 

**Error Reporting for Missing Planet IDs:**
- During planet history ingestion, if a history entry references a `planet_id` that does not exist in the `planets` table, the pipeline now detects and aggregates these errors.
- At the end of ingestion, a summary of all missing planet IDs (and their context) is logged for review.
- This feature helps diagnose data integrity issues and ensures that ingestion failures due to missing foreign keys are visible and actionable.
- See `src/test_planet_history_fetcher.py` for a test that verifies this error reporting behavior.

### War Info Table Schema (as of migration 008)

| Column                  | Type         | Description                                      |
|------------------------|--------------|--------------------------------------------------|
| war_id                 | INT (PK)     | War ID from API                                  |
| start_date             | DATETIME     | War start date (converted from int timestamp)     |
| end_date               | DATETIME     | War end date (converted from int timestamp)       |
| layout_version         | INT          | Layout version from API                          |
| minimum_client_version | VARCHAR(20)  | Minimum client version required                   |
| capital_infos          | JSON         | Capital info objects (as JSON array)              |
| planet_permanent_effects| JSON        | Permanent effects for planets (as JSON array)     |
| created_at             | TIMESTAMP    | Row creation time                                |
| updated_at             | TIMESTAMP    | Row update time                                  |

**Migration Note:**
- The war_info table was rebuilt in `migrations/008_rebuild_war_info_and_related.sql` to match the live API fields. Integer timestamps are converted to DATETIME. JSON columns are used for nested arrays/objects.

### Planet Infos Table Schema (as of migration 008)

| Column            | Type         | Description                                      |
|-------------------|--------------|--------------------------------------------------|
| war_id            | INT (FK)     | War ID, references war_info(war_id)              |
| planet_id         | INT (FK)     | Planet ID, references planets(id)                |
| position_x        | FLOAT        | X coordinate of planet position                  |
| position_y        | FLOAT        | Y coordinate of planet position                  |
| waypoints         | JSON         | List of waypoints (as JSON array)                |
| sector            | INT          | Sector number                                    |
| max_health        | BIGINT       | Maximum health of the planet                     |
| disabled          | BOOLEAN      | Whether the planet is disabled                   |
| initial_faction_id| INT (FK)     | Initial owner, references factions(id)           |
| PRIMARY KEY       | (war_id, planet_id) | Composite PK for uniqueness                |

### Home Worlds Table Schema (as of migration 008)

| Column      | Type     | Description                                 |
|-------------|----------|---------------------------------------------|
| war_id      | INT (FK) | War ID, references war_info(war_id)         |
| faction_id  | INT (FK) | Faction ID, references factions(id)         |
| planet_id   | INT (FK) | Planet ID, references planets(id)           |
| PRIMARY KEY | (war_id, faction_id, planet_id) | Composite PK       |

**Migration Note:**
- These tables were rebuilt in `migrations/008_rebuild_war_info_and_related.sql` to match the actual API response structure. All foreign keys and constraints are enforced.

### War Info API Integration Details

- The pipeline fetches the War Info API response and parses all top-level and nested fields.
- Integer timestamps (`startDate`, `endDate`) are converted to MySQL DATETIME using timezone-aware conversion.
- Nested arrays/objects (`capitalInfos`, `planetPermanentEffects`, `waypoints`) are stored as JSON.
- The transformer logic is implemented in [`src/transformers/war_info_transformer.py`](src/transformers/war_info_transformer.py).
- The fetch/store logic is in [`src/war_info_fetcher.py`](src/war_info_fetcher.py).

#### Example War Info API Response

See [`scripts/war_info_api_sample.txt`](scripts/war_info_api_sample.txt) for a full sample. Key fields:

```json
{
  "warId": 801,
  "startDate": 1833653095,
  "endDate": 1834257895,
  "layoutVersion": 40,
  "minimumClientVersion": "0.3.0",
  "capitalInfos": [...],
  "planetPermanentEffects": [...],
  "planetInfos": [
    {
      "index": 0,
      "position": {"x": 0, "y": 0},
      "waypoints": [],
      "sector": 0,
      "maxHealth": 1000000,
      "disabled": false,
      "initialOwner": 1
    },
    ...
  ],
  "homeWorlds": [
    {"race": 1, "planetIndices": [0]},
    {"race": 3, "planetIndices": [260]}
  ]
}
```

#### Field Mapping (API → DB)

| API Field                | DB Table      | DB Column                |
|--------------------------|--------------|--------------------------|
| warId                    | war_info     | war_id                   |
| startDate                | war_info     | start_date (DATETIME)    |
| endDate                  | war_info     | end_date (DATETIME)      |
| layoutVersion            | war_info     | layout_version           |
| minimumClientVersion     | war_info     | minimum_client_version   |
| capitalInfos             | war_info     | capital_infos (JSON)     |
| planetPermanentEffects   | war_info     | planet_permanent_effects (JSON) |
| planetInfos[].index      | planet_infos | planet_id                |
| planetInfos[].position.x | planet_infos | position_x               |
| planetInfos[].position.y | planet_infos | position_y               |
| planetInfos[].waypoints  | planet_infos | waypoints (JSON)         |
| planetInfos[].sector     | planet_infos | sector                   |
| planetInfos[].maxHealth  | planet_infos | max_health               |
| planetInfos[].disabled   | planet_infos | disabled                 |
| planetInfos[].initialOwner| planet_infos| initial_faction_id       |
| homeWorlds[].race        | home_worlds  | faction_id               |
| homeWorlds[].planetIndices| home_worlds | planet_id (one row per)  |

#### Testing & Validation

- Unit and integration tests cover all transformer logic and DB upserts.
- Migration scripts are tested in both live and test environments.
- End-to-end tests verify that the pipeline correctly ingests, transforms, and stores all War Info data.
- See `src/test_war_info_fetcher.py` for test coverage.

#### Workflow Summary

1. Fetch War Info API response.
2. Transform and map all fields to the new schema.
3. Store in `war_info`, `planet_infos`, and `home_worlds` tables.
4. Validate with tests and manual DB inspection.
5. Update documentation and migration notes as needed.