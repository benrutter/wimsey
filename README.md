
<div align="right">
  <details>
    <summary >🌐 Language</summary>
    <div>
      <div align="center">
        <a href="https://openaitx.github.io/view.html?user=benrutter&project=wimsey&lang=en">English</a>
        | <a href="https://openaitx.github.io/view.html?user=benrutter&project=wimsey&lang=zh-CN">简体中文</a>
        | <a href="https://openaitx.github.io/view.html?user=benrutter&project=wimsey&lang=zh-TW">繁體中文</a>
        | <a href="https://openaitx.github.io/view.html?user=benrutter&project=wimsey&lang=ja">日本語</a>
        | <a href="https://openaitx.github.io/view.html?user=benrutter&project=wimsey&lang=ko">한국어</a>
        | <a href="https://openaitx.github.io/view.html?user=benrutter&project=wimsey&lang=hi">हिन्दी</a>
        | <a href="https://openaitx.github.io/view.html?user=benrutter&project=wimsey&lang=th">ไทย</a>
        | <a href="https://openaitx.github.io/view.html?user=benrutter&project=wimsey&lang=fr">Français</a>
        | <a href="https://openaitx.github.io/view.html?user=benrutter&project=wimsey&lang=de">Deutsch</a>
        | <a href="https://openaitx.github.io/view.html?user=benrutter&project=wimsey&lang=es">Español</a>
        | <a href="https://openaitx.github.io/view.html?user=benrutter&project=wimsey&lang=it">Italiano</a>
        | <a href="https://openaitx.github.io/view.html?user=benrutter&project=wimsey&lang=ru">Русский</a>
        | <a href="https://openaitx.github.io/view.html?user=benrutter&project=wimsey&lang=pt">Português</a>
        | <a href="https://openaitx.github.io/view.html?user=benrutter&project=wimsey&lang=nl">Nederlands</a>
        | <a href="https://openaitx.github.io/view.html?user=benrutter&project=wimsey&lang=pl">Polski</a>
        | <a href="https://openaitx.github.io/view.html?user=benrutter&project=wimsey&lang=ar">العربية</a>
        | <a href="https://openaitx.github.io/view.html?user=benrutter&project=wimsey&lang=fa">فارسی</a>
        | <a href="https://openaitx.github.io/view.html?user=benrutter&project=wimsey&lang=tr">Türkçe</a>
        | <a href="https://openaitx.github.io/view.html?user=benrutter&project=wimsey&lang=vi">Tiếng Việt</a>
        | <a href="https://openaitx.github.io/view.html?user=benrutter&project=wimsey&lang=id">Bahasa Indonesia</a>
        | <a href="https://openaitx.github.io/view.html?user=benrutter&project=wimsey&lang=as">অসমীয়া</
      </div>
    </div>
  </details>
</div>

# 🔍 Wimsey

[![Codeberg](https://img.shields.io/badge/Codeberg-2185D0?style=for-the-badge&logo=Codeberg&logoColor=white)](https://codeberg.org/benrutter/wimsey)
[![PyPi](https://img.shields.io/badge/pypi-%23ececec.svg?style=for-the-badge&logo=pypi&logoColor=1f73b7)](https://pypi.org/project/wimsey/)

[![Docs](https://img.shields.io/badge/Docs-hugo-blue)](https://benrutter.codeberg.page/wimsey-site/site/)
![License](https://img.shields.io/badge/license-MIT-blue)
![coverage](https://img.shields.io/badge/coverage-100-green)


Wimsey is lightweight, flexible and fully open-source data contract library.

- 🐋 **Bring your own dataframe library**: Built on top of [Narwhals](https://github.com/narwhals-dev/narwhals) so your tests are carried out natively in your own dataframe library (including Pandas, Polars, Pyspark, Dask, DuckDB, CuDF, Rapids, Arrow and Modin)
- 🎍 **Bring your own contract format**: Write contracts in yaml, json or python - whichever you prefer!
- 🪶 **Ultra Lightweight**: Built for fast imports and minimal overwhead with only two dependencies ([Narwhals](https://github.com/narwhals-dev/narwhals) and [FSSpec](https://github.com/fsspec/filesystem_spec))
- 🥔 **Simple, easy API**: Low mental overheads with two simple functions for testing dataframes, and a simple dataclass for results.

Check out the handy [test catalogue](https://benrutter.github.io/wimsey/possible_tests/) and [quick start guide](https://benrutter.github.io/wimsey/)

## What is a data contract?

As well as being a good buzzword to mention at your next data event, data contracts are a good way of testing data values at boundary points. Ideally, all data would be usable when you recieve it, but you probably already have figured that's not always the case.

A data contract is an expression of what *should* be true of some data - we might want to check that the only columns that exist are `first_name`, `last_name` and `rating`, or we might want to check that `rating` is a number less than 10.

Wimsey let's you write contracts in json, yaml or python, here's how the above checks would look in yaml:

```yaml
- test: columns_should
  be:
    - first_name
    - last_name
    - rating
- column: rating
  test: max_should
  be_less_than_or_equal_to: 10
```

Wimsey then can execute tests for you in a couple of ways, `validate` - which will throw an error if tests fail, and otherwise pass back your dataframe - and `test`, which will give you a detailed run down of individual test success and fails.

Validate is designed to work nicely with polars or pandas `pipe` methods as a handy guard:

```python
import polars as pl
import wimsey

df = (
  pl.read_csv("hopefully_nice_data.csv")
  .pipe(wimsey.validate, "tests.json")
  .group_by("name").agg(pl.col("value").sum())
)
```

Test is a single function call, returning a `FinalResult` data-type:

```python
import pandas as pd
import wimsey

df = pd.read_csv("hopefully_nice_data.csv")
results = wimsey.test(df, "tests.yaml")

if results.success:
  print("Yay we have good data! 🥳")
else:
  print(f"Oh nooo, something's up! 😭")
  print([i for i in results.results if not i.success])
```

# Roadmap, Contributing & Feedback

Wimsey's mirrored on github, but hosted and developed on [codeberg](https://codeberg.org/benrutter/wimsey). Issues and pull requests are accepted on both.

Focus at the moment is on refining profiling and test generation, if you have tests or feature that would be helpful to you, feel free to reach out!
