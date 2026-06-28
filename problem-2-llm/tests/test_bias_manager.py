from pprint import pprint

from services.bias.manager import BiasManager


def main():

    manager = BiasManager()

    pprint(manager.run())


if __name__ == "__main__":
    main()