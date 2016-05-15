from marchgl import March
import sys

def main():
    args = sys.argv

    if len(args) == 1:
        march = March(256, 256, 2)
    elif len(args) == 4:
        march = March(args[1], args[2], args[3])
    else:
        print 'Usage: march.py [width, height, scale]'

    march.start()

if __name__ == '__main__':
    main()
