# AI Policy

This policy is inspired by [RustPython's AI policy](http://github.com/RustPython/.github/blob/main/AI_POLICY.md).

The pygame-ce project has the following requirements for AI usage:

* *All AI usage in any form **shall** be disclosed*.

    * You ***shall*** state any AI tool you use along with the extent of how much of the work was done by AI.
    * You ***shall*** disclose AI use in both your pull request description and your commit messages.
    * You ***shall*** use the `Assisted-by` git trailer in your commit messages.
        * You ***shall*** use separate trailers for each and every AI agent used.

* *Pull requests by automated agents ***shall*** only be for existing issues*.

    * You ***shall not***, under any circumstances, use an automated agent for creating pull requests for issues tagged with `good first issue`.
        These issues are specifically and solely intended for humans who want to start contributing to open source software to get their feet wet.
        Sniping these issues with an automated agent must not happen.
    * You ***shall not***, under any circumstances, create a pull request for an issue that still has ongoing discussions about the best way
        to resolve it.
    * You ***shall not***, under any circumstances, create an issue then immediately create a pull request to bypass these rules.

* *Pull requests created by AI agents ***shall*** have been vetted by a human*.

    * You ***shall*** manually review any pull requests created by an AI agent before posting it.
    * You ***shall*** manually test any pull requests created by an AI agent before posting it.
        * When you are unable to manually test, you ***shall*** explicitly state why you are unable to test your code.
        * When you are able to manually test, you ***shall*** explicitly provide all test steps and scripts you used, as well as the
            output of `pygame.print_debug_info()` for the system(s) you tested with.
    * You ***shall*** manually review and test every single commit after the pull request is open.
    * You ***shall not*** assume the maintainers count as people who can vet your pull request. That's not our job. That's your job.
    * You ***shall not*** assume any change is so minor that it does not warrant testing.
    * You ***shall not*** implicitly trust AI to have written valid code or to not have broken something.
    * You ***shall*** respond to feedback in a timely manner when a maintainer gives it.
        * When you are unable to respond specifically to feedback, you or your automated agent ***shall*** provide a timeline of when
            you expect to be able to respond to feedback. This timeline ***may*** be pushed back no more than 3 times consecutively.
            When the expected time of response expires by more than 2 hours, the pull request ***shall*** be considered abandoned.

* *Issues created by AI agents ***shall*** have been vetted by a human*.

    * You ***shall*** manually review any issues created by an AI agent before posting it.
    * You ***shall*** manually confirm that there is actually an issue and that the issue is representative of the actual problem.
        * When the issue cannot be reproduced, then you ***shall*** provide an extremely strong justification for why you think
            there is a problem here, and that reason cannot be along the lines of "The AI said so". You must provide a reason you
            cannot test the issue yourself.
        * When the issue can be reproduced, you ***shall*** provide a reproducer script as well as the output of `pygame.print_debug_info()`
            for all systems you were able to reproduce the issue with.

***Violations of this policy shall result in your issue or pull request being closed without further consideration.***

***Violations of this policy may result in your account being banned from contributing to pygame-ce.***

***This policy shall only ever be edited by a human. No AI agent must ever touch this file. When an AI agent touches this policy, your
    account shall be banned.***


These rules only apply to non-Members of the pygame-ce team. When someone has gained the Member title, they have demonstrated that they
are competent enough to be trusted with more free usage of AI. However, the rule about editing this policy ***shall*** always be followed.
Members may be exempt from immediate ban at the discretion of the Steering Council.

***The pygame-ce Steering Council reserves the right to make exceptions to these rules or enforce additional rules as deemed necessary***.

# Disclosing AI assistance in commit messages

When AI tools are used to create a commit, you ***shall not*** use the `Co-authored-by` git trailer. That trailer is reserved for human coauthors.
When AI tools are used to create a commit, you ***shall*** use the `Assisted-by` git trailer, one for each AI tool.

The format you ***shall*** use is:

```
Assisted-by: AGENT_NAME:MODEL_VERSION
```

For example:
```
Assisted-by: OpenCode:qwen3.6-plus
Assisted-by: Claude Code:claude-sonnet-4-6
Assisted-by: Gemini CLI:gemini-3.1-pro-preview
Assisted-by: Codex:gpt-5.4
```

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
