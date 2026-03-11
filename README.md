# Unofficial Python client for EquityRT API

Klient API w Pythonie z automatycznym failoverem między:

- `https://webstation-datagate1.equityrt.com`
- `https://webstation-datagate2.equityrt.com`
- `https://webstation-datagate3.equityrt.com`

## Szybki start

```python
from equityrt_api_client import EquityRTClient

client = EquityRTClient()
client.authenticate(username="email@email.com", password="YOUR_PASSWORD")

# Echo
echo_result = client.echo(version="2.6.5.471", echo=402710)
print(echo_result)

# AddIn (lista funkcji dostępnych w tej wersji)
addin_result = client.add_in(version="2.6.5.471")
print(addin_result)

# FunctionListSearchField (wyszukiwanie funkcji)
search_result = client.function_list_search_field(text="clos", source_code="PL")
print(search_result)

# SelectCountries (lista krajów)
countries_result = client.select_countries(classifications=[], zones=[])
print(countries_result)

# SourceList (lista giełd dla krajów)
sources_result = client.source_list(countries=["PL", "US", "DE"])
print(sources_result)

# SelectSecurities (lista indeksów / instrumentów na giełdzie)
securities_result = client.select_securities(
	source_code="ZAA",
	date1="2026-03-11",
	date2="2026-03-11",
)
print(securities_result)

# PopulateFormulaGrid
formula_grid_result = client.populate_formula_grid(
	formula_object_id="fte.787004",
	source_code="PL",
	grid_type="Search",
)
print(formula_grid_result)

# Invoke (uruchamianie funkcji)
invoke_result = client.invoke(
	functions=[
		{
			"I": 0,
			"F": "RasDaily",
			"A": [
				{"S": "PKN:PL"},
				{"D": 2024.0},
				{"S": "CLOSE"},
				{"S": "DEFAULT"},
				{"M": ""},
				{"D": 1.0},
			],
		}
	],
	culture_info={
		"DatePattern": "d.MM.yyyy",
		"DecimalSeparator": ",",
		"GroupSeparator": "_",
	},
)
print(invoke_result)
```

## Co jest zaimplementowane

- `EquityRTClient.authenticate(username, password, authentication_type="UsernamePassword", set_as_default_token=True)`
- `EquityRTClient.echo(version, echo, ua_cpu="AMD64")`
- `EquityRTClient.invoke(functions, token=None, culture_info=None)`
- `EquityRTClient.add_in(version, token=None)`
- `EquityRTClient.function_list_search_field(text, source_code, token=None)`
- `EquityRTClient.select_countries(classifications=None, zones=None, token=None)`

Lista giełd dla krajów (pusta lista krajów zwraca wszystkie):
`EquityRTClient.source_list(countries, token=None)`


- `EquityRTClient.select_securities(source_code, date1, date2, classifications=None, peers=None, is_financial_wizard=False, token=None)`
- `EquityRTClient.populate_formula_grid(formula_object_id, source_code, grid_type, token=None)`

## Jak działa failover

Każde wywołanie próbuje kolejno `datagate1 -> datagate2 -> datagate3`.  
Jeśli host zwróci błąd HTTP albo będzie niedostępny, klient automatycznie przechodzi do następnego.

## Uwaga

Endpointy używają formatu:

```json
{"jcontent": "<JSON jako string>"}
```

Klient robi to automatycznie, więc przekazujesz zwykłe obiekty Pythona.

## Testy integracyjne

Dodane są testy integracyjne w [tests/test_integration_equityrt_api.py](tests/test_integration_equityrt_api.py):

- pobranie spisu funkcji przez `AddIn`
- pobranie wartości akcji na dzień przez `Invoke` + `RasDaily`

Ustaw zmienne środowiskowe:

```bash
export EQUITYRT_TOKEN="YOUR_TOKEN"
export EQUITYRT_USERNAME="email@email.com" # opcjonalnie, do testu auth
export EQUITYRT_PASSWORD="YOUR_PASSWORD"   # opcjonalnie, do testu auth
export EQUITYRT_VERSION="2.6.5.471"   # opcjonalnie
export EQUITYRT_SYMBOL="PKN:PL"       # opcjonalnie
export EQUITYRT_DAY="2024"            # opcjonalnie
```

Uruchom:

```bash
python -m unittest tests/test_integration_equityrt_api.py -v
```

Jeśli `EQUITYRT_TOKEN` nie jest ustawiony, testy są automatycznie pomijane.

