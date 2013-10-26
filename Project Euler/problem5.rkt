#lang racket
;2520 is the smallest number that can be divided by each of the numbers from 1 to 10 without any remainder.
;What is the smallest positive number that is evenly divisible by all of the numbers from 1 to 20?

(define (even start end)
  (define (map-check value)
    (stream-andmap (lambda (x) (if (= (modulo value x) 0) #t #f)) (in-range start (+ 1 end))))
  (define (even-sub value)
    (if (map-check value) 
        value
        (even-sub (+ 1 value))))
  (even-sub 1))
      
