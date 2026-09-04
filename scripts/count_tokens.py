# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "tiktoken>=0.7.0",
#     "rich>=13.0.0",
# ]
# ///
"""
Token counter for LLM skill files and packages.

Calculates estimated token counts using tiktoken (defaulting to cl100k_base / o200k_base)
with clean tabular breakdowns by skill, category (SKILL.md, references, scripts/assets),
and file-level inspection.

Usage:
    uv run scripts/count_tokens.py
    uv run scripts/count_tokens.py --packaged
    uv run scripts/count_tokens.py skills/diagnosing-bugs
    uv run scripts/count_tokens.py --by-file
    uv run scripts/count_tokens.py --encoding o200k_base
"""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path
from typing import NamedTuple

try:
    import tiktoken
except ImportError:
    tiktoken = None  # Fallback will be handled gracefully

from rich.console import Console
from rich.panel import Panel
from rich.table import Table


class FileTokenInfo(NamedTuple):
    path: Path
    rel_path: str
    category: str
    tokens: int
    char_count: int
    line_count: int


class SkillTokenSummary:
    def __init__(self, name: str, base_dir: Path):
        self.name = name
        self.base_dir = base_dir
        self.files: list[FileTokenInfo] = []

    def add_file(self, file_info: FileTokenInfo):
        self.files.append(file_info)

    @property
    def total_tokens(self) -> int:
        return sum(f.tokens for f in self.files)

    @property
    def skill_md_tokens(self) -> int:
        return sum(f.tokens for f in self.files if f.category == "SKILL.md")

    @property
    def references_tokens(self) -> int:
        return sum(f.tokens for f in self.files if f.category == "Reference")

    @property
    def assets_tokens(self) -> int:
        return sum(f.tokens for f in self.files if f.category in ("Asset / Doc", "Script / Code", "Other"))

    @property
    def total_lines(self) -> int:
        return sum(f.line_count for f in self.files)

    @property
    def total_chars(self) -> int:
        return sum(f.char_count for f in self.files)


def get_tokenizer(encoding_name: str = "cl100k_base"):
    if tiktoken is not None:
        try:
            return tiktoken.get_encoding(encoding_name)
        except Exception:
            try:
                return tiktoken.get_encoding("cl100k_base")
            except Exception:
                pass
    return None


