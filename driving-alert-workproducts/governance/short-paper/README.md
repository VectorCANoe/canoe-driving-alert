# Short Paper Workspace

이 폴더는 소논문 원고와 포스터 자료를 함께 관리한다.

## Structure

- `appendix/`
  - `README.md`
  - `appendix_bundle_plan.md`
  - `source/`
  - `tex/`
- `paper/`
  - `short_paper_draft.md`
  - `short_paper_working.md`
  - `short_paper_manuscript.tex`
  - `short_paper_twocolumn.tex`
- `poster/`
  - `poster_session_draft.md`
  - `post.png`

## Build

```bash
cd driving-alert-workproducts/governance/short-paper/paper
tectonic short_paper_twocolumn.tex
```

```bash
cd driving-alert-workproducts/governance/short-paper/appendix/tex
./build_appendix_bundle.sh
```
