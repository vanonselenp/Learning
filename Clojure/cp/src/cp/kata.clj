(ns kata.cp)

;Constraints on Design

;No conditional (if, cond, switch, etc)
;No loop mechanism (for, while, loop, do, etc)

(defn create-string [character amount] 
	(apply str (map (fn [n] character) (range 0 amount))))

(defn generate-data [lines]
	(map (fn [n] [(- lines n) (- (* 2 n) 1)]) (range 1 (+ lines 1))))

(defn gen-tree [lines]
	(map (fn [x] (str (create-string " " (first x)) (create-string "*" (second x))))
		(generate-data lines)))

(defn draw [lines]
	(apply str (map println (gen-tree lines))))

