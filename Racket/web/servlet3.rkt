#lang racket

(require "servlet.rkt"
         web-server/servlet-env)

(serve/servlet start #:stateless? #t)