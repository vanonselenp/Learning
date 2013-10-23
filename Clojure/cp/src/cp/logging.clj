(ns cp.logging)

(defn print-logger
	[writer]
	#(binding [*out* writer]
		(println %)))

(def *out*-logger (print-logger *out*))

(def writer (java.io.StringWriter.))

(def retained-logger (print-logger writer))

(require 'clojure.java.io)

(defn file-logger
    [file]
    #(with-open [f (clojure.java.io/writer file :append true)]
        ((print-logger f) %)))

(def log->file (file-logger "message.log"))

(log->file "Hello")

(defn multi-logger
    [& logger-fns]
    #(doseq [f logger-fns]
        (f %)))

(def grand-logger 
    (multi-logger
        (print-logger *out*)
        (file-logger "message.log")))

(defn timestapmed-logger
    [logger]
    #(logger (format "[%1$tY-%1$tm-%1$te] %2$s" (java.util.Date.) %)))

(def log-timestamped 
    (timestapmed-logger
        (multi-logger
            (print-logger *out*)
            (file-logger "message.log"))))

;----------------------------------------------

(require 'clojure.xml)

(defn twitter-followers
    [username]
    (->> (str "https://api.twitter.com/1.1/users/show.xml?screen_name=" username)
        clojure.xml/parse
        (filter (comp #{:followers_count} :tag))
        first
        :content
        first
        Integer/parseInt))

(defn twitter
    [username]
    (->> (str "https://api.twitter.com/1.1/users/show.json?screen_name=" username)))

;------------------------------------------------

(defn prime?
    [n]
    (cond 
        (== 1 n) false
        (== 2 n) true
        (even? n) false
        :else (->> (range 3 (inc (Math/sqrt n)) 2)
            (filter #(zero? (rem n %)))
            empty?)))

(let [m-prime? (memoize prime?)]
    (time (m-prime? 1235899906842679))
    (time (m-prime? 1235899906842679)))

(defn swap-pairs
    [sequential]
    (into (empty sequential)
        (interleave
            (take-nth 2 (drop 1 sequential))
            (take-nth 2 sequential))))

(defn map-map
    [f m]
    (into (empty m)
        (for [[k v] m]
            [k (f v)])))

(let [r (range 3) 
      rst (rest r)]
  (prn (map str rst))
  (prn (map #(+ 100 %) r))
  (prn (conj r -1) (conj rst 42)))

(let [s (apply list (range 1e6))]
    (time (count s)))

(defn random-ints
    [limit]
    (lazy-seq
        (cons (rand-int limit)
            (random-ints limit))))

(let [[t d] (split-with #(< % 12) (range 1e8))]
    [(count t) (count d)])

(if-let [[k v] (find {:a 5 :b 6} :a)]
    (format "found %s => %s" k v) "not found")

(defn magnitude 
    [x]
    (-> x Math/log10 Math/floor))

(defn compare-magnitude
    [a b]
    (- (magnitude a) (magnitude b)))

(defn compare-magnitude
    [a b]
    (let [diff (- (magnitude a) (magnitude b))]
        (if (zero? diff)
            (compare a b)
            diff)))

(defn interpolate
    [points]
    (let [results (into (sorted-map) (map vec points))]
        (fn [x]
            (let [[xa ya] (first (rsubseq results <= x))
                  [xb yb] (first (subseq results > x))]
                (if (and xa xb)
                    (/ (+ (* ya (- xb x)) (* yb (- x xa)))
                       (- xb xa))
                    (or ya yb))))))

(filter (comp (partial <= 25) :age)
    [{:age 21 :name "John"}
     {:gender f :name "Sarah Jane" :age 23}
     {:name "Amy" :age 34 :location "New York"}])

(defn reduce-by
    [key-fn f init col]
    (reduce (fn [summaries x]
        (let [k (key-fn x)]
            (assoc-in summaries k (f (summaries k init) x))))
    {} col))

(def orders
    [{:product "Tardis", :customer "Doctor", :qty 1, :total 10000}
     {:product "Sonic Screwdriver", :customer "Doctor", :qty 4, :total 100}
     {:product "Fez", :customer "Jones", :qty 8, :total 200}
     {:product "Bowtie", :customer "Jones", :qty 2, :total 400}
     {:product "Bowtie", :customer "Doctor", :qty 3, :total 100}
     {:product "Banana", :customer "Amy", :qty 4, :total 500}])

(reduce-by :customer #(+ %1 (:total %2)) 0 orders)

(reduce-by :product #(conj %1 (:customer %2)) '() orders)

(reduce-by (juxt :customer :product) #(+ %1 (:total %2)) 0 orders)

;mutablea datastructures do exist
(def x (transient []))

(defn faster-into
    [collection source]
    (persistent! (reduce conj! (transient collection) source)))

(def a ^{:created (System/currentTimeMillis)} [1 2 3])


















