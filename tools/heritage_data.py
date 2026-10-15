from pydantic import BaseModel
import json
from pathlib import Path

class Coordinates(BaseModel):
    latitude: float
    longitude: float


class Source(BaseModel):
    title: str
    url: str
    source_type: str


class HeritagePlace(BaseModel):
    id: str
    name: str
    aliases: list[str]
    area: str
    district: str
    type: str
    themes: list[str]
    significance: str
    description: str
    locality_level: str
    popularity: str
    coordinates: Coordinates
    sources: list[Source]
    verification_status: str
    last_verified: str

class HeritageDataset(BaseModel):
    version: str
    last_updated: str
    places: list[HeritagePlace]

DATA_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "goa_heritage_seed.json"
)



def load_heritage_data() -> HeritageDataset:
    """Load and validate the Goa heritage seed dataset."""

    with open(DATA_PATH, "r", encoding="utf-8") as file:
        raw_data = json.load(file)

    return HeritageDataset.model_validate(raw_data)

def get_all_places() -> list[HeritagePlace]:
    """Return all heritage places."""

    dataset = load_heritage_data()
    return dataset.places