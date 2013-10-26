#lang racket
;By listing the first six prime numbers: 2, 3, 5, 7, 11, and 13, we can see that the 6th prime is 13.
;What is the 10 001st prime number?

(define (is-prime? x)
  (define (sub-prime current)
    (cond ((> current (/ x 2)) #t)
          ((and (> x 2) (= (modulo x 2) 0)) #f)
          ((= (modulo x current) 0) #f)
          (else (sub-prime (+ current 1)))))
  (sub-prime 2))

(define (find-prime target)
  (define (find-sub current found)
    (cond ((>= found target) (- current 1))
          ((is-prime? current) (find-sub (+ current 1) (+ found 1)))
          (else (find-sub (+ current 1) found))))
  (find-sub 2 0))
                             