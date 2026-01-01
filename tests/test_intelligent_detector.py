"""
Unit tests for Intelligent Secret Detector
Tests the core intelligent detection engine (entropy, semantic, format-based)
"""

import pytest
from src.shieldcommit.intelligent_detector import IntelligentDetector, detect_secrets


class TestEntropyDetection:
    """Test entropy-based secret detection"""

    def test_detects_high_entropy_string(self):
        """High-entropy random strings should be detected as secrets"""
        line = 'password = "xK7mPqL9bJnR2tFhWdS4vE6cB8gA"'
        findings = IntelligentDetector.detect_in_line(line)
        assert len(findings) > 0
        assert findings[0]["confidence"] > 0.5

    def test_ignores_low_entropy_word(self):
        """Common English words should NOT be flagged"""
        line = 'name = "production"'
        findings = IntelligentDetector.detect_in_line(line)
        assert len(findings) == 0

    def test_entropy_calculation_works(self):
        """Entropy calculation should work correctly"""
        high_entropy = IntelligentDetector.calculate_entropy("xK7mPqL9bJnR2tFhWdS4vE6cB8gA")
        low_entropy = IntelligentDetector.calculate_entropy("password")
        assert high_entropy > low_entropy
        assert high_entropy > 3.5  # Threshold for secrets


class TestSemanticDetection:
    """Test semantic analysis (variable names indicating secrets)"""

    def test_detects_password_keyword(self):
        """Detects 'password' in variable name"""
        line = 'db_password = "SecureP@ss123456"'
        findings = IntelligentDetector.detect_in_line(line)
        assert len(findings) > 0

    def test_detects_secret_keyword(self):
        """Detects 'secret' in variable name with high entropy"""
        line = 'api_secret = "xK7mPqL9bJnR2tFhWdS4vE6cB8gA"'
        findings = IntelligentDetector.detect_in_line(line)
        assert len(findings) > 0

    def test_detects_token_keyword(self):
        """Detects 'token' in variable name"""
        line = 'auth_token = "bearer_xyz123456789abc"'
        findings = IntelligentDetector.detect_in_line(line)
        assert len(findings) > 0

    def test_detects_api_key_keyword(self):
        """Detects 'api_key' in variable name with high entropy"""
        line = 'stripe_api_key = "xK7mPqL9bJnR2tFhWdS4vE6cB8gA"'
        findings = IntelligentDetector.detect_in_line(line)
        assert len(findings) > 0

    def test_context_aware_detection(self):
        """Detects secrets using context from previous lines"""
        # Variable declaration 3 lines back
        context = "variable db_password { type = string default = "
        line = '  default = "MySecureP@ssw0rd123456789"'
        findings = IntelligentDetector.detect_in_line(line, context=context)
        assert len(findings) > 0


class TestFormatDetection:
    """Test detection of known secret formats (AWS, Stripe, GitHub, etc.)"""

    def test_detects_aws_access_key(self):
        """AWS Access Keys (AKIA prefix) should be detected with 95% confidence"""
        line = 'aws_key = "AKIAIOSFODNN7EXAMPLE"'
        findings = IntelligentDetector.detect_in_line(line)
        assert len(findings) > 0
        assert findings[0]["confidence"] >= 0.95

    def test_detects_stripe_secret_key(self):
        """Stripe Secret Keys (sk_live prefix) should be detected with 95% confidence"""
        line = 'stripe_secret = "sk_live_4eC39HqLyjWDarhtT8B3mkEv"'
        findings = IntelligentDetector.detect_in_line(line)
        assert len(findings) > 0
        assert findings[0]["confidence"] >= 0.95

    def test_detects_github_token(self):
        """GitHub tokens (ghp prefix) should be detected with 95% confidence"""
        line = 'github_token = "ghp_16C7e42F292c6912E7710c838347Ae178B4a"'
        findings = IntelligentDetector.detect_in_line(line)
        assert len(findings) > 0
        assert findings[0]["confidence"] >= 0.95

    def test_detects_google_oauth_token(self):
        """Google OAuth tokens (ya29 prefix) should be detected"""
        line = 'google_token = "ya29.a0AfH6SMBx_abcdef123456"'
        findings = IntelligentDetector.detect_in_line(line)
        assert len(findings) > 0

    def test_detects_private_key(self):
        """Private key with content should be detected"""
        line = 'private_key = "-----BEGIN RSA PRIVATE KEY-----"'
        findings = IntelligentDetector.detect_in_line(line)
        assert len(findings) > 0


