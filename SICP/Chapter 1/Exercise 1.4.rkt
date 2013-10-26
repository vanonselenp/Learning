;Exercise 1.4

(define (a-plus-abs-b a b)
  ((if (> b 0) + -) a b))

;This procedure first evaluates whether to use a add or subtract. 
;then it evaluates the resulting procedure with a and b