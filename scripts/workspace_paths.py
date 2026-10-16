"""Keep generated output outside skill installation directories."""
from pathlib import Path


def output_path(value):
    path = Path(value).expanduser().resolve()
    skill = Path(__file__).resolve().parent.parent
    if path == skill or skill in path.parents:
        raise ValueError('输出目录不能位于技能安装目录内，请指定独立工作区')
    for ancestor in (path, *path.parents):
        if (ancestor / 'SKILL.md').is_file():
            raise ValueError('输出目录位于某个技能目录内，请指定独立工作区')
    return path
