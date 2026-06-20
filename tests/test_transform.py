import json
import pytest
from pipeline.transform import parse_record, build_geojson


def make_record(**kwargs):
    base = {
        "latitude": "53.5362",
        "longitude": "-113.4700",
        "date_created": "2023-07-15T20:00:00.000",
        "complaint_category": "Noise",
    }
    base.update(kwargs)
    return base


class TestParseRecord:
    def test_valid_record(self):
        result = parse_record(make_record())
        assert result["lat"] == pytest.approx(53.5362)
        assert result["lon"] == pytest.approx(-113.4700)
        assert result["dow"] == 5  # Saturday
        assert result["year"] == 2023

    def test_day_of_week_monday(self):
        result = parse_record(make_record(date_created="2023-07-17T10:00:00.000"))
        assert result["dow"] == 0  # Monday

    def test_missing_latitude(self):
        assert parse_record(make_record(latitude=None)) is None

    def test_missing_longitude(self):
        assert parse_record(make_record(longitude=None)) is None

    def test_missing_date(self):
        assert parse_record(make_record(date_created=None)) is None

    def test_empty_latitude_string(self):
        assert parse_record(make_record(latitude="")) is None

    def test_invalid_date_format(self):
        assert parse_record(make_record(date_created="not-a-date")) is None


class TestBuildGeojson:
    def test_output_structure(self):
        records = [make_record()]
        result = build_geojson(records)
        assert result["type"] == "FeatureCollection"
        assert len(result["features"]) == 1

    def test_feature_structure(self):
        records = [make_record()]
        feature = build_geojson(records)["features"][0]
        assert feature["type"] == "Feature"
        assert feature["geometry"]["type"] == "Point"
        assert len(feature["geometry"]["coordinates"]) == 2
        assert "dow" in feature["properties"]
        assert "year" in feature["properties"]

    def test_coordinates_are_lon_lat_order(self):
        records = [make_record(latitude="53.5362", longitude="-113.4700")]
        feature = build_geojson(records)["features"][0]
        lon, lat = feature["geometry"]["coordinates"]
        assert lon == pytest.approx(-113.4700)
        assert lat == pytest.approx(53.5362)

    def test_drops_records_missing_latlon(self):
        records = [make_record(), make_record(latitude=None)]
        result = build_geojson(records)
        assert len(result["features"]) == 1

    def test_empty_input(self):
        result = build_geojson([])
        assert result["features"] == []

    def test_all_seven_days_represented(self):
        # One record per day of week
        dates = [
            "2023-07-17T10:00:00.000",  # Mon
            "2023-07-18T10:00:00.000",  # Tue
            "2023-07-19T10:00:00.000",  # Wed
            "2023-07-20T10:00:00.000",  # Thu
            "2023-07-21T10:00:00.000",  # Fri
            "2023-07-22T10:00:00.000",  # Sat
            "2023-07-23T10:00:00.000",  # Sun
        ]
        records = [make_record(date_created=d) for d in dates]
        features = build_geojson(records)["features"]
        dows = {f["properties"]["dow"] for f in features}
        assert dows == {0, 1, 2, 3, 4, 5, 6}
