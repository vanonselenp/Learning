#lang racket

(define (is-factor? value x)
  (if (= (modulo value x) 0) #t #f))

(define (factors value)
  (define (sub current max lst)
    (cond ((> current max) lst)
          (else (if (is-factor? value current)
                    (sub (+ current 1) (/ value current) (append lst (list current (/ value current))))
                    (sub (+ current 1) max lst)))))
  (remove value (remove-duplicates (sub 1 value '()))))

(define (summed-factors value)
  (foldl + 0 (factors value)))

(define (is-abundant? value)
  (if (> (summed-factors value) value) #t #f))

(define (abundant-numbers-below value)
  (stream->list (stream-filter is-abundant? (in-range 1 value))))

(define (abundant-sums abundants all upperbound)
  (define (sub i j lst)
    (cond ((>= j (length abundants)) lst)
          ((>= i (length abundants)) (sub 0 (+ 1 j) lst))
          (else (define current (+ (list-ref abundants i) (list-ref abundants j)))
                (if (< current upperbound)
                    (sub (+ i 1) j (remove current lst))
                    (sub (+ i 1) j lst)))))
  (remove-duplicates (sub 0 0 all)))
          
(define (non-abundant range)
  (abundant-sums (abundant-numbers-below range) 
                 (stream->list (in-range 1 range)) 
                 range))

(define (sum-non-abundant range)
  (foldl + 0 (non-abundant range)))

