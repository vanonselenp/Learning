#lang racket

(require web-server/servlet-env
         web-server/servlet/web
         web-server/http
         web-server/managers/none)
(provide interface-version manager start)

(define interface-version 'v2)
(define manager
  (create-none-manager 
   (lambda (req)
     (response/xexpr 
      `(html (head (title "no continuations here"))
             (body (h1 "continuations not here")))))))
(define (start req)
  (response/xexpr
   `(html (head (title "hello world"))
          (body (h1 "hi all")))))

(send/back
 (response/xexpr
  `(html (body (h1 "the sum is ", (+ first-number second-number))))))

(serve/servlet start)

