ANSWERS = {
"q_auth_mechanisms": """<h2>Authentication and Authorization in .NET Core APIs</h2>
<h3>Authentication vs authorization</h3>
<table>
<tr><th></th><th>Question</th><th>When it runs</th></tr>
<tr><td><strong>Authentication</strong></td><td><em>Who are you?</em></td><td>Validates credentials or token; sets <code>HttpContext.User</code></td></tr>
<tr><td><strong>Authorization</strong></td><td><em>What may you do?</em></td><td>Checks roles, policies, or claims after authentication</td></tr>
</table>
<p>In ASP.NET Core they are <strong>separate middleware</strong> — order matters:</p>
<pre><code>app.UseAuthentication();   // first — identify the user
app.UseAuthorization();    // second — enforce access rules</code></pre>
<p><strong>401 Unauthorized</strong> = not authenticated. <strong>403 Forbidden</strong> = authenticated but not allowed.</p>
<h3>JWT vs server-side session (common follow-up)</h3>
<table>
<tr><th></th><th>JWT</th><th>Server session</th></tr>
<tr><td><strong>State</strong></td><td>Token carries claims; stateless by default</td><td>Session ID in cookie; data on server</td></tr>
<tr><td><strong>Best for</strong></td><td>REST APIs, SPAs, mobile</td><td>MVC/Razor traditional web apps</td></tr>
<tr><td><strong>Scale-out</strong></td><td>Any server validates token</td><td>Needs Redis/SQL shared session store</td></tr>
<tr><td><strong>Revocation</strong></td><td>Harder — short TTL or blocklist</td><td>Easy — delete session server-side</td></tr>
</table>
<p><strong>Related:</strong> Section 2 item 34 — Sessions in .NET Core; Section 6 item 2 — Generate JWT in Web API.</p>
<h3>Authentication mechanisms (typical .NET projects)</h3>
<table>
<tr><th>Mechanism</th><th>Best for</th><th>How it works</th></tr>
<tr><td><strong>JWT Bearer</strong></td><td>REST APIs, SPAs, mobile</td><td>Client sends <code>Authorization: Bearer &lt;token&gt;</code>; stateless</td></tr>
<tr><td><strong>Cookie authentication</strong></td><td>MVC, Razor Pages</td><td>Encrypted cookie after login form; server session</td></tr>
<tr><td><strong>ASP.NET Core Identity</strong></td><td>Apps with SQL user store</td><td>Password hash, lockout, roles, 2FA, token providers</td></tr>
<tr><td><strong>Azure AD / Entra ID</strong></td><td>Enterprise SSO</td><td>OAuth2 / OpenID Connect; trust tokens from IdP</td></tr>
<tr><td><strong>API key / custom header</strong></td><td>Service-to-service, webhooks</td><td>Validate key in middleware or handler</td></tr>
<tr><td><strong>OAuth2 / OpenID Connect</strong></td><td>Multi-app SSO</td><td>IdentityServer, OpenIddict, Azure AD issue tokens</td></tr>
</table>
<h3>Configure JWT Bearer (most common in API interviews)</h3>
<pre><code>// Program.cs
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =&gt;
    {
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuer = true,
            ValidateAudience = true,
            ValidateLifetime = true,
            ValidateIssuerSigningKey = true,
            ValidIssuer = builder.Configuration["Jwt:Issuer"],
            ValidAudience = builder.Configuration["Jwt:Audience"],
            IssuerSigningKey = new SymmetricSecurityKey(
                Encoding.UTF8.GetBytes(builder.Configuration["Jwt:Key"]!))
        };
    });

builder.Services.AddAuthorization(options =&gt;
{
    options.AddPolicy("CanManageOrders", policy =&gt;
        policy.RequireRole("Admin", "Manager"));

    options.AddPolicy("MinimumAge18", policy =&gt;
        policy.RequireClaim("age", "18", "19", "20")); // example custom claim
});

app.UseAuthentication();
app.UseAuthorization();</code></pre>
<h3>Protect endpoints</h3>
<pre><code>// Controller — role and policy
[Authorize]
[ApiController]
[Route("api/[controller]")]
public class OrdersController : ControllerBase
{
    [HttpGet]
    public IActionResult GetAll() =&gt; Ok();

    [Authorize(Roles = "Admin")]
    [HttpDelete("{id}")]
    public IActionResult Delete(int id) =&gt; NoContent();

    [Authorize(Policy = "CanManageOrders")]
    [HttpPut("{id}")]
    public IActionResult Update(int id, OrderDto dto) =&gt; Ok();
}

// Minimal API
app.MapGet("/admin/reports", () =&gt; Results.Ok())
   .RequireAuthorization("CanManageOrders");</code></pre>
<h3>Authorization approaches</h3>
<ul>
<li><strong>Role-based</strong> — <code>[Authorize(Roles = "Admin")]</code>; simple RBAC</li>
<li><strong>Policy-based</strong> — <code>RequireRole</code>, <code>RequireClaim</code>, custom <code>IAuthorizationHandler</code></li>
<li><strong>Resource-based</strong> — user may edit only their own record (<code>IAuthorizationService</code> + resource id)</li>
</ul>
<h3>Typical API login flow</h3>
<ol>
<li>Client <code>POST /api/auth/login</code> with credentials</li>
<li>Server validates user (Identity, database, Azure AD)</li>
<li>Server issues signed JWT with claims (sub, email, role, exp)</li>
<li>Client stores token; sends Bearer header on each request</li>
<li><code>JwtBearer</code> middleware validates token → <code>[Authorize]</code> checks access</li>
</ol>
<h3>Best practices</h3>
<ul>
<li>Store signing keys in Key Vault / user secrets — not in source control</li>
<li>Short-lived access tokens; use refresh tokens for long sessions</li>
<li>Use <strong>HTTPS</strong> only; never send tokens over plain HTTP</li>
<li>Prefer <strong>policies</strong> over hard-coded roles when rules grow</li>
<li>Do not put passwords or secrets in JWT payload (it is signed, not encrypted)</li>
<li>For public APIs, combine auth with rate limiting and audit logging</li>
</ul>
<h3>Real-time answer template</h3>
<p>“In my .NET Core Web APIs I use <strong>JWT bearer authentication</strong>: login returns a signed token, and each request validates issuer, audience, and expiry in middleware. I protect controllers with <code>[Authorize]</code> and enforce business rules with <strong>role and policy authorization</strong>. For enterprise apps I integrate <strong>Azure AD</strong> via OpenID Connect; for internal services I sometimes validate <strong>API keys</strong> in custom middleware.”</p>
<h3>Interview Answer</h3>
<p>Authentication identifies the caller; authorization decides access. I register JwtBearer in Program.cs, call UseAuthentication then UseAuthorization, and protect endpoints with Authorize attributes or policies. I separate 401 (not logged in) from 403 (logged in but denied), use policies for flexible rules, and keep tokens short-lived with secrets stored outside the codebase.</p>""",

"q_aspnet_jwt_details": """<h2>JWT — How It Works, Expiry &amp; Content</h2>
<p>A <strong>JSON Web Token (JWT)</strong> is a compact, signed string with three Base64URL-encoded parts: <strong>header.payload.signature</strong>. The API trusts the payload only if the signature matches and claims like <code>exp</code> are valid.</p>
<h3>How JWT works (flow)</h3>
<ol>
<li>Client sends credentials to <code>POST /api/auth/login</code>.</li>
<li>Server validates user, builds claims, signs token with secret/private key, returns JWT.</li>
<li>Client stores token and sends <code>Authorization: Bearer &lt;token&gt;</code> on each API call.</li>
<li><code>JwtBearer</code> middleware validates signature, issuer, audience, and expiry, then sets <code>HttpContext.User</code>.</li>
<li><code>[Authorize]</code> / policies check roles or claims before the action runs.</li>
</ol>
<h3>Token content (three parts)</h3>
<pre><code>// Header (algorithm + type)
{ "alg": "HS256", "typ": "JWT" }

// Payload — claims (NOT encrypted; only signed)
{
  "sub": "user-42",
  "email": "user@example.com",
  "role": "Admin",
  "iss": "https://my-api.com",
  "aud": "https://my-api.com",
  "exp": 1717000000,
  "iat": 1716996400
}

// Signature = HMAC(header + "." + payload, secret)</code></pre>
<h3>Expiry</h3>
<ul>
<li><code>exp</code> (expiration) — Unix timestamp; token rejected after this time.</li>
<li><code>nbf</code> (not before) — optional; token invalid before this time.</li>
<li>ASP.NET Core checks expiry when <code>ValidateLifetime = true</code> in <code>TokenValidationParameters</code>.</li>
<li>Short-lived access tokens (15–60 min) + refresh tokens is a common production pattern.</li>
</ul>
<pre><code>options.TokenValidationParameters = new TokenValidationParameters
{
    ValidateIssuer = true,
    ValidateAudience = true,
    ValidateLifetime = true,
    ClockSkew = TimeSpan.FromMinutes(1),
    ValidIssuer = config["Jwt:Issuer"],
    ValidAudience = config["Jwt:Audience"],
    IssuerSigningKey = new SymmetricSecurityKey(keyBytes)
};</code></pre>
<h3>Key Points</h3>
<ul>
<li>Payload is readable by anyone — do not put passwords or secrets in JWT.</li>
<li>Signature proves integrity; without it, claims can be tampered with.</li>
<li>Stateless — server does not store session; revocation needs blocklists or short expiry.</li>
</ul>
<h3>Interview Answer</h3>
<p>JWT is a signed token with claims in the payload. The client sends it as a Bearer token; middleware validates signature, issuer, audience, and expiry before authorization runs. I keep access tokens short-lived, put identity and roles in claims, and never store sensitive data in the payload because it is only signed, not encrypted.</p>""",

"q_aspnet_http_methods": """<h2>HTTP Methods in ASP.NET Core</h2>
<p>HTTP methods (verbs) tell the server <strong>what operation</strong> to perform on a resource. ASP.NET Core maps them to controller actions via attributes like <code>[HttpGet]</code>, <code>[HttpPost]</code>, etc.</p>
<table>
<tr><th>Method</th><th>Purpose</th><th>Idempotent?</th><th>Typical status</th></tr>
<tr><td><strong>GET</strong></td><td>Read / retrieve</td><td>Yes</td><td>200 OK</td></tr>
<tr><td><strong>POST</strong></td><td>Create or non-idempotent action</td><td>No</td><td>201 Created</td></tr>
<tr><td><strong>PUT</strong></td><td>Replace entire resource</td><td>Yes</td><td>200 / 204</td></tr>
<tr><td><strong>PATCH</strong></td><td>Partial update</td><td>No*</td><td>200 OK</td></tr>
<tr><td><strong>DELETE</strong></td><td>Remove resource</td><td>Yes</td><td>204 No Content</td></tr>
<tr><td><strong>HEAD</strong></td><td>GET without body (metadata)</td><td>Yes</td><td>200 OK</td></tr>
<tr><td><strong>OPTIONS</strong></td><td>CORS preflight / supported methods</td><td>Yes</td><td>204</td></tr>
</table>
<pre><code>[ApiController]
[Route("api/products")]
public class ProductsController : ControllerBase
{
    [HttpGet]              // GET /api/products
    public IActionResult GetAll() =&gt; Ok(_repo.GetAll());

    [HttpGet("{id:int}")]  // GET /api/products/5
    public IActionResult Get(int id) =&gt; Ok(_repo.Get(id));

    [HttpPost]             // POST /api/products
    public IActionResult Create([FromBody] CreateProductDto dto) { ... }

    [HttpPut("{id:int}")]  // PUT /api/products/5
    public IActionResult Update(int id, [FromBody] UpdateProductDto dto) { ... }

    [HttpDelete("{id:int}")]
    public IActionResult Delete(int id) { ... }
}</code></pre>
<h3>Key Points</h3>
<ul>
<li>GET should not change server state (safe method).</li>
<li>POST is for creates and actions that are not idempotent (e.g. <code>/orders/5/pay</code>).</li>
<li>Wrong verb → <strong>405 Method Not Allowed</strong>.</li>
<li>REST uses nouns in URLs; verbs are HTTP methods, not path segments like <code>/getUser</code>.</li>
</ul>
<h3>Interview Answer</h3>
<p>I map GET to reads, POST to creates, PUT/PATCH to updates, and DELETE to removal. ASP.NET Core binds the HTTP verb to the action via attributes. I follow REST semantics so clients and caches behave predictably and status codes match the operation.</p>""",

"q_aspnet_200_vs_201": """<h2>200 OK vs 201 Created</h2>
<p>Both are success codes (2xx), but they mean different things to API clients and HTTP caches.</p>
<table>
<tr><th></th><th>200 OK</th><th>201 Created</th></tr>
<tr><td>Meaning</td><td>Request succeeded; resource may already exist</td><td>New resource was created</td></tr>
<tr><td>Typical use</td><td>GET, PUT, PATCH, successful POST that does not create</td><td>POST that creates a new entity</td></tr>
<tr><td>Response body</td><td>Often returns data</td><td>Usually returns created resource</td></tr>
<tr><td>Location header</td><td>Not required</td><td>Should include URL of new resource</td></tr>
</table>
<pre><code>// 200 — read or update existing
[HttpGet("{id}")]
public IActionResult Get(int id)
{
    var user = _repo.Find(id);
    return user is null ? NotFound() : Ok(user);
}

// 201 — create new resource
[HttpPost]
public IActionResult Create([FromBody] CreateUserDto dto)
{
    var user = _service.Create(dto);
    return CreatedAtAction(
        nameof(Get),
        new { id = user.Id },
        user);  // 201 + Location header + body
}

// Wrong — returning 200 after create hides REST semantics
return Ok(user); // prefer CreatedAtAction for POST create</code></pre>
<h3>When to use which</h3>
<ul>
<li><strong>201</strong> — POST <code>/api/users</code> creates a user; client needs the new id and URI.</li>
<li><strong>200</strong> — GET returns data; PUT updates and returns updated entity.</li>
<li><strong>204</strong> — DELETE succeeded with no body (alternative to 200 empty).</li>
</ul>
<h3>Interview Answer</h3>
<p>200 means success for general operations like reads and updates. 201 means a new resource was created — I return it with <code>CreatedAtAction</code> or <code>Created</code> so the client gets the new URI in the Location header. Using 200 for every success makes APIs harder for clients and tools to interpret correctly.</p>""",

"q_aspnet_post_on_get": """<h2>Can We Use [HttpPost] on a GET Action?</h2>
<p><strong>Technically yes</strong> — you can decorate any action with <code>[HttpPost]</code>, but it will only respond to <strong>POST</strong> requests, not GET. The attribute defines which HTTP verb routes to that action; it does not change how the method works internally.</p>
<pre><code>// This action is ONLY reachable via POST — not GET
[HttpPost("users/search")]
public IActionResult SearchUsers([FromBody] SearchCriteria criteria)
{
    return Ok(_repo.Search(criteria));
}

// GET /users/search → 405 Method Not Allowed (no matching GET action)
// POST /users/search → runs SearchUsers</code></pre>
<h3>Common confusion</h3>
<ul>
<li><strong>Wrong pattern:</strong> naming an action <code>GetUsers</code> but marking it <code>[HttpPost]</code> — confusing for maintainers even if it compiles.</li>
<li><strong>Correct pattern:</strong> GET for reads (no body), POST for creates or complex queries with large filters in body.</li>
<li>Some teams use POST for search when filter JSON is too large for query string — still not a GET action.</li>
</ul>
<h3>What happens if verb and attribute mismatch?</h3>
<p>If the client sends GET but only a POST action exists, routing may match the route template but return <strong>405 Method Not Allowed</strong>. If no route matches at all, returns <strong>404</strong>.</p>
<h3>Interview Answer</h3>
<p>You can put [HttpPost] on any action, but then only POST requests hit it — a GET request will not execute that action. I align HTTP verbs with REST semantics: GET for safe reads, POST for creates or non-idempotent operations, rather than mixing verb names and attributes inconsistently.</p>""",

"q_aspnet_dry": """<h2>Clean Code Principles — DRY in ASP.NET Core</h2>
<p><strong>DRY (Don't Repeat Yourself)</strong> means every piece of knowledge should have a single authoritative representation. In ASP.NET Core this applies to validation, error handling, auth, and data access — not just copy-pasting code.</p>
<h3>DRY in practice</h3>
<table>
<tr><th>Repeated concern</th><th>DRY approach</th></tr>
<tr><td>Validation rules</td><td>Data annotations, FluentValidation, shared validators</td></tr>
<tr><td>Exception → HTTP response</td><td>Global exception middleware or <code>IExceptionHandler</code></td></tr>
<tr><td>Auth checks</td><td>Policies, <code>[Authorize(Roles = "...")]</code>, filters</td></tr>
<tr><td>DB access</td><td>Repository / service layer, not raw EF in every controller</td></tr>
<tr><td>Mapping DTO ↔ entity</td><td>AutoMapper profiles or explicit mapper classes</td></tr>
<tr><td>Cross-cutting logging</td><td>Middleware, <code>ILogger&lt;T&gt;</code>, action filters</td></tr>
</table>
<pre><code>// ❌ Repeated in every controller
catch (NotFoundException ex) { return NotFound(ex.Message); }

// ✅ Single global handler
app.UseExceptionHandler(appError =&gt;
{
    appError.Run(async context =&gt;
    {
        var ex = context.Features.Get&lt;IExceptionHandlerFeature&gt;()?.Error;
        var (status, message) = ex switch
        {
            NotFoundException e =&gt; (404, e.Message),
            ValidationException e =&gt; (400, e.Message),
            _ =&gt; (500, "An error occurred")
        };
        context.Response.StatusCode = status;
        await context.Response.WriteAsJsonAsync(new { message });
    });
});</code></pre>
<h3>Related clean code principles</h3>
<ul>
<li><strong>SRP</strong> — controllers thin; business logic in services.</li>
<li><strong>SoC</strong> — middleware for pipeline, filters for MVC, services for domain.</li>
<li><strong>Meaningful names</strong> — <code>OrderService</code> not <code>Helper</code>.</li>
<li>DRY ≠ never duplicate — sometimes two similar blocks diverge; premature abstraction hurts.</li>
</ul>
<h3>Interview Answer</h3>
<p>DRY means I centralize repeated logic — validation, error mapping, authorization, and mapping — in middleware, services, and shared components instead of duplicating it in every controller. I keep controllers thin and apply SOLID so changes happen in one place.</p>""",

"q_aspnet_client_errors": """<h2>Return Error Messages to the Client</h2>
<p>APIs should return <strong>consistent, structured errors</strong> with the correct HTTP status — never 200 with an error flag, and never raw exception details in production.</p>
<h3>Common patterns</h3>
<table>
<tr><th>Scenario</th><th>Status</th><th>Response shape</th></tr>
<tr><td>Validation failed</td><td>400</td><td>Field-level errors</td></tr>
<tr><td>Not authenticated</td><td>401</td><td><code>{ "message": "..." }</code></td></tr>
<tr><td>Not authorized</td><td>403</td><td><code>{ "message": "..." }</code></td></tr>
<tr><td>Resource not found</td><td>404</td><td><code>{ "message": "User not found" }</code></td></tr>
<tr><td>Business rule violation</td><td>409 / 422</td><td>Domain message</td></tr>
<tr><td>Server error</td><td>500</td><td>Generic message (log details server-side)</td></tr>
</table>
<pre><code>// Validation — automatic with [ApiController]
return BadRequest(ModelState);

// Or ProblemDetails (RFC 7807)
return ValidationProblem(ModelState);

// Custom business error
if (user is null)
    return NotFound(new { message = "User not found", id });

if (!await _authz.CanDelete(User, order))
    return Forbid();

// Global exception middleware — map domain exceptions
catch (AppException ex)
{
    await context.Response.WriteAsJsonAsync(new
    {
        status = ex.StatusCode,
        message = ex.Message,
        traceId = Activity.Current?.Id
    });
}</code></pre>
<h3>Best practices</h3>
<ul>
<li>Use a <strong>consistent JSON shape</strong> (<code>message</code>, <code>errors</code>, <code>traceId</code>).</li>
<li>Log full exception + correlation id server-side; return safe message to client.</li>
<li>Validation errors should name the field so the UI can highlight inputs.</li>
<li>Enable <code>ProblemDetails</code> services in ASP.NET Core for standard error bodies.</li>
</ul>
<h3>Interview Answer</h3>
<p>I return errors with the correct status code and a structured JSON body — ProblemDetails or a consistent custom format with message and field errors. Validation returns 400 with per-field messages; not-found returns 404; unexpected errors are logged fully but exposed to the client only as a generic 500 with a trace id.</p>""",

"q_aspnet_shared_views": """<h2>Multiple Views / Same View for Different Controllers</h2>
<p>In ASP.NET Core MVC, a <strong>view</strong> is a Razor template (<code>.cshtml</code>). Multiple controllers can return the <strong>same view</strong>; multiple actions in one controller can return <strong>different views</strong>.</p>
<h3>Same view from different controllers</h3>
<pre><code>// AdminController.cs
public IActionResult Dashboard()
{
    var model = _service.GetAdminSummary();
    return View("~/Views/Shared/Dashboard.cshtml", model);
}

// ReportsController.cs — reuse same Razor view
public IActionResult Summary()
{
    var model = _service.GetReportSummary();
    return View("~/Views/Shared/Dashboard.cshtml", model);
}

// Or place view in Views/Shared/Dashboard.cshtml
return View("Dashboard", model); // resolves Shared/Dashboard.cshtml</code></pre>
<h3>Multiple views from one controller</h3>
<pre><code>public class ProductsController : Controller
{
    public IActionResult List() =&gt; View("List", _repo.GetAll());

    public IActionResult Details(int id) =&gt; View("Details", _repo.Get(id));

    public IActionResult Edit(int id) =&gt; View("EditForm", _repo.Get(id));
}</code></pre>
<h3>View location conventions</h3>
<ul>
<li><code>Views/{Controller}/{Action}.cshtml</code> — default.</li>
<li><code>Views/Shared/{ViewName}.cshtml</code> — shared across controllers.</li>
<li>Partial views (<code>_PartialName.cshtml</code>) for reusable fragments (headers, grids).</li>
<li>View components for self-contained UI with their own logic.</li>
</ul>
<h3>Interview Answer</h3>
<p>Any controller action can return any view by name or path — I put reusable templates in Views/Shared so Admin and Reports can share a Dashboard layout. One controller can return List, Details, and Edit views from separate actions. Partial views and view components help reuse UI without duplicating Razor.</p>""",

"q_aspnet_dropdown_performance": """<h2>DropDown Performance in ASP.NET MVC / Core</h2>
<p>Populating dropdowns from large datasets (countries, products, employees) can slow page load if you load thousands of rows on every request. Optimize at data, caching, and UI layers.</p>
<h3>Strategies</h3>
<table>
<tr><th>Technique</th><th>When</th></tr>
<tr><td><strong>Select2 / autocomplete</strong></td><td>Large lists — load options via AJAX as user types</td></tr>
<tr><td><strong>Paging / server-side search</strong></td><td>API returns top N matches, not full table</td></tr>
<tr><td><strong>Caching</strong></td><td>Static lookup data (countries, statuses) — IMemoryCache / Redis</td></tr>
<tr><td><strong>Project only needed columns</strong></td><td><code>Select(x =&gt; new { x.Id, x.Name })</code> not full entities</td></tr>
<tr><td><strong>Lazy load dropdown</strong></td><td>Load child dropdown only after parent selection (cascade)</td></tr>
<tr><td><strong>ViewBag vs ViewModel</strong></td><td>Prefer typed ViewModel with <code>IEnumerable&lt;SelectListItem&gt;</code></td></tr>
</table>
<pre><code>// ❌ Slow — loads entire table every request
ViewBag.Products = _db.Products.ToList();

// ✅ Cache static lookups (5 min)
var products = await _cache.GetOrCreateAsync("product-ddl", async entry =&gt;
{
    entry.AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(5);
    return await _db.Products
        .AsNoTracking()
        .OrderBy(p =&gt; p.Name)
        .Select(p =&gt; new SelectListItem { Value = p.Id.ToString(), Text = p.Name })
        .ToListAsync();
});

// ✅ API endpoint for autocomplete
[HttpGet("api/products/search")]
public async Task&lt;IActionResult&gt; Search([FromQuery] string q, int take = 20)
{
    var items = await _db.Products
        .Where(p =&gt; p.Name.Contains(q))
        .Take(take)
        .Select(p =&gt; new { id = p.Id, text = p.Name })
        .ToListAsync();
    return Ok(items);
}</code></pre>
<h3>Key Points</h3>
<ul>
<li>Never bind 10k+ items to <code>&lt;select&gt;</code> — browser and DOM suffer.</li>
<li>Cache reference data that rarely changes.</li>
<li>Use <code>AsNoTracking()</code> for read-only dropdown queries.</li>
<li>Cascading dropdowns: second list loads via AJAX when first changes.</li>
</ul>
<h3>Interview Answer</h3>
<p>For large dropdowns I avoid loading full tables on every page — I cache small lookup lists, project only id and display text, and use autocomplete or server-side search for big datasets. Cascading dropdowns load child options on demand via AJAX rather than rendering everything upfront.</p>""",

"q_aspnet_q02": """<h2>Create a Web API Project &amp; What "Starting an App" Means</h2>
<h3>Create project</h3>
<pre><code>dotnet new webapi -n MyApi
cd MyApi
dotnet run</code></pre>
<p>Visual Studio: Create New Project → ASP.NET Core Web API → choose .NET version → enable OpenAPI if needed.</p>
<h3>What does "starting an app" mean?</h3>
<p>Launching the host process so it loads configuration, builds DI, configures middleware, and listens for requests (or runs background workers).</p>
<ol>
<li><code>WebApplication.CreateBuilder(args)</code> — load config, create service collection</li>
<li><code>builder.Services.Add...</code> — register DbContext, controllers, JWT, etc.</li>
<li><code>builder.Build()</code> — build the app and pipeline</li>
<li><code>app.Use...</code> / <code>app.MapControllers()</code> — middleware and endpoints</li>
<li><code>app.Run()</code> — start Kestrel and accept HTTP requests</li>
</ol>
<p><strong>Related:</strong> Section 2 item 4 — Program.cs vs Startup.cs (.NET 6+).</p>
<h3>Interview Answer</h3>
<p>I create APIs with dotnet new webapi. Starting the app means bootstrapping the host — config, DI, middleware, then Run() so Kestrel listens for requests.</p>""",

"q_di_scoped_in_singleton": """<h2>Why Is DbContext Scoped? Can Scoped Be Injected into Singleton?</h2>
<h3>Why DbContext is scoped (not singleton)</h3>
<ul>
<li><strong>One unit of work per request</strong> — tracks entities for that request only</li>
<li><strong>Not thread-safe</strong> — concurrent requests must not share one DbContext</li>
<li><strong>Dispose after request</strong> — connections and change tracker released properly</li>
<li><strong>Wrong data / memory leaks</strong> if a singleton captured one context forever</li>
</ul>
<pre><code>services.AddDbContext&lt;AppDbContext&gt;(options =&gt;
    options.UseSqlServer(connectionString)); // scoped by default</code></pre>
<h3>Can you inject scoped into singleton?</h3>
<p><strong>Not directly.</strong> ASP.NET Core DI blocks captive dependencies (scoped inside singleton) when detected.</p>
<h3>Correct pattern — create a scope</h3>
<pre><code>public class CacheWarmupService : IHostedService
{
    private readonly IServiceScopeFactory _scopeFactory;

    public CacheWarmupService(IServiceScopeFactory scopeFactory)
        =&gt; _scopeFactory = scopeFactory;

    public async Task StartAsync(CancellationToken ct)
    {
        using var scope = _scopeFactory.CreateScope();
        var db = scope.ServiceProvider.GetRequiredService&lt;AppDbContext&gt;();
        await db.Products.CountAsync(ct);
    }
}</code></pre>
<p><strong>Related:</strong> Section 2 item 29 — Transient, Scoped, Singleton; Section 2 item 39 — BackgroundService.</p>
<h3>Interview Answer</h3>
<p>DbContext is scoped because it represents one unit of work per request and is not thread-safe. You cannot inject scoped services into a singleton directly — use IServiceScopeFactory to create a short-lived scope in background services or singletons.</p>""",

"q_aspnet_q12": """<h2>.NET 6 vs Previous Versions &amp; Program.cs vs Startup.cs</h2>
<h3>.NET 6 vs earlier (.NET Core 3.1 / .NET 5 / Framework)</h3>
<table>
<tr><th>Area</th><th>Previous</th><th>.NET 6+</th></tr>
<tr><td>Hosting</td><td>Program + Startup classes</td><td>Minimal hosting — usually one Program.cs</td></tr>
<tr><td>Platform</td><td>.NET Framework Windows-only vs .NET Core</td><td>Unified cross-platform .NET</td></tr>
<tr><td>APIs</td><td>Controllers common</td><td>Minimal APIs + controllers</td></tr>
<tr><td>Performance</td><td>Good</td><td>Improved runtime, faster startup</td></tr>
</table>
<h3>Startup.cs (.NET Core 3.1 and earlier)</h3>
<ul>
<li><code>ConfigureServices</code> — register DI</li>
<li><code>Configure</code> — middleware pipeline</li>
</ul>
<h3>Program.cs (.NET 6+ minimal hosting)</h3>
<pre><code>var builder = WebApplication.CreateBuilder(args);
builder.Services.AddControllers();
var app = builder.Build();
app.UseAuthentication();
app.UseAuthorization();
app.MapControllers();
app.Run();</code></pre>
<h3>Interview Answer</h3>
<p>.NET 6 unified the platform with minimal Program.cs hosting instead of separate Startup. Same responsibilities — register services, configure middleware, map endpoints — with less boilerplate and better performance than .NET Core 3.1.</p>""",

"q_aspnet_q18": """<h2>Minimal APIs vs Controllers</h2>
<p>In .NET, a <strong>Minimal API</strong> is a lightweight way to build APIs with very little setup and boilerplate code, introduced in <strong>.NET 6</strong>.</p>
<p>Instead of creating controllers, <code>Startup.cs</code>, and separate routing classes, you define APIs directly in <code>Program.cs</code>.</p>
<h3>Basic example</h3>
<pre><code>var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/", () =&gt; "Hello World!");

app.MapGet("/user/{id}", (int id) =&gt;
{
    return new { Id = id, Name = "Abhisar" };
});

app.Run();</code></pre>
<h3>Features of Minimal API</h3>
<ul>
<li>Less code</li>
<li>Faster development</li>
<li>Better performance</li>
<li>Easy for microservices and small APIs</li>
<li>Supports dependency injection</li>
<li>Supports middleware</li>
<li>Supports authentication &amp; authorization</li>
</ul>
<h3>HTTP methods example</h3>
<p><strong>GET</strong></p>
<pre><code>app.MapGet("/products", () =&gt;
{
    return products;
});</code></pre>
<p><strong>POST</strong></p>
<pre><code>app.MapPost("/products", (Product product) =&gt;
{
    products.Add(product);
    return Results.Created($"/products/{product.Id}", product);
});</code></pre>
<p><strong>PUT</strong></p>
<pre><code>app.MapPut("/products/{id}", (int id, Product updatedProduct) =&gt;
{
    var product = products.FirstOrDefault(x =&gt; x.Id == id);

    if (product == null)
        return Results.NotFound();

    product.Name = updatedProduct.Name;

    return Results.Ok(product);
});</code></pre>
<p><strong>DELETE</strong></p>
<pre><code>app.MapDelete("/products/{id}", (int id) =&gt;
{
    var product = products.FirstOrDefault(x =&gt; x.Id == id);

    if (product == null)
        return Results.NotFound();

    products.Remove(product);

    return Results.Ok();
});</code></pre>
<h3>Dependency injection example</h3>
<pre><code>app.MapGet("/employees", (IEmployeeService service) =&gt;
{
    return service.GetEmployees();
});</code></pre>
<h3>Minimal API vs Controller API</h3>
<table>
<tr><th>Minimal API</th><th>Controller API</th></tr>
<tr><td>Less boilerplate</td><td>More structured</td></tr>
<tr><td>Faster for small apps</td><td>Better for large enterprise apps</td></tr>
<tr><td>Easy to learn</td><td>Better separation of concerns</td></tr>
<tr><td>High performance</td><td>Rich MVC features (filters, versioning)</td></tr>
</table>
<h3>When to use</h3>
<p><strong>Use Minimal APIs for:</strong></p>
<ul>
<li>Microservices</li>
<li>Lightweight APIs</li>
<li>Small projects</li>
<li>Fast prototyping</li>
</ul>
<p><strong>Avoid for:</strong></p>
<ul>
<li>Very large enterprise applications</li>
<li>Complex business logic with many controllers and teams</li>
</ul>
<h3>Interview comparison — Minimal API vs Traditional Web API</h3>
<table>
<tr><th>Minimal API</th><th>Traditional API</th></tr>
<tr><td>Routes in Program.cs</td><td>Routes in Controllers</td></tr>
<tr><td>Minimal code</td><td>More files</td></tr>
<tr><td>Faster startup</td><td>More structured</td></tr>
<tr><td>Best for lightweight services</td><td>Best for enterprise apps</td></tr>
</table>
<h3>How to create</h3>
<pre><code>dotnet new web
dotnet run
# Test: https://localhost:5001/</code></pre>
<h3>Interview Answer</h3>
<p>Minimal APIs (.NET 6+) let me define routes inline in Program.cs with MapGet/MapPost and DI-injected services — great for microservices and small APIs with less boilerplate. Controllers are better for large enterprise APIs that need filters, versioning, and clear separation across many endpoints. I pick based on project size and team structure.</p>""",
}
