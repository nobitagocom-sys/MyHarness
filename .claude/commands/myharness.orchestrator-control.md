Orchestrator Step-Range Controller — runs the pipeline from step A to step B, then stops. Provides precise control over the orchestrator execution scope.

Use the skill: myharness.orchestrator-control

Syntax: /myharness.orchestrator-control from=<N> to=<M> <feature-description | feature-id>

Parameters:
- from: Starting step (0-13)
- to: Ending step (0-13), must be >= from
- --dry-run (optional): show plan only, do not execute

Feature description or feature-id to process: $ARGUMENTS
