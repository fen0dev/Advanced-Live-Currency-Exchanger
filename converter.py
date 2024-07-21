import requests
import json
import os
import argparse
from datetime import datetime, time
import logging

API_URL = f'https://v6.exchangerate-api.com/v6/bb6cb9e71dcceaa20d8d2851/latest'
HISTORICAL_API_URL = 'https://open.er-api.com/v6/historical'
CACHE_FILE = 'exchange_rates.json'
CONFIG_FILE = 'config.json'

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def fetch_exchange_rates(base_currency='EUR', date=None):
    url = f'{API_URL}/{base_currency}' if date is None else f'{HISTORICAL_API_URL}/{date}'
    response = requests.get(url)
    if response.status_code == 200:
        try:
            data = response.json()
            if 'rates' in data:
                return data['rates']
            else:
                logger.error("'rates' key not found in the response.")
                logger.error(f"Response data: {data}")
                return None
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON response: {e}")
            logger.error(f"Response text: {response.text}")
            return None
    else:
        logger.error(f"Error fetching exchange rates. Status code: {response.status_code}")
        logger.error(f"Response text: {response.text}")
        return None
    
def save_exchange_rates(rates, file_name=CACHE_FILE):
    with open(file_name, 'w') as file:
        json.dump(rates, file)
    logger.info("Exchange rates saved.")

def load_exchange_rates(file_name=CACHE_FILE):
    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            json.load(file)
    return None

def load_config(file_name=CONFIG_FILE):
    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            json.load(file)
    return {}

def save_config(config, file_name=CONFIG_FILE):
    with open(file_name, 'r') as file:
        json.dump(config, file, indent=4)
    logger.info("Configuration saved.")

def auto_update_rates(base_currency, interval=24):
    while True:
        fetch_exchange_rates(base_currency)
        time.sleep(interval * 3600)

def fetch_and_save_rates(base_currency):
    rates = fetch_and_save_rates(base_currency)
    if rates:
        save_exchange_rates(rates)

def convert_currency(amount, from_currency, to_currency, rates):
    if from_currency == 'EUR':
        conversion_rate = rates[to_currency]
    elif to_currency == 'EUR':
        conversion_rate = 1 / rates[from_currency]
    else:
        conversion_rate = rates[to_currency] / rates[from_currency]

    return amount * conversion_rate

def interactive_mode(rates):
    while True:
        amount = float(input("Enter amount to convert: "))
        from_currency = input("Enter currency to convert from (e.g., USD): ").upper()
        to_currency = input("Enter currency to convert to (e.g., EUR): ").upper()

        if from_currency not in rates or to_currency not in rates:
            print(f"Invalid currency code. Available currencies: {', '.join(rates.keys())}")
            continue

        converted_amount = convert_currency(amount, from_currency, to_currency, rates)
        print(f"{amount} {from_currency} = {converted_amount:.2f} {to_currency}")

def main():
    parser = argparse.ArgumentParser(description='Advanced Live Currency Converter')
    parser.add_argument('amount', type=float, nargs='?', help='Amount to convert')
    parser.add_argument('from_currency', type=str, nargs='?', help='Currency to convert from (e.g., USD)')
    parser.add_argument('to_currency', type=str, nargs='?', help='Currency to convert to (e.g., EUR)')
    parser.add_argument('--base', type=str, default='USD', help='Base currency for exchange rates (default: EUR)')
    parser.add_argument('--update', action='store_true', help='Update exchange rates')
    parser.add_argument('--date', type=str, help='Historical date for exchange rates (YYYY-MM-DD)')
    parser.add_argument('--multiple', nargs='+', help='Multiple conversions in format amount,from,to (e.g., 100,USD,EUR 50,EUR,JPY)')
    parser.add_argument('--auto-update', type=int, help='Automatically update rates every N hours')
    parser.add_argument('--interactive', action='store_true', help='Interactive mode for conversions')
    
    args = parser.parse_args()
    
    base_currency = args.base.upper()
    rates = None

    if args.update or args.date:
        if args.date:
            try:
                datetime.strptime(args.date, '%Y-%m-%d')
            except ValueError:
                logger.error("Invalid date format. Use YYYY-MM-DD.")
                return
            rates = fetch_exchange_rates(base_currency, args.date)
        else:
            rates = fetch_exchange_rates(base_currency)
        
        if rates:
            save_exchange_rates(rates)
    else:
        rates = load_exchange_rates()
        if not rates:
            logger.info("No local exchange rates found, fetching live rates...")
            rates = fetch_exchange_rates(base_currency)
            if rates:
                save_exchange_rates(rates)
    
    if not rates:
        logger.error("No rates available.")
        return

    if args.auto_update:
        auto_update_rates(base_currency, args.auto_update)
        return
    
    if args.interactive:
        interactive_mode(rates)
        return

    conversions = []
    if args.multiple:
        for conversion in args.multiple:
            amount, from_currency, to_currency = conversion.split(',')
            conversions.append((float(amount), from_currency.upper(), to_currency.upper()))
    else:
        conversions.append((args.amount, args.from_currency.upper(), args.to_currency.upper()))

    for amount, from_currency, to_currency in conversions:
        if from_currency not in rates or to_currency not in rates:
            print(f"Invalid currency code. Available currencies: {', '.join(rates.keys())}")
            continue
        
        converted_amount = convert_currency(amount, from_currency, to_currency, rates)
        print(f"{amount} {from_currency} = {converted_amount:.2f} {to_currency}")

if __name__ == '__main__':
    main()