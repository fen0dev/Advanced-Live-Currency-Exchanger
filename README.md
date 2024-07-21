# Overview

The Advanced Live Currency Converter is a Python-based command-line tool that provides real-time and historical currency conversion capabilities. It supports multiple base currencies, automatic updates, detailed logging, and an interactive mode for user-friendly conversions. This tool is ideal for developers and users who need accurate and up-to-date exchange rates for financial calculations or travel planning.

# Features

    Real-Time Exchange Rates: Fetches the latest exchange rates for over 150 currencies.
    Historical Exchange Rates: Allows fetching and converting historical exchange rates.
    Multiple Base Currencies: Supports conversion from any specified base currency.
    Automatic Updates: Periodically updates exchange rates based on user-defined intervals.
    Interactive Mode: Provides a user-friendly interactive mode for currency conversion.
    Multiple Conversions: Supports batch processing of multiple conversion requests.
    Detailed Logging: Logs detailed information and errors for better traceability.
    Configuration File: Allows saving and loading configuration settings.

# Usage

- Basic Conversion

 Convert an amount from one currency to another:

    python currency_converter.py 100 USD EUR

- Update Exchange Rates

 Fetch and update the latest exchange rates:

    python currency_converter.py 100 USD EUR --update

- Specify Base Currency

 Use a different base currency for conversion:

    python currency_converter.py 100 USD EUR --base GBP

- Fetch Historical Rates

 Get historical exchange rates for a specific date:

    python currency_converter.py 100 USD EUR --date 2023-01-01

- Multiple Conversions

 Process multiple conversions in one command:

    python currency_converter.py --multiple 100,USD,EUR 50,EUR,JPY

- Automatic Updates

 Automatically update rates every specified number of hours:

    python currency_converter.py --auto-update 24

- Interactive Mode

 Enter interactive mode for manual currency conversions:

    python currency_converter.py --interactive

# Installation

 Clone the repository:

    git clone https://github.com/fen0dev/Advanced-Live-Currency-Exchanger.git

 Navigate to the project directory:

    cd Advanced-Live-Currency-Exchanger

Install the required dependencies:

    pip install -r requirements.txt

# Configuration

 You can save and load configuration settings using a config.json file. This file allows setting default base currency, update intervals, and more.
 License

This project is licensed under the MIT License.

# Contribution

Contributions are welcome! Please fork the repository and submit a pull request.
