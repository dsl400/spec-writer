import importlib.machinery
import importlib.util
import unittest
from pathlib import Path

HERE = Path(__file__).parent
_loader = importlib.machinery.SourceFileLoader("ste_check", str(HERE / "ste-check"))
_spec = importlib.util.spec_from_loader("ste_check", _loader)
ste = importlib.util.module_from_spec(_spec)
_loader.exec_module(ste)

VOCAB = ste.load_wordset(None)
VOCAB["project"] = {"dialog"}


def vocab_findings(text):
    return [f for f in ste.Checker("t.md", text, VOCAB).run() if f["rule"] == "1.6"]


def flagged(text):
    return [text[f["col"] - 1:].split()[0].strip(".,") for f in vocab_findings(text)]


class Vocabulary(unittest.TestCase):
    def test_inflected_unapproved_word(self):
        self.assertEqual(flagged("The user clicks the item."), ["clicks"])

    def test_word_absent_from_the_dictionary(self):
        self.assertEqual(flagged("The user sees the flurbix."), ["flurbix"])

    def test_project_term(self):
        self.assertEqual(flagged("The system opens the dialog."), [])

    def test_inflected_approved_words(self):
        for text in ("The system removed the user.",
                     "The user typed the name.",
                     "The system has a table.",
                     "The system does this.",
                     "The system made a copy.",
                     "The user is known.",
                     "The user stopped the system.",
                     "The system is removing the user."):
            with self.subTest(text=text):
                self.assertEqual(flagged(text), [])

    def test_verb_after_an_adverb(self):
        self.assertEqual(flagged("The system also closes the dialog."), [])

    def test_number_words(self):
        self.assertEqual(flagged("The system shows two tables."), [])

    def test_identifier_with_digits(self):
        self.assertEqual(flagged("See item R12."), [])

    def test_unapproved_word_keeps_its_alternative(self):
        [f] = vocab_findings("The user deletes the item.")
        self.assertIn("Approved alternative", f["message"])

    def test_unknown_word_names_the_terms_file(self):
        [f] = vocab_findings("The user sees the flurbix.")
        self.assertIn(ste.PROJECT_TERMS, f["message"])


if __name__ == "__main__":
    unittest.main()
