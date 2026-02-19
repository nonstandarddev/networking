# Network Stack

It's important to remember that whenever you leverage your local browser software (e.g. Firefox, or Chrome)
to 'surf the web' there's a tonne of stuff going on under the hood which makes that request a seamless
matter of *milliseconds*.

If we are to think about the process in abstract terms, broadly what happens is the following:

1. You request a website by its *domain name* (e.g. `https://www.google.com`)
2. Your client machine performs a translation of that domain name into an *IP address* (if the address
is not cached already!) - this translation is not performed on your client machine but is instead performed using what is known as a 'DNS lookup' (essentially, your machine sends a DNS request to your router on port `53` which, in turn, dispatches the request to your ISP's DNS server)
3. Once the IP address has been identified, your client machine (OS) is ready to send a 'formal request'. 
But the IP address isn't used yet. It's there in the background but we start with another step first: 
encapsulating the requested data in a *TCP header* - a 'header' is just metadata aboutthe request. 
In this case, a TCP header contains metadata that helps data arrive at its destination 
*reliably* and *sequentially* (preserving data integrity in the process). As part of this step, the data is also typically 'segmented' into different packets
4. Following this, an *IP header* is then attached by your client machine (OS) to the data packets assembled by the previous step - this is where the target IP address is attached (amongst other metadata)
5. At this stage of the cycle, we need to figure out 'the next best step' to get us closer to the target IP address. So, your client machine consults its 'routing table' to figure out where to send the packet. A routing table for your computer might look something like this,

    | Destination    | Next Hop    | Interface | Meaning                  |
    | -------------- | ----------- | --------- | ------------------------ |
    | 192.168.1.0/24 | — (direct)  | eth0      | Local network            |
    | 0.0.0.0/0      | 192.168.1.1 | eth0      | Everything else → router |

    What this is effectively saying is 'if the destination is 192.168.1.x, send it on the LAN otherwise send it to my router'. 
    
    For example, suppose the target IP address is `192.168.1.42` which corresponds to a device on the LAN: your client machine will then perform 'Address Resolution Protocol' (ARP) to discover the MAC address associated with the target IP address and build the subsequent ethernet frame for transmission via its NIC. Then the NIC present in both devices does a little 'bitwise dance' to communicate with each other (we've firmly left 'software land' at this point and are tredding waters in 'hardware land' now, yikes!)

    In what follows, assume the target IP address does not correspond to the subnetwork `192.168.1.0/24` as in the above example (i.e. we are looking for something on the 'internet' rather than the LAN).

6. Your router, receiving this data, strips off the ethernet header to inspect the IP header once again. The process then repeats itself again - your router checks its routing table and forwards the packet to the 'next appropriate interim device' until we finally reach our destination
7. At the final destination, all of the layers are *decapsulated* and the application listening on the server can eventually parse the initial HTTP request that we issued in the first place! Different metadata is attached to the response data throughout this communication process - for instance, TCP headers will change as the request progresses to indicate 'success' or 'failure' and, more generally, track the state of the connection as time progresses