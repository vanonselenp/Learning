#lang web-server/insta

(define (start req) 
  (response/xexpr
   `(html (head (title "Hello world!!"))
          (body (p "hey out there")))))

(static-files-path "/Users/petervanonselen/Downloads")

