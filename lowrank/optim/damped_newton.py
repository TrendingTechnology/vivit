"""PyTorch optimizer with damped Newton updates."""

import torch


class DampedNewton(torch.optim.Optimizer):
    """
    Newton optimizer damped via bootstrapped 1st- and 2nd-order directional derivatives.

    Attributes:
        SAVEFIELD (str): Field under which the damped Newton update is stored in a
            parameter.
    """

    SAVEFIELD = "damped_newton_step"

    def __init__(self, parameters, damping, computations, criterion=None):
        """Initialize the optimizer, specifying the damping damping and sample split.

        Args:
            parameters ([torch.nn.Parameters]): List of parameters to be trained.
            damping (lowrank.optim.damping.BaseDamping): Policy for selecting
                dampings along a direction from first- and second- order directional
                derivatives.
            computations (lowrank.optim.computations.BaseComputations): Assignment of
                mini-batch samples to the different computational tasks (finding
                directions, computing first- and second-order derivatives along them).
            criterion (callable, optional): Maps eigenvalues to indices of eigenvalues
                that will be kept as directions. Default: Largest two eigenvalues of a
                group. Assumes eigenvalues to be sorted in ascending order.
        """
        if criterion is None:
            criterion = self.make_default_criterion()

        defaults = dict(criterion=criterion)

        super().__init__(parameters, defaults=defaults)

        assert len(self.param_groups) == 1, "Parameter groups need tests"

        self._damping = damping
        self._computations = computations

    def get_extensions(self):
        """Return the required extensions for BackPACK.

        They can directly be placed inside a ``with backpack(...)`` context.

        Returns:
            [backpack.extensions.backprop_extension.BackpropExtension]: List of
                extensions that can be handed into a ``with backpack(...)`` context.
        """
        return self._computations.get_extensions(self.param_groups)

    def get_extension_hook(self):
        """Return hook to be executed right after a BackPACK extension during backprop.

        Returns:
            callable or None: Hook function that can be handed into a
                ``with backpack(...)`` context. ``None`` signifies no action will be
                performed.
        """
        return self._computations.get_extension_hook(self.param_groups)

    def step(self, closure=None, lr=1.0):
        """Apply damped Newton step to all parameters.

        Modifies the ``.data`` entry of each parameter.

        Args:
            closure (callable): Function to reevaluate the model and return the loss.
            lr (float): Learning rate. The Newton step is scaled by this value before
                it is applied to the network parameters. The default value is ``1.0``.
        """
        for group in self.param_groups:
            self.step_group(group, lr)

    def step_group(self, group, lr=1.0):
        """Apply damped Newton step to a parameter group.

        Modifies the ``.data`` entry of each group parameter.

        Args:
            group (dict): Parameter group. Entry of a ``torch.optim.Optimizer``'s
                ``param_groups`` list.
            lr (float): Learning rate. The Newton step is scaled by this value before
                it is applied to the network parameters. The default value is ``1.0``.
        """
        # TODO Compute during backpropagation
        # initialize field containing the damped Newton step in each parameter
        self._computations.compute_step(group, self._damping, self.SAVEFIELD)

        for param in group["params"]:
            if lr == 1.0:
                param.data.add_(getattr(param, self.SAVEFIELD))
            else:
                param.data.add_(lr * getattr(param, self.SAVEFIELD))

    def zero_newton(self):
        """Delete the parameter attributes used to store the Newton steps."""
        for group in self.param_groups:
            for param in group["params"]:
                if hasattr(param, self.SAVEFIELD):
                    delattr(param, self.SAVEFIELD)

    @staticmethod
    def make_default_criterion(k=2):
        """Return the default criterion which eigenvalues be used as directions.

        Args:
            k (int, optional): Number of leading eigenvalues to be kept by the
                criterion. Default: ``2``.

        Returns:
            criterion (callable): Maps eigenvalues to indices of eigenvalues that will
                be kept as directions. Default: Largest two eigenvalues of a group.
        """

        def top_k(evals):
            """Keep the k largest two eigenvalues.

            Assumes eigenvalues to be sorted in ascending order.

            Args:
                evals (torch.Tensor): Eigenvalues.

            Returns:
                [int]: Indices of two leading eigenvalues.
            """
            num_evals = len(evals)
            num_keep = min(num_evals, k)

            return [num_evals - num_keep + idx for idx in range(num_keep)]

        return top_k
