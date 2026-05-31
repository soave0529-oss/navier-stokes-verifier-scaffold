# Known Critical-Space Criteria Registry

Date: 2026-05-19

Status: Step 45 registry + evaluator hook complete.

Scope: Besov, Kato, Chemin-Planchon, BMO/Morrey-adjacent criteria relevant to the
remaining critical Besov and velocity Morrey candidate families. This is a known-result
overlap filter, not a proof and not a literature review complete enough for publication.

## Why This Registry Exists

The round-3 families

- `lemma_0201/0211/0221/0231/0241`: "scale-critical Besov-type norm";
- `lemma_0206/0216/0226/0236/0246`: "scale-critical Morrey norm";

are too broad to remain as unresolved candidates. Critical function-space criteria are a heavily
developed part of Navier-Stokes regularity theory. A candidate using this language should only
survive if it names exact indices, homogeneous vs inhomogeneous convention, time norm, solution
class, and a gap against the known critical-space literature.

## Anchors

| anchor | relevance |
|---|---|
| Kato 1984 | Strong `L^p` solution framework and weak-solution applications; baseline for critical/subcritical velocity-space reasoning. |
| Planchon 1996 | Global strong solutions with smallness in Besov-type norms; marks Besov criteria as known-result territory. |
| Kozono-Yamazaki 1994 | Morrey-based Besov-type spaces for heat/Navier-Stokes initial data; marks velocity Morrey language as known-result territory. |
| Koch-Tataru 2001 | `BMO^{-1}` small-data well-posedness and critical-space framework that contains or dominates many older spaces. |
| Cheskidov-Shvydkoy 2007 | Regularity of Leray-Hopf solutions in `B^{-1}_{infty,infty}` and extension of Ladyzhenskaya-Prodi-Serrin. |
| Chemin-Planchon 2011/2012 | Self-improving bounds in negative Besov scales near `-1`, extending the ESS blow-up criterion. |
| Escauriaza-Seregin-Sverak / Koch-Planchon 2014 | Critical Besov norm blow-up at a potential singularity in spaces where local existence is known. |

## Project Decision

The broad Besov/Morrey round-3 families should fail a known-overlap check until rewritten with:

- exact space: e.g. `\dot B^s_{p,q}`, `B^s_{p,q}`, Morrey-Campanato, Besov-Morrey, or `BMO^{-1}`;
- exact scaling relation;
- exact time integrability;
- homogeneous/inhomogeneous and periodic/whole-space convention;
- solution class: smooth classical, strong/mild, Leray-Hopf, or suitable weak;
- explicit statement of what is not already implied by Kato/Serrin/Koch-Tataru/Chemin-Planchon.

This does not prove the broad candidates false. It means they are not novel enough or precise enough
to remain in the active candidate set.

## Source Pointers

- Kato, "Strong Lp-Solutions of the Navier-Stokes Equation in Rm, with Applications to Weak
  Solutions", Mathematische Zeitschrift 187, 471-480 (1984): <https://eudml.org/doc/173504>
- Planchon, "Global strong solutions in Sobolev or Lebesgue spaces to the incompressible
  Navier-Stokes equations in R^3", Ann. Inst. H. Poincare 13, 319-336 (1996):
  <https://ems.press/journals/aihpc/articles/4076473>
- Kozono and Yamazaki, "Semilinear heat equations and the Navier-Stokes equation with distributions
  in new function spaces as initial data", CPDE 19(5-6), 959-1014 (1994):
  <https://doi.org/10.1080/03605309408821042>
- Koch and Tataru, "Well-posedness for the Navier-Stokes equations":
  <https://math.berkeley.edu/~tataru/papers/nas.pdf>
- Cheskidov and Shvydkoy, "On the regularity of weak solutions of the 3D Navier-Stokes equations
  in B^{-1}_{infty,infty}": <https://arxiv.org/abs/0708.3067>
- Chemin and Planchon, "Self-improving bounds for the Navier-Stokes equations":
  <https://arxiv.org/abs/1111.1356>
- Koch and Planchon, "Blow-up of critical Besov norms at a potential Navier-Stokes singularity":
  <https://arxiv.org/abs/1407.4156>
