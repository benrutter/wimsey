# Test Catalogue 🧪
This documentation is intended as an exaustive list of possible tests within Wimsey. Note that examples given intentionally use all possible keywords for demonstrative purposes. This isn't required, and you can give as many or as few keywords as you like with the exception of where `column` is required.
## mean_should

Test that column metric is within designated range

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

Test that column metric is within designated range

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

Test that column metric is within designated range

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

Test that column metric is within designated range

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
    
## count_should

Test that column metric is within designated range

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
    
## average_ratio_to_other_column_should

Test that the average ratio between column and other column are within designated bounds (for instance, a value of 1 has a ratio of 0.1 to a value of 10)

=== "yaml"
    ```yaml
    be_exactly: 300
    be_greater_than: 500
    be_greater_than_or_equal_to: 500
    be_less_than: 500
    be_less_than_or_equal_to: 300
    column: column_a
    other_column: column_b
    test: average_ratio_to_other_column_should

    ```
=== "json"
    ```json
    {
      "test": "average_ratio_to_other_column_should",
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
    from wimsey.tests import average_ratio_to_other_column_should

    keywords = {
      "column": "column_a",
      "other_column": "column_b",
      "be_exactly": 300,
      "be_less_than": 500,
      "be_less_than_or_equal_to": 300,
      "be_greater_than": 500,
      "be_greater_than_or_equal_to": 500
    }

    result = test(df, contract=[average_ratio_to_other_column_should(**keywords)])
    
    ```

<hr>
    
## max_string_length_should

Test that the maximum string length iswithin expected bounds

=== "yaml"
    ```yaml
    be_exactly: 300
    be_greater_than: 500
    be_greater_than_or_equal_to: 500
    be_less_than: 500
    be_less_than_or_equal_to: 300
    column: column_a
    test: max_string_length_should

    ```
=== "json"
    ```json
    {
      "test": "max_string_length_should",
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
    from wimsey.tests import max_string_length_should

    keywords = {
      "column": "column_a",
      "be_exactly": 300,
      "be_less_than": 500,
      "be_less_than_or_equal_to": 300,
      "be_greater_than": 500,
      "be_greater_than_or_equal_to": 500
    }

    result = test(df, contract=[max_string_length_should(**keywords)])
    
    ```

<hr>
    
## all_values_should

Test all unique values within a column are within expected group

=== "yaml"
    ```yaml
    be_one_of:
    - int64
    - float64
    column: column_a
    match_regex: at$
    not_be_one_of:
    - a
    - b
    test: all_values_should

    ```
=== "json"
    ```json
    {
      "test": "all_values_should",
      "column": "column_a",
      "be_one_of": [
        "int64",
        "float64"
      ],
      "not_be_one_of": [
        "a",
        "b"
      ],
      "match_regex": "at$"
    }
    ```
=== "python"
    ```python

    from wimsey import test
    from wimsey.tests import all_values_should

    keywords = {
      "column": "column_a",
      "be_one_of": [
        "int64",
        "float64"
      ],
      "not_be_one_of": [
        "a",
        "b"
      ],
      "match_regex": "at$"
    }

    result = test(df, contract=[all_values_should(**keywords)])
    
    ```

<hr>
    
## type_should

Check that type of column meets expected criteria. Note that because Wimsey is a dataframe agnostic tool, this should be of *Narwhals* expected types, such as Float64, Int64, String, etc. See Narwhals' documentation for more details: https://narwhals-dev.github.io/narwhals/api-reference/dtypes/

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
    
## columns_should

Check that expected columns are present / non-present within dataframe

=== "yaml"
    ```yaml
    be: int64
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
      "be": "int64"
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
      "be": "int64"
    }

    result = test(df, contract=[columns_should(**keywords)])
    
    ```

<hr>
    
## null_count_should

Check that null count of column meets expected criteria.

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
    
## null_percentage_should

Check that null percentage of column meets expected criteria.

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
    