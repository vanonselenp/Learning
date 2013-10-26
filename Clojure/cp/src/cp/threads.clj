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
		any modification to a ref must happen in a transaction
		in transaction value? 

	dosync - the scope of a transaction
	alter - if all starting vals are the same when trying to commit then commit else restart
	commute -  
	ref-set - similar to alter, with no regard for contraints, used to reinitilize values
	)

(defn character [name & {:as opts}]
	(ref (merge {:name name :items #{} :health 500}
				opts)))

(def smaug (character "Smaug" :health 500 :strength 400 :items (set (range 50))))
(def bilbo (character "Bilbo" :health 100 :strength 100))
(def gandalf (character "Gandalf" :health 75 :mana 750))

(defn loot [from to]
	(dosync 
		(when-let [item (first (:items @from))]
			(alter to update-in [:items] conj item)
			(alter from update-in [:items] disj item))))

(wait-futures 1
	(while (loot smaug bilbo))
	(while (loot smaug gandalf)))

(count (:items @bilbo))

(map (comp count :items deref) [bilbo gandalf])
(filter (:items @bilbo) (:items @gandalf))

(= (/ (/ 120 3) 4) (/ (/ 120 4) 3))
(= ((comp #(/ % 3) #(/ % 4)) 120) ((comp #(/ % 4) #(/ % 3)) 120))

(def x (ref 0))

(time (wait-futures 5
	(dotimes [_ 1000]
		(dosync (alter x + (apply + (range 1000)))))
	(dotimes [_ 1000]
		(dosync (alter x - (apply + (range 1000)))))))

(time (wait-futures 5
	(dotimes [_ 1000]
		(dosync (commute x + (apply + (range 1000)))))
	(dotimes [_ 1000]
		(dosync (commute x - (apply + (range 1000)))))))

(defn flawed-loot [from to]
	(dosync
		(when-let [item (first (:items @from))]
			(commute to update-in [:items] conj item)
			(commute from update-in [:items] disj item))))

(wait-futures 1 
	(while (flawed-loot smaug bilbo))
	(while (flawed-loot smaug gandalf)))

(defn fixed-loot [from to]
	(dosync
		(when-let [item (first (:items @from))]
			(commute to update-in [:items] conj item)
			(alter from update-in [:items] disj item))))

(wait-futures 1 
	(while (fixed-loot smaug bilbo))
	(while (fixed-loot smaug gandalf)))

(defn attack [agressor target]
	(dosync
		(let [damage (* (rand 0.1) (:strength @agressor))]
			(commute target update-in [:health] #(max 0 (- % damage))))))

(defn heal [healer target]
	(dosync 
		(let [aid (* (rand 0.1) (:mana @healer))]
			(when (pos? aid)
				(commute healer update-in [:mana] -  (max 5 (/ aid 5)))
				(commute target update-in [:health] + aid)))))

(def alive? (comp pos? :health))

(defn play [character action other]
	(while (and 
		(alive? @character)
		(alive? @other)
		(action character other))
	(Thread/sleep (rand-int 50))))

(wait-futures 1
	(play bilbo attack smaug)
	(play smaug attack bilbo))

(map (comp :health deref) [smaug bilbo])

(defn reset-health []
	(dosync
		(alter smaug assoc :health 500)
		(alter bilbo assoc :health 100)))

(wait-futures 1
	(play bilbo attack smaug)
	(play smaug attack bilbo)
	(play gandalf heal bilbo))

(map (comp #(select-keys % [:name :health :mana]) deref) 
	[smaug bilbo gandalf])

(dosync (ref-set bilbo {:name "Mr Jones"}))

(defn enfore-max-health [name health]
	(fn [character-data]
		(or (<= (:health character-data) health)
			(throw (IllegalStateException. (str name " is already at max health!"))))))

(defn character [name & {:as opts}]
	(let [cdata 
			(merge 
				{:name name :items #{} :health 500}
				opts)
		  cdata (assoc cdata :max-health (:health cdata))
		  validators (list* (enfore-max-health name (:health cdata))
		  					(:validators cdata))]
		  (ref (dissoc cdata :validators)
		  	:validator #(every? (fn [v] (v %)) validators))))

(def smaug (character "Smaug" :health 500 :strength 400 :items (set (range 50))))
(def bilbo (character "Bilbo" :health 100 :strength 100))
(def gandalf (character "Gandalf" :health 75 :mana 750))

(dosync (alter bilbo assoc-in [:health] 95))

(defn heal [healer target]
	(dosync
		(let [aid (min (* (rand 0.1) (:mana @healer))
					   (- (:max-health @target) (:health @target)))]
		(when (pos? aid)
			(commute healer update-in [:mana] - (max 5 (/ aid 5)))
			(alter target update-in [:health] + aid)))))

(defn unsafe []
	(io! (println "writing to database ...")))

(def x (ref (java.util.ArrayList.)))

(wait-futures 2 
	(dosync 
		(dotimes [v 5]
			(Thread/sleep (rand-int 50))
			(alter x #(doto % (.add v))))))

(def x (ref 0))

(dosync 
	@(future (dosync (ref-set x 0)))
	(ref-set x 1))

(def a (ref 0 :min-history 50 :max-history 100))

(future (dotimes [_ 500] (dosync 
	(Thread/sleep 20)
	(alter a inc))))

@(future (dosync (Thread/sleep 1000) @a))

(ref-history-count a)

(comment
	VARS:
		
	)

























