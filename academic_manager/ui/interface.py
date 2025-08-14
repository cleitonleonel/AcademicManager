from typing import List, Optional


class UserInterface:
    """
    Provides methods for user interaction through input prompts and selection interfaces.

    This class contains static utility methods to handle user input, including providing default values,
    allowing selection from a list, and validating user choices against predefined options. These methods
    are well-suited for building command-line interfaces or simple text-based user interactions.
    """

    @staticmethod
    def input_with_default(prompt: str, default: str) -> str:
        """
        Prompts the user for input with a default value. If the user provides input, their input is returned;
        otherwise, the default value is returned.

        :param prompt: The message is displayed to the user for input.
        :type prompt: str
        :param default: The default value to return if the user provides no input.
        :type default: str
        :return: The user's input if provided, otherwise the default value.
        :rtype: str
        """
        user_input = input(f"{prompt} {default}: ").strip()
        return user_input if user_input else default

    @staticmethod
    def select_from_list(items: List[str], prompt: str) -> Optional[str]:
        """
        This method allows a user to select an item from a list of strings by providing a numbered
        list and asking for their choice. If no items are provided in the list, it displays a
        message indicating no items are available. If the user enters an invalid option, it
        displays an error message and returns None.

        :param items: A list of strings representing the options to choose from
        :type items: List[str]
        :param prompt: A prompt message displayed to the user to guide their selection
        :type prompt: str
        :return: The selected string from the list, or None if no valid selection is made
        :rtype: Optional[str]
        """
        if not items:
            print("Nenhum item disponível.")
            return None

        print(f"\n{prompt}:")
        for idx, item in enumerate(items, 1):
            print(f"{idx}: {item}")

        try:
            choice = int(input(f"\nEscolha uma opção (1-{len(items)}): ").strip())
            if 1 <= choice <= len(items):
                return items[choice - 1]
        except ValueError:
            pass

        print("Opção inválida.")
        return None

    @staticmethod
    def get_user_choice(prompt: str, valid_choices: List[str]) -> Optional[str]:
        """
        Prompts the user with a message and asks to provide a choice from valid options. The user can quit by
        providing a specific quit command. Validates the input and returns the choice if it matches one of the
        valid options or the quit command. Otherwise, it informs about the incorrect choice.

        :param prompt: The message to be displayed prompting the user for input.
        :type prompt: str
        :param valid_choices: A list of valid strings that the user can choose from.
        :type valid_choices: List[str]
        :return: The user's choice if it's valid or matches the quit command ("q"). Returns None if invalid
                 input is entered.
        :rtype: Optional[str]
        """
        choice = input(f"{prompt} ({'/'.join(valid_choices)}, q para sair): ").strip().lower()

        if choice == 'q':
            return 'q'

        if choice in valid_choices:
            return choice

        print("Opção inválida.")
        return None