from src.function.iterator import TIterator, UIterator


def test_cases_checker():
    result = {}
    it = UIterator('../../data/analysis/user_iterator.json')
    while it.next():
        print(1)


if __name__ == '__main__':
    test_cases_checker()
