#lang racket

(define data (for/list ([x (in-range 0 3)])
    (for/list ([y (in-range 0 3)])
      (list x y))))

(define (down l)
  (list (first l) (+ 1 (second l))))

(define (right l)
  (list (+ 1 (first l)) (second l)))

(define (tran x y)
  (define (transverse l)
    (cond ((and (= (first l) x) (= (second l) y)) 1)
          ((= (first l) x) (transverse (down l)))
          ((= (second l) y) (transverse (right l)))
          (else (+ (transverse (right l)) (transverse (down l))))))
  (transverse '(0 0)))

(define (t grid-size)
  (define (sub x y)
    (cond ((and (= x grid-size) (= y grid-size)) 1)
          ((= x grid-size) (sub x (+ y 1)))
          ((= y grid-size) (sub (+ x 1) y))
          (else (+ (sub x (+ y 1)) (sub (+ x 1) y)))))
  (sub 0 0))

;(2n)!
;-----
;n!^2
(define (square x) (* x x))

(define (t2 size)
  (/ (stream-fold * 1 (in-range 1 (+ 1 (* 2 size)))) (square (stream-fold * 1 (in-range 1 (+ 1 size))))))
