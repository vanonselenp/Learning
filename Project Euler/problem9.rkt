#lang racket
;A Pythagorean triplet is a set of three natural numbers, a < b < c, for which,
;a^2 + b^2 = c^2
;For example, 3^2 + 4^2 = 9 + 16 = 25 = 5^2.
;9 + 16 + 25 = 50
;3 + 4 + 5 = 12
;There exists exactly one Pythagorean triplet for which a + b + c = 1000.
;Find the product abc.

;When m and n are any two positive integers (m < n):
;a = n^2 - m^2
;b = 2nm
;c = n^2 + m^2
;Then, a, b, and c form a Pythagorean Triple.

;set a b, derive c, 
(define (square x) (* x x))

(define (get-a m n)
  (- (square n) (square m)))

(define (get-b m n)
  (* 2 m n))

(define (get-c m n)
  (+ (square n) (square m)))

(define (triple m n)
  (+ (get-a m n) (get-b m n) (get-c m n)))

(define (calc target m n)
  (cond ((= (triple m n) target) (* (get-a m n) (get-b m n) (get-c m n)))
        ((> (triple m n) target) (calc target (+ m 1) (+ m 2)))
        (else (calc target m (+ n 1)))))