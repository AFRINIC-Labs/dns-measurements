# dns-measurements

What is going on with 1.1.1.1 in the Africa? 
- Is this the same worldwide? 
- Where are those measurements going? (traceroute to 1.1.1.1) 
- Are DNS queries intercepted? – send whoami.akamai.net A to 8.8.8.8 – Result should be any of list published at locations.publicdns.goog. TXT 

Run measurements on Speedchecker and RIPE Atlas and then compare results.

Methodology:
For each probe, get the local resolver. Run latency checks to the local resolver and run latency checks to the public DNS servers.
Compare latency_local vs latency_1.1.1.1, latency_8.8.8.8
Run traceroute from the probes to the public dns server
Check whether queries are intercepted by doing a DIG on whoami.akamai.net
