from repository import Repository
from adapters.legacy_adapter import LegacyAdapter
from adapters.json_adapter import JSONAdapter

legacy = Repository(LegacyAdapter())
json = Repository(JSONAdapter("migrated.json"))

for key, value in legacy.items():
    json[key] = value

json.store()
