import csv

from aquizz import models


def load_data_from_file(filename):
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
        for row in csv_reader:
            text = row[0].strip()
            question = models.Question.objects(text=text).first()
            if question is None:
                question = models.Question(text=text)
            option = row[1].strip()
            options = [x.value for x in question.options]
            if option not in options:
                question.options.append(models.Option(value=row[1], is_correct=True))
            question.save()
