# Carniprox

This is a small proxy to convert [Carnifex](https://github.com/TPolzer/Carnifex) api/v3 requests to the official contest API (2019).

It was written as a workaround for the FAU wintercontest to be able to use Carnifex and is a 'bit' hacky. A bit here means 'very', but it worked.

Idea: cArnifex requests informations from the proxy, the proxy converts the call to the new api, takes the answer from domjudge and converts it back to the expected format of Carnifex.

Usage:
 - Make sure the domjudge is not in external id mode (the contest ids must be integers!)
 - Download Carnifex. Before compiling, apply patch 'carnifex_patch.patch', this reorders some code to inject ids. (I used Carnifex commit 67e22c2)
 - Specify your domjudge url and api path in 'proxy.py'.
 - Configure Carnifex to use the port and address of Carniprox instead of the domjudge! (f.e. localhost and 5000)
 - Have fun with your contest.
