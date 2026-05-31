FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8

RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    tmux \
    unzip \
    ca-certificates \
    gnupg \
    lsb-release \
    jq \
    ripgrep \
    fzf \
    vim \
    && rm -rf /var/lib/apt/lists/*

# GitHub CLI
RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg \
      | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg \
    && chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" \
      | tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
    && apt-get update \
    && apt-get install -y gh \
    && rm -rf /var/lib/apt/lists/*

# Node.js LTS
RUN curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Claude Code
RUN npm install -g @anthropic-ai/claude-code

# 競技プログラミング環境（--build-arg INSTALL_COMPETITIVE=true でオン）
ARG INSTALL_COMPETITIVE=false
COPY setup-competitive.sh /tmp/setup-competitive.sh
RUN if [ "$INSTALL_COMPETITIVE" = "true" ]; then bash /tmp/setup-competitive.sh root; fi

# ubuntu ユーザー (UID=1000) が既に存在するのでそのまま使用
# --dangerously-skip-permissions は root 不可のため非 root で実行
USER ubuntu
WORKDIR /home/ubuntu
ENV PATH=/home/ubuntu/.cargo/bin:${PATH}
ENV CARGO_HOME=/home/ubuntu/.cargo
ENV RUSTUP_HOME=/home/ubuntu/.rustup
# HOME を外部から override しても XDG ディレクトリは ubuntu のホームに固定
ENV XDG_CACHE_HOME=/home/ubuntu/.cache
ENV XDG_CONFIG_HOME=/home/ubuntu/.config
ENV XDG_DATA_HOME=/home/ubuntu/.local/share
RUN if [ "$INSTALL_COMPETITIVE" = "true" ]; then bash /tmp/setup-competitive.sh user; fi
