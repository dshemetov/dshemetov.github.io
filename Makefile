get-hugo:
	wget https://github.com/gohugoio/hugo/releases/download/v0.150.1/hugo_0.150.1_linux-amd64.tar.gz
	mkdir -p bin/
	tar -xzf hugo_0.150.1_linux-amd64.tar.gz -C bin/
	rm hugo_0.150.1_linux-amd64.tar.gz
	chmod +x bin/hugo
	./bin/hugo version

build:
	./bin/hugo build

serve:
	./bin/hugo server
