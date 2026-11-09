# Icon diagram brief (Mermaid 11 icon shapes)

Goal: every chapter's **two flowcharts** (section 6 "High-level design" first diagram, and section 8 "Final architecture") become icon diagrams grouped in tiers. The **sequence diagram stays as it is**. Deep-dive ASCII stays.

## Node syntax (Mermaid 11)

Define every node ONCE with an icon shape, then use its id in edges:

```
flowchart TB
    subgraph Clients["Clients"]
        B@{ icon: "mdi:cellphone", form: "rounded", label: "Browser or app", pos: "b", h: 56 }
    end
    subgraph Edge["Edge tier"]
        CDN@{ icon: "logos:aws-cloudfront", form: "square", label: "CDN", pos: "b", h: 56 }
        LB@{ icon: "mdi:scale-balance", form: "rounded", label: "Load balancer", pos: "b", h: 56 }
    end
    subgraph Services["Service tier"]
        RS@{ icon: "mdi:server", form: "rounded", label: "Read service x8", pos: "b", h: 56 }
    end
    subgraph Data["Data tier"]
        RC@{ icon: "logos:redis", form: "square", label: "Redis cache", pos: "b", h: 56 }
        PG@{ icon: "logos:postgresql", form: "square", label: "Postgres primary", pos: "b", h: 56 }
    end
    subgraph Async["Async tier"]
        K@{ icon: "logos:kafka-icon", form: "square", label: "Kafka click events", pos: "b", h: 56 }
    end
    B --> CDN
    CDN --> LB
    LB -- GET code --> RS
    RS --> RC
    RS -- cache miss --> PG
    RS -. click event .-> K
```

Rules:
- `form` is `"square"` for product logos (`logos:*`) and `"rounded"` for generic icons (`mdi:*`). Always `pos: "b"`, `h: 56`.
- Keep the SAME node ids and the SAME edges and edge labels as the current diagram. Only the node definitions change (box -> icon). Do not drop or add edges.
- Labels: plain text, no quotes inside, no `<br>`, max 4 words. Move detail like "60s TTL" into the edge label or the table below.
- Section 6 diagram: wrap nodes in tiers too (`Clients`, `Edge`, `Services`, `Data`, and `Async` or `External` when present). Section 8 already has tiers; keep them.
- Direction: `flowchart TB` for both (icons with labels below are tall; TB fits the page).
- One icon per node. Use ONLY the vocabulary below (unknown icon names render as a blank box).

## Icon vocabulary (use exactly these names)

