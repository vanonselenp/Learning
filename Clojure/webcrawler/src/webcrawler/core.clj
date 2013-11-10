(ns webcrawler.core)

(require '[net.cgrand.enlive-html])
(use '[clojure.string :only (lower-case)])
(import '(java.net URL MalformedURLException))

(def url-queue (LinkedBlockingQueue.))
(def crawled-urls (atom #{}))
(def word-freqs (atom {}))

(defn- links-from
	[base-url html]
	(remove nil? (for [link (enlive/select html [:a])]
		(when-let [href (-> link :attrs :href)]
			(try 
				(URL. base-url href)
				(catch MalformedURLException e))))))

(defn- words-from
	[html]
	(let [chunks (-> html 
					(enlive/at [:script] nil)
					(enlive/select [:body enlive/text-node]))]
		(->> chunks
			(mapcat (partial re-seq #"\w+"))
			(remove (partial re-matches #"\d+"))
			(map lower-case))))

