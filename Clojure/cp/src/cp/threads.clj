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
		compare-and-set! - modifies state only if current val = old val
		reset! - sets state without regard to current state
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

(compare-and-set! xs :wrong "new value")

(compare-and-set! xs @xs "new value")

(def ys (atom 2000))

(reset! ys :y)

(comment
	Common between all reference types:

	deref - to dereference something (@)

	WATCHES:
		functions that observe changes in state
	add-watch - add a function to a reference that will be executed each time it is changed.
				takes [key source old new]
	remove-watch -
	identity - 

	VALIDATORS:
		to constrain a reference's state however you like
	:validator - add this option when creating an atom, ref, agent
	set-validator!
	)

;---------------------------------------------------
; Watches
;---------------------------------------------------
(defn echo-watch [key identity old new]
	(println key old "=>" new))

(def sarah (atom {:name "Sarah" :age 25}))

(add-watch sarah :echo echo-watch)

(swap! sarah update-in [:age] inc)

(add-watch sarah :echo2 echo-watch)

(remove-watch sarah :echo2)

(def history (atom ()))

(defn log->list [dest-atom key source old new]
	(when (not= old new)
		(swap! dest-atom conj new)))

(def sarah (atom {:name "Sarah", :age 25}))

(add-watch sarah :record (partial log->list history))

(swap! sarah update-in [:age] inc)

(swap! sarah assoc :wears-glasses? true)

(pprint @history)

;---------------------------------------------------
; Validators
;---------------------------------------------------

(def n (atom 1 :validator pos?))

(swap! n + 500)
(swap! n - 1000)

(def sarah (atom {:name "Sarah" :age 25}))

(set-validator! sarah :age)

(swap! sarah dissoc :age)

(set-validator! sarah #(or (:age %)
						   (throw (IllegalStateException. "People must have `:age`s!"))))

;---------------------------------------------------
; Refs
;---------------------------------------------------

(comment 
	REFS:
		synchronous, coordinated, STM
		atomic, consistent, isolated.

	)

(defn character [name & {:as opts}]
	(ref (merge {:name name :items #{} :health 500}) 
				opts))

(def smaug (character "Smaug" :health 600))

























