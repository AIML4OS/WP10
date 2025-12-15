# Norway text classification data
This folder contatins code to collect and save data from the [Norwegian business register](https://virksomhet.brreg.no/nb/oppslag/enheter) for using in testing text classification models. Information on the API (in Norwegian) can be found in the [Norwegian business register documentation](https://data.brreg.no/enhetsregisteret/api/dokumentasjon/no/index.html).

This data is shared under the conditions of the Norwegian public data license: [Norsk lisens for offentlige data](https://data.norge.no/nlod/no).

## Norwegian training and test data
### Units
The python script `create_data_norway.py´ creates a training (80 percent) and test (20 percent) dataset. The units are legal entities in the Norwegian business register that contain a valid NACE classification (rev.2.1).

The data has been extracted from the register on the 15th December 2025 and includes 436 001 units in the training data and 108 995 in the test data. 

### Variables
The following variables are included in the data:

- orgnr: (int) Identification number for the company.
- company_name: (str) Name of the company.
- company_activity: (str) General description of the activity of the company.
- company_purpose: (str) Formal statutory purpose for the company (If available).
- number_of_employees: (int) Number of registered employees.
- orgform: (str) The form of the organisation. See [Classification of Legal form](https://www.ssb.no/klass/klassifikasjoner/35) for more details.
- orgform_name_nb: (str) Norwegian name of the organistional form.
- orgform_name_en: (str) English name of the organistional form.
- date_of_incorporation: (str) Date for the registration of the company in the form 'YYYY-MM-DD'.
- website: (str) www address for the company if available
- sector_code: (str) Classification of the sector of the business. See [Classification fo Institutional sector](https://www.ssb.no/klass/klassifikasjoner/39) for more details.
- sector_name_nb:  (str) Norwegian (Bokmål) description of the sector of the business. 
- sector_name_en: (str) English description of the sector of the business.
- nace_21_code: (str) Standard industrial classification for the business (NACE) rev. 2.1. This is the 4-digit European standard and includes 623 classes in the data. Fewer class groups (591) are in the test data as groups with only 1 observation were placed in the training data only. See [Classification of Standard Industrial Classification](https://www.ssb.no/klass/klassifikasjoner/6) for more details.
- nace_21_name_nb: (str) Norwegian (Bokmål) name of the NACE rev. 2.1 (4-digit).
- nace_21_name_en: (str) English name of the NACE rev. 2.1 (4-digit).

## Data location
All Norwegian data is saved in the s3 folder `projet-aiml4os-wp10/NorwayData`. The training and test data are saved as parquet files and can be read into the SSPCloud environment using the following python code. Make sure to start your SSPCloud service from your personal project area and not the WP10 area if you are using SSPCloud/Onyxia.
```
import pandas as pd

train_path = "https://minio.lab.sspcloud.fr/projet-aiml4os-wp10/NorwayData/train_norwaydata_2025-12-15.parquet"
test_path = "https://minio.lab.sspcloud.fr/projet-aiml4os-wp10/NorwayData/test_norwaydata_2025-12-15.parquet"

train = pd.read_parquet(train_path)
test = pd.read_parquet(test_path)
```

Both training and test data is publically available so you can also read the data in environments outside of SSPCloud with the following URLs:

- [https://minio.lab.sspcloud.fr/projet-aiml4os-wp10/NorwayData/test_norwaydata.parquet](https://minio.lab.sspcloud.fr/projet-aiml4os-wp10/NorwayData/test_norwaydata_2025-12-15.parquet)
- [https://minio.lab.sspcloud.fr/projet-aiml4os-wp10/NorwayData/train_norwaydata.parquet](https://minio.lab.sspcloud.fr/projet-aiml4os-wp10/NorwayData/train_norwaydata_2025-12-15.parquet)

## Addititional data
In addition to the main training and test data, two additional data are available; one with class descriptions and one with draft index items translated to Norwegian.

### Class descriptions
The data ´class_codes_and_description.csv´ contains descriptions of the NACE rev.2.1 classes. This includes NACE codes, names and descriptions of all the 5 levels in the Norwegian NACE classifications. The data is collected from [https://www.ssb.no/klass/klassifikasjoner/6](https://www.ssb.no/klass/klassifikasjoner/6) and includes the columns: code, parentCode, level, name, shortName, notes, valideFrom and validTo. The column "notes" contains class descriptions in Norwegian, for example what is and isn't included in the groups. 

### NACE Index
The data ´nace_index_rev.2.1_norwegian_draft.csv´ contains an automatic translation (using deepl) of the draft index for the European NACE rev.2.1. This is a draft and is currently not available outside the WP10 SSPCloud environment. The data includes columns: CODE, INDEX_ENTRY, KEYWORD_NB, RECONSTRUCTED_ENTRY_NB
