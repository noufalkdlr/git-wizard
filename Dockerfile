FROM archlinux:latest

RUN pacman-key --init \
    && pacman-key --populate archlinux \
    && pacman -Syu --noconfirm \
    && pacman -S git github-cli --noconfirm \
    && pacman -Scc --noconfirm
