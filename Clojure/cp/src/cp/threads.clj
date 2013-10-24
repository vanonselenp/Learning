(ns threads.core)

(def d (delay 
	(println "Running ...")
	:done))

(defn get-document []
	{:url "http://www.mozilla.org/about/manifesto.en.html"
	 :title "The Mozilla Manifesto"
	 :mime "text/html"
	 :content (delay (slurp "http://www.mozilla.org/about/manifesto.en.html"))})

(def p (promise))

(deliver p 42)

;futures

(def long-calulation (future (apply + (range 1e9))))

(deref (future (Thread/sleep 5000) :done!)
	1000
	:impatient)

(defn get-document2 [id]
	{:url "http://www.mozilla.org/about/manifesto.en.html"
	 :title "The Mozilla Manifesto"
	 :mime "text/html"
	 :content (future (slurp "http://www.mozilla.org/about/manifesto.en.html"))})

;promises

(def p (promise))

(realized? p)

(deliver p 42)

(def a (promise))
(def b (promise))
(def c (promise))

(future
	(deliver c (+ @a @b))
	(println "Delivery complete"))

(deliver a 15)
(deliver b 16)

(defn call-service [arg1 arg2 callback-fn]
	(future (callback-fn (+ arg2 arg1) (- arg1 arg2))))

(defn sync-fn [async-fn]
	(fn [& args]
		(let [result (promise)]
			(apply async-fn (conj (vec args) #(deliver result %&)))
			@result)))

((sync-fn call-service) 8 7)

(defn phone-numbers [string]
	(re-seq #"(\d{3})[\.-]?(\d{3})[\.-]?(\d{4})" string))

(def files (repeat 100
	(apply str (concat (repeat 1000000 \space) "sunil: 617.555.2937, Betty: 508.555.2218"))))

(time (dorun (map phone-numbers files)))

(time (dorun (pmap phone-numbers files)))

;bad use of pmap
























