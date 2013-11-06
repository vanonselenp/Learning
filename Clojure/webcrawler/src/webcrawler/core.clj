(ns webcrawler.core)

(require '[net.cgrand.enlive-html])
(use '[clojure.string :only (lower-case)])
(import '(java.net URL MalformedURLException))

(defn- links-from
	[base-url html]
	)