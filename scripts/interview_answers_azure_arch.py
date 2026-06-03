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
}
