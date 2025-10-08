import pytest
from presidio_anonymizer.entities.engine.recognizer_result import RecognizerResult
from presidio_anonymizer.entities.engine.recognizer_result import create_recognizer_result


def test_given_recognizer_results_then_one_contains_another():
    first = create_recognizer_result("entity", 0.0, 0, 10)
    second = create_recognizer_result("entity", 0.0, 2, 8)
    assert first.contains(second)


def test_given_recognizer_results_then_they_do_not_contain_each_other():
    first = create_recognizer_result("entity", 0.0, 0, 10)
    second = create_recognizer_result("entity", 0.0, 4, 10)
    assert not first.contains(second)


def test_given_recognizer_results_then_they_intersect():
    first = create_recognizer_result("entity", 0.0, 0, 11)
    second = create_recognizer_result("entity", 0.0, 5, 12)
    assert first.intersects(second) == 6


def test_given_recognizer_results_then_they_do_not_intersect():
    first = create_recognizer_result("entity", 0.0, 0, 5)
    second = create_recognizer_result("entity", 0.0, 5, 10)
    assert first.intersects(second) == 0


def test_given_recognizer_result_then_equality_and_repr_work():
    r1 = create_recognizer_result("entity", 0.8, 0, 10)
    r2 = create_recognizer_result("entity", 0.8, 0, 10)
    r3 = create_recognizer_result("different", 0.9, 2, 8)

    assert r1 == r2
    assert r1 != r3
    assert "entity" in repr(r1)


# -------------------------------
# Task 1: Verify that RecognizerResult logs correctly
# -------------------------------

def test_logger(mocker):
    # Patch the logger used inside recognizer_result.py
    mock_logger = mocker.patch(
        "presidio_anonymizer.entities.engine.recognizer_result.logger"
    )

    # Create a recognizer result with example values
    entity_type = "PERSON"
    start = 5
    end = 15
    score = 0.85

    create_recognizer_result(entity_type, score, start, end)

    # Check that logger.info was called
    mock_logger.info.assert_called()

    # Grab the actual log message
    log_msg = mock_logger.info.call_args[0][0]

    # Make sure all parts appear in the log
    assert entity_type in log_msg
    assert str(start) in log_msg
    assert str(end) in log_msg
    assert f"{score:.2f}" in log_msg
