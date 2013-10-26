#lang racket

;2^15 = 32768 and the sum of its digits is 3 + 2 + 7 + 6 + 8 = 26.
;What is the sum of the digits of the number 2^1000?

(define (power-digit-sum base exponent)
  (foldl + 0 (map (lambda (x) (string->number (list->string (list x)))) (string->list (number->string (expt base exponent))))))