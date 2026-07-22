from src.utils import Model, Parser
from rich.traceback import install
install()

def main():
    parser = Parser()
    model = Model(parser)
    model.run()

if __name__ == "__main__":
    main()
    # try:
    # except KeyboardInterrupt:
    #     pass
    # except Exception as e:
    #     print(e)
    # except BaseException as e:
    #     print(e)