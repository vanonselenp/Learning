#lang racket

(define (is-divisor? value x)
  (if (= (modulo value x) 0)
      #t 
      #f))

(define (divisors value)
  (stream->list (stream-filter (lambda (x) (is-divisor? value x)) (in-range 1 value))))

(define (sum x)
  (foldl + 0 (divisors x)))

(define (amicable-numbers end)
  (stream-fold + 0 (stream-filter (lambda (x) (cond ((= x (sum x)) #f)
                                   ((= x (sum (sum x))) #t)
                                   (else #f)))
                 (in-range 1 end))))