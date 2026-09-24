# Documentation sources

This bundle contains unmodified source files from the commits below. It is a selected documentation corpus, not a complete toolkit manual or an installed toolkit. Local working-tree edits are not copied. Sources are not asserted to be mutually release-compatible.

## Coverage and limitations

Includes the selected documentation trees, public API headers/schema where useful, and selected code samples. Markdown, reStructuredText, AsciiDoc and Doxygen source retain their original syntax and copyright notices. Generated API pages are not rendered: read the bundled headers/schema for signatures. Images, notebooks, build products, most implementation/test code and unrelated LLVM documentation are omitted. Some upstream cross-references therefore require upstream browsing; use the exact commit URL rather than guessing that a missing page exists locally. Experimental/proposed extension documents are not proof of shipped support.

Unified Runtime is bundled from intel/llvm at the same commit as the SYCL docs; the standalone mirror is deliberately omitted. Intel's proprietary toolkit component manuals (including complete oneMKL, IPP, MPI, VTune, Advisor and Fortran compiler references) are not mirrored; see ../references/toolkit-and-openmp.md for official online routes. Khronos SYCL reference is explanatory; the linked SYCL specification governs normative language questions.

## Attribution

Each project's original license/notice files are included alongside its sources. Copyright remains with the upstream authors; no blanket license is assigned to this mixed-license corpus. SYCL reference document sources are CC-BY-4.0, code examples Apache-2.0; see its LICENSE.rst, COPYING.rst and LICENSES/. Files are copied without modification; the catalog, indexes and workflow guides are separately authored. Other projects' per-file notices and bundled license files govern their respective files.

