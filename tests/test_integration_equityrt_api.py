import os
import unittest

from equityrt_api_client import EquityRTClient


EQUITYRT_TOKEN = os.getenv("EQUITYRT_TOKEN")
EQUITYRT_USERNAME = os.getenv("EQUITYRT_USERNAME")
EQUITYRT_PASSWORD = os.getenv("EQUITYRT_PASSWORD")
EQUITYRT_VERSION = os.getenv("EQUITYRT_VERSION", "2.6.5.471")
EQUITYRT_SYMBOL = os.getenv("EQUITYRT_SYMBOL", "PKN:PL")
EQUITYRT_DAY = float(os.getenv("EQUITYRT_DAY", "2024"))


class TestEquityRTIntegration(unittest.TestCase):
    def setUp(self) -> None:
        self.client = EquityRTClient(token=EQUITYRT_TOKEN, timeout=20.0)

    @unittest.skipUnless(EQUITYRT_TOKEN, "Set EQUITYRT_TOKEN to run integration tests")
    def test_add_in_returns_function_catalog(self) -> None:
        response = self.client.add_in(version=EQUITYRT_VERSION)

        self.assertEqual(response.get("Status"), "Ok")
        result = response.get("Result", {})
        functions = result.get("functions", [])

        self.assertIsInstance(functions, list)
        self.assertGreater(len(functions), 0)

        function_names = [item.get("name") for item in functions if isinstance(item, dict)]
        self.assertIn("RasDaily", function_names)

    @unittest.skipUnless(
        EQUITYRT_USERNAME and EQUITYRT_PASSWORD,
        "Set EQUITYRT_USERNAME and EQUITYRT_PASSWORD to run auth test",
    )
    def test_authenticate_returns_token(self) -> None:
        token = self.client.authenticate(
            username=EQUITYRT_USERNAME,
            password=EQUITYRT_PASSWORD,
        )

        self.assertIsInstance(token, str)
        self.assertGreater(len(token), 10)
        self.assertEqual(self.client.token, token)

    @unittest.skipUnless(EQUITYRT_TOKEN, "Set EQUITYRT_TOKEN to run integration tests")
    def test_invoke_returns_daily_price(self) -> None:
        response = self.client.invoke(
            functions=[
                {
                    "I": 0,
                    "F": "RasDaily",
                    "A": [
                        {"S": EQUITYRT_SYMBOL},
                        {"D": EQUITYRT_DAY},
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

        self.assertEqual(response.get("Status"), "Ok")
        results = response.get("Results", [])
        self.assertGreater(len(results), 0)

        first = results[0]
        value = first.get("V", {})
        daily_value = value.get("D")

        self.assertIsInstance(daily_value, (int, float))


if __name__ == "__main__":
    unittest.main()