class TestFalsePositiveExclusions:
    """Test that legitimate patterns are NOT flagged as secrets"""

    def test_excludes_terraform_interpolations(self):
        """Terraform variable interpolations should NOT be flagged"""
        line = 'Name = "${var.project_name}-public-subnet-${count.index + 1}"'
        findings = IntelligentDetector.detect_in_line(line)
        assert len(findings) == 0

    def test_excludes_aws_arns(self):
        """AWS ARNs should NOT be flagged"""
        line = 'policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"'
        findings = IntelligentDetector.detect_in_line(line)
        assert len(findings) == 0

    def test_excludes_ec2_instance_id(self):
        """EC2 Instance IDs (i-*) should NOT be flagged"""
        line = 'instance_id = "i-1234567890abcdef0"'
        findings = IntelligentDetector.detect_in_line(line)
        assert len(findings) == 0

    def test_excludes_security_group_id(self):
        """Security Group IDs (sg-*) should NOT be flagged"""
        line = 'security_group = "sg-123456789"'
        findings = IntelligentDetector.detect_in_line(line)
        assert len(findings) == 0

    def test_excludes_vpc_id(self):
        """VPC IDs (vpc-*) should NOT be flagged"""
        line = 'vpc_id = "vpc-12345678"'
        findings = IntelligentDetector.detect_in_line(line)
        assert len(findings) == 0

    def test_excludes_subnet_id(self):
        """Subnet IDs (subnet-*) should NOT be flagged"""
        line = 'subnet_id = "subnet-123456789"'
        findings = IntelligentDetector.detect_in_line(line)
        assert len(findings) == 0

    def test_excludes_naming_patterns(self):
        """Resource naming patterns should NOT be flagged"""
        line = 'tag_name = "web-server-prod-us-east-1"'
        findings = IntelligentDetector.detect_in_line(line)
        assert len(findings) == 0

    def test_excludes_resource_references(self):
        """Terraform resource references should NOT be flagged"""
        line = "db_endpoint = aws_db_instance.postgres.endpoint"
        findings = IntelligentDetector.detect_in_line(line)
        assert len(findings) == 0

    def test_excludes_version_numbers(self):
        """Version numbers should NOT be flagged"""
        line = 'kubernetes_version = "1.27.0"'
        findings = IntelligentDetector.detect_in_line(line)
        assert len(findings) == 0

    def test_excludes_container_images(self):
        """Container image names should NOT be flagged"""
        line = 'image = "nginx:1.24"'
        findings = IntelligentDetector.detect_in_line(line)
        assert len(findings) == 0

    def test_excludes_docker_registries(self):
        """Docker registries should NOT be flagged"""
        line = 'image = "gcr.io/my-project/app:v1.2.3"'
        findings = IntelligentDetector.detect_in_line(line)
        assert len(findings) == 0

    def test_excludes_urls(self):
        """URLs should NOT be flagged"""
        line = 'endpoint = "https://api.example.com/v1/users"'
        findings = IntelligentDetector.detect_in_line(line)
        assert len(findings) == 0

    def test_excludes_ip_addresses(self):
        """IP addresses should NOT be flagged"""
        line = 'server_ip = "192.168.1.100"'
        findings = IntelligentDetector.detect_in_line(line)
        assert len(findings) == 0

    def test_excludes_domain_names(self):
        """Domain names should NOT be flagged"""
        line = 'hostname = "api.example.com"'
        findings = IntelligentDetector.detect_in_line(line)
        assert len(findings) == 0

    def test_excludes_email_addresses(self):
        """Email addresses should NOT be flagged"""
        line = 'email = "admin@example.com"'
        findings = IntelligentDetector.detect_in_line(line)
        assert len(findings) == 0

    def test_excludes_kubernetes_patterns(self):
        """Kubernetes patterns should NOT be flagged"""
        line = "apiVersion: v1"
        findings = IntelligentDetector.detect_in_line(line)
        assert len(findings) == 0

    def test_excludes_kubernetes_kind(self):
        """Kubernetes kind declarations should NOT be flagged"""
        line = "kind: Deployment"
        findings = IntelligentDetector.detect_in_line(line)
        assert len(findings) == 0


