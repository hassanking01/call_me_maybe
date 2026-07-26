from .model import Model
from .parser import Parser


def main() -> None:
    parser = Parser()
    model = Model(parser)
    model.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("""
 ▄████  ▄████▄ ▄████▄ ████▄  █████▄ ██  ██ ██████
██  ▄▄▄ ██  ██ ██  ██ ██  ██ ██▄▄██  ▀██▀  ██▄▄
 ▀███▀  ▀████▀ ▀████▀ ████▀  ██▄▄█▀   ██   ██▄▄▄▄
""")
    except Exception as e:
        print(e)
    except BaseException as e:
        print(e)
