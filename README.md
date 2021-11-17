# Text Anonymizer

This repository builds a Python package that performs anonymization for text 
buffers i.e. removal of PII in the text, and its substitution by a placeholder.

The package is structured by language & country, since many of the PII
elements are language- and/or -country dependent.


## Usage

### API usage

Usage of the package API goes like this:

```Python

 from text_anonymizer import TextAnonymizer, AnonTask

 # Define language, country(ies) and anonymization tasks
 lang = 'en'
 country = ['US', 'GB']
 tasklist = (AnonTask.CREDIT_CARD, AnonTask.GOVID, AnonTask.DISEASE)

 anon = TextAnonymizer(lang, country, tasks=tasklist)

 text_out = anon(text_in)
 
```

... this will load and execute anonymization tasks for English that will
anonymize credit card numbers, disease information, and Government IDs for US 
and UK (assuming all these tasks are implemented in the package).


It is also possible to load all possible tasks for a language:

```Python

 from text_anonymizer import TextAnonymizer, AnonTask

 anon = TextAnonymizer('en', 'all', all_tasks=True)

 text_out = anon(text_in)
 
```

this will load all anonymization tasks available for English, including:
  * language-independent tasks
  * language-dependent but country-independent tasks
  * country-dependent tasks for *all* countries implemented under the `en`
    language

By default all PII items found will be substituted with a `<PIINAME>`
string. If another placeholder is preferred, the `TextAnonymizer` constructor
can be called with an additional `template` argument, containing a string that
will be processed through the Python string `format()` method, and called
with an `id=PIINAME` argument.


### Command-line usage

Installing the package provides also a command-line script, `anonymize-text`,
that can be used to process files through anonymization tasks:

    anonymize-text <infile> <outfile> --lang es --country es ar mx \
	  --tasks CREDIT_CARD BITCOIN_ADDRESS BANK_ACCOUNT
	
or, to add all possible tasks for a given language:

    anonymize-text <infile> <outfile> --lang es --country all \
	   --all-tasks 


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
[contributing instructions]: doc/CONTRIBUTING.md
