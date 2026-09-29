# Future Features

Deliberately deferred out of Phase 1 (MVP) to ship the core product faster. Not forgotten — these are the next differentiation layers.

- **WAT (Written Ability Test) module** — timed essay practice, AI-graded on structure/argument coherence/language/time-adherence. Universal across IIMs (GD is being phased out at most schools), underserved by existing AI tools relative to PI.
- **Institute-specific PI personas** — IIM-A/B/C/K-style interview panels as selectable personas (aspirants report each school probes differently: extempore-heavy vs profile-deep-dive vs stress questions). MVP ships one generic panel only.
- **Weak-concept ledger feeding PI question generation** — a student weak in DILR gets probed on "how do you approach ambiguous data" style PI questions; a student weak in VARC-inference gets comprehension-style follow-ups. No competitor connects test performance to interview question selection today.
- **Real PYQ bulk-ingestion pipeline** — MVP hand-seeds ~30 questions. Scaling the bank needs a product decision on sourcing (disclosed IIM papers are public domain; vendor-scraped banks are not) before an ingestion pipeline is worth building.
- **Real percentile calibration** — MVP uses a static heuristic lookup table. Needs either historical attempt data at scale or a benchmarked scaling-curve partnership to be defensibly accurate.
- **Multi-dimension PI scoring** — MVP scores PI answers 1-10 (same shape as mock-test evaluation). A real panel-style rubric (communication clarity, composure/stress-handling, content depth, self-awareness) is a natural v2.
- **Resume-aware PI questions** — MVP's generic PI persona doesn't ingest a resume/profile yet; wiring one in makes questions more realistic (a domain Hot Seat, the sibling interview-prep platform, already has to draw a pattern from).
