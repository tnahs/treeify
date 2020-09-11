__version__ = "0.1.0"


import re
from typing import Dict, List, Optional


class TreeIndentationError(IndentationError):
    def __init__(
        self,
        lines: List[str],
        line_number: int,
        indent: str,
        generation: int,
        remainder: str,
    ):
        message = (
            f"Input string contains invalid indentation on line {line_number}.\n"
            f"{self._previous_lines(lines=lines, line_number=line_number)}\n"
            f"{line_number:03}: {lines[line_number]}\n"
            f"{line_number:03}: {indent * generation}{'^' * len(remainder)}"
        )
        super().__init__(message)

    @staticmethod
    def _previous_lines(lines, line_number) -> str:

        previous_lines: List[str] = []

        for i in range(1, 10):

            previous_line_number: int = line_number - i

            if previous_line_number < 0:
                break

            try:
                previous_line: str = lines[previous_line_number]
            except IndexError:
                break

            previous_lines.append(f"{previous_line_number:03}: {previous_line}")

        return "\n".join(reversed(previous_lines))


class Treeify:
    INDENT_TYPES_REGEX = re.compile(
        r"""
        ^
        ([ ]{1,4}|\t)
        (?=\S)
        """,
        re.VERBOSE,
    )

    def __init__(self, string: str):

        self.nodes: List["Node"] = []

        self.lines: List[str] = [i for i in string.splitlines() if i]
        self.indent: str = self.parse_indentation()
        self.indent_regex: re.Pattern = re.compile(self.indent)
        self.indent_character: str = self.indent[0]

        """ TODO: Normalize line indentation before validation:

            •••• •••• root
            •••• •••• •••• node01
            •••• •••• •••• node02

            root
            •••• node01
            •••• node02
        """

        self.validate()
        self.build()

    def __repr__(self):
        return (
            f"<{self.__class__.__name__} "
            f"indent-width: {len(self.indent)} "
            f"indent-character: '{'spaces' if self.indent_character == ' ' else 'tabs'}' "
            f"nodes: {len(self.nodes)}>"
        )

    def inspect_nodes(self) -> None:
        nodes = [f"{node!r}" for node in self.nodes]
        all = [repr(self), *nodes]
        print("\n".join(all))

    def inspect_lines(self) -> None:
        all = [repr(self), *self.lines]
        print("\n".join(all))

    def render(self) -> None:
        print(self.output)

    @property
    def output(self) -> str:
        return "\n".join([node.render() for node in self.nodes])

    def parse_indentation(self) -> str:

        for line in self.lines:

            indent: Optional[re.Match] = self.INDENT_TYPES_REGEX.search(line)

            if indent is None:
                continue

            return indent.group(0)

        raise IndentationError("Input string contains no indentation.")

    def validate(self):
        self._validate_generation_gap()
        self._validate_indentation_consistency()

    def build(self):
        """ https://stackoverflow.com/a/49912639 """

        parent_nodes: Dict[int, "Node"] = {}

        for line in self.lines:

            # With four-space indentation:
            # name:       | •••• •••• node-name -> node-name
            # generation: | •••• •••• node-name -> 2

            name: str = self.indent_regex.sub("", line)
            generation: int = len(self.indent_regex.findall(line))
            parent: Optional["Node"] = parent_nodes.get(generation - 1, None)

            node = Node(name=name, generation=generation, parent=parent)

            parent_nodes[generation] = node

            self.nodes.append(node)

    def _validate_generation_gap(self):

        for line_number, line in enumerate(self.lines):

            if line_number == 0:
                continue

            previous_line = self.lines[line_number - 1]
            previous_generation: int = len(self.indent_regex.findall(previous_line))

            generation: int = len(self.indent_regex.findall(line))

            generation_gap = generation - previous_generation

            if generation_gap > 1:

                generation -= generation_gap - 1

                remainder: str = self.indent_regex.sub("", line, generation)

                raise TreeIndentationError(
                    line_number=line_number,
                    lines=self.lines,
                    indent=self.indent,
                    generation=generation,
                    remainder=remainder,
                )

    def _validate_indentation_consistency(self):

        for line_number, line in enumerate(self.lines):

            remainder: str = self.indent_regex.sub("", line)
            generation: int = len(self.indent_regex.findall(line))

            if remainder.startswith(self.indent_character):
                raise TreeIndentationError(
                    line_number=line_number,
                    lines=self.lines,
                    indent=self.indent,
                    generation=generation,
                    remainder=remainder,
                )


class Node:

    PREFIX_MIDDLE_PARENT = "│   "
    PREFIX_LAST_PARENT = "    "
    PREFIX_MIDDLE_CHILD = "├──"
    PREFIX_LAST_CHILD = "└──"

    def __init__(
        self,
        name: str,
        generation: int,
        parent: Optional["Node"] = None,
    ):
        self.name = name
        self.generation = generation
        self.parent = parent
        self.children = []

        if self.parent is not None:
            self.parent.children.append(self)

    def __repr__(self) -> str:
        return (
            f"{'    ' * self.generation}<{self.__class__.__name__}: "
            f"{self.generation} {self.name}>"
        )

    @property
    def is_last(self) -> bool:
        try:
            return self is self.parent.children[-1]
        except IndexError:
            return True

    def render(self) -> str:

        if self.parent is None:
            return self.name

        prefix: str = (
            self.PREFIX_LAST_CHILD if self.is_last else self.PREFIX_MIDDLE_CHILD
        )

        parts: List[str] = [
            f"{prefix} {self.name}",
        ]

        parent: Optional["Node"] = self.parent

        while parent and parent.parent is not None:

            prefix: str = (
                self.PREFIX_LAST_PARENT if parent.is_last else self.PREFIX_MIDDLE_PARENT
            )

            parts.insert(0, prefix)

            parent: Optional["Node"] = parent.parent

        return "".join(parts)
