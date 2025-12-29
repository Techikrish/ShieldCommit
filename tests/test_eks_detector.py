"""
Tests for EKS (Elastic Kubernetes Service) version detection
Detects deprecated/extended support Kubernetes versions
"""

import pytest
from src.shieldcommit.eks_detector import scan_eks_versions
from pathlib import Path
import tempfile


class TestEKSVersionDetection:
    """Test AWS EKS version detection and deprecation warnings"""
    
    def test_detects_deprecated_version(self):
        """Should detect deprecated Kubernetes versions in EKS"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "main.tf"
            file_path.write_text('''
resource "aws_eks_cluster" "main" {
  kubernetes_version = "1.24"
}
''')
            
            findings = scan_eks_versions(file_path)
            assert len(findings) > 0
            # Kubernetes 1.24 should be flagged
    
    def test_detects_extended_support_version(self):
        """Should detect versions in extended support period"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "main.tf"
            file_path.write_text('''
resource "aws_eks_cluster" "main" {
  kubernetes_version = "1.27"
}
''')
            
            findings = scan_eks_versions(file_path)
            assert len(findings) > 0
            # Kubernetes 1.27 should be flagged
    
    def test_no_warning_for_current_version(self):
        """Should NOT warn for current/recent versions"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "main.tf"
            file_path.write_text('''
resource "aws_eks_cluster" "main" {
  kubernetes_version = "1.30"
}
''')
            
            findings = scan_eks_versions(file_path)
            assert len(findings) == 0
    
    def test_finds_version_in_variable_block(self):
        """Should find versions declared in variable blocks"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "variables.tf"
            file_path.write_text('''
variable "cluster_version" {
  description = "EKS cluster version"
  default     = "1.25"
}
''')
            
            findings = scan_eks_versions(file_path)
            assert len(findings) > 0
    
    def test_includes_line_numbers(self):
        """Should include line numbers in findings"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "main.tf"
            file_path.write_text('''
# Line 1
# Line 2
resource "aws_eks_cluster" "main" {
  kubernetes_version = "1.24"
}
''')
            
            findings = scan_eks_versions(file_path)
            assert len(findings) > 0
            assert 'line' in findings[0]
            assert findings[0]['line'] == 5
    
    def test_includes_file_path(self):
        """Should include file path in findings"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "main.tf"
            file_path.write_text('kubernetes_version = "1.23"')
            
            findings = scan_eks_versions(file_path)
            assert len(findings) > 0
            assert 'file' in findings[0]
            assert 'main.tf' in findings[0]['file']
    
    def test_multiple_versions_in_file(self):
        """Should detect all deprecated versions in file"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "main.tf"
            file_path.write_text('''
resource "aws_eks_cluster" "cluster1" {
  kubernetes_version = "1.23"
}

resource "aws_eks_cluster" "cluster2" {
  kubernetes_version = "1.24"
}
''')
            
            findings = scan_eks_versions(file_path)
            assert len(findings) >= 2
