import json
import pytest
from pathlib import Path
from pipeline.generate import main


FAKE_GEOJSON = {
    "type": "FeatureCollection",
    "features": [
        {"type": "Feature", "geometry": {"type": "Point", "coordinates": [-113.47, 53.54]}, "properties": {"dow": 0, "year": 2023}},
        {"type": "Feature", "geometry": {"type": "Point", "coordinates": [-113.48, 53.55]}, "properties": {"dow": 2, "year": 2024}},
    ],
}


@pytest.fixture
def site_data(tmp_path, monkeypatch):
    geojson_path = tmp_path / "complaints.geojson"
    meta_path = tmp_path / "meta.json"
    geojson_path.write_text(json.dumps(FAKE_GEOJSON))

    import pipeline.generate as gen
    monkeypatch.setattr(gen, "GEOJSON_PATH", geojson_path)
    monkeypatch.setattr(gen, "META_PATH", meta_path)

    return meta_path


def test_meta_written(site_data):
    main()
    assert site_data.exists()


def test_meta_record_count(site_data):
    main()
    meta = json.loads(site_data.read_text())
    assert meta["record_count"] == 2


def test_meta_has_built_at(site_data):
    main()
    meta = json.loads(site_data.read_text())
    assert "built_at" in meta
    assert meta["built_at"].endswith("Z")


def test_meta_built_at_format(site_data):
    from datetime import datetime
    main()
    meta = json.loads(site_data.read_text())
    datetime.strptime(meta["built_at"], "%Y-%m-%dT%H:%M:%SZ")
