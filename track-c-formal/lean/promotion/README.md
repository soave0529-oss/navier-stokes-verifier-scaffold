# Track C Promotion Queue

This directory holds type-checked Lean statement skeletons promoted from Track A candidates.

`candidate` in Track A means "not falsified by cheap filters"; it does not mean proved. Promotion files
must therefore avoid proof claims. Prefer `def <name> : Prop := ...` skeletons until the analytic
foundation is ready.

## Entries

| candidate | file | status | notes |
| --- | --- | --- | --- |
| `lemma_0001` | `lemma_0001.lean` | type-checks | BKM continuation criterion skeleton only |
