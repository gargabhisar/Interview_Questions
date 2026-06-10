ANSWERS = {
"q_azure_functions_request": """<h2>Azure Functions — Data Extraction from Request</h2>
<p>In HTTP-triggered Azure Functions you read data from the incoming request via <code>HttpRequestData</code> (isolated worker) or <code>HttpRequest</code> (in-process). Data can come from the <strong>body</strong>, <strong>query string</strong>, <strong>route</strong>, or <strong>headers</strong>.</p>
<h3>Isolated worker model (.NET 8 — recommended)</h3>
<pre><code>[Function("CreateOrder")]
public async Task&lt;HttpResponseData&gt; Run(
    [HttpTrigger(AuthorizationLevel.Function, "post", Route = "orders/{id}")]
    HttpRequestData req,
    int id,
    FunctionContext context)
{
    // Route parameter — bound automatically: id

    // Query string — ?status=pending
    var query = System.Web.HttpUtility.ParseQueryString(req.Url.Query);
    var status = query["status"];

    // Headers
    if (req.Headers.TryGetValues("X-Correlation-Id", out var corrIds))
        var correlationId = corrIds.FirstOrDefault();

    // JSON body
    var order = await req.ReadFromJsonAsync&lt;CreateOrderDto&gt;();

    var response = req.CreateResponse(HttpStatusCode.OK);
    await response.WriteAsJsonAsync(new { id, status, order });
    return response;
}</code></pre>
<h3>Where each part lives</h3>
<table>
<tr><th>Source</th><th>Example URL</th><th>How to read</th></tr>
<tr><td>Route</td><td><code>POST /api/orders/42</code></td><td>Method parameter <code>int id</code> or <code>{id}</code> in Route</td></tr>
<tr><td>Query</td><td><code>?page=2&amp;size=20</code></td><td><code>req.Query["page"]</code> or parse query string</td></tr>
<tr><td>Body</td><td>JSON POST body</td><td><code>ReadFromJsonAsync&lt;T&gt;()</code></td></tr>
<tr><td>Headers</td><td><code>Authorization: Bearer ...</code></td><td><code>req.Headers</code></td></tr>
</table>
<h3>In-process model (legacy)</h3>
<pre><code>[FunctionName("GetUser")]
public static async Task&lt;IActionResult&gt; Run(
    [HttpTrigger(AuthorizationLevel.Anonymous, "get", Route = "users/{userId}")]
    HttpRequest req, int userId, ILogger log)
{
    string name = req.Query["name"];
    var body = await req.ReadAsStringAsync();
    return new OkObjectResult(new { userId, name });
}</code></pre>
<h3>Interview Answer</h3>
<p>In Azure Functions I extract route params via method binding, query values from the URL, headers from HttpRequestData.Headers, and JSON from ReadFromJsonAsync on the body. I validate input, return 400 for bad payloads, and log correlation ids from headers for tracing in Application Insights.</p>""",

"q_azure_key_vault": """<h2>Azure Key Vault Integration with .NET API</h2>
<p><strong>Azure Key Vault</strong> stores secrets, connection strings, and certificates centrally. ASP.NET Core reads them via <code>Azure.Extensions.AspNetCore.Configuration.Secrets</code> or the <code>Azure.Security.KeyVault.Secrets</code> SDK.</p>
<h3>1. Create Key Vault secrets</h3>
<p>Store secrets like <code>ConnectionStrings--DefaultConnection</code> (double dash maps to nested config).</p>
<h3>2. Enable managed identity on App Service / Function</h3>
<p>Grant the app identity <strong>Get</strong> permission on secrets in Key Vault access policy or RBAC (<code>Key Vault Secrets User</code>).</p>
<h3>3. Load secrets into configuration (Program.cs)</h3>
<pre><code>var builder = WebApplication.CreateBuilder(args);

var keyVaultUrl = builder.Configuration["KeyVault:Url"];
if (!string.IsNullOrEmpty(keyVaultUrl))
{
    builder.Configuration.AddAzureKeyVault(
        new Uri(keyVaultUrl),
        new DefaultAzureCredential());
}

var conn = builder.Configuration.GetConnectionString("DefaultConnection");
// Value resolved from Key Vault at startup</code></pre>
<h3>4. Inject secrets via IOptions / IConfiguration</h3>
<pre><code>builder.Services.Configure&lt;JwtSettings&gt;(
    builder.Configuration.GetSection("Jwt"));

public class AuthController : ControllerBase
{
    public AuthController(IOptions&lt;JwtSettings&gt; jwt) { ... }
}</code></pre>
<h3>5. Read secret directly (SDK)</h3>
<pre><code>var client = new SecretClient(
    new Uri(keyVaultUrl),
    new DefaultAzureCredential());

KeyVaultSecret secret = await client.GetSecretAsync("ApiKey");
string apiKey = secret.Value.Value;</code></pre>
<h3>Key Points</h3>
<ul>
<li>Use <strong>Managed Identity</strong> — no secrets in code or config files.</li>
<li><code>DefaultAzureCredential</code> works locally (Visual Studio / Azure CLI) and in Azure.</li>
<li>Never commit Key Vault URLs with secrets; reference vault name in App Service settings.</li>
<li>Rotate secrets in Key Vault; apps pick up changes on restart or with reload config.</li>
</ul>
<h3>Do you fetch Key Vault secrets on every request?</h3>
<p><strong>No.</strong> Secrets load into <strong>IConfiguration at startup</strong> via <code>AddAzureKeyVault</code>. The app reads them through <code>IConfiguration</code> or <code>IOptions</code> from memory — not a Key Vault HTTP call per API request.</p>
<ul>
<li><strong>Startup load</strong> — merged into configuration once</li>
<li><strong>IOptionsMonitor</strong> — optional reload on rotation</li>
<li><strong>Direct SDK</strong> — only for special cases; cache the result</li>
</ul>
<h3>Interview Answer</h3>
<p>I store connection strings and API keys in Azure Key Vault, enable managed identity on the App Service, and add AddAzureKeyVault in Program.cs with DefaultAzureCredential. Configuration binds secrets like normal appsettings so services use IOptions without hard-coded credentials.</p>""",

"q_azure_api_troubleshooting": """<h2>Handling API Issues from the Cloud — Analysis Steps</h2>
<p>When a cloud-hosted API fails or slows down, troubleshoot <strong>layer by layer</strong> with evidence — logs, metrics, and traces — not guesses.</p>
<h3>Step-by-step analysis</h3>
<ol>
<li><strong>Reproduce &amp; scope</strong> — Which endpoint, environment (dev/staging/prod), error code, time window, affected users?</li>
<li><strong>Check health &amp; availability</strong> — App Service health check, Azure status page, deployment slot swap issues.</li>
<li><strong>Application Insights / logs</strong> — Failures blade, exceptions, dependency calls, request duration, 5xx rate spike.</li>
<li><strong>Correlate with deployment</strong> — Did a release, config change, or Key Vault secret rotation happen just before?</li>
<li><strong>Dependencies</strong> — Azure SQL DTU/throttling, Redis timeout, external API 503, Service Bus backlog.</li>
<li><strong>Database</strong> — Slow queries, blocking, connection pool exhaustion, firewall rules blocking App Service outbound IP.</li>
<li><strong>Infrastructure</strong> — CPU/memory on App Service plan, autoscale limits, cold start on Functions/Container Apps.</li>
<li><strong>Network &amp; security</strong> — CORS, WAF rules, IP restrictions, expired SSL cert, managed identity permissions.</li>
<li><strong>Fix &amp; verify</strong> — Rollback or hotfix, run smoke tests, watch metrics for 15–30 minutes.</li>
<li><strong>Post-incident</strong> — RCA document, alert tuning, runbook update.</li>
</ol>
<h3>Tools in Azure (.NET API)</h3>
<table>
<tr><th>Tool</th><th>Use</th></tr>
<tr><td>Application Insights</td><td>Traces, exceptions, dependency map, live metrics</td></tr>
<tr><td>Log Analytics (KQL)</td><td>Query requests | where success == false</td></tr>
<tr><td>App Service diagnostics</td><td>HTTP logs, failed requests, process crashes</td></tr>
<tr><td>Azure SQL Query Store</td><td>Regressed queries after deploy</td></tr>
<tr><td>Activity Log</td><td>Who changed config, scaled, restarted</td></tr>
</table>
<pre><code>// KQL example — failed API calls last hour
requests
| where timestamp &gt; ago(1h)
| where success == false
| summarize count() by resultCode, name
| order by count_ desc</code></pre>
<h3>Interview Answer</h3>
<p>I start by reproducing the issue and checking Application Insights for exceptions and slow dependencies. I correlate with recent deployments, then check SQL, Redis, and external APIs. I use KQL for failed requests, verify App Service health and Key Vault access, fix with rollback or targeted change, and document the root cause.</p>""",

"q_solid_ocp_violation": """<h2>Open/Closed Principle — Violation Example</h2>
<p><strong>Open/Closed Principle (OCP):</strong> Software entities should be <strong>open for extension</strong> but <strong>closed for modification</strong>. Adding behavior should not require editing existing, tested code.</p>
<h3>Violation — switch grows with every new type</h3>
<pre><code>public class InvoiceExporter
{
    public string Export(Invoice invoice, string format)
    {
        // ❌ Violates OCP — must edit this class for every new format
        switch (format)
        {
            case "PDF":
                return ExportPdf(invoice);
            case "Excel":
                return ExportExcel(invoice);
            case "CSV":
                return ExportCsv(invoice);
            default:
                throw new NotSupportedException(format);
        }
    }
}
// Adding JSON export → modify InvoiceExporter again</code></pre>
<h3>Fix — extend via new classes, not edits</h3>
<pre><code>public interface IInvoiceExporter
{
    string Format { get; }
    string Export(Invoice invoice);
}

public class PdfInvoiceExporter : IInvoiceExporter
{
    public string Format =&gt; "PDF";
    public string Export(Invoice invoice) =&gt; /* PDF logic */;
}

public class ExcelInvoiceExporter : IInvoiceExporter { ... }

public class InvoiceExportService
{
    private readonly IEnumerable&lt;IInvoiceExporter&gt; _exporters;
    public InvoiceExportService(IEnumerable&lt;IInvoiceExporter&gt; exporters)
        =&gt; _exporters = exporters;

    public string Export(Invoice invoice, string format) =&gt;
        _exporters.First(e =&gt; e.Format == format).Export(invoice);
}

// New JSON exporter — new class + DI registration only
public class JsonInvoiceExporter : IInvoiceExporter { ... }</code></pre>
<h3>Signs you are violating OCP</h3>
<ul>
<li>Long <code>if/switch</code> on type or string codes that keeps growing.</li>
<li>Every new feature requires changing a central "god" class.</li>
<li>Merge conflicts in the same file when multiple teams add variants.</li>
</ul>
<h3>Interview Answer</h3>
<p>OCP means I extend behavior with new classes or strategies instead of modifying existing ones. A switch on payment or export type that we edit for every new option violates OCP; replacing it with an interface and DI-registered implementations lets me add JSON or Cash payment without touching core billing code.</p>""",

"q_arch_caching_why": """<h2>Caching — Why Use It? Memory vs Redis</h2>
<p><strong>Caching</strong> stores frequently read data closer to the application to reduce latency, database load, and cost. Use it when reads dominate, data changes infrequently, or recomputing is expensive.</p>
<h3>Why cache?</h3>
<ul>
<li>Faster API responses — avoid repeated DB/API calls.</li>
<li>Lower database pressure — fewer identical queries under load.</li>
<li>Better scalability — serve hot data from memory instead of SQL.</li>
<li>Cost savings — fewer DTU/RU on cloud databases.</li>
</ul>
<h3>IMemoryCache vs Redis (IDistributedCache)</h3>
<table>
<tr><th></th><th>IMemoryCache</th><th>Redis (distributed)</th></tr>
<tr><td>Scope</td><td>Single server / process</td><td>Shared across all app instances</td></tr>
<tr><td>Speed</td><td>Fastest — in-process RAM</td><td>Network hop — still very fast</td></tr>
<tr><td>Survives restart?</td><td>No</td><td>Yes (with persistence config)</td></tr>
<tr><td>Use when</td><td>Single-node dev/small app</td><td>App Service scale-out, multiple pods</td></tr>
<tr><td>Consistency</td><td>Each node has own copy</td><td>All nodes see same cache</td></tr>
</table>
<pre><code>// In-memory — single instance
_cache.Set("product:42", product, TimeSpan.FromMinutes(5));

// Redis — multi-instance
await _distributedCache.SetStringAsync(
    "product:42",
    JsonSerializer.Serialize(product),
    new DistributedCacheEntryOptions
    {
        AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(5)
    });

// Cache-aside pattern
if (!_cache.TryGetValue(key, out Product? p))
{
    p = await _db.Products.FindAsync(id);
    _cache.Set(key, p, TimeSpan.FromMinutes(10));
}</code></pre>
<h3>When NOT to cache</h3>
<ul>
<li>Data must be real-time accurate (account balance without invalidation).</li>
<li>Highly personalized or unique per-request data with no reuse.</li>
<li>Without a clear TTL or invalidation strategy on writes.</li>
</ul>
<h3>Interview Answer</h3>
<p>I cache to cut latency and database load on hot reads using cache-aside with TTLs. IMemoryCache is fine for a single server; when the API scales to multiple instances I use Redis via IDistributedCache so all nodes share the same cache. I invalidate or update cache entries when underlying data changes.</p>""",

"q_arch_large_scale_design": """<h2>Designing a Large-Scale Application for Scalability &amp; Reliability</h2>
<p>When interviewers ask how you design a large-scale system, a strong answer is structured in <strong>layers</strong> — not random bullet points. I usually organize my response around these pillars:</p>
<ol>
<li>Scalability</li>
<li>Reliability &amp; high availability</li>
<li>Database design &amp; performance</li>
<li>Caching strategy</li>
<li>Asynchronous processing</li>
<li>Performance optimization</li>
<li>Security</li>
<li>Monitoring &amp; logging</li>
<li>Disaster recovery &amp; backup</li>
<li>CI/CD &amp; deployment</li>
</ol>
<h3>1. Scalability</h3>
<p>Scalability means the system handles increasing users, traffic, and data <strong>without degrading performance</strong>.</p>
<h3>Horizontal scaling</h3>
<p>Instead of making one server bigger (vertical scaling), I prefer <strong>horizontal scaling</strong> — add more application servers behind a load balancer and scale out based on CPU, memory, or request rate.</p>
<pre><code>Client → Load Balancer → App Server 1
                      → App Server 2
                      → App Server N → Database / Cache</code></pre>
<p><strong>Benefits:</strong> better traffic distribution, no single server bottleneck, easier failover when one node dies.</p>
<h3>Stateless APIs</h3>
<p>I design APIs as <strong>stateless</strong> whenever possible. Session data should not live only in one server’s memory — use distributed cache (Redis) or token-based auth (JWT) so <strong>any request can hit any server</strong>.</p>
<h3>Microservices (when needed)</h3>
<p>For very large domains, split into independently deployable services — e.g. Customer Service, Account Service, Payment Service, Notification Service. Each can scale and deploy independently with better fault isolation.</p>
<p><strong>Mature interview point:</strong> for smaller systems, microservices add unnecessary complexity — a <strong>modular monolith</strong> is often the better starting point until boundaries are clear.</p>
<h3>2. Reliability &amp; high availability</h3>
<p>A scalable system must also <strong>survive failures</strong>.</p>
<ul>
<li><strong>Load balancer</strong> — if one app server fails, traffic routes to healthy nodes</li>
<li><strong>Retry mechanism</strong> — transient API/DB failures retried with backoff (Polly in .NET)</li>
<li><strong>Circuit breaker</strong> — stop hammering a failing downstream service; prevent cascading failures</li>
<li><strong>Failover</strong> — database replication, multiple availability zones, warm standby servers</li>
</ul>
<h3>3. Database design &amp; performance</h3>
<p>The database is often the <strong>biggest bottleneck</strong> in large systems.</p>
<h3>Normalization &amp; denormalization</h3>
<p>Start with <strong>proper normalization</strong> to avoid redundancy and update anomalies. For heavy read/reporting workloads, apply <strong>selective denormalization</strong> (summary tables, materialized views) where reads dominate writes.</p>
<h3>Indexing</h3>
<p>I focus heavily on indexing — clustered index on primary key, non-clustered indexes on frequently filtered/joined columns.</p>
<pre><code>CREATE NONCLUSTERED INDEX IX_Account_CustomerId
ON dbo.Account (CustomerId)
INCLUDE (AccountNumber, Status);</code></pre>
<p>Without indexes, queries on millions of rows fall back to <strong>full table scans</strong> and become slow under load.</p>
<h3>Query optimization</h3>
<p>I avoid <code>SELECT *</code>, nested cursors, and unnecessary joins. I use execution plans, parameterization, proper joins, and pagination:</p>
<pre><code>SELECT AccountId, AccountNumber, Balance
FROM dbo.Account
WHERE CustomerId = @CustomerId
ORDER BY AccountId
OFFSET @Skip ROWS FETCH NEXT @Take ROWS ONLY;</code></pre>
<h3>Database scaling</h3>
<ul>
<li><strong>Read replicas</strong> — offload reporting and dashboards from the primary OLTP database</li>
<li><strong>Partitioning / sharding</strong> — split very large tables by date or region</li>
<li><strong>Caching</strong> — hot reference data and session state in Redis</li>
</ul>
<h3>4. Caching strategy</h3>
<p>Caching dramatically improves response time and reduces database pressure.</p>
<ul>
<li><strong>Application cache</strong> — Redis or IMemoryCache (single node only)</li>
<li><strong>Cache-aside pattern</strong> — read cache first; on miss, load from DB and store with TTL</li>
<li><strong>What to cache</strong> — product/catalog data, configuration, branch/lookup tables, user session claims (with invalidation on write)</li>
</ul>
<p><strong>Benefits:</strong> fewer DB round-trips, faster API responses, better headroom under peak traffic.</p>
<h3>5. Asynchronous processing</h3>
<p>Heavy work should not block the user’s HTTP request.</p>
<p><strong>Examples:</strong> email alerts, report generation, payment notifications, ETL staging.</p>
<pre><code>API → Queue (RabbitMQ / Azure Service Bus / Kafka) → Background Worker</code></pre>
<p><strong>Benefits:</strong> faster API response, independent scaling of workers, natural retry and dead-letter handling.</p>
<h3>6. Performance optimization</h3>
<ul>
<li><strong>CDN</strong> — serve static assets (images, CSS, JS) from edge locations</li>
<li><strong>Compression</strong> — Gzip/Brotli on API and static responses</li>
<li><strong>Pagination</strong> — never return unbounded datasets to the client</li>
<li><strong>Connection pooling</strong> — reuse DB connections; tune pool size under load</li>
</ul>
<h3>7. Security</h3>
<p>Large systems must be secure by design:</p>
<ul>
<li>JWT authentication and role-based authorization</li>
<li>HTTPS everywhere; secrets in Key Vault, not config files</li>
<li>API rate limiting and input validation</li>
<li>Parameterized SQL / EF Core — prevent SQL injection</li>
<li>Encryption at rest and in transit for PII and financial data</li>
</ul>
<h3>8. Monitoring &amp; logging</h3>
<p>You cannot operate what you cannot see.</p>
<ul>
<li>Centralized logging (Application Insights, ELK, Splunk)</li>
<li>Track API response times, error rates, CPU/memory, slow queries</li>
<li>Alerts on SLO breaches — not just “server is down”</li>
<li>Distributed tracing with correlation IDs across services</li>
</ul>
<h3>9. Disaster recovery &amp; backup</h3>
<ul>
<li>Automated database backups with point-in-time recovery</li>
<li>Geo-redundant storage or multi-region deployment for critical workloads</li>
<li>Documented RTO/RPO targets and tested restore drills</li>
</ul>
<h3>10. CI/CD &amp; deployment</h3>
<p>For enterprise systems, automated pipelines are essential:</p>
<ul>
<li>Build, test, and deploy on every merge</li>
<li><strong>Blue-green</strong> or <strong>rolling</strong> deployment for zero-downtime releases</li>
<li>Fast rollback when a release fails health checks</li>
</ul>
<h3>Real-world example — PNC retail banking platform</h3>
<p>When describing this in an interview, I tie the pillars to a concrete domain:</p>
<ul>
<li><strong>Stateless APIs</strong> behind Azure Application Gateway / load balancer — account inquiry hits any app node</li>
<li><strong>Redis</strong> caches branch list, product codes, and session tokens across scaled-out API instances</li>
<li><strong>SQL Server</strong> with indexes on <code>CustomerId</code>, <code>AccountNumber</code> for fast account lookup; read replica for regulatory reporting dashboards</li>
<li><strong>Azure Service Bus / RabbitMQ</strong> for async alerts — transaction confirmation SMS/email does not block the transfer API</li>
<li><strong>Polly</strong> retry + circuit breaker on external payment-network and fraud-check calls</li>
<li><strong>Application Insights</strong> monitors failed transfers, latency spikes, and dependency timeouts</li>
<li><strong>Automated backups</strong> and geo-redundant SQL for disaster recovery</li>
<li><strong>CI/CD pipeline</strong> with staged deploy (DEV → UAT → PROD) and rollback on failed smoke tests</li>
</ul>
<h3>Strong closing statement</h3>
<div class="interview-tip"><p>While designing large-scale systems, I focus on removing bottlenecks, avoiding single points of failure, improving response time, and ensuring the system can scale horizontally while remaining secure and highly available. I start with a modular monolith when appropriate, add microservices and async processing only where the domain justifies the complexity, and always pair scaling with monitoring, backups, and tested recovery.</p></div>
<h3>Interview Answer</h3>
<p>I structure large-scale design around scalability, reliability, database performance, caching, async processing, security, monitoring, DR, and CI/CD. I scale APIs horizontally with stateless design and Redis, optimize SQL with indexes and read replicas, offload heavy work to queues, use Polly for resilience on external calls, and enforce observability and automated deployment. In banking, that means fast account lookup under load, async notifications, protected payment integrations, and zero-downtime releases — without over-engineering small systems into microservices too early.</p>""",

"q_arch_microservices_comm": """<h2>How Microservices Communicate With Each Other</h2>
<p>Two fundamental styles: <strong>synchronous</strong> (caller waits for a response) and <strong>asynchronous</strong> (message sent, caller moves on). Most real systems use <strong>both</strong> — sync for queries the user is waiting on, async for events and side effects.</p>
<h3>1. Synchronous communication</h3>
<table>
<tr><th>Mechanism</th><th>Details</th><th>When</th></tr>
<tr><td><strong>REST / HTTP + JSON</strong></td><td>Simple, universal; via <code>HttpClient</code> / <code>IHttpClientFactory</code> in .NET</td><td>Default for request/response between services</td></tr>
<tr><td><strong>gRPC</strong></td><td>HTTP/2, binary Protobuf — much faster, strongly-typed contracts, streaming</td><td>High-throughput internal service-to-service calls</td></tr>
</table>
<pre><code>// Typed client via IHttpClientFactory (with Polly resilience)
builder.Services.AddHttpClient&lt;IInventoryClient, InventoryClient&gt;(c =&gt;
        c.BaseAddress = new Uri("https://inventory-svc"))
    .AddStandardResilienceHandler();   // .NET 8: retry + circuit breaker + timeout</code></pre>
<p><strong>Risk of sync chains:</strong> A → B → C means A's latency and availability depend on the whole chain (cascading failures). Keep chains short; protect with timeouts, retries, circuit breakers.</p>
<h3>2. Asynchronous communication (messaging)</h3>
<table>
<tr><th>Pattern</th><th>How</th><th>Example</th></tr>
<tr><td><strong>Queue (point-to-point)</strong></td><td>One producer → one consumer; load leveling</td><td>Azure Service Bus queue, RabbitMQ — "process this payment"</td></tr>
<tr><td><strong>Publish/Subscribe (events)</strong></td><td>Publisher emits event; <strong>many</strong> subscribers react independently</td><td>Service Bus topics, Kafka, RabbitMQ exchanges — "OrderPlaced"</td></tr>
</table>
<pre><code>OrderService ── publishes ──&gt; "OrderPlaced" event
                                  ├─&gt; InventoryService  (reserve stock)
                                  ├─&gt; EmailService      (confirmation mail)
                                  └─&gt; AnalyticsService  (update dashboard)
// Order service doesn't know or care who listens — loose coupling</code></pre>
<p><strong>Benefits:</strong> services stay decoupled, survive consumer downtime (messages wait in the broker), natural retry, scale consumers independently. <strong>Cost:</strong> eventual consistency — data is correct "soon", not instantly.</p>
<h3>3. Supporting pieces</h3>
<ul>
<li><strong>API Gateway</strong> (Azure API Management, Ocelot, YARP) — single entry point for clients; routing, auth, rate limiting. Clients never call services directly.</li>
<li><strong>Service discovery</strong> — how services find each other: Kubernetes DNS, Consul, or platform-provided.</li>
<li><strong>Outbox pattern</strong> — save DB change + event in one transaction, publish reliably afterward (no lost events).</li>
<li><strong>Saga pattern</strong> — distributed transactions as a sequence of local transactions with compensating actions (cancel payment if stock reservation fails).</li>
<li><strong>Correlation IDs</strong> — pass a request ID through every hop for end-to-end tracing (Application Insights / OpenTelemetry).</li>
</ul>
<h3>Choosing sync vs async</h3>
<table>
<tr><th>Use synchronous</th><th>Use asynchronous</th></tr>
<tr><td>User is waiting for the answer (get price, check stock)</td><td>Side effects (emails, notifications, analytics)</td></tr>
<tr><td>Simple query with low fan-out</td><td>Multiple services must react to one event</td></tr>
<tr><td>Strong consistency needed right now</td><td>Spiky load — queue levels it out</td></tr>
</table>
<h3>Key Points</h3>
<ul>
<li>Sync: REST (universal) or gRPC (fast, typed) — protect with timeouts, retries, circuit breakers.</li>
<li>Async: queues for work distribution, pub/sub events for fan-out — loose coupling, eventual consistency.</li>
<li>API Gateway for client entry; outbox for reliable event publishing; saga for distributed workflows.</li>
<li>Real systems mix both: query synchronously, propagate changes as events.</li>
</ul>
<h3>Interview Answer</h3>
<p>Microservices communicate synchronously or asynchronously. Synchronous is REST over HttpClient or gRPC for fast internal calls — I always add timeouts, retries, and circuit breakers via Polly or .NET 8's standard resilience handler, because sync chains cascade failures. Asynchronous uses a message broker like Azure Service Bus or RabbitMQ — queues for distributing work and pub/sub topics for events, so when OrderService publishes OrderPlaced, inventory, email, and analytics each react independently. That gives loose coupling and resilience at the price of eventual consistency. Around that I'd put an API gateway for client traffic, the outbox pattern so events aren't lost, sagas for multi-service transactions, and correlation IDs for tracing across services.</p>""",
}
