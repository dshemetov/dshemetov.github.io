vault := env("OBSIDIAN_VAULT", home_directory() / "Documents/obsidian-space")

[linux]
install-hugo:
    sudo pacman -S --needed hugo

[macos]
install-hugo:
    brew install hugo

build:
    hugo build

# Serve locally; pass -D to include drafts
serve *args:
    hugo server {{ args }}

# Export blog posts from the Obsidian vault into content/blog
sync:
    uv run scripts/vault_export.py "{{ vault }}"
