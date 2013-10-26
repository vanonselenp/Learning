#lang racket
;You are given the following information, but you may prefer to do some research for yourself.
;1 Jan 1900 was a Monday.
;Thirty days has September,
;April, June and November.
;All the rest have thirty-one,
;Saving February alone,
;Which has twenty-eight, rain or shine.
;And on leap years, twenty-nine.
;A leap year occurs on any year evenly divisible by 4, but not on a century unless it is divisible by 400.
;How many Sundays fell on the first of the month during the twentieth century (1 Jan 1901 to 31 Dec 2000)?

(define days '((0 "Monday")
               (1 "Tuesday")
               (2 "Wednesday")
               (3 "Thursday")
               (4 "Friday")
               (5 "Saturday")
               (6 "Sunday")))

(define months '((1 31 "January")
                 (2 28 "Febuary")
                 (3 31 "March")
                 (4 30 "April")
                 (5 31 "May")
                 (6 30 "June")
                 (7 31 "July")
                 (8 31 "August")
                 (9 30 "September")
                 (10 31 "October")
                 (11 30 "November")
                 (12 31 "December")))

(define (is-leap? year)
  (cond ((= (modulo year 400) 0) #t)
        ((= (modulo year 100) 0) #f)
        ((= (modulo year 4) 0) #t)
        (else #f)))

(define (next-year-start current-year current-index)
  (list-ref days (modulo (+ 1 (if (is-leap? current-year) 1 0) current-index) 7)))

(define (sundays index)
  (if (>= index 4) 5 4))

(define (sum-sunday start end)
  (define (sub current-year current-index total)
    (cond ((> current-year end) total)
          (else (sub (+ current-year 1) (next-year-start current-year (first current-index)) (+ total (sundays (first current-index)))))))
  (sub start (next-year-start start 0) 0))
