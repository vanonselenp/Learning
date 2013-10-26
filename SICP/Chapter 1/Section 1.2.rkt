 ;Section 1.2 

;recursive
(define (factorial n)
  (if (= n 1)
      1
      (* n (factorial (- n 1)))))

;iterative
(define (factorial1 n)
  (fact-iter 1 1 n))

(define (fact-iter product counter max-count)
  (if (> counter max-count)
      product
      (fact-iter (* counter product)
                 (+ counter 1)
                 max-count)))