# Norway text classification data
This folder contatins code to collect and save data from the [Norwegian business register](https://virksomhet.brreg.no/nb/oppslag/enheter) for using in testing text classification models. Information on the API (in Norwedgian) is located here: https://data.brreg.no/enhetsregisteret/api/dokumentasjon/no/index.html

## Units
The python script `create_data_norway.py´ creates a train (80 percent) and test (20 percent) dataset. The units are legal entities in the Norwegian business register that contain a valid NACE classification. Nace groups with less than 5 units are excluded. 

## Variables
The following variables are available:

- orgnr: (int) Identification number for the company.
- company_name: (str) Name of the company.
- company_activity: (str) General description of the activity of the company.
- company_purpose: (str) Formal statutory purpose for the company.
- number_of_employees: (int) Number of registered employees.
- orgform: (str) The form of the organisation. See [Classification of Legal form](https://www.ssb.no/klass/klassifikasjoner/35) for more details.
- orgform_description_en: (str) English description of the organistional form.
- date_of_incorporation: (str) Date for the registration of the company in the form 'YYYY-MM-DD'.
- website: (str) www address for the company if available
- sector_code: (str) Classification of the sector of the business.See [Classification fo Institutional sector](https://www.ssb.no/klass/klassifikasjoner/39) for more details.
- sector_description_nb:  (str) Norwegian (Bokmål) description of the sector of the business. 
- sector_description_en: (str) English description of the sector of the business.
- nace_21_code: (str) Standard industrial classification for the business (NACE) rev. 2.1. This is the 5-digit Norwegian standard. See [Classification of Standard Industrial Classification](https://www.ssb.no/klass/klassifikasjoner/6) for more details.
- nace_21_description_nb: (str) Norwegian (Bokmål) description of the NACE rev. 2.1.
- nace_21_description_en: (str) English description of the NACE rev. 2.1.

# Data location
The data is saved as parquet files: ´norway_train.parquet´ and ´norway_test.parquet´ ...
