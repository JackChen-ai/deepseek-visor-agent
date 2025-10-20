"""Common test fixtures and configuration"""

import pytest


@pytest.fixture(scope="session")
def test_data_dir():
    """Path to test data directory"""
    from pathlib import Path
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def sample_invoice_path(test_data_dir):
    """Path to sample invoice image"""
    return test_data_dir / "invoice_sample.jpg"


@pytest.fixture
def sample_contract_path(test_data_dir):
    """Path to sample contract image"""
    return test_data_dir / "contract_sample.pdf"
