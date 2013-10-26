#lang racket
;The sum of the primes below 10 is 2 + 3 + 5 + 7 = 17.
;Find the sum of all the primes below two million.
(define (is-prime? x)
  (define (prime-sub current)
    (cond ((> (* current current) x) #t)
          ((and (> x 2) (= (modulo x 2) 0)) #f)
          ((= (modulo x current) 0) #f)
          (else (prime-sub (+ current 1)))))
  (prime-sub 2))

(define (sum-prime under)
  (stream-fold + 0 (stream-filter is-prime? (in-range 2 under))))
