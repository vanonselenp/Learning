These are quick come back to notes for the going through of the Clojure
programming book.

The section about the way that the datastructures can be used to be awesome.
this very quickly went a bit beyond me. need to come back and re read and
figure out what the hell they are talking about. the maze generation and
conway section was a bit wtf.

Concurrency Section

Delays - holds off evaluating something until it is called for the first time, then it caches it.

Futures - immediately starts evaluating in another thread and once complete, caches it. other calls to that future get the cached response.

Promises - similar to future and delay with the exception of not having anything to evaluate at creation. the value is delivered to it