# Core Concepts

BluePepper relies on a few key components:

## MongoDB Server

Contains all the `Documents` for your project (primarily assets and shots). A `Document` is essentially the identity card of an asset or shot, think of it as metadata that BluePepper uses across many of its features.

## Lucent

The Python package [Lucent](https://pypi.org/project/lucent-codex/) is used to declare all the naming conventions for your project (i.e., how files should be named, where they should be stored, and which characters are allowed or forbidden).

Lucent holds everything together within a Codex, which contains Conventions (string templates made up of fields) and Rules (that define how fields should behave).

For more information, refer to the [Lucent documentation](https://github.com/tristanlanguebien/lucent)

## Browser

Allows you to search for files by combining the `Database` and the `Codex`. When you select a `Document` and a file type, you are effectively creating a file search that resolves the naming convention using the asset or shot document.

## Batcher

The task manager that executes in the background the actions you launch from the Browser. While it is somewhat advanced, it is a powerful tool for running an action across hundreds of shots in a single click.

Once you are familiar with these four components, a world of possibilities opens up!