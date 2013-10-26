#lang racket

(define sub-path "/Users/fallen/Documents/Development/Project Euler/sub.txt")
(define name-path "/Users/fallen/Documents/Development/Project Euler/names.txt")

(define (read-file path)
  (file->string path))

(define (format-data path)
  (map string->list 
       (sort (map (lambda (x) (string-trim x "\""))
                  (string-split (read-file path) ","))
             string<?)))

(define letters '((#\A 1)(#\B 2)(#\C 3)(#\D 4)(#\E 5)(#\F 6)(#\G 7)(#\H 8)(#\I 9)(#\J 10)(#\K 11)(#\L 12)(#\M 13)(#\N 14)(#\O 15)(#\P 16)(#\Q 17)(#\R 18)(#\S 19)(#\T 20)(#\U 21)(#\V 22)(#\W 23)(#\X 24)(#\Y 25)(#\Z 26)))

(define (name-value data)
  (foldl + 0 (map (lambda (x) (first (dict-ref letters x))) data)))

(define (name-value-of-list path)
  (map (lambda (x) (name-value x)) (format-data path)))

(define (name-scores path)
  (define data (name-value-of-list path))
  (define (sub counter len total)
    (cond ((> counter len) total)
          (else (sub (+ 1 counter) len (+ total (* counter (list-ref data (- counter 1))))))))
  (sub 1 (length data) 0)) 