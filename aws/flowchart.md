```mermaid
graph TD;
    A[Terraform Configuration] --> B[google_compute_global_address<br>External IP]

    B --> C[google_compute_target_http_proxy<br>HTTP(S) Proxy]
    C --> D[google_compute_url_map<br>Routing Rules]

    D --> E1[google_compute_backend_service blue]
    D --> E2[google_compute_backend_service green]

    E1 --> F1[Instance Group / NEG Blue]
    E2 --> F2[Instance Group / NEG Green]

    D --> G[google_compute_forwarding_rule<br>Points to target proxy]

    subgraph "Deployment Strategy"
        H[Switch traffic to blue or green<br>via Terraform updates to URL Map]
    end

    H --> D

```
