;Exercise 1.10
(define (A x y)
  (cond ((= y 0) 0)
        ((= x 0) (* 2 y))
        ((= y 1) 2)
        (else (A (- x 1)
                 (A x (- y 1))))))

;2n
(define (f n) (A 0 n)) 

;2^n
(define (g n) (A 1 n))

;
(define (h n) (A 2 n))

;5n^2
(define (k n) (* 5 n n))

;Tests
(A 1 10)
(A 2 4)
(A 3 3)

(g 1)
(g 2)
(g 3)
(g 4)
(g 5)
(g 6)

(h 1)
(h 2)
(h 3)
(h 4)

