Introduction:
=============

Here are some Racket resources to help the reviewer run and test the code that
I have provided:
* The IDE download:  http://racket-lang.org (small and open source)
* A very quick and concise reference guide: 
	- http://learnxinyminutes.com/docs/racket/

Once installed, open "AmazonCodePuzzle.rkt" in DrRacket, and click Run.

I have provided some test data in the file.


The O Notation Complexity of the Algorithm:
===========================================

In Racket all lists are by default immutable so getting the length of a list
is of O(1).

In the provided algorithm there are no nested iterations of the entire
dataset. The main pair of iterations maps a function across each sentence and
then sorts the result of that map which is O(2n). Which simplifies to O(n).

In the rest of the algorithm there are no nested iterations and each iteration
happens on subsets of the data.

This is however a functional solution with immutable data. This means it is a
space heavy solution. Each time the lists are updated, Racket is creating new
lists in memory in the background. However it would be relatively easy to
increase its processing speed by parallelizing the map across the entire
dataset.
