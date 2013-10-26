#lang racket

;Peter van Onselen

(define (amazon-challenge lst)
  (define result (create-dict-with-luckyCount-and-string lst))
  (cond ((empty? result) '())
        ((= (length result) 1) (cdar result))
        (else (list (cdr (first result)) (cdr (second result))))))

(define (create-dict-with-luckyCount-and-string lst)
  (sort (map (lambda (str) 
               (list (lucky-word-count (remove-unlucky-characters str)) str)) 
             lst)
        #:key car >))

(define (lucky-word-count lst)
  (length (filter is-list-greater-than-3? lst)))

(define (is-list-greater-than-3? x)
  (if (> (length x) 3) #t #f))

(define (remove-unlucky-characters str)
  (define unlucky-alphabet '(#\b #\d #\f #\h #\j #\l #\n #\p #\r #\t #\v #\x #\z))
  (map (lambda (word) 
         (remove* unlucky-alphabet (string->list word))) 
       (string-split str)))

;setup test data
;---------------------------------------------------------
(define nothing '())

(define one-entry '("say aaaaah for the dentist"))

(define two-entries '("say aaaaah for the dentist"
                      "say aaaaah for the dentist with more aaaaah"))

(define test-data '("once upon a midnight dreary" 
                    "say aaaaah for the dentist" 
                    "lima is in peru" 
                    "three blind mice see how they run"))
                    
(define more-data '("this is a test of the emergency broadcast system"
                    "once more unto the breach dear friends once more as we fill the gap with our english dead"
                    "now is the winter of our discontent made glorious summer by this sun of york"
                    "cry havoc and let loose the dogs of war"))

;runs the code with test data
;---------------------------------------------------------
(amazon-challenge nothing)
(amazon-challenge one-entry)
(amazon-challenge two-entries)
(amazon-challenge test-data)
(amazon-challenge more-data)