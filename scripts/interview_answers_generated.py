ANSWERS = {
"q_90": """<h2>Encapsulation in C#</h2>
<p>Encapsulation is an OOP principle that bundles data and behavior inside a class while hiding internal state from outside code. In C#, you achieve this with access modifiers (<code>private</code>, <code>protected</code>, <code>internal</code>) and controlled entry points such as properties and methods.</p>
<p>Instead of exposing fields directly, you validate and transform data through properties. This prevents invalid states, localizes change, and makes classes easier to test and maintain.</p>
<pre><code>public class BankAccount
{
    private decimal _balance;
    public decimal Balance =&gt; _balance;

    public void Deposit(decimal amount)
    {
        if (amount &lt;= 0) throw new ArgumentException("Amount must be positive.");
        _balance += amount;
    }
}</code></pre>
<h3>Key Points</h3>
<ul>
<li>Hides implementation details and protects invariants.</li>
<li>Properties provide read/write control without breaking encapsulation.</li>
<li>Encapsulation improves maintainability and reduces coupling.</li>
</ul>
<h3>Interview Answer</h3>
<p>Encapsulation means keeping an object's data private and exposing only what is necessary through a public API. In C#, I use private fields with public properties or methods so validation and business rules stay inside the class. This protects data integrity and makes future changes safer.</p>""",

"q_91": """<h2>Abstract Class vs Interface</h2>
<p>Both support abstraction and polymorphism, but they solve different design problems. An abstract class can contain state, constructors, and both abstract and concrete members. An interface defines a contract—method signatures and, since C# 8, default implementations—without enforcing a single inheritance hierarchy.</p>
<p>Choose an abstract class when related types share common behavior and fields. Choose an interface when you need multiple contracts or want to decouple consumers from concrete implementations.</p>
<table>
<tr><th>Feature</th><th>Abstract Class</th><th>Interface</th></tr>
<tr><td>Inheritance</td><td>Single base class</td><td>Multiple interfaces</td></tr>
<tr><td>State</td><td>Can have fields</td><td>No instance fields (until C# 8 defaults)</td></tr>
<tr><td>Constructors</td><td>Supported</td><td>Not allowed</td></tr>
<tr><td>Best for</td><td>Shared base behavior</td><td>Capabilities/contracts</td></tr>
</table>
<pre><code>public abstract class PaymentProcessor
{
    public abstract Task ProcessAsync(decimal amount);
}

public interface IEmailSender
{
    Task SendAsync(string to, string body);
}</code></pre>
<h3>Key Points</h3>
<ul>
<li>Abstract class = "is-a" with shared implementation.</li>
<li>Interface = "can-do" contract, supports multiple inheritance.</li>
<li>Prefer composition + interfaces for flexible ASP.NET Core designs.</li>
</ul>
<h3>Interview Answer</h3>
<p>I use abstract classes when derived types share common state and partial implementation, and interfaces when I need a contract that multiple unrelated classes can implement. In .NET APIs, interfaces are common for DI and testability because a class can implement many interfaces but inherit only one base class.</p>""",

"q_92": """<h2>Why Use Interfaces?</h2>
<p>Interfaces define what a component can do without tying callers to a specific implementation. In C# and ASP.NET Core, this is the foundation of dependency inversion: controllers depend on <code>IUserService</code>, not on a concrete database-backed service.</p>
<p>Interfaces improve testability because you can substitute mocks or fakes in unit tests. They also enable swapping implementations—SQL vs NoSQL, SMTP vs SendGrid—without changing consumer code.</p>
<pre><code>public interface IOrderRepository
{
    Task&lt;Order?&gt; GetByIdAsync(int id);
}

public class OrderController : ControllerBase
{
    private readonly IOrderRepository _repo;
    public OrderController(IOrderRepository repo) =&gt; _repo = repo;
}</code></pre>
<h3>Key Points</h3>
<ul>
<li>Decouples consumers from concrete types.</li>
<li>Enables DI, mocking, and plug-in architectures.</li>
<li>Supports multiple contracts per class.</li>
</ul>
<h3>Interview Answer</h3>
<p>Interfaces let me program against abstractions instead of concrete classes, which makes code easier to test and extend. In ASP.NET Core, registering <code>IEmailSender</code> in DI means I can change the implementation without touching controllers. They express capabilities clearly and support loose coupling across layers.</p>""",

"q_93": """<h2>Generics in C#</h2>
<p>Generics let you write type-safe, reusable code without boxing value types or casting on every use. A generic class or method is defined with a type parameter (for example, <code>T</code>) that is resolved at compile time.</p>
<p>Collections like <code>List&lt;T&gt;</code> and patterns like repositories use generics to enforce correctness while staying flexible. The compiler generates specialized code for value types and shares code for reference types.</p>
<pre><code>public class Repository&lt;T&gt; where T : class
{
    private readonly List&lt;T&gt; _items = new();
    public void Add(T item) =&gt; _items.Add(item);
    public T? Find(Predicate&lt;T&gt; match) =&gt; _items.Find(match);
}

var users = new List&lt;User&gt;();
users.Add(new User { Id = 1 }); // compile-time type safety</code></pre>
<h3>Key Points</h3>
<ul>
<li>Compile-time type safety; fewer runtime casts.</li>
<li>Constraints (<code>where T : ...</code>) limit allowed type arguments.</li>
<li>Avoids boxing for value types in generic collections.</li>
</ul>
<h3>Interview Answer</h3>
<p>Generics allow reusable, strongly typed APIs like <code>List&lt;int&gt;</code> or <code>Repository&lt;Order&gt;</code> without sacrificing performance or safety. The compiler checks types at compile time, so I get IntelliSense and fewer <code>InvalidCastException</code> issues at runtime.</p>""",

"q_106": """<h2>OOP Concepts in C#</h2>
<p>Object-Oriented Programming organizes software around objects that combine data and behavior. C# supports the four pillars: encapsulation, abstraction, inheritance, and polymorphism—plus related ideas like composition and interfaces.</p>
<p>In practice, you model domain entities as classes, hide details behind abstractions, reuse behavior through inheritance or composition, and invoke the right implementation at runtime via virtual methods or interfaces.</p>
<table>
<tr><th>Pillar</th><th>C# Example</th></tr>
<tr><td>Encapsulation</td><td>Private fields + public properties</td></tr>
<tr><td>Abstraction</td><td>Abstract classes, interfaces</td></tr>
<tr><td>Inheritance</td><td><code>class Dog : Animal</code></td></tr>
<tr><td>Polymorphism</td><td><code>override</code>, interface dispatch</td></tr>
</table>
<pre><code>public interface INotifier { void Notify(string msg); }
public class EmailNotifier : INotifier
{
    public void Notify(string msg) =&gt; Console.WriteLine(msg);
}</code></pre>
<h3>Key Points</h3>
<ul>
<li>Four pillars guide maintainable domain modeling.</li>
<li>Favor composition and interfaces over deep inheritance trees.</li>
<li>Polymorphism enables extensible, testable designs.</li>
</ul>
<h3>Interview Answer</h3>
<p>C# OOP is built on encapsulation, abstraction, inheritance, and polymorphism. I encapsulate state in classes, abstract behavior with interfaces, reuse code through inheritance or composition, and rely on polymorphism so consumers depend on contracts rather than concrete types.</p>""",

"q_116": """<h2>Encapsulation vs Abstraction</h2>
<p>These concepts are related but not the same. <strong>Encapsulation</strong> is about hiding internal details and controlling access to data. <strong>Abstraction</strong> is about exposing only essential behavior and suppressing complexity—what an object does, not how it does it.</p>
<p>Encapsulation uses access modifiers and properties. Abstraction uses interfaces, abstract classes, and high-level APIs. You often use both together: an interface abstracts payment processing while the concrete class encapsulates gateway credentials and retry logic.</p>
<table>
<tr><th>Aspect</th><th>Encapsulation</th><th>Abstraction</th></tr>
<tr><td>Focus</td><td>Data hiding</td><td>Complexity hiding</td></tr>
<tr><td>Mechanism</td><td>private, properties</td><td>interfaces, abstract members</td></tr>
<tr><td>Question answered</td><td>Who can see/change state?</td><td>What capability is offered?</td></tr>
</table>
<h3>Key Points</h3>
<ul>
<li>Encapsulation protects invariants; abstraction simplifies usage.</li>
<li>Interfaces provide abstraction; private members provide encapsulation.</li>
<li>Good design uses both at different layers.</li>
</ul>
<h3>Interview Answer</h3>
<p>Encapsulation hides and protects an object's internal state, while abstraction hides implementation complexity and shows only what callers need. A public interface method is abstraction; making the database connection string private is encapsulation.</p>""",

"q_99": """<h2>Overloading vs Overriding</h2>
<p><strong>Method overloading</strong> defines multiple methods with the same name but different parameter lists in the same class. Resolution happens at compile time (static polymorphism). <strong>Method overriding</strong> replaces a base class virtual/abstract method in a derived class; resolution happens at runtime (dynamic polymorphism).</p>
<p>Overloading improves API ergonomics (<code>Send(string)</code>, <code>Send(string, bool)</code>). Overriding enables specialized behavior in inheritance hierarchies while keeping a common contract.</p>
<table>
<tr><th></th><th>Overloading</th><th>Overriding</th></tr>
<tr><td>Scope</td><td>Same class</td><td>Base + derived class</td></tr>
<tr><td>Signature</td><td>Must differ</td><td>Same signature</td></tr>
<tr><td>Keywords</td><td>None</td><td><code>virtual</code>, <code>override</code></td></tr>
<tr><td>Binding</td><td>Compile-time</td><td>Runtime</td></tr>
</table>
<pre><code>public void Log(string msg) { }
public void Log(string msg, int level) { } // overload

public class Base { public virtual void Run() { } }
public class Derived : Base { public override void Run() { } }</code></pre>
<h3>Key Points</h3>
<ul>
<li>Overload = same name, different parameters, same class.</li>
<li>Override = redefine inherited virtual/abstract method.</li>
<li>Do not confuse override with <code>new</code> hiding.</li>
</ul>
<h3>Interview Answer</h3>
<p>Overloading is compile-time polymorphism where I define multiple methods with the same name but different signatures. Overriding is runtime polymorphism where a derived class replaces a base virtual method. Overloading improves usability; overriding enables extensible inheritance.</p>""",

"q_100": """<h2>Virtual vs Abstract Methods</h2>
<p>Both support polymorphism, but they serve different roles. A <code>virtual</code> method has a default implementation in the base class and may be overridden. An <code>abstract</code> method has no implementation and must be overridden in a non-abstract derived class.</p>
<p>Virtual methods suit optional customization points. Abstract methods force derived types to provide behavior and are only allowed in abstract classes.</p>
<table>
<tr><th></th><th>virtual</th><th>abstract</th></tr>
<tr><td>Implementation</td><td>Provided in base</td><td>Not provided</td></tr>
<tr><td>Class requirement</td><td>Any class</td><td>Abstract class only</td></tr>
<tr><td>Override required?</td><td>No</td><td>Yes (in concrete child)</td></tr>
</table>
<pre><code>public abstract class Shape
{
    public abstract double Area();
    public virtual void Draw() =&gt; Console.WriteLine("Drawing shape");
}

public class Circle : Shape
{
    public override double Area() =&gt; Math.PI * Radius * Radius;
}</code></pre>
<h3>Key Points</h3>
<ul>
<li>virtual = optional override with default behavior.</li>
<li>abstract = mandatory override, no base body.</li>
<li>Sealed override (<code>sealed override</code>) stops further overriding.</li>
</ul>
<h3>Interview Answer</h3>
<p>A virtual method provides a default implementation that derived classes can optionally replace. An abstract method declares a required operation with no implementation, so concrete subclasses must override it. I use virtual for extension points and abstract when every derived type must define the behavior.</p>""",

"q_101": """<h2>Sealed Class in C#</h2>
<p>A <code>sealed</code> class cannot be inherited. You seal a class when further derivation would break invariants, security assumptions, or performance optimizations. You can also use <code>sealed override</code> on a method to prevent further overriding down the hierarchy.</p>
<p>Common examples include framework types like <code>string</code> and utility classes that are not designed for extension. Sealing makes intent explicit and can enable compiler optimizations in some scenarios.</p>
<pre><code>public sealed class ConfigurationReader
{
    public string Read(string key) =&gt; Environment.GetEnvironmentVariable(key) ?? "";
}

// public class ExtendedReader : ConfigurationReader { } // compile error

public class Base
{
    public virtual void Execute() { }
}
public class Derived : Base
{
    public sealed override void Execute() { }
}</code></pre>
<h3>Key Points</h3>
<ul>
<li><code>sealed class</code> blocks inheritance entirely.</li>
<li><code>sealed override</code> blocks further method overriding.</li>
<li>Use when extension would be unsafe or unsupported.</li>
</ul>
<h3>Interview Answer</h3>
<p>A sealed class cannot be subclassed, which I use when inheritance would violate design or security guarantees. Sealed methods stop further overrides in the inheritance chain. It is a deliberate restriction to keep behavior predictable.</p>""",

"q_102": """<h2>Constructor Chaining in C#</h2>
<p>Constructor chaining lets one constructor call another in the same class (<code>this</code>) or a base class constructor (<code>base</code>). This avoids duplicating initialization logic and ensures objects are always created in a valid state.</p>
<p>The called constructor runs first. Use <code>: this(...)</code> to forward to another constructor in the same type, and <code>: base(...)</code> to invoke a parent constructor before your own body executes.</p>
<pre><code>public class Employee
{
    public int Id { get; }
    public string Name { get; }

    public Employee(int id) : this(id, "Unknown") { }

    public Employee(int id, string name)
    {
        Id = id;
        Name = name;
    }
}

public class Manager : Employee
{
    public Manager(int id, string name) : base(id, name) { }
}</code></pre>
<h3>Key Points</h3>
<ul>
<li><code>this(...)</code> chains constructors within the same class.</li>
<li><code>base(...)</code> calls a base class constructor.</li>
<li>Chaining must be the first statement in the constructor header.</li>
</ul>
<h3>Interview Answer</h3>
<p>Constructor chaining reuses initialization through <code>this</code> or <code>base</code> calls so setup logic is not duplicated. The chained constructor always runs first, which helps enforce consistent object construction across overloads and inheritance.</p>""",

"q_103": """<h2>Association vs Aggregation vs Composition</h2>
<p>These describe relationships between classes. <strong>Association</strong> is a general "uses" relationship. <strong>Aggregation</strong> is a weak "has-a" where the child can exist independently. <strong>Composition</strong> is a strong "part-of" where the child lifecycle is owned by the parent.</p>
<p>In C#, composition often means the parent creates and disposes nested objects. Aggregation might pass in dependencies via constructor injection without owning their lifetime.</p>
<table>
<tr><th>Relationship</th><th>Ownership</th><th>Example</th></tr>
<tr><td>Association</td><td>Independent</td><td>Teacher teaches Student</td></tr>
<tr><td>Aggregation</td><td>Weak</td><td>Department has Employees</td></tr>
<tr><td>Composition</td><td>Strong</td><td>House has Rooms</td></tr>
</table>
<pre><code>public class Order // composition
{
    private readonly List&lt;OrderLine&gt; _lines = new();
    public IReadOnlyList&lt;OrderLine&gt; Lines =&gt; _lines;
}</code></pre>
<h3>Key Points</h3>
<ul>
<li>Composition implies lifecycle dependency.</li>
<li>Aggregation allows shared ownership elsewhere.</li>
<li>Prefer composition over inheritance for flexibility.</li>
</ul>
<h3>Interview Answer</h3>
<p>Association is a general link between classes. Aggregation is has-a with independent lifecycles, while composition is part-of where the parent owns and controls the child. In .NET, composition shows up when a class creates and manages its contained objects.</p>""",

"q_104": """<h2>const vs readonly in C#</h2>
<p>Both define values that should not change casually, but they differ in when they are resolved and where they can be used. <code>const</code> values are compile-time constants and implicitly static. <code>readonly</code> fields are assigned at declaration or in the constructor and can be instance-level.</p>
<p>Use <code>const</code> for true fixed values known at compile time (mathematical constants). Use <code>readonly</code> for values computed at runtime, such as configuration loaded in a constructor.</p>
<table>
<tr><th></th><th>const</th><th>readonly</th></tr>
<tr><td>When set</td><td>Compile time</td><td>Declaration or constructor</td></tr>
<tr><td>Instance/static</td><td>Implicitly static</td><td>Either</td></tr>
<tr><td>Type restriction</td><td>Primitive/string/null</td><td>Any type</td></tr>
</table>
<pre><code>public class AppSettings
{
    public const int MaxRetries = 3;
    public readonly DateTime StartedAt;

    public AppSettings() =&gt; StartedAt = DateTime.UtcNow;
}</code></pre>
<h3>Key Points</h3>
<ul>
<li>const is compile-time; readonly is runtime-assigned once.</li>
<li>readonly supports instance fields and complex types.</li>
<li>const cannot be set from constructor logic.</li>
</ul>
<h3>Interview Answer</h3>
<p>const is a compile-time constant and must be static, while readonly is set at runtime in the constructor or field initializer and can be per-instance. I use const for fixed literals and readonly for values determined when the object is created, like injected settings.</p>""",

"q_115": """<h2>Private Constructor in C#</h2>
<p>A private constructor prevents external code from creating instances with <code>new</code>. This pattern supports singletons, factory methods, and static utility classes where controlled instantiation is required.</p>
<p>When all constructors are private, the class cannot be subclassed unless a protected constructor exists in a base class scenario. Often you expose a static <code>Create</code> or <code>Instance</code> property that manages object creation.</p>
<pre><code>public sealed class LoggerFactory
{
    private static LoggerFactory? _instance;
    private LoggerFactory() { }

    public static LoggerFactory Instance
        =&gt; _instance ??= new LoggerFactory();

    public ILogger Create(string name) =&gt; new ConsoleLogger(name);
}</code></pre>
<h3>Key Points</h3>
<ul>
<li>Blocks direct instantiation from outside the class.</li>
<li>Common in singleton and factory patterns.</li>
<li>Static classes implicitly have private instance constructors.</li>
</ul>
<h3>Interview Answer</h3>
<p>A private constructor means only the class itself can create instances, which is useful for singletons or factory-controlled creation. Callers use a static method or property instead of <code>new</code>, giving you centralized control over object lifetime.</p>""",

"q_117": """<h2>Static vs Dynamic Binding</h2>
<p><strong>Static binding</strong> (early binding) resolves method calls at compile time—method overloading and non-virtual method calls. <strong>Dynamic binding</strong> (late binding) resolves calls at runtime based on the actual object type—virtual method overriding and interface dispatch.</p>
<p>Static binding is faster because the compiler knows the exact method to invoke. Dynamic binding enables polymorphism but requires virtual tables or interface lookup at runtime.</p>
<table>
<tr><th></th><th>Static Binding</th><th>Dynamic Binding</th></tr>
<tr><td>When resolved</td><td>Compile time</td><td>Runtime</td></tr>
<tr><td>Examples</td><td>Overloading, non-virtual calls</td><td>override, interface methods</td></tr>
<tr><td>Polymorphism</td><td>No</td><td>Yes</td></tr>
</table>
<pre><code>Animal a = new Dog();
a.MakeSound(); // dynamic binding if MakeSound is virtual</code></pre>
<h3>Key Points</h3>
<ul>
<li>Overloading uses static binding.</li>
<li>virtual/override and interfaces use dynamic binding.</li>
<li>C# also has <code>dynamic</code> keyword for runtime binding via DLR.</li>
</ul>
<h3>Interview Answer</h3>
<p>Static binding resolves methods at compile time, like overload selection. Dynamic binding resolves at runtime based on the actual object type, which is how virtual methods and interfaces achieve polymorphism. Understanding both helps explain performance and extensibility trade-offs.</p>""",

"q_121": """<h2>LINQ in C#</h2>
<p>Language Integrated Query (LINQ) provides a consistent syntax to query collections, databases, XML, and more. You can write queries with method syntax (<code>Where</code>, <code>Select</code>) or query syntax (<code>from ... where ... select</code>).</p>
<p>LINQ to Objects executes in memory; LINQ providers like EF Core translate <code>IQueryable</code> expressions to SQL. Deferred execution means the query runs when you enumerate results unless you call operators like <code>ToList()</code>.</p>
<pre><code>var activeUsers = users
    .Where(u =&gt; u.IsActive)
    .OrderBy(u =&gt; u.LastName)
    .Select(u =&gt; new { u.Id, u.Email });

foreach (var u in activeUsers) { /* executes here */ }</code></pre>
<h3>Key Points</h3>
<ul>
<li>Unified query model across data sources.</li>
<li>Deferred execution unless materialized.</li>
<li>Method syntax and query syntax are equivalent.</li>
</ul>
<h3>Interview Answer</h3>
<p>LINQ lets me query data with a fluent, type-safe API in C#. It supports in-memory collections and remote providers like EF Core, with deferred execution until enumeration. I use it daily for filtering, projection, grouping, and joins with readable, composable code.</p>""",

"q_47": """<h2>Collections in C#</h2>
<p>The .NET collections framework provides typed containers for in-memory data. Non-generic legacy types (<code>ArrayList</code>) boxed values; modern code uses generic collections in <code>System.Collections.Generic</code> for type safety and performance.</p>
<p>Choose structures by access pattern: <code>List&lt;T&gt;</code> for indexed access, <code>Dictionary&lt;TKey,TValue&gt;</code> for key lookups, <code>HashSet&lt;T&gt;</code> for uniqueness, and <code>Queue&lt;T&gt;</code>/<code>Stack&lt;T&gt;</code> for FIFO/LIFO processing.</p>
<table>
<tr><th>Type</th><th>Use Case</th></tr>
<tr><td>List&lt;T&gt;</td><td>Ordered, indexable sequence</td></tr>
<tr><td>Dictionary&lt;K,V&gt;</td><td>Fast key-value lookup</td></tr>
<tr><td>HashSet&lt;T&gt;</td><td>Unique items, set operations</td></tr>
<tr><td>Queue/Stack</td><td>Processing pipelines</td></tr>
</table>
<pre><code>var cache = new Dictionary&lt;string, User&gt;();
cache["u-1"] = new User { Id = 1 };</code></pre>
<h3>Key Points</h3>
<ul>
<li>Prefer generic collections over non-generic types.</li>
<li>Pick structure based on lookup and ordering needs.</li>
<li>Consider thread-safe collections for concurrent scenarios.</li>
</ul>
<h3>Interview Answer</h3>
<p>.NET offers rich generic collections like List, Dictionary, and HashSet tuned for different access patterns. I choose based on whether I need ordering, key-based lookup, or uniqueness, and I avoid legacy non-generic collections because they require casting and boxing.</p>""",

"q_48": """<h2>Value Type vs Reference Type</h2>
<p>Value types store data directly on the stack (or inline within objects) and include primitives, enums, and structs. Reference types store a reference to heap memory and include classes, interfaces, delegates, and arrays.</p>
<p>Assignment copies value for value types and copies reference for reference types. Nullable value types (<code>int?</code>) and boxing/unboxing affect performance and API design.</p>
<table>
<tr><th></th><th>Value Type</th><th>Reference Type</th></tr>
<tr><td>Storage</td><td>Stack/inline</td><td>Heap (reference on stack)</td></tr>
<tr><td>Examples</td><td>int, struct</td><td>class, string</td></tr>
<tr><td>Default</td><td>Zeroed value</td><td>null</td></tr>
<tr><td>Assignment</td><td>Copies data</td><td>Copies reference</td></tr>
</table>
<pre><code>int a = 10, b = a; // b gets copy
var list1 = new List&lt;int&gt;();
var list2 = list1; // both refer to same list</code></pre>
<h3>Key Points</h3>
<ul>
<li>Structs are value types; classes are reference types.</li>
<li>string is a reference type but immutable.</li>
<li>Boxing wraps value types on the heap.</li>
</ul>
<h3>Interview Answer</h3>
<p>Value types hold data directly and are copied on assignment, while reference types hold a pointer to heap objects shared by multiple variables. Understanding this explains memory behavior, nullability, and why structs are preferred for small immutable data.</p>""",

"q_49": """<h2>ref vs out Parameters</h2>
<p>Both pass arguments by reference, but they differ in initialization requirements and intent. A <code>ref</code> parameter must be assigned before the call; the method can read and write it. An <code>out</code> parameter does not need prior assignment; the method must assign it before returning.</p>
<p><code>ref</code> suits scenarios where you modify existing state. <code>out</code> is common for Try-pattern methods that return success/failure and produce a value, like <code>int.TryParse</code>.</p>
<table>
<tr><th></th><th>ref</th><th>out</th></tr>
<tr><td>Must assign before call?</td><td>Yes</td><td>No</td></tr>
<tr><td>Must assign in method?</td><td>No</td><td>Yes</td></tr>
<tr><td>Typical use</td><td>Modify input</td><td>Return extra output</td></tr>
</table>
<pre><code>bool TryDivide(int a, int b, out int result)
{
    if (b == 0) { result = 0; return false; }
    result = a / b;
    return true;
}</code></pre>
<h3>Key Points</h3>
<ul>
<li>Both require <code>ref</code>/<code>out</code> at call site for clarity.</li>
<li>Prefer return tuples or objects over many out params.</li>
<li><code>out</code> variables can be declared inline in modern C#.</li>
</ul>
<h3>Interview Answer</h3>
<p>ref requires the variable to be initialized before passing and allows read/write in the method. out does not require prior initialization but the method must assign it before exit. I use out for TryParse-style APIs and ref when mutating an existing variable in place.</p>""",

"q_118": """<h2>IDisposable vs using Statement</h2>
<p><code>IDisposable</code> defines a contract for releasing unmanaged resources such as file handles, database connections, or network streams. The <code>using</code> statement (or declaration) ensures <code>Dispose()</code> is called even when exceptions occur.</p>
<p>In modern C#, <code>await using</code> works with <code>IAsyncDisposable</code> for async cleanup. ASP.NET Core scopes often dispose scoped services like DbContext at request end.</p>
<pre><code>await using var connection = new SqlConnection(connString);
await connection.OpenAsync();
// DisposeAsync called automatically at scope end</code></pre>
<h3>Key Points</h3>
<ul>
<li>IDisposable releases unmanaged/scarce resources.</li>
<li>using guarantees Dispose in a finally block.</li>
<li>Implement IDisposable pattern for classes owning handles.</li>
</ul>
<h3>Interview Answer</h3>
<p>IDisposable is the interface for deterministic cleanup of resources like files or DB connections. The using statement wraps objects so Dispose runs automatically, even on exceptions. In async code I use await using with IAsyncDisposable for the same guarantee.</p>""",

"q_81": """<h2>IEnumerable vs IQueryable</h2>
<p><code>IEnumerable&lt;T&gt;</code> represents in-memory sequences evaluated on the client when enumerated. <code>IQueryable&lt;T&gt;</code> builds expression trees that LINQ providers (like EF Core) can translate to remote queries such as SQL.</p>
<p>Filtering on <code>IQueryable</code> before materialization pushes work to the database, reducing memory and network cost. Calling <code>ToList()</code> too early forces client-side evaluation.</p>
<table>
<tr><th></th><th>IEnumerable</th><th>IQueryable</th></tr>
<tr><td>Execution</td><td>In-memory</td><td>Provider-dependent (often DB)</td></tr>
<tr><td>Best for</td><td>Collections, post-query logic</td><td>EF Core, remote data</td></tr>
<tr><td>Deferred</td><td>Yes</td><td>Yes</td></tr>
</table>
<pre><code>IQueryable&lt;Product&gt; query = db.Products.Where(p =&gt; p.IsActive);
var sqlSide = query.OrderBy(p =&gt; p.Name).Take(20); // translated to SQL</code></pre>
<h3>Key Points</h3>
<ul>
<li>IQueryable enables server-side filtering via expression trees.</li>
<li>IEnumerable is for LINQ to Objects after data is loaded.</li>
<li>Materialize (ToList) only when necessary.</li>
</ul>
<h3>Interview Answer</h3>
<p>IEnumerable runs LINQ in memory, while IQueryable delegates to a provider that can translate expressions to SQL. With EF Core I keep filters on IQueryable so the database does the work, and I only switch to IEnumerable after materializing results.</p>""",

"q_122": """<h2>First vs Single in LINQ</h2>
<p><code>First()</code> returns the first element matching a predicate or sequence start and throws if empty. <code>Single()</code> expects exactly one element and throws if zero or more than one match. Each has <code>OrDefault</code> variants that return default instead of throwing.</p>
<p>Use <code>Single</code> when duplicates indicate a data integrity bug. Use <code>First</code> when any matching row is acceptable, such as top-ranked item after <code>OrderBy</code>.</p>
<table>
<tr><th>Method</th><th>0 items</th><th>1 item</th><th>2+ items</th></tr>
<tr><td>First()</td><td>Throws</td><td>Returns</td><td>Returns first</td></tr>
<tr><td>Single()</td><td>Throws</td><td>Returns</td><td>Throws</td></tr>
</table>
<pre><code>var admin = users.Single(u =&gt; u.Role == "Admin"); // expect one
var latest = orders.OrderByDescending(o =&gt; o.Date).First();</code></pre>
<h3>Key Points</h3>
<ul>
<li>Single enforces uniqueness; First does not.</li>
<li>OrDefault variants avoid exceptions for missing data.</li>
<li>Choice communicates data expectations to readers.</li>
</ul>
<h3>Interview Answer</h3>
<p>First returns the first match and is fine when multiple results exist. Single requires exactly one element and throws if there are zero or many, which I use when the business rule demands uniqueness. Picking the right operator documents intent and catches bad data early.</p>""",

"q_2": """<h2>Monolithic vs Microservices Architecture</h2>
<p>A <strong>monolith</strong> is a single deployable application containing all modules—UI, business logic, and data access—sharing one process and often one database. <strong>Microservices</strong> split the system into independently deployable services, each owning a bounded context and communicating over HTTP or messaging.</p>
<p>Monoliths are simpler to develop and debug early on. Microservices improve scalability and team autonomy at the cost of distributed complexity—network failures, observability, and deployment pipelines multiply.</p>
<table>
<tr><th>Aspect</th><th>Monolith</th><th>Microservices</th></tr>
<tr><td>Deployment</td><td>Single unit</td><td>Independent services</td></tr>
<tr><td>Complexity</td><td>Lower initially</td><td>Higher operational overhead</td></tr>
<tr><td>Scaling</td><td>Scale entire app</td><td>Scale hot services</td></tr>
<tr><td>Best when</td><td>Small teams, MVPs</td><td>Large domains, many teams</td></tr>
</table>
<h3>Key Points</h3>
<ul>
<li>Start monolith unless clear boundaries justify splitting.</li>
<li>Microservices need strong DevOps and observability.</li>
<li>Domain boundaries matter more than technology choice.</li>
</ul>
<h3>Interview Answer</h3>
<p>A monolith is one deployable app that is easy to build initially but harder to scale independently. Microservices decompose by business capability for independent deployment and scaling, but add network, consistency, and operations complexity. I choose based on team size, domain clarity, and scaling needs—not hype.</p>""",

"q_37": """<h2>.NET Framework vs .NET (Core)</h2>
<p><strong>.NET Framework</strong> is the Windows-centric, mature runtime used for legacy desktop and ASP.NET apps. <strong>.NET</strong> (formerly .NET Core) is cross-platform, open source, and the modern unified stack for cloud, web, mobile, and microservices.</p>
<p>New development targets .NET 8+ for performance, container support, and long-term support releases. .NET Framework remains in maintenance mode; migration uses incremental strategies or side-by-side hosting.</p>
<table>
<tr><th></th><th>.NET Framework</th><th>.NET (Core+)</th></tr>
<tr><td>Platform</td><td>Windows primarily</td><td>Windows, Linux, macOS</td></tr>
<tr><td>Status</td><td>Maintenance</td><td>Active development</td></tr>
<tr><td>ASP.NET</td><td>System.Web / MVC 5</td><td>ASP.NET Core</td></tr>
<tr><td>Deployment</td><td>Machine-wide GAC</td><td>Self-contained / framework-dependent</td></tr>
</table>
<h3>Key Points</h3>
<ul>
<li>.NET is the strategic platform for new projects.</li>
<li>ASP.NET Core is modular and runs on Kestrel.</li>
<li>Migration tools and compatibility analyzers assist upgrades.</li>
</ul>
<h3>Interview Answer</h3>
<p>.NET Framework is legacy Windows-only and in maintenance, while modern .NET is cross-platform, high-performance, and where Microsoft invests new features. For greenfield APIs I use ASP.NET Core on .NET 8 because of DI, middleware, and cloud-native deployment options.</p>""",

"q_107": """<h2>Middleware and Filters in ASP.NET Core</h2>
<p><strong>Middleware</strong> forms the HTTP request pipeline—cross-cutting concerns like authentication, logging, and exception handling that run for most requests. <strong>Filters</strong> run within MVC/minimal-API controller execution for authorization, action logic, and result transformation.</p>
<p>Middleware is pipeline-order sensitive and ideal for global HTTP concerns. Filters integrate with MVC action lifecycle and can access action context like route data and model state.</p>
<table>
<tr><th></th><th>Middleware</th><th>Filters</th></tr>
<tr><td>Scope</td><td>Entire pipeline</td><td>MVC/action specific</td></tr>
<tr><td>Registration</td><td><code>app.Use...</code></td><td>Attributes or DI</td></tr>
<tr><td>Examples</td><td>Auth, CORS, routing</td><td>Authorize, Validate, Exception</td></tr>
</table>
<pre><code>app.UseAuthentication();
app.UseAuthorization();
app.MapControllers(); // filters apply inside MVC</code></pre>
<h3>Key Points</h3>
<ul>
<li>Middleware = HTTP pipeline; filters = MVC pipeline.</li>
<li>Order matters for middleware registration.</li>
<li>Use filters for action-level cross-cutting logic.</li>
</ul>
<h3>Interview Answer</h3>
<p>Middleware handles global HTTP pipeline concerns in order, like authentication and routing. Filters plug into the MVC action lifecycle for things like validation or authorization at controller/action level. I use middleware for request-wide behavior and filters when I need action-specific context.</p>""",

"q_110": """<h2>Dependency Injection in ASP.NET Core</h2>
<p>Dependency Injection (DI) is a built-in IoC container that resolves interfaces to concrete implementations at runtime. You register services in <code>Program.cs</code> and consume them via constructor injection in controllers, services, and middleware.</p>
<p>DI promotes loose coupling, testability, and clear lifetimes (singleton, scoped, transient). ASP.NET Core's default container can be extended with Autofac or other providers if advanced registration is needed.</p>
<pre><code>builder.Services.AddScoped&lt;IOrderService, OrderService&gt;();

public class OrdersController : ControllerBase
{
    private readonly IOrderService _orders;
    public OrdersController(IOrderService orders) =&gt; _orders = orders;
}</code></pre>
<h3>Key Points</h3>
<ul>
<li>Register abstractions, inject via constructors.</li>
<li>Choose correct service lifetimes to avoid bugs.</li>
<li>Built-in container covers most application needs.</li>
</ul>
<h3>Interview Answer</h3>
<p>ASP.NET Core has first-class DI where I register services in Program.cs and receive them through constructor injection. This decouples layers, makes unit testing straightforward with mocks, and lets the framework manage object lifetimes per request or application scope.</p>""",

"q_40": """<h2>Service Lifetimes in DI</h2>
<p>ASP.NET Core supports three default lifetimes. <strong>Transient</strong> creates a new instance every time requested. <strong>Scoped</strong> creates one instance per HTTP request (or scope). <strong>Singleton</strong> creates one instance for the application lifetime.</p>
<p>Misconfigured lifetimes cause subtle bugs—such as injecting a scoped DbContext into a singleton—which leads to stale state or thread-safety issues.</p>
<table>
<tr><th>Lifetime</th><th>Created</th><th>Typical Use</th></tr>
<tr><td>Transient</td><td>Every resolve</td><td>Lightweight stateless helpers</td></tr>
<tr><td>Scoped</td><td>Per request/scope</td><td>DbContext, unit of work</td></tr>
<tr><td>Singleton</td><td>Once per app</td><td>Cache, configuration readers</td></tr>
</table>
<pre><code>services.AddSingleton&lt;IMemoryCache, MemoryCache&gt;();
services.AddScoped&lt;AppDbContext&gt;();
services.AddTransient&lt;IEmailSender, SmtpEmailSender&gt;();</code></pre>
<h3>Key Points</h3>
<ul>
<li>Never inject scoped into singleton without a factory.</li>
<li>DbContext should almost always be scoped.</li>
<li>Singleton services must be thread-safe.</li>
</ul>
<h3>Interview Answer</h3>
<p>Transient gives a new instance per injection, scoped shares one instance per request, and singleton lives for the app lifetime. I register DbContext as scoped and caches as singleton, being careful not to capture scoped dependencies in singletons.</p>""",

"q_59": """<h2>IServiceProvider in .NET</h2>
<p><code>IServiceProvider</code> is the service locator abstraction that resolves registered dependencies from the DI container. In ASP.NET Core, the built-in provider is created from <code>ServiceCollection</code> during host building.</p>
<p>Prefer constructor injection over manual <code>GetService</code> calls. Use <code>IServiceProvider</code> directly in factories, middleware activation, or when creating scopes with <code>CreateScope()</code>.</p>
<pre><code>using var scope = app.Services.CreateScope();
var db = scope.ServiceProvider.GetRequiredService&lt;AppDbContext&gt;();</code></pre>
<h3>Key Points</h3>
<ul>
<li>Root provider resolves application-wide services.</li>
<li>CreateScope() for scoped resolution outside requests.</li>
<li>GetRequiredService throws if registration missing.</li>
</ul>
<h3>Interview Answer</h3>
<p>IServiceProvider is the DI container interface that resolves registered services. I rely on constructor injection in normal code, but use the provider explicitly when creating scopes—like in background tasks—via CreateScope and GetRequiredService.</p>""",

"q_60": """<h2>Ways to Implement Dependency Injection</h2>
<p>ASP.NET Core supports constructor, property, and method injection, though constructor injection is the recommended default. You can also use factory delegates (<code>AddScoped&lt;IService&gt;(sp =&gt; ...)</code>) for complex creation logic.</p>
<p>Third-party containers (Autofac, Simple Injector) integrate via <code>IServiceProviderFactory</code> when advanced features like decorators or conditional registration are required.</p>
<table>
<tr><th>Style</th><th>When to Use</th></tr>
<tr><td>Constructor</td><td>Default for required dependencies</td></tr>
<tr><td>Method</td><td>[FromServices] parameters in actions</td></tr>
<tr><td>Property</td><td>Rare; harder to test</td></tr>
<tr><td>Factory delegate</td><td>Dynamic/complex construction</td></tr>
</table>
<h3>Key Points</h3>
<ul>
<li>Constructor injection makes dependencies explicit.</li>
<li>Built-in container is sufficient for most apps.</li>
<li>Factory registration handles conditional setup.</li>
</ul>
<h3>Interview Answer</h3>
<p>The primary approach is constructor injection registered in Program.cs. Method injection via [FromServices] works for action-specific services, and factory delegates handle complex creation. I avoid service locator patterns in business code to keep dependencies visible and testable.</p>""",

"q_61": """<h2>Method Injection in ASP.NET Core</h2>
<p>Method injection supplies dependencies directly to action method parameters rather than the controller constructor. ASP.NET Core resolves parameters marked with <code>[FromServices]</code> from the DI container when the action executes.</p>
<p>This suits infrequently used services that should not bloat the controller constructor. Required dependencies shared across many actions still belong in constructor injection.</p>
<pre><code>[HttpPost]
public async Task&lt;IActionResult&gt; Notify(
    [FromBody] NotifyRequest request,
    [FromServices] IEmailSender emailSender)
{
    await emailSender.SendAsync(request.To, request.Body);
    return Ok();
}</code></pre>
<h3>Key Points</h3>
<ul>
<li>Use [FromServices] for DI-resolved action parameters.</li>
<li>Good for optional or rare dependencies.</li>
<li>Do not replace constructor injection for core deps.</li>
</ul>
<h3>Interview Answer</h3>
<p>Method injection resolves services into action parameters using [FromServices], which keeps controllers lean when a dependency is used by only one endpoint. For shared core dependencies I still prefer constructor injection because it makes requirements obvious and eases testing.</p>""",

"q_96": """<h2>Why DbContext Is Scoped</h2>
<p><code>DbContext</code> is not thread-safe and tracks entity changes for a unit of work. Registering it as <strong>scoped</strong> gives each HTTP request its own context instance, aligning with one logical transaction per request and preventing cross-request state leakage.</p>
<p>A singleton DbContext would be shared across concurrent requests, causing race conditions and stale tracked entities. Transient DbContext per injection would multiply connections and break change tracking coherence within a request.</p>
<pre><code>builder.Services.AddDbContext&lt;AppDbContext&gt;(options =&gt;
    options.UseSqlServer(connectionString)); // scoped by default</code></pre>
<h3>Key Points</h3>
<ul>
<li>DbContext tracks entities per unit of work.</li>
<li>Scoped = one context per request scope.</li>
<li>Do not share DbContext across threads.</li>
</ul>
<h3>Interview Answer</h3>
<p>EF Core DbContext is scoped because it is not thread-safe and represents a single unit of work per request. One instance per HTTP request ensures consistent change tracking and avoids concurrency bugs that would occur with a singleton context shared by all users.</p>""",

"q_41": """<h2>JWT Authentication in ASP.NET Core</h2>
<p>JSON Web Tokens (JWT) are compact, signed tokens carrying claims about a user or client. In ASP.NET Core, JWT bearer authentication validates the token signature and expiration, then builds a <code>ClaimsPrincipal</code> for authorization.</p>
<p>Typical flow: user authenticates, server issues JWT; client sends <code>Authorization: Bearer &lt;token&gt;</code> on API calls. Stateless APIs scale well, but token revocation and refresh strategies must be designed explicitly.</p>
<pre><code>builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =&gt;
    {
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuer = true,
            ValidateAudience = true,
            ValidateLifetime = true,
            ValidIssuer = config["Jwt:Issuer"],
            ValidAudience = config["Jwt:Audience"],
            IssuerSigningKey = new SymmetricSecurityKey(keyBytes)
        };
    });</code></pre>
<h3>Key Points</h3>
<ul>
<li>JWT enables stateless bearer authentication.</li>
<li>Validate issuer, audience, signature, and expiry.</li>
<li>Plan refresh tokens and secure secret storage.</li>
</ul>
<h3>Interview Answer</h3>
<p>JWT is a signed token with claims used for stateless API authentication. ASP.NET Core validates it via JwtBearer middleware and exposes claims to authorization policies. I always validate signing key, issuer, audience, and lifetime, and I plan refresh or revocation for production security.</p>""",

"q_42": """<h2>Dapper ORM</h2>
<p>Dapper is a lightweight micro-ORM that maps SQL query results to .NET objects with minimal overhead. Unlike full ORMs, you write SQL explicitly and Dapper handles materialization—ideal for performance-critical reads and complex queries.</p>
<p>Use Dapper alongside EF Core when you need raw SQL control, bulk operations, or reporting queries without change-tracking overhead.</p>
<pre><code>await using var conn = new SqlConnection(_connectionString);
var orders = await conn.QueryAsync&lt;Order&gt;(
    "SELECT Id, Total FROM Orders WHERE CustomerId = @Id",
    new { Id = customerId });</code></pre>
<h3>Key Points</h3>
<ul>
<li>Thin layer over ADO.NET; very fast.</li>
<li>You own SQL, parameters, and schema mapping.</li>
<li>Complements EF Core; does not replace migrations by itself.</li>
</ul>
<h3>Interview Answer</h3>
<p>Dapper is a high-performance micro-ORM where I write SQL and it maps rows to objects with almost no overhead. I use it for hot-path queries or reports while keeping EF Core for domain modeling and change tracking where that productivity matters.</p>""",

"q_53": """<h2>Routing in ASP.NET Core</h2>
<p>Routing maps incoming HTTP requests to endpoints. Convention-based routing uses templates like <code>{controller=Home}/{action=Index}/{id?}</code>. Attribute routing decorates controllers and actions with <code>[Route]</code> templates for explicit, version-friendly APIs.</p>
<p>Endpoint routing builds a route table at startup. Middleware like <code>UseRouting</code> and <code>UseEndpoints</code> (or <code>MapControllers</code> in minimal hosting) dispatches to the matched handler.</p>
<pre><code>[ApiController]
[Route("api/[controller]")]
public class ProductsController : ControllerBase
{
    [HttpGet("{id:int}")]
    public ActionResult&lt;Product&gt; Get(int id) =&gt; Ok(/* ... */);
}</code></pre>
<h3>Key Points</h3>
<ul>
<li>Attribute routing is standard for REST APIs.</li>
<li>Route constraints (e.g., :int) validate parameters.</li>
<li>Order and specificity determine match winner.</li>
</ul>
<h3>Interview Answer</h3>
<p>ASP.NET Core routing matches URLs to endpoints via conventions or attributes. For APIs I use attribute routing with clear templates and constraints so clients get predictable URLs and the framework selects the correct action efficiently.</p>""",

"q_54": """<h2>CORS in ASP.NET Core</h2>
<p>Cross-Origin Resource Sharing (CORS) is a browser security mechanism. When a web app at <code>https://app.example</code> calls your API at <code>https://api.example</code>, the browser sends a preflight OPTIONS request unless origins are allowed.</p>
<p>Configure CORS policies in <code>Program.cs</code> with allowed origins, methods, and headers. Apply globally or per-endpoint with <code>RequireCors</code>.</p>
<pre><code>builder.Services.AddCors(o =&gt; o.AddPolicy("WebApp", p =&gt;
    p.WithOrigins("https://app.example.com")
     .AllowAnyHeader()
     .AllowAnyMethod()));

app.UseCors("WebApp");</code></pre>
<h3>Key Points</h3>
<ul>
<li>CORS is enforced by browsers, not server-to-server calls.</li>
<li>Do not use AllowAnyOrigin with credentials.</li>
<li>Place UseCors before auth/endpoints as needed.</li>
</ul>
<h3>Interview Answer</h3>
<p>CORS lets browsers call APIs on different origins by returning appropriate Access-Control headers. In ASP.NET Core I define a named policy with specific origins and apply it via UseCors. I avoid wildcard origins when cookies or credentials are involved.</p>""",

"q_55": """<h2>REST API Design</h2>
<p>REST organizes APIs around resources identified by URLs, using HTTP verbs for semantics: GET (read), POST (create), PUT/PATCH (update), DELETE (remove). Status codes communicate outcomes—200 OK, 201 Created, 404 Not Found, 400 Bad Request.</p>
<p>Good REST APIs are stateless, use nouns in paths (<code>/api/orders/5</code>), support filtering and pagination, and version explicitly when breaking changes occur.</p>
<table>
<tr><th>Verb</th><th>Purpose</th><th>Idempotent?</th></tr>
<tr><td>GET</td><td>Retrieve</td><td>Yes</td></tr>
<tr><td>POST</td><td>Create</td><td>No</td></tr>
<tr><td>PUT</td><td>Replace</td><td>Yes</td></tr>
<tr><td>DELETE</td><td>Remove</td><td>Yes</td></tr>
</table>
<h3>Key Points</h3>
<ul>
<li>Resources are nouns; verbs are HTTP methods.</li>
<li>Use proper status codes and problem details.</li>
<li>Pagination and HATEOAS optional but helpful.</li>
</ul>
<h3>Interview Answer</h3>
<p>REST models APIs as resources manipulated with standard HTTP methods and meaningful status codes. I design stateless endpoints with clear URLs, validate input, return consistent error shapes, and version when contracts change so clients remain stable.</p>""",

"q_67": """<h2>Caching in ASP.NET Core</h2>
<p>Caching stores frequently accessed data closer to the consumer to reduce latency and database load. ASP.NET Core offers <code>IMemoryCache</code> for in-process caching and <code>IDistributedCache</code> (Redis, SQL Server) for multi-instance deployments.</p>
<p>Define expiration, cache keys, and invalidation strategy. Cache-aside is common: check cache, on miss load from DB and populate cache.</p>
<pre><code>public async Task&lt;Product?&gt; GetProductAsync(int id)
{
    var key = $"product:{id}";
    if (!_cache.TryGetValue(key, out Product? product))
    {
        product = await _db.Products.FindAsync(id);
        _cache.Set(key, product, TimeSpan.FromMinutes(5));
    }
    return product;
}</code></pre>
<h3>Key Points</h3>
<ul>
<li>In-memory for single node; distributed for scale-out.</li>
<li>Set TTL and invalidate on writes.</li>
<li>Do not cache user-specific secrets without care.</li>
</ul>
<h3>Interview Answer</h3>
<p>I use IMemoryCache for single-server scenarios and Redis via IDistributedCache when multiple nodes must share cache. I apply cache-aside with sensible TTLs and invalidate or update entries when underlying data changes to balance performance and freshness.</p>""",

"q_68": """<h2>Options Pattern in ASP.NET Core</h2>
<p>The options pattern binds configuration sections to strongly typed POCO classes and injects them via <code>IOptions&lt;T&gt;</code>, <code>IOptionsSnapshot&lt;T&gt;</code>, or <code>IOptionsMonitor&lt;T&gt;</code>. This replaces scattered <code>Configuration["Key"]</code> access.</p>
<p><code>IOptionsMonitor</code> supports change tokens for reloading appsettings changes without restart in many scenarios.</p>
<pre><code>public class SmtpSettings { public string Host { get; set; } = ""; }

builder.Services.Configure&lt;SmtpSettings&gt;(builder.Configuration.GetSection("Smtp"));

public class MailService
{
    public MailService(IOptions&lt;SmtpSettings&gt; options) =&gt; _settings = options.Value;
}</code></pre>
<h3>Key Points</h3>
<ul>
<li>Strongly typed, validated configuration.</li>
<li>IOptionsSnapshot is scoped; Monitor supports reload.</li>
<li>Validate options with IValidateOptions or DataAnnotations.</li>
</ul>
<h3>Interview Answer</h3>
<p>The options pattern maps configuration to typed settings classes injected through IOptions. It centralizes config access, enables validation, and with IOptionsMonitor I can react to configuration changes cleanly instead of magic strings throughout the codebase.</p>""",

"q_69": """<h2>Hosted Services in ASP.NET Core</h2>
<p><code>IHostedService</code> and <code>BackgroundService</code> run long-running tasks inside the generic host alongside Kestrel—timers, queue consumers, or startup initialization. The host starts them on application boot and stops them gracefully on shutdown.</p>
<p>Register with <code>AddHostedService&lt;T&gt;()</code>. Use <code>CancellationToken</code> from <code>ExecuteAsync</code> to respect shutdown signals.</p>
<pre><code>public class SyncWorker : BackgroundService
{
    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            await DoWorkAsync(stoppingToken);
            await Task.Delay(TimeSpan.FromMinutes(1), stoppingToken);
        }
    }
}</code></pre>
<h3>Key Points</h3>
<ul>
<li>Runs inside same process as the web app.</li>
<li>BackgroundService simplifies loop-based workers.</li>
<li>Respect cancellation for clean shutdown.</li>
</ul>
<h3>Interview Answer</h3>
<p>Hosted services are background tasks managed by the ASP.NET Core host via IHostedService or BackgroundService. I use them for periodic sync or queue polling inside the app process, always honoring CancellationToken so shutdown is graceful.</p>""",

"q_70": """<h2>Background Jobs in .NET</h2>
<p>Background jobs process work asynchronously outside the HTTP request path—emails, reports, imports. In-process options include <code>BackgroundService</code> and <code>Task.Run</code> (limited). Production systems often use Hangfire, Azure Functions, or message queues for reliability and retries.</p>
<p>Fire-and-forget inside requests risks lost work if the process crashes. Durable queues with idempotent handlers scale better.</p>
<table>
<tr><th>Approach</th><th>Pros</th><th>Cons</th></tr>
<tr><td>BackgroundService</td><td>Simple, in-process</td><td>Dies with app</td></tr>
<tr><td>Hangfire</td><td>Dashboard, retries</td><td>Extra infrastructure</td></tr>
<tr><td>Queue + worker</td><td>Scalable, durable</td><td>More moving parts</td></tr>
</table>
<h3>Key Points</h3>
<ul>
<li>Do not block HTTP threads for long work.</li>
<li>Use durable storage for critical jobs.</li>
<li>Design idempotent handlers for retries.</li>
</ul>
<h3>Interview Answer</h3>
<p>Background jobs handle async work like notifications outside request lifecycle. For simple cases I use BackgroundService; for production reliability I prefer Hangfire or queue-based workers with retries and persistence so jobs survive restarts and scale independently.</p>""",

"q_62": """<h2>Custom Middleware in ASP.NET Core</h2>
<p>Custom middleware is a class or delegate that processes HTTP requests and responses in the pipeline. Implement <code>InvokeAsync(HttpContext, RequestDelegate next)</code>, perform pre/post logic, and call <code>await next(context)</code> to pass control downstream unless short-circuiting.</p>
<p>Register with <code>app.UseMiddleware&lt;T&gt;()</code> or inline delegates. Typical uses: correlation IDs, request logging, global exception wrapping, and timing headers.</p>
<pre><code>public class RequestTimingMiddleware
{
    private readonly RequestDelegate _next;
    public async Task InvokeAsync(HttpContext context)
    {
        var sw = Stopwatch.StartNew();
        await _next(context);
        context.Response.Headers["X-Elapsed-Ms"] = sw.ElapsedMilliseconds.ToString();
    }
}</code></pre>
<h3>Key Points</h3>
<ul>
<li>Constructor receives next delegate and DI services.</li>
<li>Call next unless terminating the pipeline.</li>
<li>Registration order determines execution order.</li>
</ul>
<h3>Interview Answer</h3>
<p>Custom middleware is a pipeline component with access to HttpContext that runs before and after inner middleware via next. I implement InvokeAsync, register it with UseMiddleware, and use it for cross-cutting concerns like logging or adding response headers globally.</p>""",

"q_63": """<h2>Calling next Middleware</h2>
<p><code>await next(context)</code> passes the request to the next middleware in the pipeline. Code before <code>next</code> runs on the way in; code after runs on the way out when the response travels back. Omitting <code>next</code> short-circuits the pipeline—useful for auth failures or cached responses.</p>
<p>Always await <code>next</code> so exceptions propagate correctly and the response is fully generated before post-processing.</p>
<pre><code>public async Task InvokeAsync(HttpContext context, RequestDelegate next)
{
    // inbound
    await next(context);
    // outbound — response headers/body available
}</code></pre>
<h3>Key Points</h3>
<ul>
<li>next delegates to the rest of the pipeline.</li>
<li>Short-circuit by not calling next when appropriate.</li>
<li>Post-next code can modify response headers if not started.</li>
</ul>
<h3>Interview Answer</h3>
<p>Calling await next(context) forwards the request to subsequent middleware and returns when the response is coming back. Logic before next handles incoming requests; logic after handles outgoing responses. Skipping next stops further processing, which I use when rejecting unauthorized requests early.</p>""",

"q_64": """<h2>app.Map in ASP.NET Core</h2>
<p><code>app.Map</code> branches the middleware pipeline based on path prefix. Requests matching the path run the nested pipeline; others skip it. This enables isolated middleware for admin areas, webhooks, or health checks.</p>
<p>In .NET 6+ minimal hosting, <code>MapGet</code>, <code>MapPost</code>, and <code>MapControllers</code> register endpoints directly on <code>WebApplication</code>.</p>
<pre><code>app.Map("/admin", adminApp =&gt;
{
    adminApp.UseAuthentication();
    adminApp.UseAuthorization();
    adminApp.Run(async ctx =&gt; await ctx.Response.WriteAsync("Admin"));
});

app.MapControllers();
app.MapGet("/health", () =&gt; Results.Ok("healthy"));</code></pre>
<h3>Key Points</h3>
<ul>
<li>Map creates path-based pipeline branches.</li>
<li>MapGet/MapPost define minimal API endpoints.</li>
<li>Branch middleware does not affect sibling branches.</li>
</ul>
<h3>Interview Answer</h3>
<p>app.Map branches the pipeline for specific path prefixes so middleware runs only where needed. MapGet and MapControllers register endpoints in minimal hosting models. I use Map to isolate admin or webhook pipelines without affecting the main API route table.</p>""",

"q_65": """<h2>app.Map for Specific Requests</h2>
<p>Beyond global middleware, you can target specific requests with <code>MapWhen</code>, <code>Map</code>, or endpoint filters. <code>MapWhen</code> branches on arbitrary predicates—headers, query strings, or user agent—while <code>Map</code> branches on path.</p>
<p>Endpoint-specific behavior also uses route attributes, authorization policies, and minimal API route groups for cohesive URL prefixes and shared filters.</p>
<pre><code>app.MapWhen(
    ctx =&gt; ctx.Request.Headers.ContainsKey("X-Webhook"),
    branch =&gt; branch.UseMiddleware&lt;WebhookSignatureMiddleware&gt;());

var api = app.MapGroup("/api/v1/products").WithTags("Products");
api.MapGet("/", GetAll);
api.MapGet("/{id:int}", GetById);</code></pre>
<h3>Key Points</h3>
<ul>
<li>MapWhen for conditional pipeline branches.</li>
<li>Route groups organize related minimal endpoints.</li>
<li>Combine with authorization for sensitive paths.</li>
</ul>
<h3>Interview Answer</h3>
<p>I target specific requests using Map or MapWhen to branch middleware by path or condition, and route groups or attributes for endpoint-level rules. This keeps special cases like webhooks or versioned APIs isolated without polluting the global pipeline.</p>""",

"q_120": """<h2>Web API Performance Optimization</h2>
<p>Performance tuning spans database access, serialization, caching, and async patterns. Avoid N+1 queries with EF <code>Include</code> or projections, paginate large result sets, and use <code>AsNoTracking</code> for read-only queries.</p>
<p>Enable response compression, cache stable reads, minimize payload size with DTOs, and use <code>async/await</code> throughout to free threads during I/O.</p>
<pre><code>var page = await _db.Orders
    .AsNoTracking()
    .Where(o =&gt; o.CustomerId == id)
    .OrderByDescending(o =&gt; o.CreatedAt)
    .Select(o =&gt; new OrderDto(o.Id, o.Total))
    .Take(pageSize)
    .ToListAsync();</code></pre>
<h3>Key Points</h3>
<ul>
<li>Profile before optimizing; measure latency and SQL.</li>
<li>Project to DTOs; avoid over-fetching entities.</li>
<li>Use caching and compression for hot read paths.</li>
</ul>
<h3>Interview Answer</h3>
<p>I optimize APIs by reducing database round trips with efficient EF queries, pagination, and AsNoTracking for reads. I add caching for hot data, compress responses, use async I/O, and profile with Application Insights or dotTrace to fix real bottlenecks rather than guessing.</p>""",

"q_74": """<h2>Consuming External APIs in .NET</h2>
<p>Use <code>IHttpClientFactory</code> to create configured <code>HttpClient</code> instances with proper DNS handling and Polly resilience policies. Register typed clients for strong typing and centralized base address, headers, and timeouts.</p>
<p>Deserialize JSON with <code>System.Text.Json</code>, handle transient faults with retries, and propagate correlation IDs for distributed tracing.</p>
<pre><code>builder.Services.AddHttpClient&lt;IWeatherClient, WeatherClient&gt;(client =&gt;
{
    client.BaseAddress = new Uri("https://api.weather.example/");
    client.Timeout = TimeSpan.FromSeconds(10);
});

public async Task&lt;Forecast?&gt; GetAsync(string city) =&gt;
    await _http.GetFromJsonAsync&lt;Forecast&gt;($"forecast?city={city}");</code></pre>
<h3>Key Points</h3>
<ul>
<li>IHttpClientFactory avoids socket exhaustion.</li>
<li>Use Polly for retry, circuit breaker, timeout.</li>
<li>Typed clients improve testability and configuration.</li>
</ul>
<h3>Interview Answer</h3>
<p>I consume external APIs with IHttpClientFactory and typed clients registered in DI, which manages HttpClient lifetime correctly. I configure base URLs, timeouts, and Polly policies for retries, deserialize with System.Text.Json, and log failures with correlation IDs for observability.</p>""",
}
