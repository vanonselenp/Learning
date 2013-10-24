(ns cp.threads)

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

(def files (repeat 100000
	(apply str (concat (repeat 1000 \space) "sunil: 617.555.2937, Betty: 508.555.2218"))))

(time (->> files
	(partition-all 250)
	(pmap (fn [chunk] (doall (map phone-numbers chunk))))
	(apply concat)
	dorun))

(def sarah {:name "Sarah" :age 25 :wears-glasses? false})

;reference types: var ref agent atom

@(atom 12)

(agent {:c 42})

(map deref [(agent {:c 42}) (atom 12) (ref "http/clojure.org") (var +)])

(comment
	Key clojure concepts:

	coordination: 
		coordinated: cooperation of multiple actors to not get in each others way
		uncoordinated: multiple actors are unable to impact each other negatively.

	synchronization:
		synchronous: caller thread blocks until access is obtained
		asynchronous: can start or stop without blocking intiating thread

				 | coordinated 	| uncoordinated
	-------------------------------------------
	synchronous  | refs 		| atoms
	asynchronous | 				| agents

	vars are for local threads, thus don't concern with above

	)

(defmacro futures [n & exprs]
	(vec (for [_ (range n)
		       expr exprs]
		       `(future ~expr))))

(defmacro wait-futures [& args]
	`(doseq [f# (futures ~@args)]
		@f#))

(comment
	atom 
		synchronous, uncoordinated, atomic compare-and-set
		when modifiying state, block until mod is complete
		each modification is isolated
		this is atomic, if atom value changed between get and update, it retrys with new value

		swap! - modify state
		update-in - ?
	)

(def sarah (atom {:name "Sarah" :age 25 :wears-glasses false}))

(swap! sarah update-in [:age] + 3)

(swap! sarah (comp #(update-in % [:age] inc)
				   #(assoc % :wears-glasses true)))

(def xs (atom #{1 2 3}))

(wait-futures 1 (swap! xs (fn [v]
							(Thread/sleep 250)
							(println "trying 4")
							(conj v 4)))
				(swap! xs (fn [v]
							(Thread/sleep 500)
							(println "trying 5")
							(conj v 5))))

(def x (atom 2000))

(swap! x #(Thread/sleep %))




