def count_tokens_in_text(text: str, tokenizer) -> int:
    if tokenizer is not None:
        try:
            return len(tokenizer.encode(text, disallowed_special=()))
        except Exception:
            pass
    # Fast fallback estimate: ~4 chars per token for typical code / markdown
    return max(1, len(text) // 4)


def categorize_file(rel_path: Path) -> str:
    parts = rel_path.parts
    filename = rel_path.name

    if filename == "SKILL.md":
        return "SKILL.md"
    if "references" in parts:
        return "Reference"
    if "scripts" in parts or rel_path.suffix in (".sh", ".py", ".bash", ".js", ".ts"):
        return "Script / Code"
    if rel_path.suffix in (".md", ".txt", ".rst"):
        return "Asset / Doc"
    return "Other"


def analyze_skill_dir(skill_dir: Path, tokenizer) -> SkillTokenSummary:
    summary = SkillTokenSummary(name=skill_dir.name, base_dir=skill_dir)

    for file_path in sorted(skill_dir.rglob("*")):
        if file_path.is_file():
            # Skip hidden files or git directories
            if any(part.startswith(".") for part in file_path.relative_to(skill_dir).parts):
                continue

            try:
                content = file_path.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue

            tokens = count_tokens_in_text(content, tokenizer)
            lines = len(content.splitlines())
            chars = len(content)
            rel_path = file_path.relative_to(skill_dir)
            category = categorize_file(rel_path)

            summary.add_file(
                FileTokenInfo(
                    path=file_path,
                    rel_path=str(rel_path),
                    category=category,
                    tokens=tokens,
                    char_count=chars,
                    line_count=lines,
                )
            )

    return summary


def find_skill_directories(targets: list[str], default_dir: Path) -> list[Path]:
    if targets:
        resolved = []
        for t in targets:
            p = Path(t)
            if p.is_dir():
                # Check if this directory itself contains SKILL.md
                if (p / "SKILL.md").exists():
                    resolved.append(p)
                else:
                    # Look for subdirectories containing SKILL.md
                    sub_skills = [sub for sub in sorted(p.iterdir()) if sub.is_dir() and (sub / "SKILL.md").exists()]
                    if sub_skills:
                        resolved.extend(sub_skills)
                    else:
                        resolved.append(p)
            elif p.is_file():
                # Pass parent if file is SKILL.md
                resolved.append(p.parent)
        return resolved

    # Default: search default_dir
    if default_dir.exists():
        return [p for p in sorted(default_dir.iterdir()) if p.is_dir() and (p / "SKILL.md").exists()]
    return []


def format_number(n: int) -> str:
    return f"{n:,}"


def render_summary_table(summaries: list[SkillTokenSummary], console: Console, title: str):
    table = Table(
        title=title,
        show_header=True,
        header_style="bold cyan",
        title_style="bold magenta",
        show_footer=True,
        footer_style="bold green",
    )

    table.add_column("Skill Name", style="bold white", footer="Grand Total")
    table.add_column("Files", justify="right", footer=format_number(sum(len(s.files) for s in summaries)))
    table.add_column("SKILL.md", justify="right", footer=format_number(sum(s.skill_md_tokens for s in summaries)))
    table.add_column("References", justify="right", footer=format_number(sum(s.references_tokens for s in summaries)))
    table.add_column("Assets/Code", justify="right", footer=format_number(sum(s.assets_tokens for s in summaries)))
    table.add_column("Total Tokens", justify="right", style="bold yellow", footer=f"[bold yellow]{format_number(sum(s.total_tokens for s in summaries))}[/]")
    table.add_column("Total Lines", justify="right", style="dim", footer=format_number(sum(s.total_lines for s in summaries)))

    for s in sorted(summaries, key=lambda x: x.total_tokens, reverse=True):
        table.add_row(
            s.name,
            str(len(s.files)),
            format_number(s.skill_md_tokens),
            format_number(s.references_tokens) if s.references_tokens else "-",
            format_number(s.assets_tokens) if s.assets_tokens else "-",
            format_number(s.total_tokens),
            format_number(s.total_lines),
        )

    console.print(table)


def render_file_details(summaries: list[SkillTokenSummary], console: Console):
    for s in summaries:
        table = Table(
            title=f"Detailed Breakdown: [bold cyan]{s.name}[/] ({format_number(s.total_tokens)} total tokens)",
            show_header=True,
            header_style="bold cyan",
            title_style="bold magenta",
            show_footer=True,
            footer_style="bold green",
        )

        table.add_column("Relative Path", style="white", footer="Total")
        table.add_column("Category", style="dim")
        table.add_column("Lines", justify="right", footer=format_number(s.total_lines))
        table.add_column("Characters", justify="right", style="dim", footer=format_number(s.total_chars))
        table.add_column("Est. Tokens", justify="right", style="bold yellow", footer=f"[bold yellow]{format_number(s.total_tokens)}[/]")

        for f in sorted(s.files, key=lambda x: x.tokens, reverse=True):
            table.add_row(
                f.rel_path,
                f.category,
                format_number(f.line_count),
                format_number(f.char_count),
                format_number(f.tokens),
            )

        console.print(table)
        console.print()


def main():
    parser = argparse.ArgumentParser(
        description="Estimate token counts for LLM skill files and packages.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "targets",
        nargs="*",
        help="Specific skill directories or files to inspect (default: scans skills/ or output/skills/).",
    )
    parser.add_argument(
        "-p",
        "--packaged",
        action="store_true",
        help="Inspect output/skills/ (built packages with injected references) instead of source skills/.",
    )
    parser.add_argument(
        "-f",
        "--by-file",
        action="store_true",
        help="Display detailed file-by-file token breakdown for each skill.",
    )
    parser.add_argument(
        "-e",
        "--encoding",
        default="cl100k_base",
        choices=["cl100k_base", "o200k_base", "p50k_base", "r50k_base"],
        help="tiktoken encoding model to use (default: cl100k_base).",
    )

    args = parser.parse_args()
    console = Console()

    tokenizer = get_tokenizer(args.encoding)
    if tokenizer is None:
        console.print(
            "[yellow]Warning: tiktoken tokenizer could not be initialized; using ~4 chars/token heuristic.[/yellow]\n"
        )

    # Determine default directory
    repo_root = Path(__file__).resolve().parent.parent
    default_dir = repo_root / "output" / "skills" if args.packaged else repo_root / "skills"

    skill_dirs = find_skill_directories(args.targets, default_dir)

    if not skill_dirs:
        console.print(
            Panel(
                f"[bold red]No skill directories found.[/bold red]\n\n"
                f"Searched target: [cyan]{default_dir}[/cyan]\n"
                f"If using `--packaged`, make sure to run [bold]make build[/bold] first.",
                title="Error",
            )
        )
        sys.exit(1)

    summaries = [analyze_skill_dir(sd, tokenizer) for sd in skill_dirs if sd.exists()]

    if not summaries:
        console.print("[yellow]No valid skill files found in the specified targets.[/yellow]")
        sys.exit(0)

    target_desc = f"Packaged Skills (`{default_dir.relative_to(repo_root)}`)" if args.packaged else f"Source Skills (`{default_dir.relative_to(repo_root)}`)"
    if args.targets:
        target_desc = f"Targeted Skills ({len(summaries)} inspected)"

    title = f"LLM Skill Token Estimates — {target_desc} [dim]({args.encoding})[/dim]"
    render_summary_table(summaries, console, title)

    if args.by_file:
        console.print()
        render_file_details(summaries, console)


if __name__ == "__main__":
    main()
