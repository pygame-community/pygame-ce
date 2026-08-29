# Contributing to `pygame-ce`

We welcome all contributions! Typo fixes, docs corrections, new API, fixing segmentation faults, basically anything will be looked at and your help is appreciated.
This document is a general guide for how to contribute, but for more detailed information, go see [the wiki](https://github.com/pygame-community/pygame-ce/wiki#contributing),
where we have more detailed information available.

## How to Contribute

### 0. Using AI agents:
If you're using AI at all in your workflow, ensure you read and follow the instructions in AI usage instructions at the bottom of this guide. This is non-negotiable.

### 1. Fork the repository:
Click the "Fork" button in the top right corner of the GitHub page. Then you'll need to clone your fork to your local machine.

```bash
git clone https://github.com/yourusername/pygame-ce
```

### 2. Create a new branch:
Create a new branch for your changes.  This keeps your changes separate from the main project until they're ready to be merged.  A good branch name describes the changes you're making, e.g., `fix-transform-scale-segfault` or `update-docs-in-some-function`.

```bash
git checkout -b fix-transform-scale-segfault
# or git switch -c fix-transform-scale-segfault
```

### 3. Make your changes in your local copy of your fork

### 4. Test your changes:
Depending on what you're changing, there are some things you should test locally before committing. Generating docs, building and running the unit tests, running mypy, etc. Regardless of what you're doing, you should always test your changes before pushing up. Never assume that you didn't break something, even with a minor commit.

#### Building docs

```bash
python dev.py docs --full
```

#### Building `pygame-ce`

```bash
python dev.py install
```

#### Running unit tests

```bash
# build first
python dev.py test #insert module you want to test, if left empty will run every test suite
```

#### Running mypy

```bash
# build first
python dev.py stubs
```

#### Do everything above and check that you don't get any unexpected problems

```bash
python dev.py all
```

### 5. Commit your changes:
Time to commit with a clear, descriptive commit message.

```bash
git commit -m "Fixed segfault in pygame.transform.scale when X"
```

### 6. Push your changes:
Time to push up to your remote repository

```bash
git push --set-upstream origin fix-transform-scale-segfault
```

### 7. Create a pull request
Go to the original repository and click the "New pull request" button.  Select your forked repository and branch.  Provide a clear title and description of your changes in the pull request.

### 8. Review and merge
Your pull request will be reviewed by the maintainers.  They may suggest changes or ask for clarification.  Once the review is complete, your changes will be merged into the main project if it's deemed to be a change that aligns with the direction and goals of `pygame-ce`.


## Guidelines

- **Backwards compatible:** We strive for a great deal of backwards compatibility here at `pygame-ce`. If you desire to change an existing behavior, then you'll need to
provide a strong reason why we might consider it. Someone out there might be using the current behavior and we don't want to break their stuff. A usually better
alternative is to keep the default behavior the same, but add an option to run the new behavior somehow. It can be a new function, a kwarg, etc.
- **Accurate information:** Ensure that all information is accurate and up-to-date.  Double-check links and descriptions before submitting your changes.
- **Clear descriptions:** Write concise and informative descriptions for each change.  Explain what the change does and what its key features are.
- **Do not lie:** If you use AI to generate part or all of your changes, state that in your pull request. Also state exactly how much of your change was written by AI and how
you verified that the changes don't have any unintended side-effects and that they do what they're supposed to do.
- **New functionality always gets new tests:** You should always write new unit tests in the appropriate file in the test directory for any added/changed functionality, if at all
possible. Sometimes it's not possible to test things, but that's a minuscule minority of the changes we see. Write tests, or explain why no new tests are added.
- **Join the [PGC Discord](https://pyga.me/discord):** Besides the role you can get in the server upon your first pull request being merged, regular contributors are active members of the discord server and are willing to give you a hand if crafting your pull request gets to be painful.

Thank you for contributing!

## AI Usage Guidelines

The pygame-ce project has the following requirements for AI usage:

- Any pull request or issue opened with the aid of AI shall be vetted by a human.
- All changes shall be manually tested by a human. Maintainers should never be the first real person to test your code.
- Automated agents shall not open pull requests to resolve issues labeled `good first issue`. These issues are specifically
 intended for humans who want to start contributing.
- Disclosure of AI usage in any form is highly encouraged, disclosure of AI-generated code is required.
- Pull requests driven by AI agents may be subject to stricter rules regarding response time to feedback or questions as opposed
 to a human contributor. The entire point of using an AI agent is to push out changes quickly, so they should respond quickly as well.

***The pygame-ce Steering Council reserves the right to make exceptions to these rules or enforce additional rules as deemed necessary***.

# We are humans
Keep in mind that pygame-ce is maintained by humans.

Every issue, pull request, discord conversation, etc is read and reviewed by humans. Even when we use AI tools like CodeRabbit to
aid in pull request review, there is still a human that must read it themselves. It is disrespectful to put in zero effort when
you put in untested, unvetted work and try to get it into the project. The maintainers should not be the first people that test
your code, because we have lives too. We are busy people. There ***shall*** be a human on the other end of every external interaction,
because the onus is on the one who wants to make the change to ensure that it is a quality change.

# AI is not unwelcome here
Pygame-ce has some AI-written code in it by now, and many of our maintainers are starting to adopt using AI more regularly in their workflows.
As a project, we will not outright ban AI usage, because it can be an extremely powerful tool.

*Our reason for this policy is not an anti-AI stance*. Our reason for this policy is the number of unqualified people starting up
automated agents to go create an endless torrent of slop pull requests. We have neither the time nor the energy to filter out
the slop when no effort has been put in by the "author" to verify that the changes are actually reasonable. If you can't put in
the effort to vet your changes, you aren't contributing anything of value. It's these people that are the problem, not the tool
that is AI.

This section is included to be transparent about how AI must be handled in this repository, and to explain that it's neither inherently
anti-AI, nor is it inherently pro-AI. AI is a tool that can be very powerful used responsibly, but that "responsibly" is a very
load-bearing word. This policy lists out the rules that users of AI must follow to contribute to this repository. When followed,
these rules lend themselves to a far more responsible use of AI as an assistant, rather than a faulty replacement.
