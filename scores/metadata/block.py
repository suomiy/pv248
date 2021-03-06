from data.edition import Edition
from data.edition_author import EditionAuthor
from data.person import Person
from data.print_cls import Print
from data.score import Score
from data.score_author import ScoreAuthor
from data.voice import Voice


class Block:
    def __init__(self, conn):
        if not conn:
            raise Exception('needs connection to initialize')
        self.conn = conn

        self.score = Score(conn)
        self.partiture = Print(conn)
        self.edition = Edition(conn)
        self.composers = []
        self.editors = []
        self.voices = []

    def add_composer(self, name, born, died):
        self.composers.append(Person(self.conn, name=name, born=born, died=died))

    def add_editor(self, name, born, died):
        self.editors.append(Person(self.conn, name=name, born=born, died=died))

    def add_voice(self, score, name, number):
        self.voices.append(Voice(self.conn, score=score, number=number, name=name))

    def clear(self):
        self.score = Score(self.conn)
        self.partiture = Print(self.conn)
        self.edition = Edition(self.conn)
        self.composers.clear()
        self.editors.clear()
        self.voices.clear()

    def store(self):
        score = self.score
        conn = self.conn

        score.store()

        for composer in self.composers:
            composer.store()
            ScoreAuthor(conn, score=score, composer=composer).store()

        for voice in self.voices:
            voice.score_id = score.id
            voice.store()

        self.edition.score_id = score.id
        self.edition.store()

        for editor in self.editors:
            editor.store()
            EditionAuthor(conn, edition=self.edition, editor=editor).store()

        self.partiture.edition_id = self.edition.id
        self.partiture.store()
