#!/usr/bin/env python3
"""Read-only local executable and output-location check; no downloads."""
import argparse
import json
from pathlib import Path
import shutil
import sys
from workspace_paths import output_path


def main():
    parser = argparse.ArgumentParser(description='检查前置工具及输出隔离，不安装软件或创建目录')
    parser.add_argument('--workspace', type=Path, default=Path.cwd() / 'outputs/wechat-news-card')
    args = parser.parse_args()
    try:
        workspace = output_path(args.workspace)
    except ValueError as error:
        print(json.dumps({'ok': False, 'error': str(error)}, ensure_ascii=False))
        return 1
    tools = {name: shutil.which(name) for name in ('node', 'npm', 'npx', 'ffmpeg', 'ffprobe')}
    missing = [name for name, found in tools.items() if not found]
    python_ok = sys.version_info >= (3, 9)
    print(json.dumps({
        'ok': not missing and python_ok,
        'workspace': str(workspace),
        'workspace_exists': workspace.exists(),
        'python': sys.version.split()[0],
        'python_supported': python_ok,
        'tools': tools,
        'missing': missing,
        'manual_checks': ['按实际安装方式检查HyperFrames CLI及对应技能',
                          '运行HyperFrames doctor核验浏览器和编码依赖',
                          '选择中文字体并实测字重、换行与封面裁切'],
        'note': '只发现本机命令，不联网、不安装、不保证工具版本兼容或字体可用。',
    }, ensure_ascii=False, indent=2))
    return 0 if not missing and python_ok else 1


if __name__ == '__main__':
    raise SystemExit(main())
