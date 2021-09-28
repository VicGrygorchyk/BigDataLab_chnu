import sys

from receiver import listen_queue


if __name__ == "__main__":
    try:
        listen_queue()
    except KeyboardInterrupt:
        print('Exiting listener app.')
        sys.exit(0)
