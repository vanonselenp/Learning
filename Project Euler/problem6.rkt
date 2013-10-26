#lang racket
;The sum of the squares of the first ten natural numbers is,
;1^2 + 2^2 + ... + 10^2 = 385
;The square of the sum of the first ten natural numbers is,
;(1 + 2 + ... + 10)^2 = 552 = 3025
;Hence the difference between the sum of the squares of the first ten natural numbers and the square of the sum is 3025  385 = 2640.
;Find the difference between the sum of the squares of the first one hundred natural numbers and the square of the sum.

(define (calc range-end)
  (define (square x)
    (* x x))
  (- (square (for/sum ([x (in-range 1 (+ 1 range-end))]) x))
     (for/sum ([x (stream-map (lambda (x) (square x)) (in-range 1 (+ 1 range-end)))]) x)))
