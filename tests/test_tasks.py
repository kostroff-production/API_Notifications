import pytest
from app import tasks


class TestTasks:

    @pytest.mark.django_db(transaction=True)
    def test_schedule_send(self, celery_worker, setUP):
        result = tasks.schedule_send.delay()
        assert result.get() == None
        assert result.successful()

    @pytest.mark.django_db(transaction=True)
    def test_send_message(self, celery_worker, setUP):
        result = tasks.send_message.apply_async((setUP[0].id,), countdown=2)
        assert result.get() == None
        assert result.successful()

    @pytest.mark.django_db(transaction=True)
    def test_post_message(self, celery_worker, setUP):
        json = {
            "id": setUP[2].id,
            "phone": setUP[1].phone,
            "text": setUP[0].message
        }
        result = tasks.post_message.apply_async((json,), countdown=4)
        assert result.get() == None
        assert result.successful()

    @pytest.mark.django_db(transaction=True)
    def test_send_statistic(self, celery_worker, setUP):
        result = tasks.send_statistic.delay()
        assert result.get() == None
        assert result.successful()








