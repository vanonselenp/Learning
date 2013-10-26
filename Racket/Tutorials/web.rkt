#lang web-server/insta

(struct post (title body))

(define first (post "First Post!" "test of the broadcast system"))

(define blog 
  (list (post "Second post?" "more test because fun?")
        first))

(define (start request)
  (local [(define a-blog
            (cond [(can-parse-post? (request-bindings request))
                   (cons (parse-post (request-bindings request))
                         blog)]
                  [else
                   blog]))]
    (render-blog-page a-blog request)))

(define (render-blog-page a-blog request)
  (response/xexpr
   `(html (head (title "Blog of stuff"))
          (body (h1 "The Blog of Doom")
                ,(render-posts a-blog)
                (form
                 (input ((name "title")))
                 (input ((name "body")))
                 (input ((type "submit"))))))))

(define (render-posts posts)
   `(div ((class "posts")) 
         ,@(map render-post posts)))

(define (render-post p)
   `(div ((class "post")) 
         (h2 ,(post-title p)) 
         (p ,(post-body p))))

(define (can-parse-post? bindings)
  (and 
   (exists-binding? 'title bindings)
   (exists-binding? 'body bindings)))

(define (parse-post bindings)
  (post (extract-binding/single 'title bindings)
        (extract-binding/single 'title bindings)))


  


#| This is code i figured out along the way

;not sure what this is doing. need to deconstruct it
(define xexpr/c
  (flat-rec-contract
   xexpr
   (or/c string? 
         (cons/c symbol? (listof xexpr))
         (cons/c symbol? 
                 (cons/c (listof (list/c symbol? string?))
                         (listof xexpr))))))

(define (render-greeting a-name)
  (response/xexpr
   `(html (head (title "Welcome"))
          (body (p ,(string-append "Hello " a-name))))))

(define (render-as-itemized-list fragments)
  `(ul ,@(map render-as-item fragments)))

(define (render-as-item fragment)
  `(li ,fragment))
|#