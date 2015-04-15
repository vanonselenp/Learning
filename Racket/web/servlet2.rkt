#lang racket

(require web-server/servlet
         web-server/servlet-env)

(define (start req)
  (response/xexpr
   `(html (head (title "hellow world 2"))
          (body (p "paragraph text")))))

(serve/servlet start 
               #:port 8080
               #:extra-files0=-paths)