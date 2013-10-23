(ns conway.core)

(def empty-world #{})
(def glider #{[1 0] [2 1] [0 2] [1 2] [2 2]})
(def blinker #{[1 1] [1 2] [1 3]})

(defn neighbours [[x y]]
	(for [dx [-1 0 1] dy [-1 0 1] :when (not= 0 dx dy)]
		[(+ dx x) (+ dy y)]))

(defn step [world]
	(set (for [[cell v] (frequencies (mapcat neighbours world))
		  :when (or (= v 3) 
		  		    (and (= v 2) 
		  				 (contains? world cell)))]
		cell)))

