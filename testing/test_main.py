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

def test_no_command_shows_help():
    parser = build_parser()
    # Because subparsers.required = True, no subcommand should raise SystemExit
    with pytest.raises(SystemExit):
        parser.parse_args([])  # equivalent to running just `prog`
