#lang racket
#|
The following algorithm generates the next permutation lexicographically after a given permutation. 
It changes the given permutation in-place.
* Find the largest index k such that a[k] < a[k + 1]. If no such index exists, the permutation is the last permutation.
* Find the largest index l such that a[k] < a[l].
* Swap the value of a[k] with that of a[l].
* Reverse the sequence from a[k + 1] up to and including the final element a[n].
DCFEBA”. The next permutation in sorted order should be “DEABCF”. 
(0 1 2)(0 2 1)(1 0 2)(1 2 0)(2 0 1)(2 1 0)(1 0 2)
 0 1 2  0 2 1  1 0 2  1 2 0  2 0 1  2 1 0
|#

(define data '(0 1 2 3 4 5 6 7 8 9))
(define sub '(0 1 2))

(define (find-k lst)
  (define (loop index max)
    (cond ((= index (- (length lst) 1)) max)
          ((< (list-ref lst index) (list-ref lst (+ 1 index))) (loop (+ 1 index) index))
          (else (loop (+ 1 index) max))))
  (loop 0 0))

(define (find-l lst k)
  (define (loop index max)
    (cond ((= index (length lst)) max)
          ((and (> (list-ref lst index) (list-ref lst k)) 
                (< (list-ref lst index) (list-ref lst max))) 
           (loop (+ 1 index) index))
          (else (loop (+ index 1) max))))
  (loop (+ k 1) (+ k 1)))

(define (swap lst k l)
  (append (take lst k) 
          (list (list-ref lst l)) 
          (reverse (append (take (drop lst (+ k 1)) (- (- l k) 1)) 
                           (list (list-ref lst k)) 
                           (drop lst (+ l 1))))))

(define (lex lst target)
  (define (loop current temp)
    (cond ((>= current target) temp)
          (else (define k (find-k temp))
                (define l (find-l temp k))
                (loop (+ 1 current) (swap temp k l)))))
  (string->number (foldr string-append "" (map (lambda (x) 
                                                 (number->string x)) (loop 1 lst)))))

(lex data 1000000)

;2783915406
;2783915460