import unittest

from ai_persistence.sql_builder import (
    average_latency_by_model_query,
    failed_runs_query,
    insert_message_query,
    list_messages_query,
)


class SQLBuilderTest(unittest.TestCase):
    def test_list_messages_query_is_parameterized(self):
        sql, params = list_messages_query()
        self.assertIn("where conversation_id = %s", sql)
        self.assertEqual(params, ("conversation_id",))
        self.assertIn("order by created_at asc", sql)

    def test_failed_runs_query_rejects_invalid_limit(self):
        with self.assertRaises(ValueError):
            failed_runs_query(0)
        with self.assertRaises(ValueError):
            failed_runs_query(1000)

    def test_failed_runs_query_uses_status_filter(self):
        sql, params = failed_runs_query(50)
        self.assertIn("where status = 'failed'", sql)
        self.assertEqual(params, (50,))

    def test_average_latency_query_groups_by_model(self):
        sql = average_latency_by_model_query()
        self.assertIn("avg(latency_ms)", sql)
        self.assertIn("group by model", sql)

    def test_insert_message_query_contract(self):
        sql, params = insert_message_query()
        self.assertIn("insert into messages", sql)
        self.assertEqual(params, ("conversation_id", "role", "content"))


if __name__ == "__main__":
    unittest.main()
