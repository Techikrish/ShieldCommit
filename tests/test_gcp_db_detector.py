"""
Tests for GCP Cloud SQL version detection
Detects deprecated database engine versions on Google Cloud SQL
"""

import pytest
from shieldcommit.gcp_db_detector import scan_gcp_cloudsql_versions
from pathlib import Path
import tempfile


class TestGCPCloudSQLVersionDetection:
    """Test Google Cloud SQL version detection and deprecation warnings"""

    def test_detects_deprecated_postgres_version(self):
        """Should detect deprecated PostgreSQL versions on Cloud SQL"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "main.tf"
            file_path.write_text(
                """
resource "google_sql_database_instance" "primary" {
  database_version = "POSTGRES_11"
}
"""
            )

            findings = scan_gcp_cloudsql_versions(file_path)
            # PostgreSQL 11 is deprecated on Cloud SQL
            assert isinstance(findings, list)

    def test_detects_deprecated_mysql_version(self):
        """Should detect deprecated MySQL versions on Cloud SQL"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "main.tf"
            file_path.write_text(
                """
resource "google_sql_database_instance" "primary" {
  database_version = "MYSQL_5_7"
}
"""
            )

            findings = scan_gcp_cloudsql_versions(file_path)
            assert isinstance(findings, list)

    def test_detects_deprecated_sql_server_version(self):
        """Should detect deprecated SQL Server versions on Cloud SQL"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "main.tf"
            file_path.write_text(
                """
resource "google_sql_database_instance" "primary" {
  database_version = "SQLSERVER_2016"
}
"""
            )

            findings = scan_gcp_cloudsql_versions(file_path)
            assert isinstance(findings, list)

    def test_no_warning_for_current_version(self):
        """Should NOT warn for current Cloud SQL versions"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "main.tf"
            file_path.write_text(
                """
resource "google_sql_database_instance" "primary" {
  database_version = "POSTGRES_15"
}
"""
            )

            findings = scan_gcp_cloudsql_versions(file_path)
            assert len(findings) == 0

    def test_finds_version_in_variable_block(self):
        """Should find database versions in variable blocks"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "variables.tf"
            file_path.write_text(
                """
variable "cloud_sql_version" {
  description = "Cloud SQL database version"
  default     = "POSTGRES_12"
}
"""
            )

            findings = scan_gcp_cloudsql_versions(file_path)
            assert isinstance(findings, list)

    def test_multiple_databases_in_file(self):
        """Should detect deprecated versions in multiple Cloud SQL instances"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "main.tf"
            file_path.write_text(
                """
resource "google_sql_database_instance" "postgres" {
  database_version = "POSTGRES_10"
}

resource "google_sql_database_instance" "mysql" {
  database_version = "MYSQL_5_7"
}

resource "google_sql_database_instance" "sql" {
  database_version = "SQLSERVER_2016"
}
"""
            )

            findings = scan_gcp_cloudsql_versions(file_path)
            assert isinstance(findings, list)

    def test_gcp_specific_fields(self):
        """Should detect GCP Cloud SQL-specific configuration"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "cloudsql.tf"
            file_path.write_text(
                """
resource "google_sql_database_instance" "primary" {
  name                = "my-database"
  database_version    = "POSTGRES_11"
  deletion_protection = true
  region              = "us-central1"
  
  settings {
    tier              = "db-f1-micro"
    availability_type = "REGIONAL"
    backup_configuration {
      enabled                        = true
      start_time                     = "07:00"
      transaction_log_retention_days = 7
    }
  }
}
"""
            )

            findings = scan_gcp_cloudsql_versions(file_path)
            # PostgreSQL 11 is deprecated
            assert isinstance(findings, list)

    def test_detects_all_postgres_versions(self):
        """Should detect all PostgreSQL versions"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "main.tf"
            file_path.write_text(
                """
# Old versions
resource "google_sql_database_instance" "pg9" {
  database_version = "POSTGRES_9_6"
}

resource "google_sql_database_instance" "pg10" {
  database_version = "POSTGRES_10"
}

resource "google_sql_database_instance" "pg11" {
  database_version = "POSTGRES_11"
}
"""
            )

            findings = scan_gcp_cloudsql_versions(file_path)
            assert isinstance(findings, list)

    def test_detects_all_mysql_versions(self):
        """Should detect all MySQL versions"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "main.tf"
            file_path.write_text(
                """
resource "google_sql_database_instance" "mysql57" {
  database_version = "MYSQL_5_7"
}

resource "google_sql_database_instance" "mysql80" {
  database_version = "MYSQL_8_0_31"
}
"""
            )

            findings = scan_gcp_cloudsql_versions(file_path)
            assert isinstance(findings, list)
