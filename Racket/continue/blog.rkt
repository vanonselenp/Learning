#lang web-server/insta

(define (start request)
  (response/xexpr 
   `(html 
     (head (title "Blog Example from racket continue"))
     (body (h1 "under construction")
           (p "come back later")))))
