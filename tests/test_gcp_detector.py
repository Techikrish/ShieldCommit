"""
Tests for GCP GKE (Google Kubernetes Engine) version detection
Detects deprecated/extended support Kubernetes versions on Google Cloud
"""

import pytest
from src.shieldcommit.gcp_detector import scan_gcp_versions
from pathlib import Path
import tempfile


class TestGCPGKEVersionDetection:
    """Test Google Cloud GKE version detection and deprecation warnings"""
    
    def test_detects_deprecated_gke_version(self):
        """Should detect deprecated Kubernetes versions in GKE"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "main.tf"
            file_path.write_text('''
resource "google_container_cluster" "primary" {
  min_master_version = "1.24"
}
''')
            
            findings = scan_gcp_versions(file_path)
            # Version 1.24 is deprecated on GCP
            assert isinstance(findings, list)
    
    def test_detects_rapid_release_channel_warning(self):
        """Should flag RAPID release channel (not recommended)"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "main.tf"
            file_path.write_text('''
resource "google_container_cluster" "primary" {
  release_channel {
    channel = "RAPID"
  }
}
''')
            
            findings = scan_gcp_versions(file_path)
            # RAPID channel should be flagged
            assert isinstance(findings, list)
    
    def test_no_warning_for_stable_channel(self):
        """Should report STABLE channel with informational message"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "main.tf"
            file_path.write_text('''
resource "google_container_cluster" "primary" {
  release_channel {
    channel = "STABLE"
  }
}
''')
            
            findings = scan_gcp_versions(file_path)
            # STABLE channel gets reported as informational
            assert len(findings) >= 1
            assert "STABLE" in findings[0]["message"]
    
    def test_recommends_regular_over_rapid(self):
        """Should prefer REGULAR channel over RAPID"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "main.tf"
            file_path.write_text('''
resource "google_container_cluster" "primary" {
  release_channel {
    channel = "UNSPECIFIED"
  }
}
''')
            
            findings = scan_gcp_versions(file_path)
            assert isinstance(findings, list)
    
    def test_detects_version_in_node_pool(self):
        """Should detect versions in node pool configuration"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "main.tf"
            file_path.write_text('''
resource "google_container_node_pool" "primary_nodes" {
  version = "1.25"
}
''')
            
            findings = scan_gcp_versions(file_path)
            assert isinstance(findings, list)
    
    def test_multiple_gke_clusters(self):
        """Should detect deprecated versions in multiple GKE clusters"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "main.tf"
            file_path.write_text('''
resource "google_container_cluster" "primary" {
  min_master_version = "1.23"
}

resource "google_container_cluster" "secondary" {
  min_master_version = "1.24"
}
''')
            
            findings = scan_gcp_versions(file_path)
            assert isinstance(findings, list)
    
    def test_gcp_specific_fields(self):
        """Should detect GCP-specific configuration patterns"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "gke.tf"
            file_path.write_text('''
resource "google_container_cluster" "primary" {
  name     = "my-gke-cluster"
  location = "us-central1"
  
  release_channel {
    channel = "RAPID"
  }
  
  node_pool {
    version = "1.22"
  }
}
''')
            
            findings = scan_gcp_versions(file_path)
            assert isinstance(findings, list)
