import unittest
from unittest.mock import patch, MagicMock
from app.routers.products import update_prices_manual
from app.routers.admin import update_all_prices_manual
import asyncio

class TestManualUpdateSync(unittest.TestCase):

    @patch('app.routers.products.update_prices')
    @patch('app.routers.products.update_price_drops_report')
    @patch('app.routers.products.get_users_collection')
    def test_products_update_prices_manual_triggers_report(self, mock_get_users, mock_update_report, mock_update_prices):
        # Mocking dependencies
        mock_current_user = "testuser"
        mock_users_coll = MagicMock()
        mock_get_users.return_value = mock_users_coll
        
        # Calling the function (it's async, so we need to run it)
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(update_prices_manual(current_user=mock_current_user, users_collection=mock_users_coll))
        
        # Assertions
        mock_update_prices.assert_called_once_with(mock_users_coll, user_filter=mock_current_user)
        mock_update_report.assert_called_once()
        self.assertEqual(result["message"], "Price update triggered manually and report updated")

    @patch('app.routers.admin.update_prices')
    @patch('app.routers.admin.update_price_drops_report')
    @patch('app.routers.admin.get_users_collection')
    def test_admin_update_all_prices_manual_triggers_report(self, mock_get_users, mock_update_report, mock_update_prices):
        # Mocking dependencies
        mock_users_coll = MagicMock()
        mock_get_users.return_value = mock_users_coll
        
        # Calling the function
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(update_all_prices_manual(users_collection=mock_users_coll))
        
        # Assertions
        mock_update_prices.assert_called_once_with(mock_users_coll, user_filter=None)
        mock_update_report.assert_called_once()
        self.assertEqual(result["message"], "Manual price update for all products completed and report updated")

if __name__ == '__main__':
    unittest.main()
