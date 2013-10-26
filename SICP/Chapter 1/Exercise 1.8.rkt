;Exercise 1.8

(define (cube x)
  (cube-iter 1 0 x))

(define (cube-iter guess previous x)
  (if (good-enough? guess previous) guess
      (cube-iter (improve guess x)
                 guess
                 x)))

(define (good-enough? guess previous)
  (< (abs (- guess previous)) 0.001))

(define (square x) (* x x))

(define (improve y x)
  (/ (+ (/ x (square y)) 
        (* 2 y)) 
      3))

;Tests
(cube 27.0)  ;expect 3
(cube 125.0) ;expect 5