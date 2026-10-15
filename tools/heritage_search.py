from .heritage_data import HeritagePlace, get_all_places


def search_heritage(
    query: str | None = None,
    district: str | None = None,
    area: str | None = None,
    type: str | None = None,
    theme: str | None = None,
    popularity: str | None = None,
    locality_level: str | None = None,
) -> list[HeritagePlace]:

    places = get_all_places()

    results = []

    for place in places:

        # Text search
        if query:
            query_lower = query.lower()

            searchable_text = " ".join(
                [
                    place.name,
                    *place.aliases,
                    place.area,
                    place.description,
                    place.significance,
                    *place.themes,
                ]
            ).lower()

            if query_lower not in searchable_text:
                continue

        # District filter
        if district:
            if place.district.lower() != district.lower():
                continue

        # Area filter
        if area:
            if place.area.lower() != area.lower():
                continue

        # Type filter
        if type:
            if place.type.lower() != type.lower():
                continue

        # Theme filter
        if theme:
            if theme.lower() not in [
                item.lower() for item in place.themes
            ]:
                continue

        # Popularity filter
        if popularity:
            if place.popularity.lower() != popularity.lower():
                continue

        # Locality filter
        if locality_level:
            if place.locality_level.lower() != locality_level.lower():
                continue

        results.append(place)

    return results

def format_search_results(
    places: list[HeritagePlace],
) -> list[dict]:

    return [
        {
            "id": place.id,
            "name": place.name,
            "area": place.area,
            "district": place.district,
            "type": place.type,
            "themes": place.themes,
            "popularity": place.popularity,
            "locality_level": place.locality_level,
            "significance": place.significance,
        }
        for place in places
    ]