import os
import json
import pdb
import re

import rich
from icecream import ic
from rich.console import Console


class PyQuest:
    def __init__(self, config, parent=False):
        """
            Create a loop that reads in JSON or a file
        """

        # Differentiate between passed JSON and a file containing JSON
        if isinstance(config, str) and os.path.exists(config):
            with open(config, "r") as f:
                try:
                    self.config = json.load(f)
                except json.JSONDecodeError as exc:
                    print(exc)
        else:
            self.config = config

        self.__validate_config()

        self.parent = parent
        self.console = Console()

    def __validate_config(self):
        if str(self.config).find('-1') != -1:
            self.__print_warning__('-1 is a reserved parameter please validate your config.')
            exit()

    def start(self, position=0):
        """
            Start the loop at the position of which correlates to the order at which the questions appear in the
            configuration file/data.
        """

        for question in self.config[position:]:
            answer = self.__ask__(question)
            question["answer"] = answer

        return self.config

    def __ask__(self, question):
        self.__print_question__(question['question'])
        answer = -1

        while answer == -1:
            if question.get("sub-questions"):
                sub_answer_index = self.__ordered_answer__(question['answers'])
                if sub_answer_index > -1:
                    # Recursively ask sub-questions and store the answer
                    sub_question = question['sub-questions'][sub_answer_index]
                    sub_answer = self.__ask__(sub_question)
                    # Ensure that the sub-answer is correctly stored in the sub-question
                    sub_question["answer"] = sub_answer
                    # Return the answer index of the chosen sub-question
                answer = sub_answer_index
            elif isinstance(question['answers'], list):
                answer = self.__unordered_answer__(question['answers'])
            elif isinstance(question['answers'], dict):
                if question['answers'].get("regex_validation"):
                    answer = self.__regex_answer__(question['answers'])
                elif question['answers'].get("math_validation"):
                    answer = self.__mathematics_answer__(question['answers'])
        return answer

    def __mathematics_answer__(self, answers):
        """
            Utilizes the Eval function to calculate whether an answer fits. Math answers can only be digits no eqastions
            :param answers:
            :return:
        """
        answer = 1
        digitString = "\\d+"
        answer = self.__answer__(digitString)

        while not eval(answers['math_validation'].replace('<answer>', answer)):
            self.__print_warning__(
                answers['error'] if answers.get("error") else "Answer does not match mathematical validation."
            )
            answer = self.__answer__(digitString)
        return answer

    def __regex_answer__(self, answers):

        return self.__answer__(
            regex=answers["regex_validation"],
            error=answers['error'] if answers.get("error") else "Answer does not match regex validation."
        )

    def __unordered_answer__(self, answers):

        for index, answer in enumerate(answers):
            self.__print_answer__(answer, index)

        if self.parent:
            self.__print_answer__("<-- Back", len(answers))
            answer = int(self.__answer__(len(answers) + 1))
        else:
            answer = int(self.__answer__(len(answers)))

        if answer == len(answers):
            return -1
        else:
            return answer

    def __ordered_answer__(self, answers):
        """
            Ordered answers are stored within the answers list of tuples
            Returns the value of the answered number
        """

        for index, answer in enumerate(answers):
            self.__print_answer__(answer['answer'], index)

        if self.parent:
            self.__print_answer__("<-- Back", len(answers))
            answer = int(self.__answer__(len(answers) + 1))
        else:
            answer = int(self.__answer__(len(answers)))

        # Handles going back
        if answer == len(answers):
            return -1
        else:
            return answers[answer]['value']

    def __answer__(self, regex, error="Answer does not match expected answer."):
        """
            Handles receiving the answer, validating it, and returning it back.
            Validation is split between general regex, and standard 0-x answers
        """
        answer = None
        if isinstance(regex, str):
            pattern = re.compile(regex)
            answered = False
            while not answered:
                answer = self.__print_answer_prompt__()
                if pattern.match(answer) and len(answer) > 0:
                    answered = True
                else:
                    self.__print_warning__(error)
        else:
            answer = int(self.__answer__("\\d+"))
            while not (0 <= answer < regex):
                self.__print_warning__(error)
                answer = int(self.__answer__("\\d+"))

        return answer

    def __print_answer_prompt__(self):

        return self.console.input("[bold green]Answer > ")

    @staticmethod
    def __print_question__(question):
        rich.print(f"[bold red][Q][/bold red] {question}")

    @staticmethod
    def __print_warning__(warning):
        rich.print(f"[bold yellow][!][/bold yellow] {warning}")

    @staticmethod
    def __print_answer__(answer, order):
        rich.print(f"[bold green][A].[{order}][/bold green]\t {answer}")


if __name__ == "__main__":
    quest = PyQuest("/Users/carterloyd/PycharmProjects/PyQuest/tester.json")
    answers = quest.start()

    print(answers)
