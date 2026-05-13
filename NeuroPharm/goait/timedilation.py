from typing import Any, Callable, Dict
import jax.numpy as jnp
from flax import nnx
import jaxtyping
import numpy as np

# Import original TimesFM components
from timesfm.src.timesfm.flax import transformer, dense, util
from timesfm.src.timesfm.timesfm_2p5 import timesfm_2p5_flax, timesfm_2p5_base

# Import our Goait components
import goait
from goait.layers.dilation import BogoliubovDilationLayer

Array = jaxtyping.Array
Float = jaxtyping.Float
Bool = jaxtyping.Bool

class TimeDilationModule(nnx.Module):
    """
    Modified TimesFM Module with Bogoliubov Dilation.
    Enhanced for High-Hardware (i9 + 5090).
    """
    def __init__(self, base_module: timesfm_2p5_flax.TimesFM_2p5_200M_flax_module, dilation_depth: int = 4):
        self.base = base_module
        self.dilation = BogoliubovDilationLayer(base_module.md)
        self.dilation_depth = dilation_depth
        
        # We need a way to get primes. For now, we'll use a pre-computed list.
        # In a real scenario, this would be passed or linked to the time index.
        self.primes = self._get_primes(4096) 

    def _get_primes(self, n):
        # Sieve for demo purposes
        primes = []
        is_prime = [True] * (n * 10)
        for p in range(2, n * 10):
            if is_prime[p]:
                primes.append(p)
                for i in range(p * p, n * 10, p):
                    is_prime[i] = False
            if len(primes) >= n:
                break
        return np.array(primes, dtype=np.float32)

    def __call__(
        self,
        inputs: Float[Array, "b n p"],
        masks: Bool[Array, "b n p"],
        decode_cache: Any = None,
    ):
        # 1. Tokenize as usual
        tokenizer_inputs = jnp.concatenate([inputs, masks.astype(inputs.dtype)], axis=-1)
        input_embeddings = self.base.tokenizer(tokenizer_inputs)
        
        # 2. APPLY TIME DILATION
        # We use the primes corresponding to the sequence length 'n'
        batch_size, seq_len, _ = input_embeddings.shape
        # Note: In JAX, we'd want this to be purely functional. 
        # For the demo, we'll call our Goait engine.
        
        p_subset = self.primes[:seq_len]
        
        # Dilation effect (simplified for JAX compatibility in this wrapper)
        dilated_embeddings = self.dilation(input_embeddings, p_subset)
        
        # 3. Pass through transformers
        output_embeddings, decode_cache = timesfm_2p5_flax._apply_stacked_transformers(
            self.base.stacked_xf, dilated_embeddings, masks[..., -1], decode_cache
        )
        
        # 4. Project outputs
        output_ts = self.base.output_projection_point(output_embeddings)
        output_quantile_spread = self.base.output_projection_quantiles(output_embeddings)
        
        return (
            dilated_embeddings,
            output_embeddings,
            output_ts,
            output_quantile_spread,
        ), decode_cache

class TimeDilation(timesfm_2p5_flax.TimesFM_2p5_200M_flax):
    """
    Hybrid TimesFM with Protoreal Dilation.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Wrap the internal module
        self.model = TimeDilationModule(self.model)
