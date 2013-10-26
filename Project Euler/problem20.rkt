#lang racket
 
(define (factorial x)
  (if (= x 1) x (* (factorial (- x 1)) x)))

(define (factorial-digit-sum number)
  (foldl + 0 (map (lambda (x) 
                    (string->number (list->string (list x)))) 
                  (string->list (number->string (factorial number))))))