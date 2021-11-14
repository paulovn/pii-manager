# Text Anonymizer

This repository builds a Python package that performs anonymization for text 
buffers i.e. removal of PII in the text, and its substitution by a placeholder.

The package is structured by language & country, since many of the PII
elements are language- and/or -country dependent.


## Usage

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

this will load and execute anonymization tasks for English that will anonymize
credit card numbers, disease information, and Government IDs for US and UK
(assuming all these tasks are implemented in the package)


It is also possible to load all possible tasks for a language:

```Python

 from text_anonymizer import TextAnonymizer, AnonTask

 anon = TextAnonymizer('en', 'all', all_tasks=True)

 text_out = anon(text_in)
 
```

this will load all anonymization tasks available for English, including:
  * language-independent tasks
  * language-dependent but country-independent tasks
  * country-dependent tasks for all countries implemented under the `en`
    language
	
By default all PII items found will be substituted with a `<PIINAME>`
string. If another placeholder is preferred, the `TextAnonymizer` constructor
can be called with an additional `template` argument, containing a string that
will be processed through the Python string `format()` method, and called
with an `id=PIINAME` argument.


## Adding tasks

To add an anonymization task to the package:

 1. If the task is a new one, add an identifier for it in [TaskEnum]
 2. If it is for a language not yet covered, add a new language subfolder
    undder the [lang] folder, using the [ISO 639-1] code for the language
 3. Then
    * If it is a country-independent PII, it goes in the `any` subdir (create
	  it if not present)
    * if it is country-dependent, create a country subdir if not present, 
	  using a **lowercased version** of its [ISO 3166-1] country code
 4. Under this final chosen subfolder, add the task as a Python `taskname.py`
    module (the name of the file is not relevant). The module must contain:
	* The task implementation, which can have any of two flavours (regex or
	  function), see below
    * The task descriptor, a list with the (compulsory) name
      `ANONTASKS` (see below)
 5. Finally, add a unit test to check the validity for the task code, in the
    proper place under [test/unit/lang]. There should be at least a positive
	and a negative test

### Task implementation

A task can be either:
 - a RegEx string that matches a PII (it will be used to perform a `re.sub`)
   on the documents. Note that it must be present as the *pattern* string, not
   the compiled regex (it will be compiled by the main code when loading)
 - a callable, for the cases that more sophisticated matching is neeeded. The
   callable will be called with a string argument, and it must return an 
   *iterable* of PII substrings matched inside the string
   
### Task descriptor

The task descriptor is a Python list that contains at least one tuple defining
the entry points for this task (there might be more than one, if the file
implements more than one PII).

* The name of the list **must be** `ANONTASKS`
* Each defined task must be a 4-element tuple, with these elements:
   - the PII identifier from [TaskEnum]
   - a function to be called for initialization of the task, if needed (use
     `None` if not needed)
   - the [task implementation]: either a Regex raw string or a function
   - a text description of the task (for documentation purposes)

   
## Building

The provided [Makefile] can be used to process the package:
 * `make pkg` will build the Python package
 * `make unit` will launch all unit tests (using [pytest], so pytest must be
   available)
 * `make install` will install the package in a virtualenv. The virtualenv
   will be
     - the one defined in the `VENV` environment variable
	 - if there is a virtualenv activated in the shell, it will be used
	 - otherwise, a default is chosen (which will probably not be available)


## Command-line script

Installing the package provides also a command-line script, `anonymize-text`,
that can be used to process files through anonymization tasks:

    anonymize-text <infile> <outfile> --lang es --country es ar mx \
	  --tasks CREDIT_CARD BITCOIN_ADDRESS BANK_ACCOUNT
	
or, to add all possible tasks:

    anonymize-text <infile> <outfile> --lang es --country all \
	   --all-tasks 

 


[task implementation]: #task-implementation
[TaskEnum]: src/text_anonymizer/tasks.py
[lang]: src/text_anonymizer/lang
[test/unit/lang]: test/unit/lang
[Makefile]: Makefile
[ISO 639-1]: https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
[ISO 3166-1]: https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2
[pytest]: https://docs.pytest.org
