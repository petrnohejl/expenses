Expenses
========

Expenses is a simple script, which helps to organize personal expenses.
It adapt data in CSV for pivot table and charts. Script can work only with
CSV data export from Fio bank.

Expenses script make 3 modifications to CSV file:

* invert sign of amounts because of pie chart (earnings gonna be negative,
  expenses gonna be positive)
* add category column (categories are automatically detected by regex)
* add month column

I wrote [a blog post about Expenses](http://blog.petrnohejl.cz/evidence-osobnich-vydaju) (in Czech).


Usage
=====

Expenses is a console application and is written in Python 2.7. To run it,
you must have installed Python interpreter, which can be downloaded
at www.python.org.

```bash
$ python expenses.py mydata.csv    # run expenses script
```


Developed by
============

* [Petr Nohejl](http://petrnohejl.cz)


License
=======

    Copyright 2014 Petr Nohejl

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
