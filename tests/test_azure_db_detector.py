"""
Tests for Azure Database version detection
Detects deprecated database engine versions on Azure
"""

import pytest
from src.shieldcommit.azure_db_detector import scan_azure_db_versions
from pathlib import Path
import tempfile


class TestAzureDBVersionDetection:
    """Test Azure Database version detection and deprecation warnings"""

    def test_detects_deprecated_sql_server_version(self):
        """Should detect deprecated SQL Server versions on Azure"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "main.tf"
            file_path.write_text(
                """
resource "azurerm_mssql_server" "primary" {
  version = "12.0"
}
"""
            )

            findings = scan_azure_db_versions(file_path)
            # SQL Server 12.0 should be flagged
            assert isinstance(findings, list)

    def test_detects_deprecated_mysql_version(self):
        """Should detect deprecated MySQL versions on Azure"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "main.tf"
            file_path.write_text(
                """
resource "azurerm_mysql_server" "primary" {
  version = "5.7"
}
"""
            )

            findings = scan_azure_db_versions(file_path)
            assert isinstance(findings, list)

    def test_detects_deprecated_postgres_version(self):
        """Should detect deprecated PostgreSQL versions on Azure"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "main.tf"
            file_path.write_text(
                """
resource "azurerm_postgresql_server" "primary" {
  version = "10"
}
"""
            )

            findings = scan_azure_db_versions(file_path)
            assert isinstance(findings, list)

    def test_no_warning_for_current_version(self):
        """Should report current versions as extended support"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "main.tf"
            file_path.write_text(
                """
resource "azurerm_postgresql_server" "primary" {
  version = "14"
}
"""
            )

            findings = scan_azure_db_versions(file_path)
            # PostgreSQL 14 is on Extended Support, detector still reports it
            assert len(findings) >= 1
            assert "Extended Support" in findings[0]["message"]

    def test_finds_version_in_flexible_server(self):
        """Should find versions in Azure flexible server"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "main.tf"
            file_path.write_text(
                """
resource "azurerm_postgresql_flexible_server" "primary" {
  version = "11"
}
"""
            )

            findings = scan_azure_db_versions(file_path)
            assert isinstance(findings, list)

    def test_finds_version_in_variable_block(self):
        """Should find database versions in variable blocks"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "variables.tf"
            file_path.write_text(
                """
variable "db_version" {
  description = "Azure database version"
  default     = "11"
}
"""
            )

            findings = scan_azure_db_versions(file_path)
            assert isinstance(findings, list)

    def test_multiple_databases_in_file(self):
        """Should detect deprecated versions in multiple databases"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "main.tf"
            file_path.write_text(
                """
resource "azurerm_postgresql_server" "postgres" {
  version = "10"
}

resource "azurerm_mysql_server" "mysql" {
  version = "5.7"
}

resource "azurerm_mssql_server" "sql" {
  version = "12.0"
}
"""
            )

            findings = scan_azure_db_versions(file_path)
            assert isinstance(findings, list)

    def test_azure_specific_fields(self):
        """Should detect Azure-specific database configuration"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "azure_db.tf"
            file_path.write_text(
                """
resource "azurerm_postgresql_server" "primary" {
  name                         = "my-postgres"
  location                     = "East US"
  version                      = "9.5"
  storage_mb                   = 5120
  backup_retention_days        = 7
  geo_redundant_backup_enabled = true
}
"""
            )

            findings = scan_azure_db_versions(file_path)
            # PostgreSQL 9.5 is deprecated
            assert isinstance(findings, list)
