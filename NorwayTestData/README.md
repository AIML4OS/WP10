# Norway text classification data
This folder contatins code to collect and save data from the [Norwegian business register](https://virksomhet.brreg.no/nb/oppslag/enheter) for using in testing text classification models. Information on the API (in Norwedgian) can be found in the [Norwegian business register documentation](https://data.brreg.no/enhetsregisteret/api/dokumentasjon/no/index.html).

This data is shared under the conditions of the license: [Norsk lisens for offentlige data](https://data.norge.no/nlod/no).

## Units
The python script `create_data_norway.py´ creates a train (80 percent) and test (20 percent) dataset. The units are legal entities in the Norwegian business register that contain a valid NACE classification (rev.2.1). NACE groups with less than 5 units are excluded.

The data has been extracted from the register on the 15th November 2025 and includes 435831 units in the training data and 108958 in the test data. 

## Variables
The following variables are included in the data:

- orgnr: (int) Identification number for the company.
- company_name: (str) Name of the company.
- company_activity: (str) General description of the activity of the company.
- company_purpose: (str) Formal statutory purpose for the company (If available).
- number_of_employees: (int) Number of registered employees.
- orgform: (str) The form of the organisation. See [Classification of Legal form](https://www.ssb.no/klass/klassifikasjoner/35) for more details.
- orgform_description_en: (str) English description of the organistional form.
- date_of_incorporation: (str) Date for the registration of the company in the form 'YYYY-MM-DD'.
- website: (str) www address for the company if available
- sector_code: (str) Classification of the sector of the business.See [Classification fo Institutional sector](https://www.ssb.no/klass/klassifikasjoner/39) for more details.
- sector_description_nb:  (str) Norwegian (Bokmål) description of the sector of the business. 
- sector_description_en: (str) English description of the sector of the business.
- nace_21_code: (str) Standard industrial classification for the business (NACE) rev. 2.1. This is the 5-digit Norwegian standard and includes 635 classes. See [Classification of Standard Industrial Classification](https://www.ssb.no/klass/klassifikasjoner/6) for more details.
- nace_21_description_nb: (str) Norwegian (Bokmål) description of the NACE rev. 2.1 (5-digit).
- nace_21_description_en: (str) English description of the NACE rev. 2.1 (5-digit).

# Data location
The data is saved as parquet files in the s3 folder `projet-aiml4os-wp10/NorwayData`.
The training and test data can be read in the SSPCloud environment using the following python code. Make sure to start your SSPCloud service from your personal project area and not the WP10 area if you are using SSPCloud/Oniyxia. This is to ensure that the AWS_S3_ENDPOINT is set correctly:
```
import os
import s3fs
import pandas as pd

S3_ENDPOINT_URL = "https://" + os.environ["AWS_S3_ENDPOINT"]
fs = s3fs.S3FileSystem(client_kwargs={'endpoint_url': S3_ENDPOINT_URL})

filpath_train = "projet-aiml4os-wp10/NorwayData/train_norwaydata.parquet"
with fs.open(filpath_train, mode="rb") as file_in:
    train = pd.read_parquet(file_in)

filpath_test = "projet-aiml4os-wp10/NorwayData/test_norwaydata.parquet"
with fs.open(filpath_test, mode="rb") as file_in:
    test = pd.read_parquet(file_in)
```

Both training and test data is publically available. To read the data outside the SSPCloud environment, you can use the following URLs:
[https://minio.lab.sspcloud.fr/projet-aiml4os-wp10/NorwayData/test_norwaydata.parquet](https://minio.lab.sspcloud.fr/projet-aiml4os-wp10/NorwayData/test_norwaydata.parquet)
[https://minio.lab.sspcloud.fr/projet-aiml4os-wp10/NorwayData/train_norwaydata.parquet](https://minio.lab.sspcloud.fr/projet-aiml4os-wp10/NorwayData/train_norwaydata.parquet)
