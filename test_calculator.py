import pytest
from calculator import add, sub, mul, div

def test_add():
	assert add(2,3) == 5
def test_sub():
	assert sub(7,5) == 2
def test_mul():
	assert mul(3,5) == 15
def test_div():
	assert div(4,2) == 2
	with pytest.raises(ValueError):
	 div(10,0)
