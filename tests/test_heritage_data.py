from tools.heritage_data import load_heritage_data, get_all_places
from tools.heritage_search import search_heritage


def test_dataset_loads():
    dataset = load_heritage_data()

    assert dataset is not None
    assert len(dataset.places) > 0


def test_all_places_have_unique_ids():
    places = get_all_places()

    ids = [place.id for place in places]

    assert len(ids) == len(set(ids))


def test_places_have_required_fields():
    places = get_all_places()

    for place in places:
        assert place.id
        assert place.name
        assert place.area
        assert place.district
        assert place.type
        assert place.coordinates
        assert place.sources


def test_search_by_name():
    places = get_all_places()

    first_place = places[0]

    results = search_heritage(
        query=first_place.name
    )

    assert len(results) > 0


def test_filter_by_type():
    places = search_heritage(
        type="temple"
    )

    for place in places:
        assert place.type.lower() == "temple"


def test_filter_by_district():
    places = search_heritage(
        district="South Goa"
    )

    for place in places:
        assert place.district.lower() == "south goa"


def test_combined_filters():
    places = search_heritage(
        district="South Goa",
        type="temple",
        popularity="lesser_known",
    )

    for place in places:
        assert place.district.lower() == "south goa"
        assert place.type.lower() == "temple"
        assert place.popularity.lower() == "lesser_known"


def test_unknown_place_returns_empty():
    results = search_heritage(
        query="This Place Definitely Does Not Exist In Goa"
    )

    assert results == []


def test_all_places_are_in_goa():
    places = get_all_places()

    for place in places:
        assert place.district in ["North Goa", "South Goa"]