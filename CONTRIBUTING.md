# Contributing to Pygame CE

Pygame CE is an open-source project that welcomes contributions from the community. Whether you are a beginner or an experienced developer, there are many ways to contribute to the pygame project. This document provides an overview of how you can contribute to the pygame project, including ways to contribute that do not involve writing code.

Please make sure to follow our [Code of Conduct](https://github.com/pygame-community/pygame-ce?tab=coc-ov-file) to maintain a welcoming and inclusive community.

## Table of Contents

- [Ways to Contribute](#ways-to-contribute)
- [Contributing Code: Step-by-Step](#contributing-code-step-by-step)
- [Labelling & Linking Reported Issues](#labelling--linking-reported-issues)
- [Useful Information](#useful-information)
- [Key Takeaways](#key-takeaways)

## Ways to Contribute

Most of the time when we talk about contributions to open source projects, we are referring to opening a pull request to a code repository. However, the pygame community has many ways to contribute that don't require writing code:

- **Report Bugs**: If you find a bug in the pygame library, report it on the [pygame issue tracker](https://github.com/pygame-community/pygame-ce/issues) using the "Guided bug report" template.
- **Request Features**: If you have an idea for a new feature or improvement, submit a feature request on the [pygame issue tracker](https://github.com/pygame-community/pygame-ce/issues) using the "Enhancement" request template.
- **Create Tutorials**: Create video or written tutorials or guides to help others learn how to use pygame.
- **Answer Questions**: If you're knowledgeable about pygame, help answer questions on platforms such as Reddit, Discord, and Stack Overflow.
- **Write Documentation**: Help improve the pygame documentation by fixing typos, adding examples, and/or writing new tutorials.

On the other hand, if you are interested in contributing **code** to the pygame project, you can use the steps [below](#contributing-code-step-by-step).

## Contributing Code: Step-by-Step
### **1. Get an Understanding of Project**

It is a good idea to poke around the codebase and understand how the project is structured before you start contributing. Familiarize yourself with the project's goals, objectives, and scope. If you have any questions or need clarification, don't hesitate to ask!

### **2. Fork the Repository**

Create a fork of the pygame-ce repository on your own github profile. You do this by clicking the 'Fork' button on the top right hand side of the repository:

<div style="text-align: center;">
  <img src="https://user-images.githubusercontent.com/13382426/218566753-e7d1ff25-f296-4308-bd57-5522220a6254.png" alt="Fork Image" title="Pygame">
</div>

### **3. Clone the Repository**

Clone your new fork to your local machine. GitHub provides many options for doing this.

<div style="text-align: center;">
  <img src="https://user-images.githubusercontent.com/13382426/218567122-99b745d8-cab7-4fc0-b94a-2b027f919054.png" alt="Clone Options" title="Pygame">
</div>

The method to use depends on personal preference and the tools you have installed on your machine. However, I prefer using [IDE PyCharm](https://www.jetbrains.com/pycharm/) to clone the repository from this menu:

<div style="text-align: center;">
  <img src="https://user-images.githubusercontent.com/13382426/218567466-c6544380-776a-45a8-b380-7435dcafaca2.png" alt="Clone Options" title="Pygame">
</div>

### **4. Create a Branch**
Create a new branch from the main branch of your forked, cloned local repository where you will make your changes. Try to give it a sensible name that relates to your changes, this will help reviewers later. Back to the PyCharm example, found in the bottom right corner of the window, you can see the current branch you are on. Click on it and select 'New Branch' to create a new branch.

<div style="text-align: center;">
  <img src="https://user-images.githubusercontent.com/13382426/218568063-a82a5499-5b8c-4c26-8a59-40381f8668c4.png" alt="Clone Options" title="Pygame">
</div>

### **5. Make Changes**
Time to actually make your changes. This is a whole separate topic but we will assume you have successfully fixed a bug or made that amazing new feature.
### **6. Test Your Changes**
Before you submit your changes ensure that your code compiles correctly and performs its intended function through some testing. For better reliability, consider writing unit tests or continuous integration (CI) tests for the fix or new feature.
### **7. Lint and Autoformat**
Run your changes through the linting and autoformatting programs. For python code this would be something like:
```bash
black test/blit_test.py
```
For C code, you might use clang-format:
```bash
clang-format src_c/math.c -i
```
PyCharm has a terminal built in, but you can use your normal OS terminal to run these commands. `black` is easy to install from [PyPI](https://pypi.org/) using `pip`, but `clang-format` may require a bit more effort on some platforms to make it actually work. You can try grabbing the [latest LLVM release](https://github.com/llvm/llvm-project/releases) and install the python package from [PyPI](https://pypi.org/).
### **8. Commit Your Changes**
Once you are happy with your changes, commit everything to your local repository with a short sensible one line commit message. This message will eventually be visible in the public GitHub repo so you want it to make some sense.
### **9. Push Your Changes**
Push your changes to your forked repository on GitHub. This will make your changes visible to the pygame maintainers.
### **10. Create a Pull Request**
Create a pull request from your branch to the main branch of the pygame-ce repository. You can do this from the GitHub [Pull requests page](https://github.com/pygame-community/pygame-ce/pulls) and clicking the 'New Pull Request' button To make your pull request the best it can be, make sure to do the following:
- **Explain WHY you are making the change**: Provide a clear and concise description of the problem you are solving or the feature you are adding. This will help reviewers understand the context of your changes.
- **Justify why pygame CE should accept your changes**: There are, of course, infinite things that you can code, but not all of them should be in pygame CE. This library has a particular niche being an easy-to-use, yet DIY collection of code for making games & wrapping the SDL library. Pygame CE is a module that is designed to be welcoming to people installing an external package from PyPI for the first time, but still capable enough to put a commercial game on Steam. It is not trying to be an off the shelf game engine, nor is it trying to compete with unity and unreal in their latest 3D graphics effects. It may be that your idea for a complete racing track level editor is great - but pygame CE is not the right place for it.
- **Add a Copy and Paste-able human test program**: This helps reviewers quickly test your code on their machine and makes it more likely your code is going to get human testing on a variety of machines. It can also help explain your PR and justify it.
- **Add CI/unit tests in the test folder**: This helps make sure your code stays working over time and helps future programmers who may want to make optimisations to it in the future.
- **Documentation and Type hints**: If nobody out in user land knows how your new code works, then they won't use it. If nobody uses it, why did you write it?
- **Screenshots, Diagrams and Graphs**: If you think they would help then stick 'em in.

It can also be helpful to take a look at pygame CE's [revision process](https://github.com/pygame-community/pygame-ce/wiki/The-Reviewing-Process) to understand how your pull request will be reviewed and merged.

### **11. Respond to Feedback**
Once you have submitted your pull request, the pygame maintainers will review your changes and provide feedback. Be responsive during the code review process. Address any feedback or comments provided by reviewers. Be open to constructive criticism and willing to make necessary changes.

Please remember to follow our [Code of Conduct](https://github.com/pygame-community/pygame-ce?tab=coc-ov-file) through this process to ensure a respectful and collaborative environment.

## Labelling & Linking Reported Issues
### **Labelling Issues**
It is helpful when searching the issues in the repository if they have useful labels:
- What Pygame CE submodule they relate to.
- The specific platform(s) if the issue only happens on one or two platforms.
- Specific versions of software the issue occurs on (i.e. Python 3.7 or SDL 2.0.8)
- The general subject area they are trying to address (e.g. performance, accuracy, compatibility)
- Is it a bug or an enhancement?
Adding, removing and updating labels is the broad responsibility of all members of the contributors team. A nice tidy issues list helps us clear out problems faster and tie similar issues together.
### **Linking Issues**
If an issue is related to another issue or pull request, you can link them together. This helps to provide context and show the relationship between different issues and helps when cleaning up the repository issues list after a pull request gets merged. Information on linking issues can be found [here](https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue).

## Useful Information
- The main C code is tucked away in the [/src_c/](https://github.com/pygame-community/pygame-ce/tree/main/src_c) folder.
- The main Python code is under [/src_py/](https://github.com/pygame-community/pygame-ce/tree/main/src_py).
- The tests are in the [/test/](https://github.com/pygame-community/pygame-ce/tree/main/test) folder.
- The examples are in the [/examples/](https://github.com/pygame-community/pygame-ce/tree/main/examples) folder.
- Reference for navigating the code is the [Python C API documentation](https://docs.python.org/3/c-api/index.html) where you can find out all about how arguments passed in from python code are [parsed into C data types](https://docs.python.org/3/c-api/arg.html) and other such things.
- The [ SDL API documentation](https://wiki.libsdl.org/wiki/index) is also useful for understanding the underlying library that pygame CE wraps.

## Key Takeaways

- **Contributing is More Than Code**: There are many ways to contribute to the pygame project that [do not involve writing code](#ways-to-contribute). Reporting bugs, requesting features, creating tutorials, answering questions, and writing documentation are all valuable contributions.
- **Understand the Project**: Before contributing code, take the time to understand the project's goals, objectives, and scope.
- **Try and Be Kind**: Contributing and reviewing, like anything involving programming computers, can be a bit stressful. Remember there is a human at the other end of most (all?) keyboards and try to kind to them.
- **Games are supposed to be Fun**: Try to take a little bit of joy in contributing. If you are not having fun, then take a break! Pygame has been around in one form or another for over twenty years and will still be here when you come back.