| Thing in diagram | icon | form |
|---|---|---|
| person / user / customer / driver / rider | `mdi:account` | rounded |
| many users / audience / viewers | `mdi:account-group` | rounded |
| phone / mobile app / browser or app | `mdi:cellphone` | rounded |
| browser / web client / laptop | `mdi:laptop` | rounded |
| DNS | `mdi:dns` | rounded |
| CDN | `logos:aws-cloudfront` | square |
| load balancer / API gateway / reverse proxy | `mdi:scale-balance` | rounded |
| Nginx | `logos:nginx` | square |
| any stateless service / API server / worker fleet | `mdi:server` | rounded |
| background worker / consumer / job runner | `mdi:cogs` | rounded |
| scheduler / cron / timer | `mdi:clock-outline` | rounded |
| Lambda / serverless function | `logos:aws-lambda` | square |
| Postgres | `logos:postgresql` | square |
| MySQL | `logos:mysql` | square |
| DynamoDB | `logos:aws-dynamodb` | square |
| Cassandra / wide-column | `logos:cassandra` | square |
| MongoDB | `logos:mongodb-icon` | square |
| generic database / SQL / replica / shard | `mdi:database` | rounded |
| Redis / cache / counter / leaderboard sorted set | `logos:redis` | square |
| Memcached / in-process cache | `mdi:memory` | rounded |
| Kafka / event log / stream | `logos:kafka-icon` | square |
| Kinesis | `logos:aws-kinesis` | square |
| SQS / generic queue / DLQ | `logos:aws-sqs` | square |
| RabbitMQ | `logos:rabbitmq-icon` | square |
| S3 / blob / object store / files / videos at rest | `logos:aws-s3` | square |
| disk / HDFS / local storage | `mdi:harddisk` | rounded |
| Elasticsearch / search index / inverted index | `logos:elasticsearch` | square |
| search service (not ES) | `mdi:magnify` | rounded |
| Flink / stream processor | `logos:flink` | square |
| Spark / batch job / MapReduce | `logos:apache-spark` | square |
| analytics / metrics / time series | `mdi:chart-line` | rounded |
| Prometheus | `logos:prometheus` | square |
| Grafana / dashboard | `logos:grafana` | square |
| ZooKeeper / etcd / coordination / config | `mdi:file-tree` | rounded |
| lock / lease / distributed lock | `mdi:lock` | rounded |
| auth / API key check / identity | `mdi:shield-lock` | rounded |
| rate limiter / throttle | `mdi:speedometer` | rounded |
| WebSocket / long-lived connection / gateway for sockets | `mdi:lan-connect` | rounded |
| push notification / APNs / FCM | `mdi:bell` | rounded |
| email / SES / SendGrid | `mdi:email` | rounded |
| SMS | `mdi:message-text` | rounded |
| chat message / comments | `mdi:comment-multiple` | rounded |
| payment provider / Stripe / bank / card | `logos:stripe` | square |
| ledger / wallet / money | `mdi:bank` | rounded |
| map / GPS / location / geo index | `mdi:map-marker` | rounded |
| Google Maps / routing API | `logos:google-maps` | square |
| video / transcoder / encoder / player | `mdi:video` | rounded |
| image / thumbnail / photo | `mdi:image` | rounded |
| upload / ingest | `mdi:cloud-upload` | rounded |
| ML model / ranking / recommender / LLM | `mdi:brain` | rounded |
| OpenAI / model API | `logos:openai-icon` | square |
| GPU / inference fleet | `mdi:chip` | rounded |
| crawler / bot / fetcher | `mdi:robot` | rounded |
| document / doc store / CRDT / text | `mdi:file-document` | rounded |
| news / articles / feed source | `mdi:newspaper` | rounded |
| external website / third party / the internet | `mdi:earth` | rounded |
| GitHub | `logos:github-icon` | square |
| Docker / container | `logos:docker-icon` | square |
| Kubernetes / orchestrator / runner fleet | `logos:kubernetes` | square |
| code / judge / sandbox / compiler | `mdi:code-braces` | rounded |
| ticket / seat / inventory / stock | `mdi:ticket` | rounded |
| cart / order / checkout | `mdi:cart` | rounded |
| auction / bid / hammer | `mdi:gavel` | rounded |
| game / match / move | `mdi:gamepad-variant` | rounded |
| chess engine | `mdi:chess-king` | rounded |
| like / match / heart / swipe | `mdi:heart` | rounded |
| counter / top-k / aggregator / sketch | `mdi:counter` | rounded |
| filter / dedupe / bloom filter | `mdi:filter` | rounded |
| fan-out / router / dispatcher | `mdi:swap-horizontal` | rounded |
| monitoring / alerting / alarm | `mdi:bell-alert` | rounded |
| price / money tracking | `mdi:tag` | rounded |
| shard router / partitioner / hash ring | `mdi:source-branch` | rounded |
| ID generator / snowflake | `mdi:identifier` | rounded |
| anything else | `mdi:cube-outline` | rounded |

## Check before you save a file

1. Every node id used in an edge is defined exactly once with `@{ icon: ... }`.
2. No `[...]`, `[(...)]`, `[[...]]`, `((...))`, `{...}` node shapes remain in the two flowcharts.
3. Every `icon:` value is in the table above.
4. The sequence diagram and the deep-dive ASCII blocks are byte-for-byte unchanged.
5. The file still starts with its `# N. Title (Level)` line and keeps every section.
