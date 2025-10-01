def validate_contract_format(output: str) -> bool:
    required = ["# Título", "## Partes", "## Obrigações", "## Assinaturas"]
    return all(r in output for r in required)

def test_contract_has_required_sections():
    sample = (
        "# Título\n"
        "## Partes\n"
        "## Obrigações\n"
        "## Assinaturas\n"
    )
    assert validate_contract_format(sample)
