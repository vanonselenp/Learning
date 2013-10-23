(ns conway.core-test
  (:require [clojure.test :refer :all]
            [conway.core :refer :all]))

(deftest nieghbours-generation
	(testing "Given a coordinate When generating neighbours Then coordinate isn't include in the list"
		(def actual (set (neighbours [1 2])))
		(is (= (contains? actual [1 2]) false)))
	
	(testing "Given coordinate when generating neighbours then 8 neighbours are returned"
		(def actual (neighbours [1 2]))
		(is (= 8 (count actual)))))

(deftest conway-rules
	(testing "given an empty world when step then world is empty"
		(def world #{})
		(def actual (step world))
		(is (= 0 (count actual))))
	
	(testing "given world with one cell when step then world is empty"
		(def world #{[1 1]})
		(def actual (step world))
		(is (= 0 (count actual))))
	
	(testing "given a live cell with 2 neighbours when step then cell is alive and neighbours are dead"
		(def world #{[0 0] [1 1] [2 2]})
		(def actual (step world))
		(is (= 1 (count actual)))
		(is (contains? actual [1 1])))

	(testing "given a live cell with 3 neighbours when step then cell is alive"
		(def world #{[1 1] [1 2] [1 3] [2 2]})
		(def actual (step world))
		(is (contains? actual [1 2])))

	(testing "given a dead cell with 3 neighbours when step then cell is alive"
		(def world #{[1 1] [1 3] [2 2]})
		(def actual (step world))
		(is (contains? actual [1 2])))

	(testing "given a live cell has more than 3 neighbours when step then cell is dead"
		(def world #{[1 1] [1 2] [1 3] [2 2] [2 1]})
		(def actual (step world))
		(is (not (contains? actual [1 2])))))


