#lang racket

(require racket/date)

;(date-week-day (seconds->date (find-seconds 0 0 0 2 8 2013 #t)))

(define (months-per-year year)
  (build-list 12 (lambda (x) (seconds->date (find-seconds 0 0 0 1 (+ 1 x) year)))))

(define (how-many-sundays months)
  (length (filter (lambda (x) (if (= (date-week-day x) 0) #t #f)) months)))

(define (sum-sunday start end)
  (stream-fold + 0 (stream-map (lambda (x) (how-many-sundays (months-per-year x))) (in-range start end))))

;165 + 1 + 2 + 2
;this is done due to racket failing to process a date. wtf
(define year-1903 3)
(+ (sum-sunday 1904 2001) (sum-sunday 1901 1903) year-1903)