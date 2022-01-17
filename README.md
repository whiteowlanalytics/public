### Notes

Made a keywordsdatapull class that could be generalized later for other data pull jobs 

Need to make the insert function operate as a batch because bigquery counts each insert against the daily limit (better to do batches)

It might be better to have a table in bigquery dedicated to campaigns where company name and make the update of that table a separate job