| Project | Commit | Commit date | Files |
|---|---|---|---:|
| [SYCL-Reference](https://github.com/KhronosGroup/SYCL_Reference/tree/5528bdaacc9b27604534ca66f8edaa06104cfd36) | `5528bdaacc9b27604534ca66f8edaa06104cfd36` | 2026-02-11T09:27:08-06:00 | 118 |
| [oneAPI-spec](https://github.com/uxlfoundation/oneAPI-spec/tree/70993d33d4f180bb7be400b95f15cbc32bc588dc) | `70993d33d4f180bb7be400b95f15cbc32bc588dc` | 2026-09-09T19:22:37-04:00 | 964 |
| [llvm](https://github.com/intel/llvm/tree/dc45357926029cd6a49e9a1c5349c27d689e4536) | `dc45357926029cd6a49e9a1c5349c27d689e4536` | 2026-09-23T12:33:39-07:00 | 327 |
| [level-zero-spec](https://github.com/oneapi-src/level-zero-spec/tree/143853c129b66d337d3823db7f1ec1abd61c6940) | `143853c129b66d337d3823db7f1ec1abd61c6940` | 2026-09-16T15:40:32-07:00 | 227 |
| [level-zero](https://github.com/oneapi-src/level-zero/tree/934714b278f850d164627eeaaa043eee02785a9e) | `934714b278f850d164627eeaaa043eee02785a9e` | 2026-09-17T16:29:59-07:00 | 24 |
| [compute-runtime](https://github.com/intel/compute-runtime/tree/05b847e3d2e72a6d68813a876a29b852db28200d) | `05b847e3d2e72a6d68813a876a29b852db28200d` | 2026-09-23T19:01:12+02:00 | 24 |
| [intel-graphics-compiler](https://github.com/intel/intel-graphics-compiler/tree/f586d8b2df5d747635d9754157f718e81e17e152) | `f586d8b2df5d747635d9754157f718e81e17e152` | 2026-09-23T12:44:34-04:00 | 147 |
| [unified-memory-framework](https://github.com/oneapi-src/unified-memory-framework/tree/19ce12f5f40213a612828e32a3b1d1b857222312) | `19ce12f5f40213a612828e32a3b1d1b857222312` | 2026-09-10T10:11:36+02:00 | 74 |
| [oneTBB](https://github.com/uxlfoundation/oneTBB/tree/8976636cbd8962464cebabf4e097626ceda64809) | `8976636cbd8962464cebabf4e097626ceda64809` | 2026-09-23T12:40:25+02:00 | 561 |
| [oneDPL](https://github.com/uxlfoundation/oneDPL/tree/2d68a32569e455cc926cb589edb4cc5902f61f93) | `2d68a32569e455cc926cb589edb4cc5902f61f93` | 2026-09-23T12:04:05-05:00 | 121 |
| [oneMath](https://github.com/uxlfoundation/oneMath/tree/3273ca2205065817459f61c93b008aa94ae8f513) | `3273ca2205065817459f61c93b008aa94ae8f513` | 2026-09-18T08:15:08-07:00 | 470 |
| [oneDNN](https://github.com/uxlfoundation/oneDNN/tree/7af4aecc7fb5dc2b50edfbb621b76b612ae185c9) | `7af4aecc7fb5dc2b50edfbb621b76b612ae185c9` | 2026-09-23T10:03:29-07:00 | 351 |
| [oneCCL](https://github.com/uxlfoundation/oneCCL/tree/c5108e797317bf62d2ed830d869f199bed6792e6) | `c5108e797317bf62d2ed830d869f199bed6792e6` | 2026-09-17T22:08:45+03:00 | 34 |
| [oneDAL](https://github.com/uxlfoundation/oneDAL/tree/80387026db8c322920638ee5a6e5f7b9ec36ff7a) | `80387026db8c322920638ee5a6e5f7b9ec36ff7a` | 2026-09-23T16:42:47-07:00 | 673 |
| [scikit-learn-intelex](https://github.com/uxlfoundation/scikit-learn-intelex/tree/a0fc42c38ebd67d361fdeab334edc21120a38166) | `a0fc42c38ebd67d361fdeab334edc21120a38166` | 2026-09-22T09:51:41-07:00 | 67 |
| [cryptography-primitives](https://github.com/intel/cryptography-primitives/tree/817e83b47655f565922fa2f46b16a7d09a46ffcd) | `817e83b47655f565922fa2f46b16a7d09a46ffcd` | 2026-09-22T11:48:35Z | 556 |
| [SYCLomatic](https://github.com/oneapi-src/SYCLomatic/tree/1bf0129453c284110ac35fe59e3f9a38c1e3d110) | `1bf0129453c284110ac35fe59e3f9a38c1e3d110` | 2026-09-14T13:27:00-05:00 | 210 |
| [pti-gpu](https://github.com/intel/pti-gpu/tree/8f063593943dc7f97b068a110843a9e1887008de) | `8f063593943dc7f97b068a110843a9e1887008de` | 2026-09-10T18:29:33-04:00 | 134 |
| [oneAPI-samples](https://github.com/oneapi-src/oneAPI-samples/tree/9ddf63720937c3f8a638022499394d3522f65f9b) | `9ddf63720937c3f8a638022499394d3522f65f9b` | 2026-07-28T07:45:15-05:00 | 930 |

## Reproduce or update

Selection rules and exact revisions are in scripts/sources.json (copied here as sources.lock.json). Run `python3 scripts/sync_docs.py --sources-root /path/to/checkouts` from the skill directory to reproduce. Every listed checkout must contain its pinned commit; the tool never fetches, switches branches or changes source checkouts. To update, deliberately edit the revisions in scripts/sources.json and review the resulting diff. No automatic tracking of moving branches.

`catalog.json` records project, source path, file kind, byte count and SHA-256 per copied file. Source URL = project tree URL above plus its source path (replace /tree/ with /blob/). `inventory.json` additionally hashes generated indexes and metadata. Run `python3 scripts/sync_docs.py --verify` to check the delivered bundle. Hashes detect accidental drift, not adversarial tampering.
