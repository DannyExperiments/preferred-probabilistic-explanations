# Rotating support points

Open index.html directly from the extracted explorer ZIP. Toggle selectors in a conjunction. Drag the diagram horizontally or use the arrow keys while it has focus. The browser counts the supported valuations satisfying the selected term and separately tests classical entailment for the example.

The fallback point s and each of four one-zero selector points have mass 1/5. Each selector removes its own point, and any nonempty selector term also removes the fallback point. The first still has three surviving points and fails entailment. The second has two and satisfies the observation, so it beats s. The third has only one and ties s. Grey points are excluded by the selected term.

To rebuild, use Python 3.11 or newer and Pillow 10.1 or newer. Run python3 visualization/render.py from the repository root. The renderer uses Pillow's bundled default font. It produces a looping 704 × 835 GIF and an offline-only two-file ZIP. The GIF uses a projection of the illustrated points with all masses exactly as in the example.
