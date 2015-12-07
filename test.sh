sbcl --load ./deps/lisp-unit.lisp \
     --load ./deps/split-sequence.lisp \
     --load day1.lisp \
     --load day2.lisp \
     --load day3.lisp \
     --eval "(run-tests)" \
     --non-interactive 2> /tmp/advent_test.err | grep -E "TOTAL:.*0 failed*" || cat /tmp/advent_test.err
