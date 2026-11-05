# Agent runtimes

Products reach every agent runtime only through one runtime trait owned by AgentQ. Runtime names appear only inside AgentQ adapters and as opaque data.

## Runtime neutrality

- Product code never branches on a runtime name: no `if runtime == ...`, no switch over runtime names, no name-based defaults.
- Runtime specifics live in AgentQ adapters: command lines, flags, file layouts, environment, session formats, quota sources and login checks.
- Runtime, session and model ids are opaque data. A product stores, compares, displays and passes them back; it never parses them or derives behavior from them.
- A product that needs a behavior difference reads a capability from the runtime descriptor, never the runtime name.

## Runtime trait

Each adapter implements the full trait. An operation that a runtime cannot support returns an explicit unsupported or unknown result, never a fake success ([unknown is never healthy](verification.md#unknown-is-never-healthy)).

| Operation | Contract |
|---|---|
| `launch` | Start a run from ordered input parts (text and images), working directory, abstract permission policy, tools and instructions. |
| `resume` | Continue an existing session by its opaque session id. |
| `input` | Send further user input to a running session. |
| `cancel` | Stop a run; the result states whether it stopped. |
| `poll` | Return the run state: running, finished, failed or unknown. |
| `report` | Return the final result text and outcome of a finished run. |
| `progress` | Return ordered typed events of a running session: text delta, complete message, tool start and end, quota windows, context use and other activity. |
| `session_id` | Return the opaque session id of a run. |
| `session_url` | Return a link to the session when the runtime has one, otherwise none. |
| `transcript` | Return the session transcript or its location. |
| `ready` | Report install, version and login state; each part reads ok, missing or unknown. |
| `quota` | Report every quota window before launch, each with used fraction, reset and length; unread windows stay unknown; a launch checks them first. |
| `catalogue` | List the models a login can use, or return unsupported. |
| `running` | Return the count of runs active for this runtime. |
| `protected_paths` | List paths the runtime owns that a run must not overwrite. |
| `home_env` | Return the environment that isolates the runtime home for a run. |

## One run path

- A product states what a run needs: input parts, tools, instructions and live text. The adapter chooses the native transport from those needs; a product never names or selects a transport.
- `progress` events have one meaning across runtimes. A product never parses a native record and never replies to a native protocol request. An event a runtime cannot produce stays absent, never invented.
- Product tools reach every runtime over MCP, the one tool boundary. Native tool protocols of one runtime are not product interfaces.
- A session under a protected host stays an explicit capability, because its authority comes from that host, not from the adapter.

## Permissions and descriptor

- Permissions are an abstract policy: read scope, write scope, network, tools and approval mode. The adapter maps the policy to native flags; a product never passes native flags. A policy part the runtime cannot enforce refuses launch ([permission authority](permission-authority.md)).
- The runtime descriptor is the only runtime metadata a product reads: `name`, `label`, `brand`, `family` and `capabilities`. A product treats `name` as an opaque id and shows `label` and `brand` to people.

## Check

- Product CI flags runtime-name literals outside AgentQ adapters, tests and data tables (descriptor and configuration data). A flagged literal fails the check until it moves into one of those places.
- The check script and the runtime-name list stay in each consumer contract, like the [rule-change gate](agent-workflow.md#decided-rules).
