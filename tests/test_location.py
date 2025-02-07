import pytest
from datetime import datetime
from unittest import mock
from app import location, coordinates, timeline

def mocked_timeline(*args, **kwargs):
    class TestTimeline:
        def __init__(self, latest):
            self.latest = latest
            
    return TestTimeline(args[0])

@pytest.mark.parametrize("test_id, country, country_code, country_population, province, latitude, longitude, confirmed_latest, deaths_latest, recovered_latest", [
    (0, "Thailand", "TH", 1000, "", 15, 100, 1000, 1111, 22222),
    (1, "Deutschland", "DE", 1000, "", 15, 100, 1000, 1111, 22222),
    (2, "Cruise Ship", "XX", 1000, "", 15, 100, 1000, 1111, 22222)
])
@mock.patch('app.timeline.Timeline', side_effect=mocked_timeline)
def test_location_class(mocked_timeline, test_id, country, country_code, country_population, province, latitude, longitude, confirmed_latest, deaths_latest, recovered_latest):

    # id, country, province, coordinates, confirmed, deaths, recovered
    coords = coordinates.Coordinates(latitude=latitude, longitude=longitude)

    # Timelines
    confirmed = timeline.Timeline(confirmed_latest)
    deaths    = timeline.Timeline(deaths_latest)
    recovered = timeline.Timeline(recovered_latest)

    # Date now.
    now = datetime.utcnow().isoformat() + 'Z'

    # Location.
    location_obj = location.TimelinedLocation(test_id, country, province, coords, now, {
        'confirmed': confirmed, 
        'deaths'   : deaths,
        'recovered': recovered,
    })

    assert location_obj.country_code == country_code
    assert not location_obj.serialize() == None
