from logging import Logger, basicConfig, getLogger


def logging_factory(name: str) -> Logger:
    basicConfig(
        level="INFO",
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    )

    logger = getLogger(name)

    return logger