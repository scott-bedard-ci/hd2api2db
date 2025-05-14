#!/bin/bash
# Create helldivers2_test database and apply schema

MYSQL_USER="root"
MYSQL_DB="helldivers2_test"
MIGRATION_FILE="migrations/001_create_schema.sql"

# Create the test database if it doesn't exist
mysql -u $MYSQL_USER -e "CREATE DATABASE IF NOT EXISTS $MYSQL_DB;"

# Apply the migration SQL to the test database
mysql -u $MYSQL_USER $MYSQL_DB < $MIGRATION_FILE

echo "Test database '$MYSQL_DB' is ready." 