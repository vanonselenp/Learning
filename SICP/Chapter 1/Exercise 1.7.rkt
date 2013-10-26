;Exercise 1.7

(define (sqrt-custom x)
  (sqrt-iter 1.0 0 x))

(define (sqrt-iter guess previous-guess x)
  (if (good-enough? guess previous-guess)
      guess
      (sqrt-iter (improve guess x)
                 guess
                 x)))

;(define (good-enough? guess x)
;  (< (abs (- (square guess) x)) 0.001))

(define (good-enough? guess previous-guess)
  (< (abs (- guess previous-guess)) 0.001))

(define (square x) (* x x))
  
(define (improve guess x)
  (average guess (/ x guess)))
  
(define (average x y)
  (/ (+ x y) 2))

;after changing good enough to make the comparison between 2 versions of the guess
;the speed increased and it returned results from the large value.

;Tests
;any value less than the precision value of 0.001 will faile to get an accurate result
(sqrt-custom 0.0001)

;any value sufficeintly large as to force the interpreter to run out of memory
(sqrt-custom 100000000000000000)