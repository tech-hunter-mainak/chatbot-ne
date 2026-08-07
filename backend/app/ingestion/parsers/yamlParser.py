from pathlib import Path
from datetime import datetime

import yaml

from .baseParser import BaseParser


class YamlParser(BaseParser):

    def parse(self, filePath: Path) -> dict:

        with open(
            filePath,
            "r",
            encoding="utf-8"
        ) as file:

            data = yaml.safe_load(file)

        if data is None:
            data = {}

        title = data.get(
            "title",
            filePath.stem.replace("_", " ")
        )

        content = ""

        if "content" in data:

            if isinstance(data["content"], str):

                content = data["content"]

            else:

                content = yaml.dump(
                    data["content"],
                    allow_unicode=True
                )

        else:

            content = yaml.dump(
                data,
                allow_unicode=True
            )

        stat = filePath.stat()

        return {

            "title": title,

            "text": content,

            "source": str(filePath),

            "file_name": filePath.name,

            "file_type": "yaml",

            "extension": filePath.suffix.lower(),

            "author": "",

            "created": datetime.fromtimestamp(
                stat.st_ctime
            ).isoformat(),

            "modified": datetime.fromtimestamp(
                stat.st_mtime
            ).isoformat(),

            "size": stat.st_size,

            "raw_yaml": data
        }