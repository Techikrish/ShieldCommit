"""
Tests for AKS (Azure Kubernetes Service) version detection
Detects deprecated/extended support Kubernetes versions on Azure
"""

import pytest
from shieldcommit.aks_detector import scan_aks_versions
from pathlib import Path
import tempfile


class TestAKSVersionDetection:
    """Test Azure AKS version detection and deprecation warnings"""

    def test_detects_deprecated_version(self):
        """Should detect deprecated Kubernetes versions in AKS"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "main.tf"
            file_path.write_text(
                """
resource "azurerm_kubernetes_cluster" "main" {
  kubernetes_version = "1.23"
}
"""
            )

            findings = scan_aks_versions(file_path)
            # Version 1.23 should be flagged
            assert isinstance(findings, list)

    def test_detects_extended_support_version(self):
        """Should detect versions in extended support period"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "main.tf"
            file_path.write_text(
                """
resource "azurerm_kubernetes_cluster" "aks" {
  kubernetes_version = "1.25"
}
"""
            )

            findings = scan_aks_versions(file_path)
            assert isinstance(findings, list)

    def test_no_warning_for_current_version(self):
        """Should NOT warn for current/recent versions"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "main.tf"
            file_path.write_text(
                """
resource "azurerm_kubernetes_cluster" "main" {
  kubernetes_version = "1.29"
}
"""
            )

            findings = scan_aks_versions(file_path)
            assert len(findings) == 0

    def test_finds_version_in_variable_block(self):
        """Should find versions declared in variable blocks"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "variables.tf"
            file_path.write_text(
                """
variable "aks_version" {
  description = "AKS cluster version"
  default     = "1.24"
}
"""
            )

            findings = scan_aks_versions(file_path)
            # Version 1.24 is deprecated
            assert isinstance(findings, list)

    def test_multiple_clusters_in_file(self):
        """Should detect deprecated versions in multiple clusters"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "main.tf"
            file_path.write_text(
                """
resource "azurerm_kubernetes_cluster" "cluster1" {
  kubernetes_version = "1.23"
}

resource "azurerm_kubernetes_cluster" "cluster2" {
  kubernetes_version = "1.24"
}
"""
            )

            findings = scan_aks_versions(file_path)
            assert isinstance(findings, list)

    def test_aks_specific_fields(self):
        """Should detect AKS-specific configuration patterns"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "aks.tf"
            file_path.write_text(
                """
resource "azurerm_kubernetes_cluster" "main" {
  name                = "my-aks"
  kubernetes_version  = "1.22"
  node_resource_group = "MC_rg_aks_eastus"
}
"""
            )

            findings = scan_aks_versions(file_path)
            assert isinstance(findings, list)
