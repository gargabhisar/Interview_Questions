ANSWERS = {
"q_111": """<h2>async/await vs Task.Run</h2>
<p><strong>async/await</strong> is for non-blocking asynchronous I/O (HTTP, database, file streams). It frees the calling thread while work completes and resumes on a synchronization context when the await finishes. <strong>Task.Run</strong> offloads CPU-bound work to a thread-pool thread; it does not make I/O async—it wraps synchronous CPU work so the UI or request thread stays responsive.</p>
<pre><code>// I/O-bound: async/await (no extra thread while waiting)
public async Task&lt;string&gt; GetUserAsync(int id)
{
    var response = await _httpClient.GetAsync($"/users/{id}");
    return await response.Content.ReadAsStringAsync();
}

// CPU-bound: Task.Run (uses thread pool)
public async Task&lt;int&gt; ComputeHashAsync(byte[] data)
{
    return await Task.Run(() =&gt; ExpensiveHash(data));
}

// Anti-pattern: Task.Run around I/O
await Task.Run(() =&gt; _httpClient.GetStringAsync(url)); // wastes a thread</code></pre>
<h3>Key Points</h3>
<ul>
<li>async/await = cooperative, I/O-bound; Task.Run = parallel CPU on pool threads.</li>
<li>Never wrap pure async I/O in Task.Run on ASP.NET Core—it reduces scalability.</li>
<li>async void only for event handlers; prefer async Task everywhere else.</li>
<li>ConfigureAwait(false) in library code avoids deadlocks on UI/legacy ASP.NET.</li>
</ul>
<h3>Interview Answer</h3>
<p>Use <strong>async/await</strong> when waiting on I/O so threads are not blocked. Use <strong>Task.Run</strong> when you must run CPU-intensive synchronous code off the caller thread. They solve different problems; combining them means async/await waits for CPU work queued via Task.Run, not replacing it.</p>""",

"q_105": """<h2>Why async/await When Task Already Exists?</h2>
<p><code>Task</code> and <code>Task&lt;T&gt;</code> represent ongoing or completed asynchronous work. Raw Tasks force manual continuation chaining (<code>.ContinueWith</code>, callbacks), exception handling, and return-value plumbing. <strong>async/await</strong> is syntactic sugar that compiles to a state machine: readable sequential code, automatic exception propagation, and correct Task return types for callers.</p>
<pre><code>// Without async/await — hard to read and error-prone
Task&lt;Order&gt; GetOrderOld(int id)
{
    return _repo.GetCustomerAsync(id)
        .ContinueWith(t =&gt;
        {
            if (t.IsFaulted) throw t.Exception!;
            return _repo.GetOrderAsync(t.Result.OrderId);
        }).Unwrap();
}

// With async/await — same semantics, clearer flow
async Task&lt;Order&gt; GetOrderAsync(int id)
{
    var customer = await _repo.GetCustomerAsync(id);
    return await _repo.GetOrderAsync(customer.OrderId);
}</code></pre>
<h3>Key Points</h3>
<ul>
<li>Task = the abstraction; async/await = ergonomic way to compose Tasks.</li>
<li>Await unwraps exceptions; ContinueWith requires manual fault checking.</li>
<li>Compiler generates IAsyncStateMachine—no magic threads, just continuations.</li>
<li>Methods marked async always return Task/Task&lt;T&gt; (or ValueTask) to callers.</li>
</ul>
<h3>Interview Answer</h3>
<p>We still use <code>Task</code>—async/await does not replace it. Tasks model async operations; async/await lets us write and maintain that logic like synchronous code while preserving non-blocking behavior and proper exception flow.</p>""",

"q_71": """<h2>Task.Run Explained</h2>
<p><code>Task.Run</code> queues a delegate on the .NET thread pool for CPU-bound work. The caller gets a <code>Task</code> immediately; pool threads execute the delegate concurrently. It is ideal when synchronous, compute-heavy code would block a sensitive thread (UI, ASP.NET request thread in older patterns).</p>
<pre><code>// Offload CPU work
var result = await Task.Run(() =&gt; SimulateMonteCarlo(iterations: 1_000_000));

// Overload with CancellationToken
var cts = new CancellationTokenSource(TimeSpan.FromSeconds(30));
await Task.Run(() =&gt; ProcessBatch(items, cts.Token), cts.Token);

// Long-running alternative when you need a dedicated thread
await Task.Factory.StartNew(
    () =&gt; LongRunningListener(),
    TaskCreationOptions.LongRunning);</code></pre>
<h3>Key Points</h3>
<ul>
<li>Schedules work to ThreadPool—not for I/O-bound async APIs.</li>
<li>Returns hot Task; exceptions stored on Task, surfaced on await/Wait.</li>
<li>Prefer async I/O APIs over Task.Run for network/database calls.</li>
<li>LongRunning creates a non-pool thread when pool starvation is a risk.</li>
</ul>
<h3>Interview Answer</h3>
<p><code>Task.Run</code> moves CPU-bound synchronous work to a background thread-pool thread and returns a Task you can await. Use it for parallel computation, not as a substitute for truly asynchronous I/O.</p>""",

"q_72": """<h2>Thread vs Task</h2>
<p>A <strong>Thread</strong> is an OS-level execution unit—you create it, set priority, and manage its lifetime manually. A <strong>Task</strong> is a higher-level abstraction representing work that the thread pool may run; the runtime schedules Tasks onto available threads efficiently.</p>
<pre><code>// Thread — explicit, heavier
var thread = new Thread(() =&gt; DoWork()) { IsBackground = true };
thread.Start();
thread.Join();

// Task — preferred for most scenarios
await Task.Run(() =&gt; DoWork());

// Task enables composition
var tasks = urls.Select(url =&gt; DownloadAsync(url));
await Task.WhenAll(tasks);</code></pre>
<h3>Key Points</h3>
<ul>
<li>Threads are expensive (~1 MB stack); pool reuse is cheaper.</li>
<li>Tasks support await, WhenAll, cancellation, and exception aggregation.</li>
<li>Creating many raw Threads can hurt scalability; Task uses pool.</li>
<li>Use dedicated Thread only for STA COM, long-blocking listeners, or special cases.</li>
</ul>
<h3>Interview Answer</h3>
<p>Threads are low-level OS workers you manage directly. Tasks represent units of work scheduled by the thread pool with rich async composition. In modern .NET, prefer Task/async unless you have a specific reason to own a Thread.</p>""",

"q_73": """<h2>Task.Wait and Blocking Pitfalls</h2>
<p><code>Task.Wait()</code>, <code>Task.Result</code>, and <code>GetAwaiter().GetResult()</code> synchronously block the calling thread until the Task completes. On contexts with a synchronization context (UI, legacy ASP.NET), blocking while waiting for code that needs that same context causes <strong>deadlocks</strong>.</p>
<pre><code>// Dangerous on UI / ASP.NET (deadlock risk)
public Order GetOrderBlocking(int id)
{
    return _service.GetOrderAsync(id).Result; // blocks
}

// Preferred
public async Task&lt;Order&gt; GetOrderAsync(int id)
{
    return await _service.GetOrderAsync(id);
}

// Library code avoiding context capture
await _httpClient.GetAsync(url).ConfigureAwait(false);</code></pre>
<h3>Key Points</h3>
<ul>
<li>Never block on async code in ASP.NET Core request paths if avoidable.</li>
<li>AggregateException wraps Task exceptions on Wait/Result—harder to debug.</li>
<li>async all the way down is the scalable pattern.</li>
<li>ConfigureAwait(false) in libraries reduces deadlock on sync-over-async.</li>
</ul>
<h3>Interview Answer</h3>
<p><code>Task.Wait</code> blocks the current thread until completion. Avoid it in async-friendly apps—use await instead. Blocking on incomplete Tasks tied to the same synchronization context is a common deadlock source.</p>""",

"q_75": """<h2>Delegates in C#</h2>
<p>A <strong>delegate</strong> is a type-safe function pointer: it references a method with a matching signature. Delegates enable callbacks, event handling, LINQ, and functional patterns. Multicast delegates invoke multiple methods in order.</p>
<pre><code>public delegate int MathOp(int a, int b);

MathOp add = (a, b) =&gt; a + b;
MathOp multiply = (a, b) =&gt; a * b;

MathOp combined = add + multiply; // multicast
Console.WriteLine(combined(2, 3)); // 5 then 6

// Common built-ins
Func&lt;int, int, int&gt; sum = (a, b) =&gt; a + b;
Action&lt;string&gt; log = msg =&gt; Console.WriteLine(msg);</code></pre>
<h3>Key Points</h3>
<ul>
<li>Delegates are reference types; null delegate throws on invoke.</li>
<li>+= and -= add/remove targets on multicast delegates.</li>
<li>Func, Action, Predicate are predefined generic delegate types.</li>
<li>Events are delegates with restricted add/remove accessors.</li>
</ul>
<h3>Interview Answer</h3>
<p>A delegate defines a method signature and holds one or more method references. They decouple callers from implementations—used for events, callbacks, and passing behavior as data. Built-in generic delegates reduce boilerplate.</p>""",

"q_77": """<h2>Action, Func, and Predicate</h2>
<p>These are predefined generic delegates in <code>System</code>. <strong>Action</strong> returns void. <strong>Func</strong> returns a value (last type parameter is return type). <strong>Predicate</strong> returns bool—a special case of Func for filtering.</p>
<pre><code>Action&lt;string&gt; print = s =&gt; Console.WriteLine(s);
Action&lt;int, int&gt; logSum = (a, b) =&gt; Console.WriteLine(a + b);

Func&lt;int, int, int&gt; add = (a, b) =&gt; a + b;
Func&lt;string, bool&gt; isValid = s =&gt; !string.IsNullOrEmpty(s);

Predicate&lt;int&gt; isEven = n =&gt; n % 2 == 0;
// equivalent: Func&lt;int, bool&gt; isEven = n =&gt; n % 2 == 0;

var evens = numbers.FindAll(isEven);</code></pre>
<h3>Key Points</h3>
<ul>
<li>Action&lt;T1,...&gt; — up to 16 params, no return value.</li>
<li>Func&lt;T1,..., TResult&gt; — last generic arg is return type.</li>
<li>Predicate&lt;T&gt; is Func&lt;T, bool&gt;; common in List.FindAll.</li>
<li>Prefer these over custom delegate types unless naming adds clarity.</li>
</ul>
<h3>Interview Answer</h3>
<p>Action is a void-returning delegate, Func returns a typed result, and Predicate is a bool-returning filter delegate. They standardize passing lambdas and methods as arguments across LINQ, callbacks, and APIs.</p>""",

"q_79": """<h2>Preventing Memory Leaks in .NET</h2>
<p>.NET has GC, but leaks still occur when rooted objects hold references to objects that should be collected—event handlers, static caches, undisposed unmanaged resources, and long-lived collections capturing short-lived contexts.</p>
<pre><code>// Leak: subscriber never unsubscribes
publisher.Raised += OnRaised;

// Fix: unsubscribe or weak event pattern
publisher.Raised -= OnRaised;

// Always dispose unmanaged / IDisposable resources
await using var conn = new SqlConnection(cs);
await conn.OpenAsync();

// Avoid capturing large graphs in static caches without eviction
_cache.Set(key, value, TimeSpan.FromMinutes(5));</code></pre>
<h3>Key Points</h3>
<ul>
<li>Unsubscribe events or use WeakReference for long-lived publishers.</li>
<li>Implement IDisposable/IAsyncDisposable for files, sockets, handles.</li>
<li>Be cautious with static fields, singletons, and Timer callbacks.</li>
<li>Profile with dotMemory, PerfView, or VS Diagnostic Tools for retained paths.</li>
</ul>
<h3>Interview Answer</h3>
<p>Prevent leaks by breaking unintended object graphs: unsubscribe events, dispose resources, limit static/cache retention, and avoid holding references to UI or request-scoped objects in singletons. Use profiling to find what keeps objects alive.</p>""",

"q_82": """<h2>yield return and Iterators</h2>
<p><code>yield return</code> builds an iterator: the compiler generates a state machine implementing <code>IEnumerable&lt;T&gt;</code> or <code>IAsyncEnumerable&lt;T&gt;</code>. Elements are produced lazily on demand—memory-efficient for large or infinite sequences.</p>
<pre><code>public IEnumerable&lt;int&gt; GetSquares(int max)
{
    for (int i = 0; i &lt; max; i++)
        yield return i * i;
}

foreach (var sq in GetSquares(1_000_000)) { /* one at a time */ }

// Async streaming (.NET Core+)
async IAsyncEnumerable&lt;Order&gt; StreamOrdersAsync()
{
    await foreach (var batch in _repo.ReadBatchesAsync())
        foreach (var order in batch)
            yield return order;
}</code></pre>
<h3>Key Points</h3>
<ul>
<li>Lazy evaluation—work runs when enumerator moves Next.</li>
<li>Cannot yield in try block with catch (language restriction; use finally carefully).</li>
<li>Iterator methods cannot have ref/out parameters.</li>
<li>Prefer yield for pipelines; materialize with ToList when reuse needed.</li>
</ul>
<h3>Interview Answer</h3>
<p><code>yield return</code> defers execution and streams items one-by-one instead of building a full in-memory collection. It simplifies lazy pipelines and reduces memory for large datasets.</p>""",

"q_83": """<h2>Alternatives to Task.WhenAll</h2>
<p><code>Task.WhenAll</code> waits for multiple Tasks concurrently. Alternatives depend on semantics: fail-fast vs collect-all-errors, throttling, sequential dependency, or parallel loops over CPU work.</p>
<pre><code>// WhenAll — all parallel, one exception on await (others may still run)
var results = await Task.WhenAll(tasks);

// WhenAny — first completion (timeout/race pattern)
var finished = await Task.WhenAny(task, Task.Delay(5000));

// Parallel.ForEachAsync — bounded parallelism (.NET 6+)
await Parallel.ForEachAsync(items,
    new ParallelOptions { MaxDegreeOfParallelism = 4 },
    async (item, ct) =&gt; await ProcessAsync(item, ct));

// Manual throttling with SemaphoreSlim
using var gate = new SemaphoreSlim(4);
var throttled = items.Select(async i =&gt; {
    await gate.WaitAsync();
    try { return await WorkAsync(i); }
    finally { gate.Release(); }
});
await Task.WhenAll(throttled);</code></pre>
<h3>Key Points</h3>
<ul>
<li>WhenAny for timeouts, caching first response, or competitive calls.</li>
<li>Parallel.ForEach/ForEachAsync for CPU-bound batch with degree control.</li>
<li>SemaphoreSlim limits concurrent I/O when APIs have rate limits.</li>
<li>Task.WhenAll fails on first fault unless you observe all Task.Exception.</li>
</ul>
<h3>Interview Answer</h3>
<p>Use WhenAll for unconstrained parallel awaits. Use WhenAny for first-wins scenarios, Parallel.ForEachAsync for bounded CPU parallelism, and SemaphoreSlim when you must cap concurrent operations. Choose based on error handling and resource limits.</p>""",

"q_84": """<h2>Parallel Programming in .NET</h2>
<p>Parallel programming splits work across cores. .NET offers <code>Parallel</code> (PLINQ, Parallel.For/ForEach), TPL Dataflow for pipelines, and async coordination via Tasks. Effective parallelism requires CPU-bound work and minimal shared mutable state.</p>
<pre><code>// Parallel.For — partition work across cores
Parallel.For(0, items.Length, i =&gt; Process(items[i]));

// PLINQ
var primes = Enumerable.Range(2, 10000)
    .AsParallel()
    .WithDegreeOfParallelism(4)
    .Where(IsPrime)
    .ToList();

// Thread-safe aggregation
var bag = new ConcurrentBag&lt;Result&gt;();
Parallel.ForEach(source, item =&gt; bag.Add(Transform(item)));</code></pre>
<h3>Key Points</h3>
<ul>
<li>Parallelism helps CPU-bound work—not blocked I/O (use async there).</li>
<li>Race conditions need locks, Interlocked, or concurrent collections.</li>
<li>Over-parallelization adds scheduling overhead—tune MaxDegreeOfParallelism.</li>
<li>Amdahl's Law: speedup limited by serial portions of algorithm.</li>
</ul>
<h3>Interview Answer</h3>
<p>.NET parallel APIs map work to multiple cores via the thread pool. Use Parallel/PLINQ for CPU-heavy batches with controlled concurrency and thread-safe aggregation. Combine with async for I/O, not as a replacement.</p>""",

"q_85": """<h2>Multithreading Fundamentals</h2>
<p>Multithreading runs multiple threads within one process sharing memory space. It improves throughput for parallel workloads but introduces complexity: race conditions, deadlocks, and visibility issues without proper synchronization.</p>
<pre><code>private readonly object _lock = new();
private int _count;

void Increment()
{
    lock (_lock) { _count++; } // mutual exclusion
}

// Or lock-free
Interlocked.Increment(ref _count);

// Reader/writer scenario
private readonly ReaderWriterLockSlim _rw = new();
_rw.EnterReadLock();
try { /* read shared data */ }
finally { _rw.ExitReadLock(); }</code></pre>
<h3>Key Points</h3>
<ul>
<li>Shared mutable state requires synchronization (lock, Monitor, SemaphoreSlim).</li>
<li>Prefer higher abstractions (Task, ConcurrentDictionary) over raw locks when possible.</li>
<li>Deadlock: circular lock acquisition—consistent lock ordering prevents it.</li>
<li>volatile/Interlocked address visibility and atomic ops, not complex invariants.</li>
</ul>
<h3>Interview Answer</h3>
<p>Multithreading executes concurrent paths in one process for parallelism. Success depends on identifying shared state, choosing correct synchronization, and avoiding deadlocks and races—often by immutability or concurrent collections.</p>""",

"q_66": """<h2>API Performance Optimization</h2>
<p>Production API tuning spans architecture, data access, and runtime behavior. Measure first (p95/p99 latency, throughput, error rate), then optimize the slowest layers—usually database, serialization, or unnecessary work per request.</p>
<pre><code>// Response caching + compression
services.AddResponseCaching();
services.AddResponseCompression();

// Efficient data access — projection, no N+1
var orders = await _db.Orders
    .AsNoTracking()
    .Where(o =&gt; o.CustomerId == id)
    .Select(o =&gt; new OrderDto { Id = o.Id, Total = o.Total })
    .ToListAsync();

// Pagination — never return unbounded lists
return await query.Skip(page * size).Take(size).ToListAsync();</code></pre>
<h3>Key Points</h3>
<ul>
<li>Cache hot reads (Redis/CDN); invalidate explicitly on writes.</li>
<li>Async I/O, connection pooling, indexed queries, avoid SELECT *.</li>
<li>Pagination, compression, and DTO projection reduce payload size.</li>
<li>Rate limiting, circuit breakers, and horizontal scale for resilience.</li>
</ul>
<h3>Interview Answer</h3>
<p>Optimize APIs by profiling end-to-end, fixing database and N+1 bottlenecks, caching idempotent reads, paginating responses, using async I/O, and designing for horizontal scale with observability on latency percentiles—not just averages.</p>""",

"q_86": """<h2>Production RCA Steps</h2>
<p>Root Cause Analysis in production is a structured incident response: stabilize, observe, hypothesize, verify, fix, and prevent recurrence. Speed matters, but changing production without evidence increases blast radius.</p>
<pre><code>// Observability-first mindset
// 1. Check alerts, dashboards (latency, errors, saturation)
// 2. Correlate logs/traces by correlationId
_logger.LogError(ex, "Payment failed {OrderId} {CorrelationId}",
    orderId, Activity.Current?.Id);

// 3. Compare deploy/config changes in incident window
// 4. Roll forward fix or rollback behind feature flag
if (_flags.IsEnabled("new-pricing-engine"))
    await _newEngine.PriceAsync(order);
else
    await _legacyEngine.PriceAsync(order);</code></pre>
<h3>Key Points</h3>
<ul>
<li>Stabilize: rollback, scale, drain, or feature-flag off bad path.</li>
<li>Timeline: deploys, config, traffic spikes, dependency outages.</li>
<li>Use logs, metrics, traces—not guesses; reproduce in staging if possible.</li>
<li>Post-incident: blameless review, action items, runbooks, alerting gaps.</li>
</ul>
<h3>Interview Answer</h3>
<p>RCA starts with customer impact and mitigation, then uses telemetry and change history to find the true root cause—not the symptom. Document timeline, fix with validation, and close with preventive measures and improved monitoring.</p>""",

"q_3": """<h2>Capital Markets: KYC, AML, Trade Lifecycle, MDOP</h2>
<p>Capital markets systems must satisfy regulatory controls while executing trades accurately. Interviewers expect fluency in onboarding compliance and operational data flows from order capture through settlement.</p>
<pre><code>// Illustrative trade lifecycle states
public enum TradeStatus
{
    Captured, Validated, Enriched, SentToExchange,
    Acknowledged, Filled, Allocated, Confirmed, Settled
}

// KYC/AML checks often gate account activation
if (!await _kycService.IsVerifiedAsync(clientId))
    throw new ComplianceException("KYC incomplete");
await _amlService.ScreenTransactionAsync(trade);</code></pre>
<h3>Key Points</h3>
<ul>
<li><strong>KYC</strong>: verify identity, beneficial ownership, risk profile before trading.</li>
<li><strong>AML</strong>: monitor transactions, sanctions screening, SAR escalation.</li>
<li><strong>Trade lifecycle</strong>: order → execution → allocation → confirmation → settlement (T+n).</li>
<li><strong>MDOP</strong>: Market Data Operations Platform—feeds, entitlements, symbology, golden copy.</li>
</ul>
<h3>Interview Answer</h3>
<p>KYC onboards compliant clients; AML detects suspicious activity ongoing. Trades move through capture, validation, execution, allocation, and settlement with audit trails. MDOP ensures authoritative market data distribution with entitlements and consistent instrument identifiers across front-to-back systems.</p>""",

"q_4": """<h2>Multiple catch Blocks in try-catch</h2>
<p>C# evaluates <code>catch</code> clauses top to bottom; the first matching exception type handles it. Specific exceptions must come before general ones. Only one catch runs per thrown exception.</p>
<pre><code>try
{
    var json = File.ReadAllText(path);
    var data = JsonSerializer.Deserialize&lt;Order&gt;(json);
}
catch (JsonException ex)
{
    _logger.LogWarning(ex, "Invalid JSON");
}
catch (FileNotFoundException ex)
{
    _logger.LogError(ex, "File missing");
}
catch (IOException ex) when (ex.HResult == -2147024784)
{
    // filter clause — disk full
}
catch (Exception ex)
{
    _logger.LogCritical(ex, "Unexpected failure");
    throw; // preserve stack trace
}</code></pre>
<h3>Key Points</h3>
<ul>
<li>Order: most specific → least specific; Exception last.</li>
<li>catch when filters on type plus condition without catching base first incorrectly.</li>
<li>Use throw; not throw ex; to rethrow preserving stack.</li>
<li>finally runs regardless—use for cleanup (Dispose patterns).</li>
</ul>
<h3>Interview Answer</h3>
<p>Multiple catch blocks let you handle different failure types differently. Place specific handlers first, optionally use exception filters with when, and use a general catch only for logging before rethrow or graceful degradation.</p>""",

"q_45": """<h2>Async &amp; Await in C#</h2>
<p><strong>async/await</strong> enables non-blocking asynchronous code. The compiler rewrites an <code>async</code> method into a state machine that can suspend at <code>await</code> and resume when the awaited <code>Task</code> completes — without holding a thread while waiting on I/O.</p>
<pre><code>// I/O-bound — thread is released while waiting
public async Task&lt;User&gt; GetUserAsync(int id)
{
    var response = await _httpClient.GetAsync($"/users/{id}");
    response.EnsureSuccessStatusCode();
    return await response.Content.ReadFromJsonAsync&lt;User&gt;();
}

// Multiple awaits — sequential flow, still readable
public async Task&lt;OrderSummary&gt; BuildSummaryAsync(int orderId)
{
    var order = await _repo.GetOrderAsync(orderId);
    var customer = await _repo.GetCustomerAsync(order.CustomerId);
    return new OrderSummary(order, customer);
}

// Parallel I/O
var tasks = ids.Select(id =&gt; GetUserAsync(id));
var users = await Task.WhenAll(tasks);</code></pre>
<h3>How It Works</h3>
<ul>
<li><code>async</code> on a method returns <code>Task</code> or <code>Task&lt;T&gt;</code> (or <code>void</code> for event handlers only).</li>
<li>At each <code>await</code>, if the operation is incomplete, the method returns control to the caller; the thread can serve other work.</li>
<li>When the awaited task completes, the state machine resumes — often on a thread-pool thread (ASP.NET Core has no sync context by default).</li>
<li>Exceptions thrown inside an async method are captured on the returned Task and rethrown when you await it.</li>
</ul>
<h3>async/await vs Task.Run</h3>
<p>Use <strong>async/await</strong> for I/O-bound work (HTTP, DB, files). Use <strong>Task.Run</strong> only to offload CPU-bound synchronous code to the thread pool — wrapping I/O in Task.Run wastes threads.</p>
<h3>Key Points</h3>
<ul>
<li>Prefer <code>async Task</code> over <code>async void</code> except for event handlers.</li>
<li>Avoid <code>.Result</code> and <code>.Wait()</code> on async code — can deadlock on UI or legacy ASP.NET.</li>
<li><code>ConfigureAwait(false)</code> in library code avoids capturing synchronization context.</li>
<li>async all the way down: async controllers/services/repos compose cleanly.</li>
</ul>
<h3>Interview Answer</h3>
<p>async/await lets you write sequential-looking code that does not block threads during I/O. The compiler builds a state machine around Tasks. I use it for HTTP, database, and file operations; I avoid blocking on Tasks and I do not wrap async I/O in Task.Run on server code.</p>""",

"q_51": """<h2>.NET Garbage Collector</h2>
<p>The GC reclaims managed heap memory for objects no longer reachable from GC roots (stack, static fields, CPU registers). It uses generational collection: Gen0 (short-lived), Gen1 (buffer), Gen2 (long-lived), plus LOH for large objects.</p>
<h3>How It Works</h3>
<ol>
<li><strong>Mark</strong> — Starting from roots, the GC traces object references and marks every reachable object.</li>
<li><strong>Sweep / compact</strong> — Unmarked objects are reclaimed; on younger generations the heap may be compacted to reduce fragmentation.</li>
<li><strong>Promote survivors</strong> — Objects that survive a Gen0 collection move to Gen1; survivors of Gen1 move to Gen2. Long-lived objects are collected less often.</li>
<li><strong>Finalizers</strong> — Objects with destructors go to a finalizer queue; they survive one extra collection cycle (prefer <code>IDisposable</code> instead).</li>
</ol>
<p>Collections are triggered when a generation budget is exceeded or under memory pressure. Full Gen2 collections are the most expensive.</p>
<pre><code>// Gen0 collections are frequent and cheap
var list = new List&lt;byte[]&gt;();
for (int i = 0; i &lt; 1000; i++)
    list.Add(new byte[100]); // mostly Gen0, ephemeral

// LOH allocations (&gt;= 85 KB) collected less often
var big = new byte[100_000];

// Reduce GC pressure — pool/reuse
var buffer = ArrayPool&lt;byte&gt;.Shared.Rent(4096);
try { /* use buffer */ }
finally { ArrayPool&lt;byte&gt;.Shared.Return(buffer); }</code></pre>
<h3>Key Points</h3>
<ul>
<li>Generational hypothesis: most objects die young.</li>
<li>Full GC (Gen2) is expensive—avoid unnecessary allocations in hot paths.</li>
<li>IDisposable is for unmanaged resources; GC handles managed memory.</li>
<li>Server GC vs Workstation GC tuned for throughput vs interactive apps.</li>
</ul>
<h3>Interview Answer</h3>
<p>The GC is a generational, tracing collector: it marks reachable objects from roots, frees unreachable ones, and promotes survivors across Gen0/Gen1/Gen2 to keep collections cheap for short-lived objects. I minimize allocations in hot paths, avoid LOH churn, and use IDisposable for unmanaged resources the GC does not know about.</p>""",

"q_52": """<h2>throw vs throw ex</h2>
<p><code>throw;</code> rethrows the current exception preserving the original stack trace. <code>throw ex;</code> (or <code>throw someCaughtEx</code>) resets the stack trace to the rethrow site, hiding where the error actually occurred—bad for diagnostics.</p>
<pre><code>try
{
    await _repo.SaveAsync(entity);
}
catch (SqlException ex)
{
    _logger.LogError(ex, "DB save failed");
    throw; // correct — original stack preserved
}

// Anti-pattern
catch (Exception ex)
{
    throw ex; // stack starts here — loses root frame info
}

// Wrapping when adding context
catch (Exception ex)
{
    throw new OrderProcessingException("Save failed", ex);
}</code></pre>
<h3>Key Points</h3>
<ul>
<li>Always use bare throw; inside catch to rethrow.</li>
<li>throw ex resets StackTrace—avoid in production code.</li>
<li>Wrap with inner exception when translating domain errors.</li>
<li>ExceptionDispatchInfo.Capture(ex).Throw() preserves stack outside catch.</li>
</ul>
<h3>Interview Answer</h3>
<p>Use <code>throw;</code> to rethrow without losing stack trace. Use <code>throw ex;</code> only if you intentionally want a new stack (rare). When wrapping, pass the original as InnerException for full context.</p>""",

"q_78": """<h2>Extension Methods</h2>
<p>Extension methods are static methods in static classes that appear as instance methods on the extended type via <code>this</code> on the first parameter. They cannot access private members; they enable fluent APIs without modifying sealed or third-party types.</p>
<pre><code>public static class StringExtensions
{
    public static bool IsNullOrBlank(this string? value)
        =&gt; string.IsNullOrWhiteSpace(value);

    public static string Truncate(this string value, int max)
        =&gt; value.Length &lt;= max ? value : value[..max];
}

// Usage
if (input.IsNullOrBlank()) return;
var shortText = name.Truncate(50);

// LINQ itself uses extensions on IEnumerable&lt;T&gt;</code></pre>
<h3>Key Points</h3>
<ul>
<li>Must live in non-generic static class; method must be static.</li>
<li>Namespace must be in scope (using) for IntelliSense to find it.</li>
<li>Resolution: instance method wins over extension if both match.</li>
<li>Use sparingly—avoid polluting IntelliSense on core types.</li>
</ul>
<h3>Interview Answer</h3>
<p>Extension methods add functionality to existing types syntactically like instance methods but compile to static calls. They power LINQ and cross-cutting helpers on types you cannot inherit or modify.</p>""",
}
