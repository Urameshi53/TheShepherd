import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.views import generic

from .models import Discussion

class DiscussionModelTests(TestCase):
    def test_was_published_recently_with_future_discussion(self):
        """
        was_published_recently() returns False for discussions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_discussion = Discussion(pub_date=time)
        self.assertIs(future_discussion.was_published_recently(), False)

def test_was_published_recently_with_old_discussion(self):
    """
    was_published_recently() returns False for discussions whose pub_date
    is older than 1 day.
    """
    time = timezone.now() - datetime.timedelta(days=1, seconds=1)
    old_discussion = Discussion(pub_date=time)
    self.assertIs(old_discussion.was_published_recently(), False)


def test_was_published_recently_with_recent_discussion(self):
    """
    was_published_recently() returns True for discussions whose pub_date
    is within the last day.
    """
    time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
    recent_discussion = Discussion(pub_date=time)
    self.assertIs(recent_discussion.was_published_recently(), True)


def create_discussion(discussion_text, days):
    """
    Create a discussion with the given `discussion_text` and published the
    given number of `days` offset to now (negative for discussions published
    in the past, positive for discussions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Discussion.objects.create(discussion_text=discussion_text, pub_date=time)


class discussionIndexViewTests(TestCase):
    def test_no_discussions(self):
        """
        If no discussions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_discussion_list"], [])

    def test_past_discussion(self):
        """
        discussions with a pub_date in the past are displayed on the
        index page.
        """
        discussion = create_discussion(discussion_text="Past discussion.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_discussion_list"],
            [discussion],
        )

    def test_future_discussion(self):
        """
        discussions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_discussion(discussion_text="Future discussion.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_discussion_list"], [])

    def test_future_discussion_and_past_discussion(self):
        """
        Even if both past and future discussions exist, only past discussions
        are displayed.
        """
        discussion = create_discussion(discussion_text="Past discussion.", days=-30)
        create_discussion(discussion_text="Future discussion.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_discussion_list"],
            [discussion],
        )

    def test_two_past_discussions(self):
        """
        The discussions index page may display multiple discussions.
        """
        discussion1 = create_discussion(discussion_text="Past discussion 1.", days=-30)
        discussion2 = create_discussion(discussion_text="Past discussion 2.", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_discussion_list"],
            [discussion2, discussion1],
        )

class DetailView(generic.DetailView):
    ...

    def get_queryset(self):
        """
        Excludes any discussions that aren't published yet.
        """
        return Discussion.objects.filter(pub_date__lte=timezone.now())

class discussionDetailViewTests(TestCase):
    def test_future_discussion(self):
        """
        The detail view of a discussion with a pub_date in the future
        returns a 404 not found.
        """
        future_discussion = create_discussion(discussion_text="Future discussion.", days=5)
        url = reverse("polls:detail", args=(future_discussion.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_discussion(self):
        """
        The detail view of a discussion with a pub_date in the past
        displays the discussion's text.
        """
        past_discussion = create_discussion(discussion_text="Past discussion.", days=-5)
        url = reverse("polls:detail", args=(past_discussion.id,))
        response = self.client.get(url)
        self.assertContains(response, past_discussion.discussion_text)