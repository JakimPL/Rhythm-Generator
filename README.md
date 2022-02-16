# Rhythm Generator

A simple rhythm score generator based on `abjad` package which uses `lilypond`.

### Usage

To use a rhythm generator, just instantiate a `RhythmGenerator` object. If no settings are provided, default are being used.

```python
from rhygen import RhythmGenerator
rhythm_generator = RhythmGenerator()
```

Calling a `RhythmGenerator` generates _n_ groups of _m_ measures with certain rhythm patterns. To save a score to an image, one can use an auxiliary function `save_score`:

```python
from rhygen.misc import save_score

score = rhythm_generator()
save_score(score, 'score.png')
```

Use `rhythm_generator.cache` for raw strings of score.

### Settings

Settings provides information about following elements:
 * `groups` — number of different groups
 * `measures` — number of measures
 * settings for each group (containing set of possible notes and phrases) via method `set_group`, including a default setting `default_group_settings`.

A `GroupSettings` object contains two fields:
 * `notes` a list of notes 
 * `phrases` a list of phrases (i.e. list of notes)

`rhygen` can interpret a note in two ways:
 * as integer, its length is an inverse of provided value
 * a fraction, i.e. tuple of the form `(numerator, denominator)` of length `numerator / denominator`

For example `4` is the same as `(1, 4)` and corresponds to a quarter note. Dotted half-note is `(3, 4)`. A phrase `[4, 8, 8, 4]` corresponds to a quarter note, two eighths notes and a quarter note.

Not every possible note is supported. For example, triplets (notes such as `(1, 3)`) are not supported yet.
