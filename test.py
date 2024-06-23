from Tank.base import APIClientFactory, load_config


def main():
    # Load configuration
    config = load_config('config.yaml')
    print(config)

main()