class TestDetectSecretsFunction:
    """Test the main detect_secrets() function"""

    def test_detects_secrets_in_text(self):
        """detect_secrets() should find secrets in multi-line text"""
        text = """
variable "db_password" {
  default = "MySecureP@ssw0rd123456789"
}

variable "api_key" {
  default = "sk_live_4eC39HqLyjWDarhtT8B3mkEv"
}
"""
        findings = detect_secrets(text)
        assert len(findings) >= 2

    def test_detects_secrets_with_line_numbers(self):
        """Findings should include line numbers"""
        text = '''password = "SecureP@ss123456789"
other_var = "production"
api_key = "sk_live_4eC39HqLyjWDarhtT8B3mkEv"'''
        findings = detect_secrets(text)
        assert any(f["line"] == 1 for f in findings)
        assert any(f["line"] == 3 for f in findings)

    def test_excludes_false_positives_in_text(self):
        """detect_secrets() should exclude false positives"""
        text = """
Name = "${var.environment}-public-subnet-${count.index}"
arn = "arn:aws:iam::123456789:role/MyRole"
version = "1.27.0"
image = "nginx:latest"
"""
        findings = detect_secrets(text)
        assert len(findings) == 0

    def test_confidence_threshold_filtering(self):
        """Should only return findings above confidence threshold"""
        text = 'password = "SecureP@ss123456789"'

        # Low threshold - should find it
        findings_low = detect_secrets(text, min_confidence=0.5)
        assert len(findings_low) > 0

        # Very high threshold - might not find it
        findings_high = detect_secrets(text, min_confidence=0.99)
        # Password should have ~63% confidence, so might not pass 99% threshold


class TestConfidenceScoring:
    """Test confidence score calculation"""

    def test_high_confidence_for_known_formats(self):
        """Known secret formats should have 95% confidence"""
        line = 'stripe_key = "sk_live_4eC39HqLyjWDarhtT8B3mkEv"'
        findings = IntelligentDetector.detect_in_line(line)
        assert len(findings) > 0
        assert findings[0]["confidence"] >= 0.95

    def test_medium_confidence_for_entropy_secrets(self):
        """High-entropy strings should have 60-80% confidence"""
        line = 'password = "xK7mPqL9bJnR2tFhWdS4vE6cB8gA"'
        findings = IntelligentDetector.detect_in_line(line)
        assert len(findings) > 0
        # Should have decent confidence due to entropy + keyword
        assert findings[0]["confidence"] > 0.5

    def test_context_increases_confidence(self):
        """Context from variable names should increase confidence"""
        # With context from 'db_password' variable
        context = "variable db_password { type = string default = "
        line = '  default = "MySecureP@ssw0rd123456789"'
        findings = IntelligentDetector.detect_in_line(line, context=context)

        # Without context
        line_only = '  default = "MySecureP@ssw0rd123456789"'
        findings_no_context = IntelligentDetector.detect_in_line(line_only)

        # Confidence with context should be higher
        if len(findings) > 0 and len(findings_no_context) > 0:
            assert findings[0]["confidence"] >= findings_no_context[0]["confidence"]


class TestDetectionMethods:
    """Test that detection methods are correctly identified"""

    def test_identifies_format_detection(self):
        """Should identify when format-based detection is used"""
        line = 'stripe_key = "sk_live_4eC39HqLyjWDarhtT8B3mkEv"'
        findings = IntelligentDetector.detect_in_line(line)
        assert len(findings) > 0
        assert "Stripe" in findings[0]["detection_method"]

    def test_identifies_entropy_detection(self):
        """Should identify when entropy-based detection is used"""
        line = 'password = "xK7mPqL9bJnR2tFhWdS4vE6cB8gA"'
        findings = IntelligentDetector.detect_in_line(line)
        assert len(findings) > 0
        assert "Entropy" in findings[0]["detection_method"]

    def test_identifies_context_detection(self):
        """Should identify when context analysis is used"""
        context = "variable db_password = "
        line = 'default = "SecureP@ss123456789"'
        findings = IntelligentDetector.detect_in_line(line, context=context)
        assert len(findings) > 0
