from commander.organization import ROLE_BINDINGS, get_role_binding, operational_roles


def test_all_operating_roles_have_explicit_status_and_implementation():
    expected = {"commander", "scout", "reach", "scribe", "coder", "measurement", "publisher"}
    assert set(ROLE_BINDINGS) == expected
    for binding in ROLE_BINDINGS.values():
        assert binding["status"] in {"operational", "conditional", "blocked"}
        assert binding["implementation"]


def test_only_verified_operational_roles_are_reported_operational():
    assert operational_roles() == ("commander", "reach", "scribe", "measurement")


def test_coder_has_a_canonical_check_entrypoint():
    binding = get_role_binding("coder")
    assert binding["status"] == "conditional"
    assert binding["entrypoints"] == ("/home/yampa/projects/active/hermes/agents/coder/run.sh --check",)


def test_unknown_role_fails_closed():
    try:
        get_role_binding("unknown")
    except KeyError as exc:
        assert "Unknown Commander role" in str(exc)
    else:
        raise AssertionError("Unknown roles must fail closed")


def test_no_role_binding_uses_removed_legacy_olsp_root():
    for binding in ROLE_BINDINGS.values():
        assert "hermes/projects/profit-and-privilege" not in str(binding)
