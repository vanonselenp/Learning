#lang racket

;The prime factors of 13195 are 5, 7, 13 and 29.
;What is the largest prime factor of the number 600851475143 ?

(define (is-prime? x)
  (define (sub-prime current)
    (cond ((> current (/ x 2)) #t)
          ((and (> x 2) (= (modulo x 2) 0)) #f)
          ((= (modulo x current) 0) #f)
          (else (sub-prime (+ 1 current)))))
  (sub-prime 2))

(define (factors x)
  (define (sub-factors y current max)
    (cond ((> current y) (display max))
          ((is-prime? current) (cond ((= (modulo y current) 0) 
                                      (sub-factors (/ y current) 2 (cond ((> current max) current) (else max))))
                                     (else (sub-factors y (+ 1 current) max))))
          (else (sub-factors y (+ 1 current) max))))
  (sub-factors x 2 0))
