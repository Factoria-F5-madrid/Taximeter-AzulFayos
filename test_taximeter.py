import unittest
from unittest.mock import patch, mock_open
from taximeter import Taximeter

class TestTaximeter(unittest.TestCase):

  def setUp(self):
    self.taxi = Taximeter(stop_price=2, moving_price=5)

  @patch("builtins.input", side_effect=["s"])
  def test_confirm_yes(self, mock_input):
    self.assertTrue(self.taxi.confirm("¿Confirmar?"))

  @patch("builtins.input", side_effect=["n"])
  def test_confirm_no(self, mock_input):
    self.assertFalse(self.taxi.confirm("¿Confirmar?"))

  @patch("builtins.input", side_effect=["abc", "-1", "3"])
  def test_change_price_invalid_then_valid(self, mock_input):
    result = self.taxi.change_price()
    self.assertEqual(result, 3)

  @patch("builtins.input", side_effect=["1", "10", "n"])
  def test_ask_prices_change_stop_price(self, mock_input):
    self.taxi.ask_prices()
    self.assertEqual(self.taxi.stop_price, 10)

  @patch("builtins.input", side_effect=["2", "20", "n"])
  def test_ask_prices_change_moving_price(self, mock_input):
    self.taxi.ask_prices()
    self.assertEqual(self.taxi.moving_price, 20)

  @patch("builtins.input", side_effect=["0"])
  def test_ask_prices_cancel(self, mock_input):
    original_stop = self.taxi.stop_price
    original_moving = self.taxi.moving_price
    self.taxi.ask_prices()
    self.assertEqual(self.taxi.stop_price, original_stop)
    self.assertEqual(self.taxi.moving_price, original_moving)

  @patch("os.rename")
  def test_log_on_end_renames_log(self, mock_rename):
    self.taxi.log_on_end()
    mock_rename.assert_called_once()

  @patch("builtins.input", return_value="n")
  @patch("taximeter.Taximeter.log_on_end")
  @patch("builtins.open", new_callable=mock_open)
  def test_on_end_calculation_and_log(self, mock_file, mock_log_on_end, mock_input):
    with self.assertRaises(SystemExit):
      self.taxi.on_end(subtrac=1)

    mock_file.assert_called_with(self.taxi.BASE_DIR + "\\txt_log.txt", "a", encoding='utf-8')
    
    total = ((self.taxi.moving_count * self.taxi.moving_price) + (self.taxi.stop_count * self.taxi.stop_price)) / 100
    total = round(total, 2)

  @patch("taximeter.quit")
  @patch("builtins.input", return_value="n")
  @patch("builtins.open", new_callable=mock_open)
  def test_on_end_subtract_time(self, mock_file, mock_input, mock_quit):
    subtrac_value = 2
    self.taxi.moving_count = 10
    self.taxi.stop_count = 10

    self.taxi.on_end(subtrac=subtrac_value)

    self.assertEqual(self.taxi.moving_count, 8)
    self.assertEqual(self.taxi.stop_count, 8)
    mock_file().write.assert_called()
    mock_quit.assert_called()

if __name__ == '__main__':
  unittest.main()
