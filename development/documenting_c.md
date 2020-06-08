# Documenting SpiNNaker C Code using Doxygen

We use [Doxygen](https://www.doxygen.nl/manual/) to translate special comments
in our C code into our online documentation trees.

Doxygen is very complicated, but we only use a subset of it. The configuration
file for the Doxygen build is called `Doxyfile`, and is huge and complex; we
try to turn off most of the features.

## Documented files

We configure Doxygen to make documentation from all files with the extensions
`*.c`, `*.h`, `*.md` (good for auxiliary pages) and `*.dox`.

The `*.dox` files should contain a single C-style documentation comment, and
are places for putting code information that doesn't fit anywhere else. For
example, they can be used to provide the front page of the documentation tree,
or to contain directory level documentation if there isn't an obvious other
file to put them in. _Note that `*.dox` files do not appear in the file tree._

## Documentation comment format

All Doxygen documentation (in C) is placed in a comment like this (common):

```c
//! ...
```

or like this (uncommon):

```c
/*!
 * ...
 */
```

Or like this (very uncommon in our code):

```c
/**
 * ...
 */
```

## Directives

All directives (within a documentation comment) start with either `\` or `@`
(you can use either; we commonly use backslash). The main ones you need to
know are:

* `\file` — _Every_ `*.c` and `*.h` file needs _one_ of these. Probably
  followed by a `\brief` directive to provide a short description of the file.

* `\brief` — A _short_ description of something, usually a function, macro,
  variable, structure, etc. Lasts until the next block-level directive or a
  blank doc-comment line. Under normal circumstances, this should be a short
  sentence.

* `\details` — The _long_ description of something. Can be multiple paragraphs.
  Paragraphs are basically in Markdown format.

* `\param` — Describes a parameter to a function or macro. Optionally followed
  by `[in]`, `[out]`, or `[in,out]` to say what the parameter is doing (`[in]`
  is probably the normal case). That is then followed by the _name_ of the
  parameter (which must match the declaration) and an optional colon (`:`);
  the colon is _strongly recommended_ for clarity.

  For example, this might document an argument `int foo`:

    ```
    \param[in] foo: This is the primary foo thing in consideration.
    ```

* `\return` — Describes the result of the function or macro. Functions that
  have `void` as their result type _must not_ have a `\return` directive!

Bare documentation comments without any directive are treated as `\brief` if
they are a single line, and are treated as `\details` otherwise.

### Inline directives

We don't use many directives, but here are some useful ones:

* `\a` — The next word is an argument. See also `\p`.

* `\p` — The next word is a parameter. See also `\a`.

* `\c` — The next word is to be in typewriter font. Normally it is easier to
  use markdown-style backticks.

* `\f$` — Marks the start _and end_ of some inline mathematical content. The
  part inside should be in LaTeX format.

* `\f[` ... `\f]` — Contains a long-format formula in LaTeX format.

Note that Doxygen is apparently poor at recovering from typos in formulæ.

### Rare directives

You won't see these so much.

* `\mainpage` — Used to provide content for the main page of the documentation
  tree. Obviously, there should only be one of these per repository!

* `\dir` — Used to describe a whole directory. Only appears once at most in
  that entire directory.

* `\section` — Starts a section in the documentation. Not that useful when
  incorporated into pages that actually document code, but may be useful in
  auxiliary pages (such as the main page).

* `\name` — Introduces a section of declarations within a file. The
  declarations themselves are then surrounded by `\{` and `\}`. Useful in long
  files with many declarations and some natural grouping, but where a file has
  few declarations it is unnecessary.

* `\note` — Marks a paragraph as worthy of note to the user.

* `\warning` — Marks a paragraph as _particularly_ worthy of note!

* `\todo` — Marks something that's perhaps unfinished. These are also called
  out to a separate summary file.

* `\bug` — Marks something that's outright wrong. These are also called
  out to a separate summary file. _If putting one of these in, make sure you
  have also filed an Issue on Github!_

* `\cond` ... `\endcond` — Used to hide things from Doxygen's output. Try to
  avoid using these!

* `\internal` — Used to hide things from Doxygen's output.

* `\author`, `\copyright`, `\date` — Fairly obvious things for the file
  header material.

## Writing style

Every public symbol should have a `\brief` description.

Functions should have their brief description begin with a present tense
immediate active verb. Thus, instead of:

```
This function frobnicates the mome-raths.
```

or:

```
Frobnicates the mome-raths.
```

use:

```
Frobnicate the mome-raths.
```

Macros that are used like functions should follow the same rules.

Things that work like enumerations should _be_ enumerations, and not just big
collections of `#define`s! (Unless it is impossible for type reasons.)

Do not describe the type of arguments or return values in documentation
comments. The documentation tool picks up the type just fine from the
declaration itself.

## Predefined macros

We disable most C macro processing when loading in source files, but we do
enable _some._ In particular, we define the symbol `DOXYGEN` when building and
you can use that to hide things from the processing tool that confuse it
(notably including `__attribute__(...)` annotations).

The configuration of that is controlled by the `PREDEFINED` configuration value
in the `Doxyfile`. An example setting there is:

```
PREDEFINED             = DOXYGEN=1 \
                         NO_INLINE= \
                         UNIMPLEMENTED=
```

This provides default empty definitions for the `NO_INLINE` and `UNIMPLEMENTED`
macros, which are defined like this in an appropriate C file:

```c
#ifndef DOXYGEN
#define NO_INLINE      __attribute__((noinline))
#define UNIMPLEMENTED  __attribute__((deprecated("Not implemented")))
#endif // DOXYGEN
```

The standard pattern of `#ifndef`/`#define` guards for a whole file do not need
to be documented (and should not be).
