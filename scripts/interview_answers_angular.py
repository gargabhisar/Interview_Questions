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
<p><strong>1. Root component</strong> — main component loaded first, usually <code>app.component</code>. Bootstrapped in <code>main.ts</code>; every other component renders inside it.</p>
<p><strong>2. Child component</strong> — nested inside another component:</p>
<pre><code>&lt;app-navbar&gt;&lt;/app-navbar&gt;
&lt;app-dashboard&gt;&lt;/app-dashboard&gt;</code></pre>
<p><strong>3. Shared / reusable component</strong> — reusable UI blocks like button, loader, or modal popup.</p>
<p><strong>4. Smart (container) vs Dumb (presentational)</strong> — a common architectural split:</p>
<table>
<tr><th></th><th>Smart / Container</th><th>Dumb / Presentational</th></tr>
<tr><td>Role</td><td>Fetches data (injects services), holds state</td><td>Only displays what it's given</td></tr>
<tr><td>Inputs/Outputs</td><td>Few</td><td>Communicates only via <code>@Input</code>/<code>@Output</code></td></tr>
<tr><td>Reusability</td><td>Low — page specific</td><td>High — drop anywhere</td></tr>
<tr><td>Example</td><td><code>OrdersPageComponent</code></td><td><code>OrderCardComponent</code></td></tr>
</table>
<p><strong>5. Standalone vs Module-based</strong> — standalone components (Angular 14+, default from 17) declare their own imports and don't need an NgModule; module-based components are declared in an NgModule. (Details: item 5.)</p>
<p><strong>6. Dynamic components</strong> — created at runtime with <code>ViewContainerRef.createComponent()</code>, e.g. modals, toasts, dashboard widgets.</p>
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

"q_angular_directives": """<h2>Directives in Angular</h2>
<p>A <strong>directive</strong> is a class that adds <strong>behavior to elements</strong> in the DOM — it can change appearance, structure, or behavior of elements. Angular has <strong>three types</strong>:</p>
<table>
<tr><th>Type</th><th>What it does</th><th>Examples</th></tr>
<tr><td><strong>1. Component</strong></td><td>Directive <em>with a template</em> — technically every component is a directive</td><td><code>@Component</code></td></tr>
<tr><td><strong>2. Structural</strong></td><td><strong>Changes the DOM layout</strong> — adds/removes elements</td><td><code>*ngIf</code>, <code>*ngFor</code>, <code>*ngSwitch</code></td></tr>
<tr><td><strong>3. Attribute</strong></td><td><strong>Changes appearance/behavior</strong> of an existing element</td><td><code>ngClass</code>, <code>ngStyle</code>, <code>ngModel</code></td></tr>
</table>
<h3>Structural directives (note the *)</h3>
<pre><code>&lt;!-- *ngIf — add/remove element from DOM (not just hide) --&gt;
&lt;div *ngIf="isLoggedIn"&gt;Welcome back!&lt;/div&gt;
&lt;div *ngIf="user; else loading"&gt;{{ user.name }}&lt;/div&gt;
&lt;ng-template #loading&gt;Loading...&lt;/ng-template&gt;

&lt;!-- *ngFor — repeat element per item --&gt;
&lt;li *ngFor="let order of orders; let i = index; trackBy: trackById"&gt;
  {{ i + 1 }}. {{ order.product }}
&lt;/li&gt;

&lt;!-- *ngSwitch --&gt;
&lt;div [ngSwitch]="status"&gt;
  &lt;p *ngSwitchCase="'active'"&gt;Active&lt;/p&gt;
  &lt;p *ngSwitchDefault&gt;Unknown&lt;/p&gt;
&lt;/div&gt;</code></pre>
<p>The <code>*</code> is syntactic sugar — Angular wraps the element in an <code>&lt;ng-template&gt;</code> and the directive decides whether/how many times to stamp it out.</p>
<h3>New control flow (Angular 17+)</h3>
<pre><code>@if (isLoggedIn) {
  &lt;div&gt;Welcome back!&lt;/div&gt;
} @else {
  &lt;div&gt;Please log in&lt;/div&gt;
}

@for (order of orders; track order.id) {
  &lt;li&gt;{{ order.product }}&lt;/li&gt;
} @empty {
  &lt;li&gt;No orders&lt;/li&gt;
}</code></pre>
<p>Built-in template syntax replacing <code>*ngIf/*ngFor</code> — faster, no imports needed, with built-in <code>@empty</code>. The old directives still work.</p>
<h3>Attribute directives</h3>
<pre><code>&lt;!-- ngClass — conditional CSS classes --&gt;
&lt;div [ngClass]="{ 'active': isActive, 'error': hasError }"&gt;...&lt;/div&gt;

&lt;!-- ngStyle — conditional inline styles --&gt;
&lt;div [ngStyle]="{ 'color': isError ? 'red' : 'green' }"&gt;...&lt;/div&gt;

&lt;!-- ngModel — two-way binding (FormsModule) --&gt;
&lt;input [(ngModel)]="username" /&gt;</code></pre>
<h3>Custom attribute directive</h3>
<pre><code>import { Directive, ElementRef, HostListener, Input } from '@angular/core';

@Directive({
  selector: '[appHighlight]',
  standalone: true
})
export class HighlightDirective {
  @Input() appHighlight = 'yellow';

  constructor(private el: ElementRef) {}

  @HostListener('mouseenter')
  onEnter() { this.el.nativeElement.style.background = this.appHighlight; }

  @HostListener('mouseleave')
  onLeave() { this.el.nativeElement.style.background = ''; }
}

// Usage
&lt;p [appHighlight]="'lightblue'"&gt;Hover me&lt;/p&gt;</code></pre>
<h3>Directive vs Component</h3>
<ul>
<li>Component = directive <strong>with a template</strong>; creates its own view.</li>
<li>Directive = attaches behavior to an <strong>existing</strong> element; no template of its own.</li>
<li>Multiple directives can sit on one element; only one component per element.</li>
</ul>
<h3>Key Points</h3>
<ul>
<li>Three types: Component (template), Structural (changes DOM — <code>*</code> prefix), Attribute (changes behavior/appearance).</li>
<li><code>*ngIf</code> removes from DOM; CSS <code>hidden</code> only hides — different for performance and lifecycle.</li>
<li>Always use <code>trackBy</code>/<code>track</code> with loops for rendering performance.</li>
<li>Angular 17+ <code>@if/@for</code> control flow replaces structural directives in new code.</li>
<li>Custom directives: <code>@Directive</code> + <code>ElementRef</code> + <code>@HostListener</code>.</li>
</ul>
<h3>Interview Answer</h3>
<p>Directives add behavior to DOM elements. There are three types: components, which are directives with templates; structural directives like *ngIf and *ngFor that add or remove elements from the DOM; and attribute directives like ngClass and ngStyle that change an element's appearance or behavior. I've written custom attribute directives using @Directive with ElementRef and HostListener — for example a highlight-on-hover or permission-based show/hide directive. In Angular 17+ the new @if/@for control flow syntax replaces structural directives with faster built-in blocks.</p>""",

