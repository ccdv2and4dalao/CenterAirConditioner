def raise_xxx():
    raise Exception('xxx')


if __name__ == '__main__':
    try:
        raise_xxx()
    finally:
        print('qwq')
    assert False
