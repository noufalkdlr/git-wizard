FROM archlinux:latest

ENV PIP_BREAK_SYSTEM_PACKAGES=1

RUN pacman-key --init \
  && pacman-key --populate archlinux \
  && pacman -Syu --noconfirm \
  && pacman -S git github-cli python python-pip --noconfirm \
  && pacman -Scc --noconfirm

CMD pip install -e . && /bin/bash
