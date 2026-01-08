FROM archlinux:latest

RUN pacman -Syu --noconfirm && pacman -S git github-cli --noconfirm && pacman -Scc --noconfirm
