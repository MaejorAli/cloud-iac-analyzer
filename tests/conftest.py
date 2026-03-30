import pytest
import json

# Helper fixture for creating JSON files
@pytest.fixture
def create_temp_file(tmp_path):
    def _create(data, filename):
        path = tmp_path / filename
        path.write_text(json.dumps(data))
        return path
    return _create