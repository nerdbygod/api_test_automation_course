class TestPhrase:
    def test_phrase_length(self):
        phrase = str(input("Set a phrase: "))

        phrase_max_length = 15

        assert len(phrase) < phrase_max_length, f"Phrase length is {len(phrase)}, " \
                                                f"it should not be longer than {phrase_max_length}"
