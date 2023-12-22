from django.test import SimpleTestCase
from django.urls import resolve, reverse
from ..views import *
import inspect
from ..urls import urlpatterns, urls_add, urls_student_overview, urls_view

total_urls = len(urlpatterns) + len(urls_add) + len(urls_student_overview) + len(urls_view) - 3

class TestUrls(SimpleTestCase):
  def test_admin_panel_url(self):
    url = reverse('admin-panel-page') # url name
    # func: function based view
    # func.view_class: class based view
    self.assertEquals(resolve(url).func, custom_admin)

  def test_add_subject_url(self):
    url = reverse('add-subject-page')
    self.assertEquals(resolve(url).func, add_subject_view)

  def test_add_quiz_url(self):
    url = reverse('add-quiz-page')
    self.assertEquals(resolve(url).func, add_quiz_view)

  def test_add_question_url(self):
    url = reverse('add-question&answer-page')
    self.assertEquals(resolve(url).func, add_question_view)

  def test_add_answer_url(self):
    url = reverse('add-answer-page')
    self.assertEquals(resolve(url).func, add_answer_view)

  def test_view_subjects_url(self):
    url = reverse('view-subjects-page')
    self.assertEquals(resolve(url).func, display_subjects_view)

  def test_modify_subjects_url(self):
    url = reverse('modify-subject-page')
    self.assertEquals(resolve(url).func, modify_subject_view)

  def test_view_quizes_url(self):
    url = reverse('view-quizes-page')
    self.assertEquals(resolve(url).func, display_quizes_view)

  def test_modify_quiz_url(self):
    url = reverse('modify-quiz-page')
    self.assertEquals(resolve(url).func, modify_quiz_view)

  def test_view_questions_url(self):
    url = reverse('view-questions-page')
    self.assertEquals(resolve(url).func, display_questions_view)

  def test_view_allquestions_url(self):
    url = reverse('view-Allquestions-page')
    self.assertEquals(resolve(url).func, display_Allquestions_view)

  def test_modify_question_url(self):
    url = reverse('modify-question-page')
    self.assertEquals(resolve(url).func, modify_question_view)

  def test_student_overview_url(self):
    url = reverse('students-page')
    self.assertEquals(resolve(url).func, students_view)

lenTestUrls = len(inspect.getmembers(TestUrls, inspect.ismethod))
print("Total number of URL test performed: ", lenTestUrls)
print("Total number of URL present: ", total_urls)
