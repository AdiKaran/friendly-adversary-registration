from database.models import Adversary


def test_adversary_model(session):
    adversary = Adversary(
        name="adversary_name",
        ip_address="168.212. 226.204",
        email="email@website.domain",
        planned_activity={"foo": "bar", "bar": "baz"},
    )
    session.add(adversary)
    session.commit()

    assert adversary.name == "adversary_name"
    assert adversary.ip_address == "168.212. 226.204"
    assert adversary.email == "email@website.domain"
    assert adversary.planned_activity == {"foo": "bar", "bar": "baz"}


def test_adversary_model_required_parameters(session):
    adversary = Adversary(name="adversary_name", ip_address="168.212. 226.204")
    session.add(adversary)
    session.commit()

    assert adversary.name == "adversary_name"
    assert adversary.ip_address == "168.212. 226.204"
    assert adversary.email is None
    assert adversary.planned_activity is None
