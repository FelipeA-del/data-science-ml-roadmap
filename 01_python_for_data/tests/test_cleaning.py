import pytest
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from scripts.cleaning import remove_duplicates, fill_missing, validate_no_nulls


# ─── Tests de remove_duplicates ───────────────────────────

def test_remove_duplicates_caso_normal():
    df = pd.DataFrame({'a': [1, 1, 2], 'b': ['x', 'x', 'y']})
    resultado = remove_duplicates(df)
    assert len(resultado) == 2


def test_remove_duplicates_sin_duplicados():
    df = pd.DataFrame({'a': [1, 2, 3]})
    resultado = remove_duplicates(df)
    assert len(resultado) == 3


def test_remove_duplicates_dataframe_vacio():
    df = pd.DataFrame()
    resultado = remove_duplicates(df)
    assert resultado.empty


# ─── Tests de fill_missing ────────────────────────────────

def test_fill_missing_con_mean():
    df = pd.DataFrame({'a': [1.0, None, 3.0]})
    resultado = fill_missing(df, strategy='mean')
    assert resultado['a'].isnull().sum() == 0


def test_fill_missing_estrategia_invalida():
    df = pd.DataFrame({'a': [1.0, None]})
    with pytest.raises(ValueError):
        fill_missing(df, strategy='invalida')


# ─── Tests de validate_no_nulls ───────────────────────────

def test_validate_no_nulls_ok():
    df = pd.DataFrame({'nombre': ['Ana', 'Luis'], 'edad': [25, 30]})
    validate_no_nulls(df, ['nombre', 'edad'])  # no debe lanzar error


def test_validate_no_nulls_con_nulos():
    df = pd.DataFrame({'nombre': ['Ana', None]})
    with pytest.raises(ValueError):
        validate_no_nulls(df, ['nombre'])


def test_validate_no_nulls_columna_inexistente():
    df = pd.DataFrame({'nombre': ['Ana']})
    with pytest.raises(KeyError):
        validate_no_nulls(df, ['columna_falsa'])