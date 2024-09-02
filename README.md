# LLM vet records

## Objective
Supporting scripts for manuscript: "Classification performance and reproducibility 
of GPT-4 omni for information extraction from veterinary electronic 
health records" (Wulcan et al 2024)

## Structure
A series of nested R and python scripts were used to conduct the study. 
A graphical overview of how scripts, input and output 
files relate to each other is in overview.pptx. Below are lists of
- Scripts (order of paper)
- Input files (manually produced or output from scripts outside of the project)
- Intermediates files (output of scripts in this project used for other scripts in this project) 
- Output files (output of scripts in this project used in paper)
After each script or file is the origin/location/summary in parenthesis
More detail on each script is in the script Rmd

## Scripts (in order of paper)
- randomize_authors (randomizes the co-author order (of equal contributors))

### 2.1 Study design and sample size
- sample_size.Rmd (calculates sample size for the study)
- estimate prevalence.Rmd (estimates prevalence of clinical signs)

### 2.2 Case material
- sample records.Rmd (samples EHRs for sets used in study)
- parse_deid.Rmd (parses deidentified EHRs for further processing)

### 2.4 Variable selection and prompt engineering
- prompt_engineering.Rmd (documents process of prompt engineering)

### 2.5 LLM analysis
- api_GPT35.py (calls LLM api (GPT version 3.5 turbo))
- api_GPT4o.py (calls LLM api (GPT version  4 omni))
- parse_llm_output.Rmd (parses LLM output for further processing
- explore_output_format.Rmd (explores invalid LLM output formats)

### 2.6 Human analysis
- make_survey.Rmd (makes a qualtrics survey - for collecting human responses)
- parse_survey.Rmd (parses survey responses for further processing)
- combine_responses.Rmd (combines human and llm responses)

### 2.7 Classification performance
- add_mode (calculates mode and agreement)
- classification_performance.Rmd (analyzes classification performance)

### 2.8 Reproducibility
- reproducibility.Rmd (analyses reproducibility)

### 2.9 Quality assessment of responses
- explore_compliance (detailed analysis of compliance to instructions)

### 2.10 Error analysis
- explore_agreement.Rmd (raw data exploratory plots)
- explore errors (detailed analysis of classification errors)

- explore_cost_and_time.Rmd

## Input data 
- contains_free_text.rds (input) (VMACS/all_cats_ever/output/contains_free_text)
Dataframe with all EHRs from VMTH UC Davis 1985-2023 with text in any of the
visit text fields. Only used for the first pilot set and prevalence estimates.
- pilot_free_text_graded.xlsx (input)(manually graded pilot cases from first pilot set)
- contains_hx.rds (input) (VMACS/all_cats_ever/output/contains_free_text)
Dataframe with all EHRs from VMTH UC Davis 1985-2023 with text in the pertinent
 history field. This is the source from which the second pilot set, the tuning
 set and the test set is pulled.
- tuning_deid.xlsx (input)(manually deidentified tuning set)
- pilot_hx_deidentified.xlsx (input)(manually deidentified pilot set)
- test_deidentified.xlsx (input)(manually deidentified test set)
- tuning_prompt_engineering.xlsx (input)(manually documented llm responses prompt engineering)
- pilot_hx_response.rds (input) (qualtrics response pilot)
- tuning_response.csv (input) (qualtrics reponse tuning)
- test_response.csv (input) (qualtrics response_test)
- prompt_tuning_1.txt (prompts)
- prompt_test_1.txt (prompts)
- test_GPT4o.json (experiment/test_4o) llm output
- test_GPT4o_corrected.json (input)(manually corrected json format of test GPT4o.json)
- test_GPT35.json (experiment/test35) llm output
- categorize_errors.xlsx (manually classified errors at temp 0 for GPT4o test)
- corrected_references.xlsx (inputDir, manually corrected quotation marks and single spaces between citation strings for humans and GPT4o test set)
- reference_mismatch.xlsx (inputDir, manually assessed and categorized mismatched citations for humans and GPT4o temp 0 test set)

## Intermediate files 
- pilot_free_text.rds (intermediates/sample_records)
- pilot_hx.rds (intermediates/sample_records)
- pilot_hx_response_parsed (intermediates/parse_survey)
- tuning_deid.json (intermediates/parse_deid)
- test_deid.json (intermediates/parse/deid)
- test_response_parsed.rds (intermediates/parse_survey) parsed human responses
- test_GPT-4o_parsed.rds (intermediates/parse_llm_output) parsed llm response
- test_GPT4o_corrected_parsed (intermediates/parse_llm_output)
- test_GPT35_parsed.rds (intermediates/parse_llm_output) parsed llm response
- tuning_GPT4o_parsed (intermediates/parse_llm_response)
- test_response_human_GPT4o.rds (intermediates/combine_responses)
- test_response_human_GPT35.rds (intermediates/combine_responses)
- mode_test_GPT4o.rds (intermediates/add_mode)
- mode_test_GPT35 (intermediates/add_mode)
- long_test_GPT4o.rds(intermediates/add_mode)
- test_GPT4o_confusion_matrix.rds (intermediates/clasification_performance)


## Output files (files produced in the project in order of paper)
## 2.1 Study design and sample size
- prevalence_gi.csv (output/estimate_prevalence_)
### Case material
- year_words_test_set.csv

### 2.5 LLM analysis
- FS1_tuning_GPT4o_invalid_output.png (output/explore_output_format)
- tuning_GPT4o_invalid_output_summary.csv (output/explore_output_format)

### 3.2 Classification performance
- test_GPT4o_classification_metrics.csv (output/classification_performance) (per clinical sign)
- test_GPT4o_classification_summary.csv (output/classification_performance) (averaged across clinical signs)
- mcNemar_temp_test_GPT4o.csv (output/classification_performance) (compare temps)
- F1_test_GPT4o_classification_performance.png (output/classification_performance)
- test_GPT35_classification_metrics.csv (output/classification_performance) (per clinical sign)
- test_GPT35_classification_summary.csv (output/classification_performance) (averaged across clinical signs)
- mcNemar_model_test.csv (output/classification_performance) GPT35 vs GPT4o

### 3.3 Reproducibility
- F2A_kappas_test_GPT4o.png (output/reproducibility)
- kappas_test_GPT4o.csv (output/reproducibility)
- kappas_test_GPT35.csv (output/reproducibility)

### 3.4 Quality assessment of responses
- F2B_compliance_by_temp_test_gpt4o.png (output/explore_compliance)
- compliance_summary_test_GPT4o.csv (output/explore_compliance)

### 3.5 Error analysis
- FS3_decreased_appetite (output/explore_agreement)
- FS4_vomiting (output/explore_agreement)
- FS5_weight_loss (output/explore_agreement)
- FS6_diarrhea (output/explore_agreement)
- FS7_constipation (output/explore_agreement)
- FS8_polyphagia (output/explore_agreement)
- F3a_error_tile_plot_test_GPT4o.png  (output/explore_agreement)
- F3b_alluvian_error_test_GPT4_t0.png (output/explore_errors)
- summary_errors_GPT4o_temp0.csv (output/explore_errors)
- summary_error_type_GPT4o_temp0.csv (output/explore_errors)
- summary_disagreement_GPT4o_temp0.csv (output/explore_errors)
- summary_human_agreement_GPT4o_temp0.csv (output/explore_errors)
- summary_disagreement_type_GPT4o_temp0.csv (output/explore_errors)
- summary_ambiguity_in_interpretation_disagreement_GPT4o_temp0.csv (output/explore_errors)
- summary_ambiguity_in_citation_disagreement_GPT4o_temp0.csv (output/explore_errors)
- summary_confusion_class_in_nonambiguos_citation_disagreement_GPT4o_temp0.csv (output/explore_errors)


### 3.6 Time and Cost
- test_GPT4o_cost_and_time.csv (output/explore_cost_and_time)
- test_GPT35_cost_and_time.csv (output/explore_cost_and_time)


## Comments
The python scripts are run from their folders 
(containing scripts, files with API key, prompt and EHRs). 
The API key and endpoints can be obtained on the azure account web interface 
(log in to azure, select resource in "resource list", select 
"Resource management" in left menu, select "Keys and Endpoints" (
requires "owner" permission)). 















