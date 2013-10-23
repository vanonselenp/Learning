(ns conway.display
  (:require [conway.core :refer :all]))

(import '(javax.swing JFrame JPanel)
	    '(java.awt Dimension Color)
	    '(java.awt.image BufferedImage))

(def size 800)

(defn paint-cell [graphics color cell-size [x y]]
    (.setColor graphics color)
    (.fillRect graphics
      (* x cell-size) (* y cell-size) cell-size cell-size))

(defn paint [panel game]
	(let [img (new BufferedImage size size (. BufferedImage TYPE_INT_ARGB))
          bg (.getGraphics img)
          graphics (.getGraphics panel)]
     	(doto bg 
     		(.setColor (. Color white))
     		(.fillRect 0 0 (. img (getWidth)) (. img (getHeight))))
		(doseq [cell game]
			(paint-cell bg Color/GREEN 10 cell))
		(. graphics (drawImage img 0 0 nil))
		(.dispose bg)))

(defn create-panel [width height]
  (proxy [JPanel] []
    (getPreferredSize [] (Dimension. width height))))

(defn draw []
	(def panel (create-panel size size))
	(def frame 
		(doto
			(new JFrame)
			(.setDefaultCloseOperation JFrame/EXIT_ON_CLOSE)
			(.add panel)
			(.pack)
  			(.setVisible true)))
	(loop [game glider]
		(paint panel game)
		(Thread/sleep 200)
		(recur (step game))))
