[👷🏗👷🏗 **Coming soon!** Official release with improved docs. Stay tuned. 👷🏗👷🏗]

# ViViT: Curvature access through the generalized Gauss-Newton's low-rank structure

[![Python
3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/release/python-370/)
[![tests](https://github.com/f-dangel/vivit/actions/workflows/test.yaml/badge.svg)]

ViViT is a collection of numerical tricks to efficiently access curvature from
the generalized Gauss-Newton (GGN) matrix based on its low-rank structure.
Provided functionality includes computing
- GGN eigenvalues
- GGN eigenpairs (eigenvalues + eigenvector)
- 1ˢᵗ- and 2ⁿᵈ-order directional derivatives along GGN eigenvectors
- Newton steps

These operations can also further approximate the GGN to reduce cost via
sub-sampling, Monte-Carlo approximation, and block-diagonal approximation.

**How does it work?** ViViT uses and extends
 [BackPACK](https://github.com/f-dangel/backpack) for
 [PyTorch](https://github.com/pytorch/pytorch). The described functionality is
 realized through a combination of existing and new BackPACK extensions and
 hooks into its backpropagation.

## Installation
👷🏗👷🏗 The [PyPI](https://pypi.org/) release is coming soon. 👷🏗👷🏗

For now, you need to install from GitHub via
```bash
pip install vivit-for-pytorch@git+https://github.com/f-dangel/vivit.git#egg=vivit-for-pytorch
```

## Examples
👷🏗👷🏗 Coming soon! 👷🏗👷🏗

## How to cite
If you are using ViViT, consider citing the [paper](https://arxiv.org/abs/2106.02624)
```
@misc{dangel2022vivit,
      title={{ViViT}: Curvature access through the generalized Gauss-Newton's low-rank structure},
      author={Felix Dangel and Lukas Tatzel and Philipp Hennig},
      year={2022},
      eprint={2106.02624},
      archivePrefix={arXiv},
      primaryClass={cs.LG}
}
```
