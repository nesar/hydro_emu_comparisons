---
name: venv-nbconvert-execution
description: "How to execute this repo's notebooks headlessly (the .venv jupyter shim is broken; use python -m nbconvert with kernel hydro-emu-venv)"
metadata: 
  node_type: memory
  type: project
  originSessionId: 288b244b-a542-4e5f-9cbf-53460e84a140
  modified: 2026-09-02T21:57:18.023Z
---

The `.venv/bin/jupyter` shim has a stale shebang pointing at a renamed directory
(`Hydro_runs/emu_comparisons/.venv`) and fails with "bad interpreter". System `python3`
lacks pyccl/cosmohydro_emu. Working recipe (run from `notebooks/`, paths are relative):

```
../.venv/bin/python -m nbconvert --to notebook --execute --inplace \
    --ExecutePreprocessor.timeout=1200 --ExecutePreprocessor.kernel_name=hydro-emu-venv <nb>.ipynb
```

**Why:** the notebooks store executed outputs (figures) in git, so a new/edited notebook
should be executed in place before handing it back; a full run loads all emulators
(~1-2 min).

**How to apply:** verify edits by executing this way and reading the extracted PNGs;
percent signs inside matplotlib mathtext labels must be escaped (`\%`). Related:
[[nb5-scale-conventions]]
