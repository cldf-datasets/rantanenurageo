# Releasing rantanenurageo

The dataset should be "installed", i.e. you should have run
```shell
pip install -e .[test,geo]
```
ideally in a separate virtual environment.


- Recreate the CLDF data:
  ```shell
  cldfbench makecldf cldfbench_rantanenurageo.py --glottolog-version v4.8 --with-zenodo --with-cldfreadme
  ```
- Validate it:
  ```shell
  pytest
  ```
- Recreate the human-readable dataset description:
  ```shell
  cldfbench readme cldfbench_rantanenurageo.py
  ```
