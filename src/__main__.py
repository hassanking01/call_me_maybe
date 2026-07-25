from rich.traceback import install

from utils import Model, Parser

install()


def main():
    parser = Parser()
    model = Model(parser)
    model.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)
    except BaseException as e:
        print(e)
