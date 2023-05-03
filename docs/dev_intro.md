# Intro to Developers
Welcome to PrettyCopy! Thanks for your interest in contributing. We're happy to have you :)

## Reporting Issues, Feature Requests
You have an issue or feature request? Great to know! Just head to the Issues page on our GitHub, [PrettyCopy Issues](https://github.com/hippothebrave/prettycopy/issues), open a "New Issue," and fill it out with whatever you have.

A good bug report includes:

- Expected behavior
- Actual behavior
- Steps to reproduce (preferably as minimal as possible)
- Anything else you think is relevant.

The more information you give us, the more likely it is that we can find a solution!

## Developing
Want to help with development? Even better! Here's how to begin.

(Note: PrettyCopy comes equipped with a Makefile, so you'll be able to simply type 'make [X]' into the command line for a lot of the commands.)

### Setup
Prerequisites: Install Python. At the moment, PrettyCopy runs on Python version 3.7 and higher.

1. Fork the repository on GitHub.
2. Clone your forked repository to your local computer using `git clone https://github.com/[YOUR_USERNAME]/prettycopy.git`
3. Navigate to the folder, and type `make develop` to install the development dependencies. (You can check the file *pyproject.toml* to see what they are.)
4. Congrats, you're ready to get started coding!

### Make changes
Now make your changes.

Create, add to, and run tests to ensure that your changes work as expected and do not break anything. Run tests with the command `make test`, and check if there's any code left untested with the command `make coverage`. All test files should go under the *prettycopy/tests/* directory, and all test functions must begin with the prefix `test_` in order to be recognized.

Check the formatting of your code by running `make lint`. As necessary, automatically fix the formatting by running `make format`.

Finally, as a last check, you may wish to try building your code before making the pull request. That means running, in order,

```
make develop

make build

make lint

make checks

make coverage
```

Commit your final changes, and publish the branch to your GitHub repo.

Finally, head to [PrettyCopy PRs](https://github.com/hippothebrave/prettycopy/pulls) on the main repo and add a pull request linked to your forked repo. 

Thank you so much for your contribution! 