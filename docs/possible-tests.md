# Test Catalogue 🧪
This documentation is intended as an exaustive list of possible tests within Wimsey. Note that examples given intentionally use all possible keywords for demonstrative purposes. This isn't required, and you can give as many or as few keywords as you like with the exception of where `column` is required.
## mean_should

Test that column mean is within designated range

=== "yaml"
    ```yaml
    be_exactly: 300
    be_greater_than: 500
    be_greater_than_or_equal_to: 500
    be_less_than: 500
    be_less_than_or_equal_to: 300
    column: column_a
    test: mean_should

    ```
=== "json"
    ```json
    {
      "test": "mean_should",
      "column": "column_a",
      "be_exactly": 300,
      "be_less_than": 500,
      "be_less_than_or_equal_to": 300,
      "be_greater_than": 500,
      "be_greater_than_or_equal_to": 500
    }
    ```
=== "python"
    ```python

    from wimsey import test
    from wimsey.tests import mean_should

    keywords = {
      "column": "column_a",
      "be_exactly": 300,
      "be_less_than": 500,
      "be_less_than_or_equal_to": 300,
      "be_greater_than": 500,
      "be_greater_than_or_equal_to": 500
    }

    result = test(df, contract=[mean_should(**keywords)])
    
    ```

<hr>
    
## min_should

Test that column min is within designated range

=== "yaml"
    ```yaml
    be_exactly: 300
    be_greater_than: 500
    be_greater_than_or_equal_to: 500
    be_less_than: 500
    be_less_than_or_equal_to: 300
    column: column_a
    test: min_should

    ```
=== "json"
    ```json
    {
      "test": "min_should",
      "column": "column_a",
      "be_exactly": 300,
      "be_less_than": 500,
      "be_less_than_or_equal_to": 300,
      "be_greater_than": 500,
      "be_greater_than_or_equal_to": 500
    }
    ```
=== "python"
    ```python

    from wimsey import test
    from wimsey.tests import min_should

    keywords = {
      "column": "column_a",
      "be_exactly": 300,
      "be_less_than": 500,
      "be_less_than_or_equal_to": 300,
      "be_greater_than": 500,
      "be_greater_than_or_equal_to": 500
    }

    result = test(df, contract=[min_should(**keywords)])
    
    ```

<hr>
    
## max_should

Test that column max is within designated range

=== "yaml"
    ```yaml
    be_exactly: 300
    be_greater_than: 500
    be_greater_than_or_equal_to: 500
    be_less_than: 500
    be_less_than_or_equal_to: 300
    column: column_a
    test: max_should

    ```
=== "json"
    ```json
    {
      "test": "max_should",
      "column": "column_a",
      "be_exactly": 300,
      "be_less_than": 500,
      "be_less_than_or_equal_to": 300,
      "be_greater_than": 500,
      "be_greater_than_or_equal_to": 500
    }
    ```
=== "python"
    ```python

    from wimsey import test
    from wimsey.tests import max_should

    keywords = {
      "column": "column_a",
      "be_exactly": 300,
      "be_less_than": 500,
      "be_less_than_or_equal_to": 300,
      "be_greater_than": 500,
      "be_greater_than_or_equal_to": 500
    }

    result = test(df, contract=[max_should(**keywords)])
    
    ```

<hr>
    
## std_should

Test that column std is within designated range

=== "yaml"
    ```yaml
    be_exactly: 300
    be_greater_than: 500
    be_greater_than_or_equal_to: 500
    be_less_than: 500
    be_less_than_or_equal_to: 300
    column: column_a
    test: std_should

    ```
=== "json"
    ```json
    {
      "test": "std_should",
      "column": "column_a",
      "be_exactly": 300,
      "be_less_than": 500,
      "be_less_than_or_equal_to": 300,
      "be_greater_than": 500,
      "be_greater_than_or_equal_to": 500
    }
    ```
=== "python"
    ```python

    from wimsey import test
    from wimsey.tests import std_should

    keywords = {
      "column": "column_a",
      "be_exactly": 300,
      "be_less_than": 500,
      "be_less_than_or_equal_to": 300,
      "be_greater_than": 500,
      "be_greater_than_or_equal_to": 500
    }

    result = test(df, contract=[std_should(**keywords)])
    
    ```

<hr>
    
## null_count_should

Test that column null_count is within designated range

=== "yaml"
    ```yaml
    be_exactly: 300
    be_greater_than: 500
    be_greater_than_or_equal_to: 500
    be_less_than: 500
    be_less_than_or_equal_to: 300
    column: column_a
    test: null_count_should

    ```
=== "json"
    ```json
    {
      "test": "null_count_should",
      "column": "column_a",
      "be_exactly": 300,
      "be_less_than": 500,
      "be_less_than_or_equal_to": 300,
      "be_greater_than": 500,
      "be_greater_than_or_equal_to": 500
    }
    ```
=== "python"
    ```python

    from wimsey import test
    from wimsey.tests import null_count_should

    keywords = {
      "column": "column_a",
      "be_exactly": 300,
      "be_less_than": 500,
      "be_less_than_or_equal_to": 300,
      "be_greater_than": 500,
      "be_greater_than_or_equal_to": 500
    }

    result = test(df, contract=[null_count_should(**keywords)])
    
    ```

<hr>
    
## count_should

Test that column count is within designated range

=== "yaml"
    ```yaml
    be_exactly: 300
    be_greater_than: 500
    be_greater_than_or_equal_to: 500
    be_less_than: 500
    be_less_than_or_equal_to: 300
    column: column_a
    test: count_should

    ```
