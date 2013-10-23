(ns cp.core)

;the point of this project is to put the code of the clojure programming
;book.

(defn foo
  "I don't do a whole lot."
  [x]
  (println x "Hello, World!"))

(defn average
	[numbers]
	(/ (apply + numbers) (count numbers)))

(read-string "(+ 1 2)")

(def person {:name "John Smith" :city "Tardis"})

(:city person)

;an example of namespaces, a way of binding a var, keyword etc
;to a specific name so that if can be used multiple times.

;these are named values, sybols are the other named values (such as vars)

(def pizza
	{:name "Gino's"
	 :location "Robertsham"
	 ::location "43222 342432"})

(user/location pizza)

(name :user/location)
(namespace :user/location)

;anything that includes a / is indicating the namespace it is from

;regex any string wtih a # is treated as a regex

(re-seq #"(...) (...)" "foo bar")
;?? (re-seq #"(\d+)-(\d+)" "1-3")

;wait what? can comment out parts of a form with #_
(+ 1 2 3 #_(* 2 222) 8)

;lists
'(1 2 3 4) 		;lists
[1 2 3 4] 		;vectors
{:a "a" :b "b"}	;maps
#{1 2 3}		;set

(def x 1)
(def x "hello")

(let [a (inc (rand-int 6))
	  b (inc (rand-int 6))]
	(println (format "You rolled a %s and a %s" a b))
	(+ a b))

(defn hypot
	[x y]
	(let [x2 (* x x)
		  y2 (* y y)]
		(Math/sqrt (+ x2 y2))))

;Destructureing a vector
(def v [42 "foo" 99.2 [5 12]])

(let [[x y z] v] (+ x z))

(let [[x _ _ [y z]] v] (+ x y z))

(let [[x & rest] v] rest) ;rest is a var name not a keyword

(let [[x _ z :as original-vector] v]
	(conj original-vector (+ x z)))

;Destructuring a map
(def m {:a 5, :b 6
	    :c [7 8 9]
	    :d {:e 10 :f 11}
	    "foo" 88
	    42 false})

(let [{a :a b :b} m]
	(+ a b))

(let [{f "foo"} m]
	(+ f 12))

(def chas {:name "Chas" :age 31 :location "Johannesburg"})

(let [{:keys [name age location]} chas]
	(format "%s is %s years old and lives in %s." name age location))

(def user-info ["robert" 2011 :name "Bob" :city "Cape Town"])

(let [[username account-year & {:keys [name city]}] user-info] 
	(format "%s is in %s" username city))

(fn [x] (+ 10 x)) ;anoymous methods ... lambdas?

(def strange-adder 
	(fn adder-self-reference
		([x] (adder-self-reference x 1))
		([x y] (+ x y))))

(loop [x 5]
	(if (neg? x)
		x
		(recur (dec x))))

(defn embedded-repl
	[]
	(print (str (ns-name *ns*) ">>> "))
	(flush)
	(let [expr (read)
		  value (eval expr)]
	   (when (not= :quit value)
	   	  (println value)
	   	  (recur))))

(defn call-twice [f x]
	(f x)
	(f x))

(def squared-up
	(reduce 
		(fn [m v]
			(assoc m v (* v v))) 
		{}
		[ 1 2 3 4]))

(def only-strings (partial filter string?))

(only-strings ["a" 5 6 "b"])

(defn negated-sum-str
	[& numbers]
	(str (- (apply + numbers))))

(def negated-sum-str-2 (comp str - +))

(require '[clojure.string :as str])

;due to the \- this has to be copied to the repl and not run through 
;the auto evaluate run thing
(def camel->keyword (comp keyword
					      str/join
                          (partial interpose \-)
                          (partial map str/lower-case)
                          #(str/split % #"(?<=[a-z])(?=[A-Z])")))

(camel->keyword "CamelCaseAndOtherCoolThings")
(camel->keyword2 "CamelCaseAndOtherCoolThings")

(defn camel->keyword2
    [s]
    (->> (str/split s #"(?<=[a-z])(?=[A-Z])")
        (map str/lower-case)
        (interpose \-)
        str/join
        keyword))

(def camel-pairs->map (comp (partial apply hash-map)
                            (partial map-indexed (fn [i x]
                                (if (odd? i)
                                    x
                                    (camel->keyword x))))))

(camel-pairs->map ["CamelCase" 5])

(defn adder
    [n]
    (fn [x] (+ n x)))

(defn doubler
    [f]
    (fn [& args]
        (* 2 (apply f args))))

(def double-+ (doubler +))







