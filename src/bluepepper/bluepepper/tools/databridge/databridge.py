from __future__ import annotations

import logging
import shutil
from pathlib import Path
from typing import Callable

from lucent import Convention

from bluepepper.tools.sanitycheck import SanityCheck


def _default_dst_callback(
    src: Path, src_convention: Convention, dst_convention: Convention
) -> Path:
    fields = src_convention.parse(src)
    return Path(dst_convention.format(fields))


def _default_transfer_callback(
    src: Path, dst: Path, src_convention: Convention, dst_convention: Convention
) -> None:
    if dst.exists():
        raise FileExistsError(f"The destination file already exists : {dst}")
    dst.parent.mkdir(exist_ok=True, parents=True)

    if src.is_file():
        shutil.copy2(src, dst)
        return

    if src.is_dir():
        shutil.copytree(src, dst)
        return


def _default_post_transfer_callback(
    src: Path, dst: Path, src_convention: Convention, dst_convention: Convention
):
    logging.info(
        f"Finished transferring {src} to {dst} ({src_convention.name} -> {dst_convention.name})"
    )


class TransferProtocols:
    def __init__(self) -> None:
        self.protocols: dict[str, TransferProtocol] = {}

    def register_protocol(self, protocol: TransferProtocol):
        if self.protocols.get(protocol.src_convention.name):
            raise KeyError(
                f"A protocol was already registered for convention {protocol.src_convention.name}"
            )
        self.protocols[protocol.src_convention.name] = protocol

    def get_protocol_for_path(self, path: Path) -> TransferProtocol:
        for protocol in self.protocols.values():
            if protocol.src_convention.match(path):
                return protocol
        raise RuntimeError(f"No protocol was found for {path}")


class TransferProtocol:
    def __init__(
        self,
        src_convention: Convention,
        dst_convention: Convention,
        dst_callback: Callable | None = None,
        transfer_callback: Callable | None = None,
        chunking_callback: Callable | None = None,
        sanitycheck: SanityCheck | None = None,
        post_transfer_callbacks: list[Callable] | None = None,
    ) -> None:
        self.src_convention = src_convention
        self.dst_convention = dst_convention
        self.dst_callback: Callable = dst_callback or _default_dst_callback
        self.transfer_callback: Callable = (
            transfer_callback or _default_transfer_callback
        )
        self.chunking_callback = chunking_callback
        self.sanitycheck = sanitycheck
        self.post_transfer_callbacks: list[Callable] = post_transfer_callbacks or [
            _default_post_transfer_callback
        ]

    def _get_destination(self, path: Path) -> Path:
        return self.dst_callback(path, self.src_convention, self.dst_convention)


class PathTransfer:
    def __init__(self, path: Path, protocol: TransferProtocol) -> None:
        self.path = path
        self.protocol = protocol

    def transfer(self):
        if not self.path.exists():
            raise FileNotFoundError(f"The file {self.path} does not exist")

        dst = self.protocol._get_destination(self.path)
        logging.info(f"Copying {self.path} to {dst}")
        self.protocol.transfer_callback(
            self.path, dst, self.protocol.src_convention, self.protocol.dst_convention
        )
        for callback in self.protocol.post_transfer_callbacks:
            callback(
                self.path,
                dst,
                self.protocol.src_convention,
                self.protocol.dst_convention,
            )