=== "json"
    ```json
    {
      "test": "count_should",
      "column": "column_a",
      "be_exactly": 300,
      "be_less_than": 500,
      "be_less_than_or_equal_to": 300,
      "be_greater_than": 500,
      "be_greater_than_or_equal_to": 500
    }
    ```
=== "python"
    ```python

    from wimsey import test
    from wimsey.tests import count_should

    keywords = {
      "column": "column_a",
      "be_exactly": 300,
      "be_less_than": 500,
      "be_less_than_or_equal_to": 300,
      "be_greater_than": 500,
      "be_greater_than_or_equal_to": 500
    }

    result = test(df, contract=[count_should(**keywords)])
    
    ```

<hr>
    
## null_percentage_should

Test that column null_percentage is within designated range

=== "yaml"
    ```yaml
    be_exactly: 300
    be_greater_than: 500
    be_greater_than_or_equal_to: 500
    be_less_than: 500
    be_less_than_or_equal_to: 300
    column: column_a
    test: null_percentage_should

    ```
=== "json"
    ```json
    {
      "test": "null_percentage_should",
      "column": "column_a",
      "be_exactly": 300,
      "be_less_than": 500,
      "be_less_than_or_equal_to": 300,
      "be_greater_than": 500,
      "be_greater_than_or_equal_to": 500
    }
    ```
=== "python"
    ```python

    from wimsey import test
    from wimsey.tests import null_percentage_should

    keywords = {
      "column": "column_a",
      "be_exactly": 300,
      "be_less_than": 500,
      "be_less_than_or_equal_to": 300,
      "be_greater_than": 500,
      "be_greater_than_or_equal_to": 500
    }

    result = test(df, contract=[null_percentage_should(**keywords)])
    
    ```

<hr>
    
## columns_should

Test column names match up with expected values

=== "yaml"
    ```yaml
    be:
    - column_a
    - column_b
    have:
    - column_a
    not_have:
    - column_c
    test: columns_should

    ```
=== "json"
    ```json
    {
      "test": "columns_should",
      "have": [
        "column_a"
      ],
      "not_have": [
        "column_c"
      ],
      "be": [
        "column_a",
        "column_b"
      ]
    }
    ```
=== "python"
    ```python

    from wimsey import test
    from wimsey.tests import columns_should

    keywords = {
      "have": [
        "column_a"
      ],
      "not_have": [
        "column_c"
      ],
      "be": [
        "column_a",
        "column_b"
      ]
    }

    result = test(df, contract=[columns_should(**keywords)])
    
    ```

<hr>
    
## type_should

Test column type matches up with expected value. Note that this will expect *polars* style types, although does not require that they be case sensitive. For example, if testing a pandas dataframe for integer type, specify "int64" rather than, say, "int64[pyarrow]" or otherwise.

=== "yaml"
    ```yaml
    be: int64
    be_one_of:
    - int64
    - float64
    column: column_a
    not_be: string
    test: type_should

    ```
=== "json"
    ```json
    {
      "test": "type_should",
      "column": "column_a",
      "be": "int64",
      "not_be": "string",
      "be_one_of": [
        "int64",
        "float64"
      ]
    }
    ```
=== "python"
    ```python

    from wimsey import test
    from wimsey.tests import type_should

    keywords = {
      "column": "column_a",
      "be": "int64",
      "not_be": "string",
      "be_one_of": [
        "int64",
        "float64"
      ]
    }

    result = test(df, contract=[type_should(**keywords)])
    
    ```

<hr>
    
## row_count_should

Test that dataframe row count is within designated range

=== "yaml"
    ```yaml
    be_exactly: 300
    be_greater_than: 500
    be_greater_than_or_equal_to: 500
    be_less_than: 500
    be_less_than_or_equal_to: 300
    test: row_count_should

    ```
=== "json"
    ```json
    {
      "test": "row_count_should",
      "be_less_than": 500,
      "be_less_than_or_equal_to": 300,
      "be_greater_than": 500,
      "be_greater_than_or_equal_to": 500,
      "be_exactly": 300
    }
    ```
=== "python"
    ```python

    from wimsey import test
    from wimsey.tests import row_count_should

    keywords = {
      "be_less_than": 500,
      "be_less_than_or_equal_to": 300,
      "be_greater_than": 500,
      "be_greater_than_or_equal_to": 500,
      "be_exactly": 300
    }

    result = test(df, contract=[row_count_should(**keywords)])
    
    ```

<hr>
    
## average_difference_from_other_column_should

Test that the average difference between column and other column are within designated bounds.

=== "yaml"
    ```yaml
    be_exactly: 300
    be_greater_than: 500
    be_greater_than_or_equal_to: 500
    be_less_than: 500
    be_less_than_or_equal_to: 300
    column: column_a
    other_column: column_b
    test: average_difference_from_other_column_should

    ```
=== "json"
    ```json
    {
      "test": "average_difference_from_other_column_should",
      "column": "column_a",
      "other_column": "column_b",
      "be_exactly": 300,
      "be_less_than": 500,
      "be_less_than_or_equal_to": 300,
      "be_greater_than": 500,
      "be_greater_than_or_equal_to": 500
    }
    ```
=== "python"
    ```python

    from wimsey import test
    from wimsey.tests import average_difference_from_other_column_should

    keywords = {
      "column": "column_a",
      "other_column": "column_b",
      "be_exactly": 300,
      "be_less_than": 500,
      "be_less_than_or_equal_to": 300,
      "be_greater_than": 500,
      "be_greater_than_or_equal_to": 500
    }

    result = test(df, contract=[average_difference_from_other_column_should(**keywords)])
    
    ```

<hr>
    