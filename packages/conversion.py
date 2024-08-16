CONVERSION_DICT = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

def convert_rating(value: str) -> int:
    """Conversion de la note d'un produit en donnée numérique

    Args:
        texte (string): Texte de 1 à 5 (One, Two, Three, Four, Five)

    Returns:
        Int: Retourne une version numérique de la note
    """
    return CONVERSION_DICT[value]