# Pii Manager

This repository builds a Python package that performs PII processing for text 
data i.e. replacement/tagging/extraction of PII in the text.

The PII Tasks in the package are structured by language & country, since many
of the PII elements are language- and/or -country dependent.


## API usage

There are two types of API usage: the file-based API and the object-based API

### Object API

Usage of the object-based package API goes like this:

```Python

 from pii_manager import PiiEnum
 from pii_manager.api import PiiManager

 # Define language, country(ies) and PII tasks
 lang = 'en'
 country = ['US', 'GB']
 tasklist = (PiiEnum.CREDIT_CARD, PiiEnum.GOVID, PiiEnum.DISEASE)

 # Instantiate object
 proc = PiiManager(lang, country, tasks=tasklist)

 # Process a text buffer
 text_out = proc(text_in)
 
```

... this will load and execute anonymization tasks for English that will
anonymize credit card numbers, disease information, and Government IDs for US 
and UK (assuming all these tasks are implemented in the package).


It is also possible to load all possible tasks for a language:

```Python

 from pii_manager import PiiEnum
 from pii_manager.api import PiiManager

 proc = PiiManager('en', 'all', all_tasks=True)

 text_out = proc(text_in)
 
```

...this will load all anonymization tasks available for English, including:
 * language-independent tasks
 * language-dependent but country-independent tasks
 * country-dependent tasks for *all* countries implemented under the `en`
   language


### File-based API

The file-based API reads from a file, and writes to an output file. It is
executed as:

```Python

 from pii_manager import PiiEnum
 from pii_manager.api import process_file

 # Define language, country(ies) and PII tasks
 lang = 'en'
 country = ['US', 'GB']
 tasklist = (PiiEnum.CREDIT_CARD, PiiEnum.GOVID, PiiEnum.DISEASE)

 # Process the file
 process_file(infilename, outfilename, lang, 
              country=country, tasks=tasklist)
 
```

The file-based API accepts also the `all_tasks` argument to add all suitable
defined tasks.


## Command-line usage

Installing the package provides also a command-line script, `pii-manage`,
that can be used to process files through PII tasks:

    pii-manage <infile> <outfile> --lang es --country es ar mx \
	  --tasks CREDIT_CARD BITCOIN_ADDRESS BANK_ACCOUNT
	
or, to add all possible tasks for a given language:

    pii-manage <infile> <outfile> --lang es --country all \
	   --all-tasks 


## Processing mode

PII processing accetps three modes: _replace_ , _tag_ and _extract_. To show
an example, let us consider a fragment such as:

> my credit card number is 4273 9666 4581 5642

with this input, the output for each of the three processing modes will be:

* for _replace_, the PII will be replaced by a placeholder describing the PII
  name:

> my credit card number is <CREDIT_CARD>

* for _tag_, the PII is tagged with the PII name, but the original string is
  also kept:

> my credit card number is <CREDIT_CARD:4273 9666 4581 5642>

* for _extract_, a list of detected PIIs is returned, as a dict in the
  buffer-based API, or as a [NDJSON] file for the file-based API

> {"name": "CREDIT_CARD", "value": "4273 9666 4581 5642", "pos": 25, "line": 1}


By default in _replace_ mode all PII items found will be substituted with 
a `<PIINAME>` string. If another placeholder is preferred, the `PiiManager`
constructor can be called with an additional `template` argument, containing
a string that will be processed through the Python string `format()` method,
and called with a `(name=PIINAME)` argument. In _tag_ mode, the template is
called with `(name=PIINAME, value=VALUE)` argument.

The file-based API has an additional option: how the file is splitted when
calling the PII tasks:

* `line`: (default) the file is splitted line-by-line
* `block`: the file is sent as a single block
* `sentences`: the file is split by sentence separators (periods, etc)


## Building

The provided [Makefile] can be used to process the package:
 * `make pkg` will build the Python package, creating a file that can be
   installed with `pip`
 * `make unit` will launch all unit tests (using [pytest], so pytest must be
   available)
 * `make install` will install the package in a Python virtualenv. The
   virtualenv will be chosen as, in this order:
     - the one defined in the `VENV` environment variable, if it is defined
	 - if there is a virtualenv activated in the shell, it will be used
	 - otherwise, a default is chosen (which will probably not be available)


## Contributing

To add a new PII-anonymization task, please see the [contributing instructions]


[Makefile]: Makefile
[pytest]: https://docs.pytest.org
[contributing instructions]: doc/contributing.md
[NDJSON]: http://ndjson.org/
