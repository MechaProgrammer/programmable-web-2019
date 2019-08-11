import pytest
from spending_tracker.cli import run_client
import click
from click.testing import CliRunner
from spending_tracker import create_app
from unittest.mock import patch
from flask import Flask


@pytest.fixture()
def test_client(mocker):
    mocker.patch("flask_sqlalchemy.SQLAlchemy.init_app", return_value=True)
    mocker.patch("flask_sqlalchemy.SQLAlchemy.create_all", return_value=True)
    mocker.patch("flask.Flask.run", return_value=True)
    app = create_app()
    return app


@patch('spending_tracker.cli.run_client')
def test_port1(mock_run, test_client):
    # runner = CliRunner()
    runner = test_client.test_cli_runner()
    result = runner.invoke(run_client, ['--port', 5000, '--debug'])
    assert result.exit_code == 0
