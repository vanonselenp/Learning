(ns threads.core)

(defn get-document []
	{:url "http://www.mozilla.org/about/manifesto.en.html"
	 :title "The Mozilla Manifesto"
	 :mime "text/html"
	 :content (delay (slurp "http://www.mozilla.org/about/manifesto.en.html"))})

(def p (promise))

(deliver p 42)