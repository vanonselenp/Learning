#lang web-server/insta

(struct post (title body))

(define first (post "First post" "this is only a test of the emergency broadcast system"))

(define blog (list first))

(define (start request)
  (response/xexpr 
   `(html 
     (head (title "Blog Example from racket continue"))
     (body ,(render-post first)))))

(define (render-post post)
   `(div ((class "post"))
         (h1 ,(post-title post)) 
         (p ,(post-body post))))
           
(define (render-greeting name)
  (response/xexpr 
   `(html (head (title "Welcome"))
          (body (p ,(string-append "hello " name))))))