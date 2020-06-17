```mermaid
sequenceDiagram
    Note over 10.0.0.1: ARP <br>Type=Request<br>MACSrc=c4:01:32:58:00:00, IPSrc=10.0.0.1<br>MACDst=c4:02:32:6b:00:00, IPDst=10.0.0.2<br>
    10.0.0.2->>10.0.0.1: ARP <br>Type=Reply<br>MACSrc=c4:02:32:6b:00:00, IPSrc=10.0.0.2
```
