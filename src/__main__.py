from src.utils import Model, Parser
from rich.traceback import install
install()

def main():
    parser = Parser()
    model = Model(parser)
    model.test_collect_tokens()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)
    except BaseException as e:
        print(e)