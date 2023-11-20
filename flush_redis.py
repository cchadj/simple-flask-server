import os
import sys

import redis


def main() -> int:
    # ask for confirmation
    print("This will flush all Redis data. Are you sure? (y/N)")
    answer = input()

    if answer != "y":
        print("Aborting")
        return os.EX_OK

    r = redis.Redis()
    r.flushall()
    print("Redis flushed")

    return os.EX_OK


if __name__ == "__main__":
    sys.exit(main())
