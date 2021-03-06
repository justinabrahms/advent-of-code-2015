(use-package :lisp-unit)

(defun santa-elevator (cmd-str)
  (reduce '+ (map 'list (lambda (x) (if (equal x #\)) -1 1)) cmd-str)))

(define-test santa-answer
  (assert-equal 0 (santa-elevator "(())"))
  (assert-equal 0 (santa-elevator "()()"))
  (assert-equal 3 (santa-elevator "((("))
  (assert-equal 3 (santa-elevator "(()(()("))
  (assert-equal -1 (santa-elevator "())"))
  (assert-equal -1 (santa-elevator "))("))
  (assert-equal -3 (santa-elevator ")))"))
  (assert-equal -3 (santa-elevator ")())())")))


(defun count-floors (x)
  (if (equal x #\)) -1 1))

(defun inner-santa-nb (cmds current-floor count)
  (if cmds
      (if (equal 0 (+ (first cmds) current-floor))
          (+ 1 count)
          (inner-santa-nb (rest cmds) (+ (first cmds) current-floor) (+ 1 count)))
      count))

                                        ;returns the number in the string that causes santa to enter the basement.
(defun santa-no-basement (cmd-str)
  (inner-santa-nb (map 'list 'count-floors cmd-str) 1 0))

(define-test no-basement-tests
  (assert-equal 1 (santa-no-basement ")"))
  (assert-equal 1 (santa-no-basement ")(("))
  (assert-equal 5 (santa-no-basement "()())")))

