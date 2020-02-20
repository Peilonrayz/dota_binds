import time
import sys
import curses

if False:
    def pbar(window):
        for i in range(10):
            j = str(i*10)
            window.addstr(0, 0, 'Time to download '+"[" + ("#" * i) + ("-" * (9 - i )) + "]"+' '*len(j)+j+'%')
            window.addstr(10, 10, "[" + ("#" * i) + ("-" * (9 - i )) + "]")
            window.refresh()
            time.sleep(0.5)

    curses.wrapper(pbar)

else:
    for i in range(11):
        sys.stdout.write("\r[{0}{1}] {2}%".format("#"*i, "-"*(10-i), i*10))
        sys.stdout.flush()
        time.sleep(0.5)
    print
