get-hugo:
	VERSION=$$(curl -fsSL https://api.github.com/repos/gohugoio/hugo/releases/latest | grep -Po '"tag_name": "v\K[^"]+') && \
	mkdir -p ~/.local/bin && \
	curl -fsSL https://github.com/gohugoio/hugo/releases/download/v$$VERSION/hugo_$${VERSION}_linux-amd64.tar.gz | tar -xz -C ~/.local/bin hugo
	hugo version

build:
	hugo build

serve:
	hugo server
