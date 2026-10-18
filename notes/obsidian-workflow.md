# Writing posts in Obsidian

Blog posts live in the `blog/` folder of the Obsidian vault (`~/Documents/obsidian-space`, synced across machines by Obsidian Sync). `content/blog/` in this repo is generated from them, so don't edit it by hand: changes there are overwritten by the next export.

## Workflow

1. Write a note in the vault's `blog/` folder. Move a note there to make it a post.
2. Keep `draft: true` in its properties until it's ready. Drafts stay in the vault: the export skips them, so they never reach this repo.
3. Run `just sync` in this repo, review the diff, and commit.

Set `OBSIDIAN_VAULT` if the vault lives somewhere else on a machine.

## What the export does

`scripts/vault_export.py` regenerates every bundle in `content/blog/` (except `_index.md`) from the vault's non-draft notes:

- Each note `blog/My Post.md` becomes `content/blog/my-post/index.md`. The page URL still comes from the title (see `[permalinks]` in `hugo.toml`), not the filename.
- A post without a `title` uses its date as the title and link text, and its URL comes from the note's filename. A missing `date` is set to the current time and written back into the vault note, so it stays fixed across exports.
- `![[image.png]]`, `![[image.png|alt text]]` and `![alt](image.png)` copy the image into the bundle (spaces in filenames become `-`) and become standard markdown images. `![[image.png|600]]` becomes a `figure` shortcode with that width. An italic line directly under an image embed (`*A caption.*`) becomes the figure's caption. Images are found the way Obsidian finds them: relative to the note first, then by filename anywhere in the vault.
- `[[Other Post]]`, `[[Other Post|label]]` and `[[Other Post#Heading]]` become `relref` links when the target is another note in `blog/`. Links to notes outside `blog/` become plain text, with a warning, so private notes don't leak.
- `%%comments%%` are removed.
- Code blocks and inline code are left untouched.
- Embeds of non-image files (other notes, PDFs) are left as is, with a warning.

## Home page

The home page shows the 20 most recent posts. Posts up to 300 words appear in full. Longer posts show their first paragraph and first image, followed by a `[… N words]` link to the full post. Set `longform: true` or `longform: false` on a note to override the word count rule.

## Math macros

Custom LaTeX macros like `\Z` live in `preamble.sty` at the vault root, as `\newcommand` (or `\renewcommand`, `\DeclareMathOperator`) lines. Obsidian loads that file through the Extended MathJax community plugin; after editing it, run Obsidian's "Reload app without saving" command. `just sync` turns the same file into `data/math_macros.json`, which `layouts/partials/math.html` passes to MathJax on the site.
