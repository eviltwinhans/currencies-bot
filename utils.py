import json
import requests
from config import APIKEY, currency_codes


class ConversionException(Exception):
    pass


class MoneyConverter:
    @staticmethod
    def convert(amount: str, base: str, quote: str):
        if quote == base:
            raise ConversionException("Please specify *two different* currencies.")

        if base not in currency_codes.values():
            raise ConversionException(f"Failed to process *{base}* currency.")

        if quote not in currency_codes.values():
            raise ConversionException(f"Failed to process *{quote}* currency.")

        try:
            amount = float(amount)
        except ValueError:
            raise ConversionException(f"Failed to process *{amount}* amount.")

        url = "https://api.apilayer.com/fixer/latest"
        querystring = {"base": base, "symbols": quote}
        headers = {"apikey": APIKEY}
        response = requests.request("GET", url, headers=headers, params=querystring)
        rate = json.loads(response.content)['rates'][quote]

        return rate * amount
