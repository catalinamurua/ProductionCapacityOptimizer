from optimizador.services.results_handler import ResultsHandler

def test_format_results_returns_expected_keys():
    mock_solution = {
        "Product_A_units": 10,
        "Product_B_units": 5,
        "Total_Revenue": 175.0
    }

    formatted = ResultsHandler.format_results(mock_solution)

    assert "summary" in formatted
    assert "total_revenue" in formatted
    assert "graph_path" in formatted
