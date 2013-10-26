#lang racket

;A palindromic number reads the same both ways. The largest palindrome made 
;from the product of two 2-digit numbers is 9009 = 91 99.
;Find the largest palindrome made from the product of two 3-digit numbers.

(define (create-list x y)
  (string->list (number->string (* x y))))

(define (compare x y)
  (cond ((and (equal? (cdr y) '()) (equal? (cdr x) '())) #t)
        ((equal? (car y) (car x)) (compare (cdr x) (cdr y)))
        (else #f)))

(define (palindrome start end)
  (define (pal-compare max)
    (for ([x (in-range start (+ 1 end))])
      (for ([y (in-range start (+ 1 end))])
        (when (compare (create-list x y) (reverse (create-list x y)))
          (when (> (* x y) max) (set! max (* x y))))))
    max)
  (pal-compare 0))
      
          
            