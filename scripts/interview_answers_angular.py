ANSWERS = {
"q_angular_lazy_loading": """<h2>What Is Lazy Loading in Angular?</h2>
<p>In Angular, <strong>lazy loading</strong> means loading a feature module or component <strong>only when the user navigates to that route</strong> — not in the initial bundle.</p>
<h3>Why use it?</h3>
<ul>
<li>Smaller first download — faster initial load</li>
<li>Admin or reporting features load only when needed</li>
<li>Better performance on slow networks</li>
</ul>
<h3>Route lazy loading (NgModule)</h3>
<pre><code>const routes: Routes = [
  {
    path: 'admin',
    loadChildren: () =&gt; import('./admin/admin.module').then(m =&gt; m.AdminModule)
  }
];</code></pre>
<h3>Standalone components (modern Angular)</h3>
<pre><code>{
  path: 'reports',
  loadComponent: () =&gt; import('./reports/reports.component')
    .then(c =&gt; c.ReportsComponent)
}</code></pre>
<p><strong>Note:</strong> This is route/code lazy loading — not EF Core lazy loading. See also <strong>Angular performance</strong> (Section 8) for OnPush, trackBy, and bundle tips.</p>
<h3>Interview Answer</h3>
<p>Lazy loading defers loading a feature until its route is visited, reducing initial bundle size. I use loadChildren or loadComponent in routing so heavy modules like admin aren't downloaded upfront.</p>""",

"q_angular_http_client": """<h2>How Do You Call APIs in Angular?</h2>
<p>Use <strong>HttpClient</strong> from <code>@angular/common/http</code>. It returns <strong>Observables</strong>, supports typed responses, interceptors, and error handling.</p>
<h3>Setup</h3>
<pre><code>import { provideHttpClient } from '@angular/common/http';

providers: [provideHttpClient()]</code></pre>
<h3>Service</h3>
<pre><code>@Injectable({ providedIn: 'root' })
export class CustomerService {
  constructor(private http: HttpClient) {}

  getCustomers(): Observable&lt;Customer[]&gt; {
    return this.http.get&lt;Customer[]&gt;('/api/customers');
  }

  createCustomer(customer: Customer): Observable&lt;Customer&gt; {
    return this.http.post&lt;Customer&gt;('/api/customers', customer);
  }
}</code></pre>
<h3>Component</h3>
<pre><code>this.customerService.getCustomers().subscribe({
  next: data =&gt; this.customers = data,
  error: err =&gt; this.handleError(err)
});

// Or in template: customers$ | async</code></pre>
<h3>Best practices</h3>
<ul>
<li>HTTP interceptor for JWT Bearer token and 401 refresh</li>
<li><code>environment.apiUrl</code> for base URL</li>
<li>Async pipe to avoid subscribe leaks</li>
</ul>
<p><strong>Related:</strong> Section 8 — HTTP Interceptor, JWT storage, Observable vs Promise.</p>
<h3>Interview Answer</h3>
<p>I inject HttpClient in a service, call get/post with typed Observables, and use subscribe or async pipe in the component. I add an interceptor to attach JWT tokens and handle errors globally.</p>""",

"q_angular_components": """<h2>Angular Components — Basics, Communication &amp; Lifecycle</h2>
<p>In Angular, a <strong>Component</strong> is the basic building block of the UI. Every screen, button section, navbar, form, or card is usually created as a component.</p>
<h3>What is an Angular component?</h3>
<p>A component controls:</p>
<ul>
<li>HTML UI (template)</li>
<li>CSS styling</li>
<li>TypeScript logic (class)</li>
</ul>
<p>It is made of three parts:</p>
<ol>
<li><strong>Template</strong> (HTML)</li>
<li><strong>Class</strong> (TS logic)</li>
<li><strong>Styles</strong> (CSS/SCSS)</li>
</ol>
<h3>Example structure</h3>
<pre><code>app/
 ├── user/
 │    ├── user.component.ts
 │    ├── user.component.html
 │    ├── user.component.css</code></pre>
<h3>Creating a component</h3>
<pre><code>ng generate component user
# or shorthand
ng g c user</code></pre>
<h3>Basic component example</h3>
<p><strong>user.component.ts</strong></p>
<pre><code>import { Component } from '@angular/core';

@Component({
  selector: 'app-user',
  templateUrl: './user.component.html',
  styleUrls: ['./user.component.css']
})
export class UserComponent {
  name: string = "Abhisar";
}</code></pre>
<p><strong>user.component.html</strong></p>
<pre><code>&lt;h1&gt;Welcome {{name}}&lt;/h1&gt;</code></pre>
<p>Output: <code>Welcome Abhisar</code></p>
<h3>Important component properties</h3>
<table>
<tr><th>Property</th><th>Purpose</th></tr>
<tr><td><code>selector</code></td><td>HTML tag name</td></tr>
<tr><td><code>templateUrl</code></td><td>HTML file</td></tr>
<tr><td><code>styleUrls</code></td><td>CSS file(s)</td></tr>
<tr><td><code>template</code></td><td>Inline HTML</td></tr>
<tr><td><code>styles</code></td><td>Inline CSS</td></tr>
</table>
<h3>Selector</h3>
<p>Used to place the component inside HTML:</p>
<pre><code>selector: 'app-user'

// Usage in a parent template:
&lt;app-user&gt;&lt;/app-user&gt;</code></pre>
<h3>Types of components</h3>
<p><strong>1. Root component</strong> — main component loaded first, usually <code>app.component</code>.</p>
<p><strong>2. Child component</strong> — nested inside another component:</p>
<pre><code>&lt;app-navbar&gt;&lt;/app-navbar&gt;
&lt;app-dashboard&gt;&lt;/app-dashboard&gt;</code></pre>
<p><strong>3. Shared / reusable component</strong> — reusable UI blocks like button, loader, or modal popup.</p>
<h3>Component communication</h3>
<p><strong>Parent → Child with <code>@Input</code></strong></p>
<pre><code>// child.component.ts
@Input() name!: string;

// parent.component.html
&lt;app-child [name]="username"&gt;&lt;/app-child&gt;</code></pre>
<p><strong>Child → Parent with <code>@Output</code></strong></p>
<pre><code>// child.component.ts
@Output() notify = new EventEmitter&lt;string&gt;();

save() {
  this.notify.emit('Saved!');
}

// parent.component.html
&lt;app-child (notify)="onNotify($event)"&gt;&lt;/app-child&gt;</code></pre>
<p><strong>Related:</strong> Section 8 item 1 — Data transfer between unrelated components (shared service + Subject).</p>
<h3>Lifecycle hooks</h3>
<table>
<tr><th>Hook</th><th>Purpose</th></tr>
<tr><td><code>ngOnInit</code></td><td>Component initialized — load data here</td></tr>
<tr><td><code>ngOnChanges</code></td><td>@Input value changed</td></tr>
<tr><td><code>ngOnDestroy</code></td><td>Cleanup — unsubscribe, clear timers</td></tr>
</table>
<pre><code>ngOnInit() {
  console.log("Component Loaded");
}</code></pre>
<h3>Data binding in components</h3>
<table>
<tr><th>Type</th><th>Syntax</th></tr>
<tr><td>Interpolation</td><td><code>{{name}}</code></td></tr>
<tr><td>Property binding</td><td><code>&lt;img [src]="imageUrl"&gt;</code></td></tr>
<tr><td>Event binding</td><td><code>&lt;button (click)="save()"&gt;Save&lt;/button&gt;</code></td></tr>
<tr><td>Two-way binding</td><td><code>&lt;input [(ngModel)]="name"&gt;</code></td></tr>
</table>
<h3>The @Component decorator</h3>
<pre><code>@Component({
  selector: 'app-home',
  templateUrl: './home.component.html'
})</code></pre>
<p>The decorator tells Angular how the component behaves, where its HTML lives, and its styling info.</p>
<h3>Component vs Module</h3>
<table>
<tr><th>Component</th><th>Module</th></tr>
<tr><td>UI block</td><td>Group of components</td></tr>
<tr><td>Controls a view</td><td>Organizes the app</td></tr>
<tr><td>Has HTML</td><td>Imports dependencies</td></tr>
</table>
<p><strong>Note:</strong> Modern Angular favors <strong>standalone components</strong> (no NgModule needed) — see Section 8 item 5.</p>
<h3>Real project example (banking app)</h3>
<table>
<tr><th>Component</th><th>Purpose</th></tr>
<tr><td>LoginComponent</td><td>Login screen</td></tr>
<tr><td>DashboardComponent</td><td>User dashboard</td></tr>
<tr><td>TransactionComponent</td><td>Transactions</td></tr>
<tr><td>NavbarComponent</td><td>Navigation bar</td></tr>
</table>
<h3>Interview Answer</h3>
<p>Angular components are the fundamental building blocks of an Angular application. A component contains HTML template, TypeScript business logic, and CSS styling. Components help create reusable, modular, and maintainable UI sections. Angular components communicate using @Input and @Output decorators and follow lifecycle hooks like ngOnInit and ngOnDestroy.</p>""",
}