"q_angular_spa": """<h2>SPA — How Angular Works as a Single Page Application</h2>
<p>Angular applications are <strong>SPAs (Single Page Applications)</strong>: the browser loads <strong>one HTML page once</strong> (<code>index.html</code>), and from then on Angular <strong>swaps views in JavaScript</strong> — navigation never triggers a full page reload.</p>
<h3>Traditional website vs SPA</h3>
<table>
<tr><th></th><th>Traditional (MPA)</th><th>SPA (Angular)</th></tr>
<tr><td>Navigation</td><td>Every click → server returns a <strong>new full HTML page</strong></td><td>One page loaded once; views swapped <strong>client-side</strong></td></tr>
<tr><td>Server returns</td><td>HTML</td><td>JSON (REST APIs) — UI is rendered by the browser</td></tr>
<tr><td>Page reload</td><td>Yes, every navigation</td><td>No — instant view changes</td></tr>
<tr><td>State</td><td>Lost between pages</td><td>Kept in memory (services, stores)</td></tr>
</table>
<h3>How Angular implements the SPA</h3>
<pre><code>1. Browser requests the site → server returns index.html + JS bundles
2. main.ts bootstraps the root component (&lt;app-root&gt;)
3. Angular Router watches the URL
4. URL changes → Router swaps components inside &lt;router-outlet&gt;
5. Data comes from Web APIs via HttpClient (JSON) — no page reloads</code></pre>
<pre><code>// app.routes.ts — Router maps URLs to components
export const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'orders', component: OrdersComponent },
  { path: 'orders/:id', component: OrderDetailComponent },
  // lazy loading — module/component loaded only when visited
  { path: 'admin', loadChildren: () =&gt;
      import('./admin/admin.routes').then(m =&gt; m.ADMIN_ROUTES) },
];</code></pre>
<pre><code>&lt;!-- app.component.html — views swap here, page never reloads --&gt;
&lt;app-navbar&gt;&lt;/app-navbar&gt;
&lt;router-outlet&gt;&lt;/router-outlet&gt;</code></pre>
<p>Navigation uses <code>routerLink</code> (not <code>href</code> — href would cause a full reload):</p>
<pre><code>&lt;a [routerLink]="['/orders', order.id]"&gt;View order&lt;/a&gt;</code></pre>
<h3>Benefits</h3>
<ul>
<li><strong>Fast navigation</strong> — no full page round-trips after first load.</li>
<li><strong>App-like UX</strong> — smooth transitions, state preserved in memory.</li>
<li><strong>Clean separation</strong> — Angular front end + .NET Web API backend over JSON.</li>
<li><strong>Less server load</strong> — server serves static files + APIs only.</li>
</ul>
<h3>Challenges (and Angular's answers)</h3>
<table>
<tr><th>Challenge</th><th>Solution</th></tr>
<tr><td>Slow first load (big JS bundle)</td><td><strong>Lazy loading</strong>, AOT compilation, tree shaking</td></tr>
<tr><td>SEO — crawlers may not run JS</td><td><strong>Angular SSR</strong> (server-side rendering / hydration)</td></tr>
<tr><td>Browser back/forward</td><td>Router integrates with browser history API</td></tr>
<tr><td>Deep links (refresh on /orders/5)</td><td>Server rewrite rule → always serve index.html (e.g. IIS URL Rewrite)</td></tr>
</table>
<h3>Key Points</h3>
<ul>
<li>SPA = one index.html; Angular Router swaps components in <code>&lt;router-outlet&gt;</code> — no reloads.</li>
<li>Data flows through HttpClient → REST APIs (JSON), not server-rendered HTML.</li>
<li>routerLink instead of href; lazy loading for bundle size; SSR for SEO.</li>
<li>Deployment needs a URL-rewrite rule so deep links serve index.html.</li>
</ul>
<h3>Interview Answer</h3>
<p>Angular apps are single page applications — the browser loads index.html and the JS bundles once, then the Angular Router takes over navigation, swapping components inside router-outlet as the URL changes, with no full page reloads. Data comes from REST APIs as JSON via HttpClient, so in my projects the .NET Web API serves data and Angular renders everything client-side. To handle SPA challenges I use lazy loading to keep the initial bundle small, and on the server a rewrite rule sends deep links back to index.html; if SEO matters, Angular SSR with hydration renders pages on the server first.</p>""",
}
