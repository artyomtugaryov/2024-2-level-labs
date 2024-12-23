"""
Checks the fourth lab's ClusteringSearchEngine class.
"""

# pylint: disable=duplicate-code
import unittest
from unittest.mock import MagicMock, patch

import pytest

from lab_4_retrieval_w_clustering.main import ClusteringSearchEngine


class ClusteringSearchEngineTest(unittest.TestCase):
    """
    Tests ClusteringSearchEngine class functionality.
    """

    def setUp(self) -> None:
        self.mock_db = MagicMock()
        self.mock_db.get_tokenizer.return_value.tokenize.return_value = ["token1", "token2"]
        self.mock_db.get_vectorizer.return_value.vectorize.return_value = (0.5, 0.5)
        self.mock_db.get_raw_documents.return_value = ["Document 1", "Document 2"]

        self.mock_kmeans = MagicMock()
        self.mock_kmeans.infer.return_value = [(0.1, 0), (0.2, 1)]
        self.mock_kmeans.calculate_square_sum.return_value = 1.0

        with patch("lab_4_retrieval_w_clustering.main.KMeans", return_value=self.mock_kmeans):
            self.engine = ClusteringSearchEngine(self.mock_db, n_clusters=2)

    @pytest.mark.lab_4_retrieval_w_clustering
    @pytest.mark.mark8
    @pytest.mark.mark10
    def test_engine_initial(self):
        """
        Test initialization of ClusteringSearchEngine instance.
        """
        self.assertIsInstance(self.engine, ClusteringSearchEngine)

    @pytest.mark.lab_4_retrieval_w_clustering
    @pytest.mark.mark8
    @pytest.mark.mark10
    def test_retrieve_relevant_documents_ideal(self):
        """
        Test retrieval of relevant documents.
        """
        query = "test query"
        n_neighbours = 2
        result = self.engine.retrieve_relevant_documents(query, n_neighbours)

        expected_result = [(0.1, "Document 1"), (0.2, "Document 2")]
        self.assertEqual(result, expected_result)

    @pytest.mark.lab_4_retrieval_w_clustering
    @pytest.mark.mark8
    @pytest.mark.mark10
    def test_retrieve_relevant_documents_empty_query(self):
        """
        Test retrieval with an empty query.
        """
        with self.assertRaises(ValueError):
            self.engine.retrieve_relevant_documents("", 2)

    @pytest.mark.lab_4_retrieval_w_clustering
    @pytest.mark.mark8
    @pytest.mark.mark10
    def test_retrieve_relevant_documents_invalid_neighbours(self):
        """
        Test retrieval with an invalid number of neighbours.
        """
        with self.assertRaises(ValueError):
            self.engine.retrieve_relevant_documents("test query", 0)

    @pytest.mark.lab_4_retrieval_w_clustering
    @pytest.mark.mark8
    @pytest.mark.mark10
    def test_retrieve_relevant_documents_tokenizer_returns_none(self):
        """
        Test retrieval when tokenizer returns None.
        """
        self.mock_db.get_tokenizer.return_value.tokenize.return_value = None
        with self.assertRaises(ValueError):
            self.engine.retrieve_relevant_documents("test query", 2)

    @pytest.mark.lab_4_retrieval_w_clustering
    @pytest.mark.mark8
    @pytest.mark.mark10
    def test_retrieve_relevant_documents_vectorizer_returns_none(self):
        """
        Test retrieval when vectorizer returns None.
        """
        self.mock_db.get_vectorizer.return_value.vectorize.return_value = None
        with self.assertRaises(ValueError):
            self.engine.retrieve_relevant_documents("test query", 2)

    @pytest.mark.lab_4_retrieval_w_clustering
    @pytest.mark.mark8
    @pytest.mark.mark10
    def test_retrieve_relevant_documents_infer_returns_none(self):
        """
        Test retrieval when infer returns None.
        """
        self.mock_kmeans.infer.return_value = None
        with self.assertRaises(ValueError):
            self.engine.retrieve_relevant_documents("test query", 2)

    @pytest.mark.lab_4_retrieval_w_clustering
    @pytest.mark.mark10
    def test_calculate_square_sum_ideal(self):
        """
        Test calculation of the square sum of distances.
        """
        square_sum = self.engine.calculate_square_sum()
        self.assertEqual(square_sum, 1.0)
