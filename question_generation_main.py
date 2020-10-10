'''This module ties together the
questions generation and incorrect answer
generation modules
'''
from question_extraction import QuestionExtractor
from incorrect_answer_generation import IncorrectAnswerGenerator

class QuestionGeneration:
	'''This class contains the method
	to generate questions
	'''

	def __init__(self, num_questions, num_options):
		self.num_questions = num_questions
		self.num_options = num_options
		self.question_extractor = QuestionExtractor(num_questions)

	def generate_questions_dict(self, document):
		self.questions_dict = self.question_extractor.get_questions_dict(document)
		self.incorrect_answer_generator = IncorrectAnswerGenerator(document)

		for i in range(1, self.num_questions+1):
			if i not in self.questions_dict:
				continue
			self.questions_dict[i]["options"] \
				= self.incorrect_answer_generator.get_all_options_dict(
						self.questions_dict[i]["answer"],
						self.num_options
						)

		return self.questions_dict
