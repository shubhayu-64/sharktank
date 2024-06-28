from pprint import pprint
from Tank.base import APIClientFactory, load_config
from Tank.yahoofinance_client import YahooFinanceAPIClient


def main():
    # Load configuration
    config = load_config('config.yaml')

    # Initialize APIClientFactory
    client_factory = APIClientFactory()
    
    # Register YahooFinanceAPIClient manually
    yahoo_finance_client = YahooFinanceAPIClient()
    client_factory.register_client('yahoo_finance', yahoo_finance_client)

    # Fetch live data for GOOGL using the registered client
    client = client_factory.get_client('yahoo_finance')
    nike_data = client.fetch_live_data('NKE')

    # nike_info = client.fetch_info('NKE')
    pprint(nike_data)

main()