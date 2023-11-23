import spacy
from spacy.matcher import Matcher

from src.logger import Logger

class SubstanceSizeExtractor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.matcher = Matcher(self.nlp.vocab)
        # Define the patterns for matching substance sizes and characteristics
        self.size_pattern = [{"LIKE_NUM": True}, {"LOWER": "nm"}]
        # Register patterns with matcher
        self.matcher.add("SIZE", [self.size_pattern])

    def extract_sizes(self, text):
        sizes = []
        doc = self.nlp(text)
        matches = self.matcher(doc)
        for match_id, start, end in matches:
            rule_id = self.nlp.vocab.strings[match_id]
            if rule_id == "SIZE":
                size = doc[start:end].text
                sizes.append(size)
        return sizes


if __name__ == "__main__":
    extractor = SubstanceSizeExtractor()

    text_examples = [
        "The synthesis of 4 nm CoFe2O4 nanoparticles is described in the article...",
        "For the synthesis of 15 nm CoFe2O4 nanoparticles, 8 mmol of Fe(acac)3...",
        "To synthesize near corner-grown cubic NPs with a size of 24.5 nm, 2 mmol...",
        "For the synthesis of near cubic NPs with a size of 45.2 nm, 4 mmol...",
        "The starlike NPs with a size of 35 nm are synthesized..."
    ]

    for example in text_examples:
        sizes = extractor.extract_sizes(example)
        if sizes:
            Logger.info(f"Substance sizes in '{example}': {', '.join(sizes)}")
