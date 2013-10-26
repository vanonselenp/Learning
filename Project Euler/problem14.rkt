#lang racket
;The following iterative sequence is defined for the set of positive integers:
;n  n/2 (n is even)
;n  3n + 1 (n is odd)
;Using the rule above and starting with 13, we generate the following sequence:
;13 -> 40 -> 20 -> 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1
;It can be seen that this sequence (starting at 13 and finishing at 1) contains 10 terms. Although it has not been proved yet (Collatz Problem), it is thought that all starting numbers finish at 1.
;Which starting number, under one million, produces the longest chain?
;NOTE: Once the chain starts the terms are allowed to go above one million.

(define (even n) (/ n 2))
(define (odd n) (+ (* 3 n) 1))

(define (apply a)
  (define (sub n terms)
    (cond ((= n 1) (length (append terms (list n))))
          ((= (modulo n 2) 0) (sub (even n) (append terms (list n))))
          (else (sub (odd n) (append terms (list n))))))
  (sub a '()))

(define (chain2 from to current max-value max-terms)
  (define result (apply current))
  (cond ((> current to) max-value)
        ((> result max-terms) (chain2 from to (+ current 1) current result))
        (else (chain2 from to (+ current 1) max-value max-terms))))
        

(define (chain from to)
  (stream->list (stream-fold (lambda (x r) 
                               (cond ((> (second x) (second r)) x) 
                                     (else r))) 
                             '(0 0) 
                             (stream-map (lambda (x) 
                                           (list x (apply x))) 
                                         (in-range from (+ 1 to))))))