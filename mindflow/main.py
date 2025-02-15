"""
This module contains the main CLI for Mindflow.
"""
import argparse
import sys

from mindflow.prompt_generator import generate_diff_prompt
from mindflow.requests.query import QueryRequestHandler
from mindflow.requests.response import get_response
from mindflow.utils.token import set_token


COPY_TO_CLIPBOARD = True

MF_DESCRIPTION = """

Welcome to Mindflow. A command line tool for intelligent development and collaboration.

"""

MF_USAGE = """

mf <command> [<args>]
The commands available in this CLI are:

diff       `mf diff [<git diff args>]`                   Runs a `git diff` and summarizes the changes.
query      `mf query "<YOUR QUERY>" [<Files + Folders>]` Ask a query using all or a subset of your notes as a reference.
auth       Authorize Mindflow with JWT.


"""


def _add_reference_args(parser):
    """
    Add arguments for commands that require references to text.
    """
    parser.add_argument(
        "query", type=str, help="The query you want to make on some data."
    )
    parser.add_argument(
        "references",
        nargs="+",
        help="A list of references to summarize (file path, API, web address).",
    )
    parser.add_argument(
        "-s",
        "--skip-response",
        action="store_true",
        help="Generate prompt only.",
    )
    parser.add_argument(
        "-t",
        "--skip-clipboard",
        action="store_true",
        help="Do not copy to clipboard (testing).",
    )


def _add_diff_args(parser):
    """
    Add arguments for the diff command.
    """
    parser.add_argument(
        "diffargs",
        nargs="*",
        help="This argument is used to pass to git diff.",
    )
    parser.add_argument(
        "-s",
        "--skip-response",
        action="store_true",
        help="Generate prompt only.",
    )
    parser.add_argument(
        "-t",
        "--skip-clipboard",
        action="store_true",
        help="Do not copy to clipboard (testing).",
    )

def _add_auth_args(parser):
    """
    Add arguments for the diff command.
    """
    # Argument for JWT token (optional)
    parser.add_argument(
        "token",
        type=str,
        nargs='?',
        help="JWT token used to authorize usage.",
    )

def _add_ask_args(parser):
    """
    Add arguments for commands that require references to text.
    """
    parser.add_argument(
        "prompt", type=str, help="Prompt for GPT model."
    )
    parser.add_argument(
        "-s",
        "--skip-response",
        action="store_true",
        help="Generate prompt only.",
    )
    parser.add_argument(
        "-t",
        "--skip-clipboard",
        action="store_true",
        help="Do not copy to clipboard (testing).",
    )

class MindFlow:
    """
    This class is the CLI for Mindflow.
    """

    def __init__(self):
        parser = argparse.ArgumentParser(
            description=MF_DESCRIPTION,
            usage=MF_USAGE,
        )
        parser.add_argument("command", help="Subcommand to run")
        args = parser.parse_args(sys.argv[1:2])

        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        if not hasattr(self, args.command):
            print("Unrecognized command")
            parser.print_help()
            sys.exit(1)

        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()

    def auth(self):
        """
        This function is used to generate a git diff and then use it as a prompt for GPT bot.
        """
        parser = argparse.ArgumentParser(
            description="Authorize User.",
        )
        _add_auth_args(parser)
        args = parser.parse_args(sys.argv[2:])
        set_token(args.token)
    
    def ask(self):
        """
        This function is used to generate a git diff and then use it as a prompt for GPT bot.
        """
        parser = argparse.ArgumentParser(
            description="Prompt GPT model with basic request.",
        )
        _add_ask_args(parser)
        args = parser.parse_args(sys.argv[2:])
        response = get_response(args.prompt)
        print(response)

    def diff(self):
        """
        This function is used to generate a git diff and then use it as a prompt for GPT bot.
        """
        parser = argparse.ArgumentParser(
            description="Summarize a git diff.",
        )
        _add_diff_args(parser)
        args = parser.parse_args(sys.argv[2:])
        prompt = generate_diff_prompt(args)
        response = get_response(prompt)
        print(response)

    def query(self):
        """
        This function is used to ask a custom question about any number of files, folders, and websites.
        """
        parser = argparse.ArgumentParser(
            description="This command is use to query files, folders, and websites.",
        )
        _add_reference_args(parser)
        args = parser.parse_args(sys.argv[2:])
        response = QueryRequestHandler(args.query, args.references).query()
        print(response)
    
    # Alias for query
    def q(self):
        return self.query()


def main():
    """
    This is the main function.
    """
    MindFlow()
