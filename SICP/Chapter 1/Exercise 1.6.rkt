;Exercise 1.6

;What Happens:
;The program trys to evaluate the new if, which expands it, which then evaluates both the predicate
;and the two clauses then and else. This then calls the sqrt iter again which then evaluates new if 
;again. This creates an infinite loop which quickly runs out of memory.

;This happens due to if being a special case where the then and else clauses are not evaluated until
;they need to be based on the evaluation of if.

(define (sqrt-custom x)
  (sqrt-iter 1.0 x))

(define (new-if predicate then-clause else-clause)
  (cond (predicate then-clause)
        (else else-clause)))

(define (sqrt-iter guess x)
  (new-if (good-enough? guess x)
      guess
      (sqrt-iter (improve guess x)
                 x)))

(define (good-enough? guess x)
  (< (abs (- (square guess) x)) 0.001))

(define (square x) (* x x))
  
(define (improve guess x)
  (average guess (/ x guess)))
  
(define (average x y)
  (/ (+ x y) 2))