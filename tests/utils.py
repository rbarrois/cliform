import typing
import re


class Expect(typing.NamedTuple):
    prompt: str
    reply: str


class SequenceRunner:
    _sequence: typing.List[Expect]

    def __init__(self, sequence: typing.List[Expect]):
        self._sequence = sequence

    def run(self, displayed, emit_reply):
        loop = self._loop()
        loop.send()  # Initialize loop
        for prompt in displayed:
            reply = loop.send(prompt)
            emit_reply(reply)

        # Ensure we've run to the end of the expected sequence
        loop.close()

    def _loop(self):
        reply = None
        for expected, answer in self._sequence:
            prompt = yield reply
            if not re.match(expected, prompt):
                raise ValueError("Prompt %r doesn't match expected %r" % (prompt, expected))
            reply = answer
        yield reply
