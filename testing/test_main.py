# test_main.py
import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import build_parser

def test_add_user_command(monkeypatch):
    parser = build_parser()
    test_args = ["prog", "add-user", "--name", "Alex"]
    monkeypatch.setattr(sys, "argv", test_args)
    args = parser.parse_args()
    assert args.name == "Alex"
    assert args.command == "add-user"

def test_no_command_shows_help(capsys):
    parser = build_parser()

    # Because subparsers.required=True, argparse should exit if no subcommand is provided.
    # pytest.raises(SystemExit) catches that exit so the test can verify it happened.
    with pytest.raises(SystemExit) as e:
        # [] = running CLI with no arguments at all
        parser.parse_args([])  

    # e.value.code holds the exit code argparse used (usually 2 for usage errors)
    assert e.value.code == 2

    # Capture printed output (both stdout and stderr)
    captured = capsys.readouterr()

    # Verify that help/usage text was printed
    assert "usage:" in captured.err  # argparse prints usage to stderr on error
    assert "add-user" in captured.err  # should list available subcommands
    assert "add-project" in captured.err
    assert "add-task" in captured.err
