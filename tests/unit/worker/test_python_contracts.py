import os


def test_import_source(fixtures_dir):
    import importlib.machinery
    import inspect
    import sys

    contract_path = os.path.join(fixtures_dir, "python_contracts", "baln")

    # Import the source
    sys.path.insert(0, contract_path)  #
    loader = importlib.machinery.SourceFileLoader("this", os.path.join(contract_path, "balance.py"))
    # loader.load_module()

    # Same error as when we import it manually
    try:
        loader.load_module()
    except ValueError as e:

        print(e)
        # raise e

    # from iconservice import IconScoreBase, IconScoreDatabase
    # scores = IconScoreBase.__subclasses__()
    # contract_obj = scores[1]
    # contract = inspect.signature(contract_obj)
    #
    # sys.path.remove(contract_path)
